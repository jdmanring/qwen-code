/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { safeJsonStringify } from '../utils/safeJsonStringify.js';
import {
  BaseDeclarativeTool,
  BaseToolInvocation,
  Kind,
  ToolCallConfirmationDetails,
  ToolConfirmationOutcome,
  ToolInvocation,
  ToolMcpConfirmationDetails,
  ToolResult,
} from './tools.js';
import { CallableTool, FunctionCall, Part } from '@google/genai';
import { ToolErrorType } from './tool-error.js';

type ToolParams = Record<string, unknown>;

// Discriminated union for MCP Content Blocks to ensure type safety.
type McpTextBlock = {
  type: 'text';
  text: string;
};

type McpMediaBlock = {
  type: 'image' | 'audio';
  mimeType: string;
  data: string;
};

type McpResourceBlock = {
  type: 'resource';
  resource: {
    text?: string;
    blob?: string;
    mimeType?: string;
  };
};

type McpResourceLinkBlock = {
  type: 'resource_link';
  uri: string;
  title?: string;
  name?: string;
};

type McpContentBlock =
  | McpTextBlock
  | McpMediaBlock
  | McpResourceBlock
  | McpResourceLinkBlock;

class DiscoveredMCPToolInvocation extends BaseToolInvocation<
  ToolParams,
  ToolResult
> {
  private static readonly allowlist: Set<string> = new Set();

  constructor(
    private readonly mcpTool: CallableTool,
    readonly serverName: string,
    readonly serverToolName: string,
    readonly displayName: string,
    readonly timeout?: number,
    readonly trust?: boolean,
    params: ToolParams = {},
    private readonly cliConfig?: Config,
    private readonly mcpClient?: McpDirectClient,
    private readonly mcpTimeout?: number,
    private readonly mcpToolIdleTimeoutMs?: number,
    private readonly annotations?: McpToolAnnotations,
    private readonly retryCount: number = 0,
  ) {
    super(params);
  }

  override async shouldConfirmExecute(
    _abortSignal: AbortSignal,
  ): Promise<ToolCallConfirmationDetails | false> {
    const serverAllowListKey = this.serverName;
    const toolAllowListKey = `${this.serverName}.${this.serverToolName}`;

    if (this.trust) {
      return false; // server is trusted, no confirmation needed
    }

    if (
      DiscoveredMCPToolInvocation.allowlist.has(serverAllowListKey) ||
      DiscoveredMCPToolInvocation.allowlist.has(toolAllowListKey)
    ) {
      return false; // server and/or tool already allowlisted
    }

    const confirmationDetails: ToolMcpConfirmationDetails = {
      type: 'mcp',
      title: 'Confirm MCP Tool Execution',
      serverName: this.serverName,
      toolName: this.serverToolName, // Display original tool name in confirmation
      toolDisplayName: this.displayName, // Display global registry name exposed to model and user
      onConfirm: async (outcome: ToolConfirmationOutcome) => {
        if (outcome === ToolConfirmationOutcome.ProceedAlwaysServer) {
          DiscoveredMCPToolInvocation.allowlist.add(serverAllowListKey);
        } else if (outcome === ToolConfirmationOutcome.ProceedAlwaysTool) {
          DiscoveredMCPToolInvocation.allowlist.add(toolAllowListKey);
        }
      },
    };
    return confirmationDetails;
  }

  // Determine if the response contains tool errors
  // This is needed because CallToolResults should return errors inside the response.
  // ref: https://modelcontextprotocol.io/specification/2025-06-18/schema#calltoolresult
  isMCPToolError(rawResponseParts: Part[]): boolean {
    const functionResponse = rawResponseParts?.[0]?.functionResponse;
    const response = functionResponse?.response;

    interface McpError {
      isError?: boolean | string;
    }

    if (response) {
      const error = (response as { error?: McpError })?.error;
      const isError = error?.isError;

      if (error && (isError === true || isError === 'true')) {
        return true;
      }
    }
    return false;
  }

  private async attemptReconnect(): Promise<DiscoveredMCPTool | null> {
    if (!this.cliConfig) {
      return null;
    }

    try {
      debugLogger.info(
        `Attempting to reconnect MCP server '${this.serverName}'...`,
      );
      const toolRegistry = this.cliConfig.getToolRegistry();
      await toolRegistry.discoverToolsForServer(this.serverName);

      const newTool = await toolRegistry.ensureTool(
        `mcp__${this.serverName}__${this.serverToolName}`,
      );
      if (newTool instanceof DiscoveredMCPTool) {
        debugLogger.info(
          `Successfully reconnected to MCP server '${this.serverName}'`,
        );
        return newTool;
      }
      return null;
    } catch (error) {
      debugLogger.error(
        `Failed to reconnect MCP server '${this.serverName}': ${error}`,
      );
      return null;
    }
  }

  private async handleReconnectOnError(
    error: unknown,
    signal: AbortSignal,
    updateOutput?: (output: ToolResultDisplay) => void,
  ): Promise<ToolResult> {
    debugLogger.error(`MCP server error '${this.serverName}': ${error}`);

    if (!this.shouldAttemptReconnect(error)) {
      throw error;
    }

    if (this.retryCount < DiscoveredMCPToolInvocation.MAX_RECONNECT_RETRIES) {
      debugLogger.info(
        `Reconnection attempt ${this.retryCount + 1}/${DiscoveredMCPToolInvocation.MAX_RECONNECT_RETRIES} for MCP server '${this.serverName}'`,
      );
      const newTool = await this.attemptReconnect();
      if (newTool) {
        const newInvocation = new DiscoveredMCPToolInvocation(
          newTool['mcpTool'],
          this.serverName,
          this.serverToolName,
          this.displayName,
          this.trust,
          this.params,
          this.cliConfig,
          newTool['mcpClient'],
          this.mcpTimeout,
          this.mcpToolIdleTimeoutMs,
          this.annotations,
          this.retryCount + 1,
        );
        return newInvocation.execute(signal, updateOutput);
      }
    } else if (
      this.retryCount >= DiscoveredMCPToolInvocation.MAX_RECONNECT_RETRIES
    ) {
      debugLogger.error(
        `Max reconnection attempts (${DiscoveredMCPToolInvocation.MAX_RECONNECT_RETRIES}) reached for MCP server '${this.serverName}'`,
      );
    }

    throw error;
  }

  private shouldAttemptReconnect(error: unknown): boolean {
    if (isAbortError(error)) {
      return false;
    }

    if (getMCPServerStatus(this.serverName) === MCPServerStatus.DISCONNECTED) {
      return true;
    }

    const message = getErrorMessage(error);
    return MCP_CONNECTION_ERROR_PATTERNS.some((pattern) =>
      pattern.test(message),
    );
  }

  async execute(
    signal: AbortSignal,
    updateOutput?: (output: ToolResultDisplay) => void,
  ): Promise<ToolResult> {
    // Use direct MCP client if available (supports progress notifications),
    // otherwise fall back to the @google/genai mcpToTool wrapper.
    if (this.mcpClient) {
      return this.executeWithDirectClient(signal, updateOutput);
    }
    return this.executeWithCallableTool(signal);
  }

  /**
   * Execute using the raw MCP SDK Client, which supports progress
   * notifications via the onprogress callback. This enables real-time
   * streaming of progress updates to the user during long-running
   * MCP tool calls (e.g., browser automation).
   */
  private async executeWithDirectClient(
    signal: AbortSignal,
    updateOutput?: (output: ToolResultDisplay) => void,
  ): Promise<ToolResult> {
    // Create an AbortController for idle timeout
    const idleTimeoutController = new AbortController();
    let idleTimeoutId: ReturnType<typeof setTimeout> | undefined;

    // Combine the external signal with our idle timeout controller
    const combinedSignal = AbortSignal.any([
      signal,
      idleTimeoutController.signal,
    ]);

    const resetIdleTimeout = () => {
      if (idleTimeoutId) {
        clearTimeout(idleTimeoutId);
      }
      if (this.mcpToolIdleTimeoutMs && this.mcpToolIdleTimeoutMs > 0) {
        const timer = setTimeout(() => {
          const error = new Error(
            `MCP tool '${this.serverToolName}' on server '${this.serverName}' ` +
              `did not respond within ${this.mcpToolIdleTimeoutMs}ms idle timeout`,
          );
          error.name = 'AbortError';
          idleTimeoutController.abort(error);
        }, this.mcpToolIdleTimeoutMs);
        timer.unref();
        idleTimeoutId = timer;
      }
    };

    try {
      // Start the idle timeout
      resetIdleTimeout();

      const callToolResult = await this.mcpClient!.callTool(
        {
          name: this.serverToolName,
          arguments: this.params as Record<string, unknown>,
        },
        undefined,
        {
          onprogress: (progress) => {
            // Reset idle timeout on progress
            resetIdleTimeout();

            if (updateOutput) {
              const progressData: McpToolProgressData = {
                type: 'mcp_tool_progress',
                progress: progress.progress,
                ...(progress.total != null && { total: progress.total }),
                ...(progress.message != null && { message: progress.message }),
              };
              updateOutput(progressData);
            }
          },
          timeout: this.mcpTimeout,
          signal: combinedSignal,
        },
      );

      // Wrap the raw CallToolResult into the Part[] format that the
      // existing transform/display functions expect.
      const rawResponseParts = wrapMcpCallToolResultAsParts(
        this.serverToolName,
        callToolResult,
      );

      if (this.isMCPToolError(rawResponseParts)) {
        const errorMessage = `MCP tool '${
          this.serverToolName
        }' reported tool error for function call: ${safeJsonStringify({
          name: this.serverToolName,
          args: this.params,
        })} with response: ${safeJsonStringify(rawResponseParts)}`;
        return {
          llmContent: errorMessage,
          returnDisplay: `Error: MCP tool '${this.serverToolName}' reported an error.`,
          error: {
            message: errorMessage,
            type: ToolErrorType.MCP_TOOL_ERROR,
          },
        };
      }

      const transformedParts = transformMcpContentToParts(rawResponseParts);
      const truncatedParts = await this.truncateTextParts(transformedParts);

      return {
        llmContent: truncatedParts,
        returnDisplay: getDisplayFromParts(truncatedParts),
      };
    } catch (error) {
      return this.handleReconnectOnError(error, signal, updateOutput);
    } finally {
      // Clear the idle timeout in all cases
      if (idleTimeoutId) {
        clearTimeout(idleTimeoutId);
      }
    }
  }

  /**
   * Fallback: execute using the @google/genai CallableTool wrapper.
   * This path does NOT support progress notifications.
   */
  private async executeWithCallableTool(
    signal: AbortSignal,
  ): Promise<ToolResult> {
    const functionCalls: FunctionCall[] = [
      {
        name: this.serverToolName,
        args: this.params,
      },
    ];

    const rawResponseParts = await this.mcpTool.callTool(functionCalls);

    // Ensure the response is not an error
    if (this.isMCPToolError(rawResponseParts)) {
      const errorMessage = `MCP tool '${
        this.serverToolName
      }' reported tool error for function call: ${safeJsonStringify(
        functionCalls[0],
      )} with response: ${safeJsonStringify(rawResponseParts)}`;
      return {
        llmContent: errorMessage,
        returnDisplay: `Error: MCP tool '${this.serverToolName}' reported an error.`,
        error: {
          message: errorMessage,
          type: ToolErrorType.MCP_TOOL_ERROR,
        },
      };
    }

    const transformedParts = transformMcpContentToParts(rawResponseParts);

    return {
      llmContent: transformedParts,
      returnDisplay: getStringifiedResultForDisplay(rawResponseParts),
    };
  }

  getDescription(): string {
    return safeJsonStringify(this.params);
  }
}

export class DiscoveredMCPTool extends BaseDeclarativeTool<
  ToolParams,
  ToolResult
> {
  constructor(
    private readonly mcpTool: CallableTool,
    readonly serverName: string,
    readonly serverToolName: string,
    description: string,
    override readonly parameterSchema: unknown,
    readonly timeout?: number,
    readonly trust?: boolean,
    nameOverride?: string,
    private readonly cliConfig?: Config,
    private readonly mcpClient?: McpDirectClient,
    private readonly mcpTimeout?: number,
    private readonly mcpToolIdleTimeoutMs?: number,
    readonly annotations?: McpToolAnnotations,
    alwaysLoad = false,
  ) {
    super(
      nameOverride ?? generateValidName(serverToolName),
      `${serverToolName} (${serverName} MCP Server)`,
      description,
      Kind.Other,
      parameterSchema,
      true, // isOutputMarkdown
      true, // canUpdateOutput — enables streaming progress for MCP tools
      true, // shouldDefer — MCP tools are discovered via ToolSearch to keep the
      //   initial tool-declaration list small when many MCP servers are attached.
      alwaysLoad,
      // searchHint: server name boosts fuzzy matching when the user references
      // the server in their query ("send a slack message").
      `mcp ${serverName}`,
    );
  }

  asFullyQualifiedTool(): DiscoveredMCPTool {
    return new DiscoveredMCPTool(
      this.mcpTool,
      this.serverName,
      this.serverToolName,
      this.description,
      this.parameterSchema,
      this.timeout,
      this.trust,
      generateValidName(`mcp__${this.serverName}__${this.serverToolName}`),
      this.cliConfig,
      this.mcpClient,
      this.mcpTimeout,
      this.mcpToolIdleTimeoutMs,
      this.annotations,
      this.alwaysLoad,
    );
  }

  /**
   * Return a clone of this tool with a different `trust` value while
   * keeping every other field (including the shared underlying
   * `CallableTool` / MCP transport) identical.
   *
   * pool path: a single shared pool entry produces one
   * `DiscoveredMCPTool` snapshot; each `SessionMcpView` clones with
   * its own per-session trust before registering into its session's
   * `ToolRegistry`. Without this clone, mutating `trust` on the shared
   * instance would cross-contaminate sessions.
   *
   * Trust is the only field that legitimately varies per session;
   * everything else (transport, schema, name) is transport-level.
   */
  withTrust(trust: boolean | undefined): DiscoveredMCPTool {
    if (trust === this.trust) return this;
    return new DiscoveredMCPTool(
      this.mcpTool,
      this.serverName,
      this.serverToolName,
      this.description,
      this.parameterSchema,
      trust,
      // Preserve the original name (do NOT re-call generateValidName)
      // — equal-by-name is the registry's deduplication key, and a
      // different name would race-register two tools in the same
      // session.
      this.name,
      this.cliConfig,
      this.mcpClient,
      this.mcpTimeout,
      this.mcpToolIdleTimeoutMs,
      this.annotations,
      this.alwaysLoad,
    );
  }

  protected createInvocation(
    params: ToolParams,
  ): ToolInvocation<ToolParams, ToolResult> {
    return new DiscoveredMCPToolInvocation(
      this.mcpTool,
      this.serverName,
      this.serverToolName,
      this.displayName,
      this.timeout,
      this.trust,
      params,
      this.cliConfig,
      this.mcpClient,
      this.mcpTimeout,
      this.mcpToolIdleTimeoutMs,
      this.annotations,
    );
  }
}

function transformTextBlock(block: McpTextBlock): Part {
  return { text: block.text };
}

function transformImageAudioBlock(
  block: McpMediaBlock,
  toolName: string,
): Part[] {
  return [
    {
      text: `[Tool '${toolName}' provided the following ${
        block.type
      } data with mime-type: ${block.mimeType}]`,
    },
    {
      inlineData: {
        mimeType: block.mimeType,
        data: block.data,
      },
    },
  ];
}

function transformResourceBlock(
  block: McpResourceBlock,
  toolName: string,
): Part | Part[] | null {
  const resource = block.resource;
  if (resource?.text) {
    return { text: resource.text };
  }
  if (resource?.blob) {
    const mimeType = resource.mimeType || 'application/octet-stream';
    return [
      {
        text: `[Tool '${toolName}' provided the following embedded resource with mime-type: ${mimeType}]`,
      },
      {
        inlineData: {
          mimeType,
          data: resource.blob,
        },
      },
    ];
  }
  return null;
}

function transformResourceLinkBlock(block: McpResourceLinkBlock): Part {
  return {
    text: `Resource Link: ${block.title || block.name} at ${block.uri}`,
  };
}

/**
 * Transforms the raw MCP content blocks from the SDK response into a
 * standard GenAI Part array.
 * @param sdkResponse The raw Part[] array from `mcpTool.callTool()`.
 * @returns A clean Part[] array ready for the scheduler.
 */
function transformMcpContentToParts(sdkResponse: Part[]): Part[] {
  const funcResponse = sdkResponse?.[0]?.functionResponse;
  const mcpContent = funcResponse?.response?.['content'] as McpContentBlock[];
  const toolName = funcResponse?.name || 'unknown tool';

  if (!Array.isArray(mcpContent)) {
    return [{ text: '[Error: Could not parse tool response]' }];
  }

  const transformed = mcpContent.flatMap(
    (block: McpContentBlock): Part | Part[] | null => {
      switch (block.type) {
        case 'text':
          return transformTextBlock(block);
        case 'image':
        case 'audio':
          return transformImageAudioBlock(block, toolName);
        case 'resource':
          return transformResourceBlock(block, toolName);
        case 'resource_link':
          return transformResourceLinkBlock(block);
        default:
          return null;
      }
    },
  );

  return transformed.filter((part): part is Part => part !== null);
}

/**
 * Processes the raw response from the MCP tool to generate a clean,
 * human-readable string for display in the CLI. It summarizes non-text
 * content and presents text directly.
 *
 * @param rawResponse The raw Part[] array from the GenAI SDK.
 * @returns A formatted string representing the tool's output.
 */
function getStringifiedResultForDisplay(rawResponse: Part[]): string {
  const mcpContent = rawResponse?.[0]?.functionResponse?.response?.[
    'content'
  ] as McpContentBlock[];

  if (!Array.isArray(mcpContent)) {
    return '```json\n' + JSON.stringify(rawResponse, null, 2) + '\n```';
  }

  const displayParts = mcpContent.map((block: McpContentBlock): string => {
    switch (block.type) {
      case 'text':
        return block.text;
      case 'image':
        return `[Image: ${block.mimeType}]`;
      case 'audio':
        return `[Audio: ${block.mimeType}]`;
      case 'resource_link':
        return `[Link to ${block.title || block.name}: ${block.uri}]`;
      case 'resource':
        if (block.resource?.text) {
          return block.resource.text;
        }
        return `[Embedded Resource: ${
          block.resource?.mimeType || 'unknown type'
        }]`;
      default:
        return `[Unknown content type: ${(block as { type: string }).type}]`;
    }
  });

  return displayParts.join('\n');
}

/** Visible for testing */
export function generateValidName(name: string) {
  // Replace invalid characters (based on 400 error message from Gemini API) with underscores
  let validToolname = name.replace(/[^a-zA-Z0-9_.-]/g, '_');

  // If longer than 63 characters, replace middle with '___'
  // (Gemini API says max length 64, but actual limit seems to be 63)
  if (validToolname.length > 63) {
    validToolname =
      validToolname.slice(0, 28) + '___' + validToolname.slice(-32);
  }
  return validToolname;
}
