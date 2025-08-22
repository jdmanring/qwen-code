/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  describe,
  it,
  expect,
  vi,
  beforeEach,
  afterEach,
  Mocked,
} from 'vitest';
import { safeJsonStringify } from '../utils/safeJsonStringify.js';
import { DiscoveredMCPTool, generateValidName } from './mcp-tool.js'; // Added getStringifiedResultForDisplay
import { ToolResult, ToolConfirmationOutcome } from './tools.js'; // Added ToolConfirmationOutcome
import { CallableTool, Part } from '@google/genai';
import { ToolErrorType } from './tool-error.js';

// Mock @google/genai mcpToTool and CallableTool
// We only need to mock the parts of CallableTool that DiscoveredMCPTool uses.
const mockCallTool = vi.fn();
const mockToolMethod = vi.fn();

const mockCallableToolInstance: Mocked<CallableTool> = {
  tool: mockToolMethod as any, // Not directly used by DiscoveredMCPTool instance methods
  callTool: mockCallTool as any,
  // Add other methods if DiscoveredMCPTool starts using them
};

describe('generateValidName', () => {
  it('should return a valid name for a simple function', () => {
    expect(generateValidName('myFunction')).toBe('myFunction');
  });

  it('should replace invalid characters with underscores', () => {
    expect(generateValidName('invalid-name with spaces')).toBe(
      'invalid-name_with_spaces',
    );
  });

  it('should truncate long names', () => {
    expect(generateValidName('x'.repeat(80))).toBe(
      'xxxxxxxxxxxxxxxxxxxxxxxxxxxx___xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    );
  });

  it('should handle names with only invalid characters', () => {
    expect(generateValidName('!@#$%^&*()')).toBe('__________');
  });

  it('should handle names that are exactly 63 characters long', () => {
    expect(generateValidName('a'.repeat(63)).length).toBe(63);
  });

  it('should handle names that are exactly 64 characters long', () => {
    expect(generateValidName('a'.repeat(64)).length).toBe(63);
  });

  it('should handle names that are longer than 64 characters', () => {
    expect(generateValidName('a'.repeat(80)).length).toBe(63);
  });
});

describe('DiscoveredMCPTool', () => {
  const serverName = 'mock-mcp-server';
  const serverToolName = 'actual-server-tool-name';
  const baseDescription = 'A test MCP tool.';
  const inputSchema: Record<string, unknown> = {
    type: 'object' as const,
    properties: { param: { type: 'string' } },
    required: ['param'],
  };

  let tool: DiscoveredMCPTool;

  beforeEach(() => {
    mockCallTool.mockClear();
    mockToolMethod.mockClear();
    tool = new DiscoveredMCPTool(
      mockCallableToolInstance,
      serverName,
      serverToolName,
      baseDescription,
      inputSchema,
    );
    // Clear allowlist before each relevant test, especially for shouldConfirmExecute
    const invocation = tool.build({ param: 'mock' }) as any;
    invocation.constructor.allowlist.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('constructor', () => {
    it('should set properties correctly', () => {
      expect(tool.name).toBe(serverToolName);
      expect(tool.schema.name).toBe(serverToolName);
      expect(tool.schema.description).toBe(baseDescription);
      expect(tool.schema.parameters).toBeUndefined();
      expect(tool.schema.parametersJsonSchema).toEqual(inputSchema);
      expect(tool.serverToolName).toBe(serverToolName);
      expect(tool.timeout).toBeUndefined();
    });

    it('should accept and store a custom timeout', () => {
      const customTimeout = 5000;
      const toolWithTimeout = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        customTimeout,
      );
      expect(toolWithTimeout.timeout).toBe(customTimeout);
    });
  });

  describe('execute', () => {
    it('should call mcpTool.callTool with correct parameters and format display output', async () => {
      const params = { param: 'testValue' };
      const mockToolSuccessResultObject = {
        success: true,
        details: 'executed',
      };
      const mockFunctionResponseContent = [
        {
          type: 'text',
          text: JSON.stringify(mockToolSuccessResultObject),
        },
      ];
      const mockMcpToolResponseParts: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: { content: mockFunctionResponseContent },
          },
        },
      ];
      mockCallTool.mockResolvedValue(mockMcpToolResponseParts);

      const invocation = tool.build(params);
      const toolResult: ToolResult = await invocation.execute(
        new AbortController().signal,
      );

      expect(mockCallTool).toHaveBeenCalledWith([
        { name: serverToolName, args: params },
      ]);

      const stringifiedResponseContent = JSON.stringify(
        mockToolSuccessResultObject,
      );
      expect(toolResult.llmContent).toEqual([
        { text: stringifiedResponseContent },
      ]);
      expect(toolResult.returnDisplay).toBe(stringifiedResponseContent);
    });

    it('should handle empty result from getStringifiedResultForDisplay', async () => {
      const params = { param: 'testValue' };
      const mockMcpToolResponsePartsEmpty: Part[] = [];
      mockCallTool.mockResolvedValue(mockMcpToolResponsePartsEmpty);
      const invocation = tool.build(params);
      const toolResult: ToolResult = await invocation.execute(
        new AbortController().signal,
      );
      expect(toolResult.returnDisplay).toBe('```json\n[]\n```');
      expect(toolResult.llmContent).toEqual([
        { text: '[Error: Could not parse tool response]' },
      ]);
    });

    it('should propagate rejection if mcpTool.callTool rejects', async () => {
      const params = { param: 'failCase' };
      const expectedError = new Error('MCP call failed');
      mockCallTool.mockRejectedValue(expectedError);

      const invocation = tool.build(params);
      await expect(
        invocation.execute(new AbortController().signal),
      ).rejects.toThrow(expectedError);
    });

    it.each([
      { isErrorValue: true, description: 'true (bool)' },
      { isErrorValue: 'true', description: '"true" (str)' },
    ])(
      'should return a structured error if MCP tool reports an error',
      async ({ isErrorValue }) => {
        const tool = new DiscoveredMCPTool(
          mockCallableToolInstance,
          serverName,
          serverToolName,
          baseDescription,
          inputSchema,
        );
        const params = { param: 'isErrorTrueCase' };
        const functionCall = {
          name: serverToolName,
          args: params,
        };

        const errorResponse = { isError: isErrorValue };
        const mockMcpToolResponseParts: Part[] = [
          {
            functionResponse: {
              name: serverToolName,
              response: { error: errorResponse },
            },
          },
        ];
        mockCallTool.mockResolvedValue(mockMcpToolResponseParts);
        const expectedErrorMessage = `MCP tool '${
          serverToolName
        }' reported tool error for function call: ${safeJsonStringify(
          functionCall,
        )} with response: ${safeJsonStringify(mockMcpToolResponseParts)}`;
        const invocation = tool.build(params);
        const result = await invocation.execute(new AbortController().signal);

        expect(result.error?.type).toBe(ToolErrorType.MCP_TOOL_ERROR);
        expect(result.llmContent).toBe(expectedErrorMessage);
        expect(result.returnDisplay).toContain(
          `Error: MCP tool '${serverToolName}' reported an error.`,
        );
      },
    );

    it.each([
      { isErrorValue: false, description: 'false (bool)' },
      { isErrorValue: 'false', description: '"false" (str)' },
    ])(
      'should consider a ToolResult with isError ${description} to be a success',
      async ({ isErrorValue }) => {
        const tool = new DiscoveredMCPTool(
          mockCallableToolInstance,
          serverName,
          serverToolName,
          baseDescription,
          inputSchema,
        );
        const params = { param: 'isErrorFalseCase' };
        const mockToolSuccessResultObject = {
          success: true,
          details: 'executed',
        };
        const mockFunctionResponseContent = [
          {
            type: 'text',
            text: JSON.stringify(mockToolSuccessResultObject),
          },
        ];

        const errorResponse = { isError: isErrorValue };
        const mockMcpToolResponseParts: Part[] = [
          {
            functionResponse: {
              name: serverToolName,
              response: {
                error: errorResponse,
                content: mockFunctionResponseContent,
              },
            },
          },
        ];
        mockCallTool.mockResolvedValue(mockMcpToolResponseParts);

        const invocation = tool.build(params);
        const toolResult = await invocation.execute(
          new AbortController().signal,
        );

        const stringifiedResponseContent = JSON.stringify(
          mockToolSuccessResultObject,
        );
        expect(toolResult.llmContent).toEqual([
          { text: stringifiedResponseContent },
        ]);
        expect(toolResult.returnDisplay).toBe(stringifiedResponseContent);
      },
    );

    it('should handle a simple text response correctly', async () => {
      const params = { param: 'test' };
      const successMessage = 'This is a success message.';

      // Simulate the response from the GenAI SDK, which wraps the MCP
      // response in a functionResponse Part.
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              // The `content` array contains MCP ContentBlocks.
              content: [{ type: 'text', text: successMessage }],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      // 1. Assert that the llmContent sent to the scheduler is a clean Part array.
      expect(toolResult.llmContent).toEqual([{ text: successMessage }]);

      // 2. Assert that the display output is the simple text message.
      expect(toolResult.returnDisplay).toBe(successMessage);

      // 3. Verify that the underlying callTool was made correctly.
      expect(mockCallTool).toHaveBeenCalledWith([
        { name: serverToolName, args: params },
      ]);
    });

    it('should handle an AudioBlock response', async () => {
      const params = { param: 'play' };
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [
                {
                  type: 'audio',
                  data: 'BASE64_AUDIO_DATA',
                  mimeType: 'audio/mp3',
                },
              ],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      expect(toolResult.llmContent).toEqual([
        {
          text: `[Tool '${serverToolName}' provided the following audio data with mime-type: audio/mp3]`,
        },
        {
          inlineData: {
            mimeType: 'audio/mp3',
            data: 'BASE64_AUDIO_DATA',
          },
        },
      ]);
      expect(toolResult.returnDisplay).toBe('[Audio: audio/mp3]');
    });

    it('should handle a ResourceLinkBlock response', async () => {
      const params = { param: 'get' };
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [
                {
                  type: 'resource_link',
                  uri: 'file:///path/to/thing',
                  name: 'resource-name',
                  title: 'My Resource',
                },
              ],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      expect(toolResult.llmContent).toEqual([
        {
          text: 'Resource Link: My Resource at file:///path/to/thing',
        },
      ]);
      expect(toolResult.returnDisplay).toBe(
        '[Link to My Resource: file:///path/to/thing]',
      );
    });

    it('should handle an embedded text ResourceBlock response', async () => {
      const params = { param: 'get' };
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [
                {
                  type: 'resource',
                  resource: {
                    uri: 'file:///path/to/text.txt',
                    text: 'This is the text content.',
                    mimeType: 'text/plain',
                  },
                },
              ],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      expect(toolResult.llmContent).toEqual([
        { text: 'This is the text content.' },
      ]);
      expect(toolResult.returnDisplay).toBe('This is the text content.');
    });

    it('should handle an embedded binary ResourceBlock response', async () => {
      const params = { param: 'get' };
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [
                {
                  type: 'resource',
                  resource: {
                    uri: 'file:///path/to/data.bin',
                    blob: 'BASE64_BINARY_DATA',
                    mimeType: 'application/octet-stream',
                  },
                },
              ],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      expect(toolResult.llmContent).toEqual([
        {
          text: `[Tool '${serverToolName}' provided the following embedded resource with mime-type: application/octet-stream]`,
        },
        {
          inlineData: {
            mimeType: 'application/octet-stream',
            data: 'BASE64_BINARY_DATA',
          },
        },
      ]);
      expect(toolResult.returnDisplay).toBe(
        '[Embedded Resource: application/octet-stream]',
      );
    });

    it('should handle a mix of content block types', async () => {
      const params = { param: 'complex' };
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [
                { type: 'text', text: 'First part.' },
                {
                  type: 'image',
                  data: 'BASE64_IMAGE_DATA',
                  mimeType: 'image/jpeg',
                },
                { type: 'text', text: 'Second part.' },
              ],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      expect(toolResult.llmContent).toEqual([
        { text: 'First part.' },
        {
          text: `[Tool '${serverToolName}' provided the following image data with mime-type: image/jpeg]`,
        },
        {
          inlineData: {
            mimeType: 'image/jpeg',
            data: 'BASE64_IMAGE_DATA',
          },
        },
        { text: 'Second part.' },
      ]);
      expect(toolResult.returnDisplay).toBe(
        'First part.\n[Image: image/jpeg]\nSecond part.',
      );
    });

    it('should ignore unknown content block types', async () => {
      const params = { param: 'test' };
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [
                { type: 'text', text: 'Valid part.' },
                { type: 'future_block', data: 'some-data' },
              ],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      expect(toolResult.llmContent).toEqual([{ text: 'Valid part.' }]);
      expect(toolResult.returnDisplay).toBe(
        'Valid part.\n[Unknown content type: future_block]',
      );
    });

    it('should handle a complex mix of content block types', async () => {
      const params = { param: 'super-complex' };
      const sdkResponse: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [
                { type: 'text', text: 'Here is a resource.' },
                {
                  type: 'resource_link',
                  uri: 'file:///path/to/resource',
                  name: 'resource-name',
                  title: 'My Resource',
                },
                {
                  type: 'resource',
                  resource: {
                    uri: 'file:///path/to/text.txt',
                    text: 'Embedded text content.',
                    mimeType: 'text/plain',
                  },
                },
                {
                  type: 'image',
                  data: 'BASE64_IMAGE_DATA',
                  mimeType: 'image/jpeg',
                },
              ],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(sdkResponse);

      const invocation = tool.build(params);
      const toolResult = await invocation.execute(new AbortController().signal);

      expect(toolResult.llmContent).toEqual([
        { text: 'Here is a resource.' },
        {
          text: 'Resource Link: My Resource at file:///path/to/resource',
        },
        { text: 'Embedded text content.' },
        {
          text: `[Tool '${serverToolName}' provided the following image data with mime-type: image/jpeg]`,
        },
        {
          inlineData: {
            mimeType: 'image/jpeg',
            data: 'BASE64_IMAGE_DATA',
          },
        },
      ]);
      expect(toolResult.returnDisplay).toBe(
        'Here is a resource.\n[Link to My Resource: file:///path/to/resource]\nEmbedded text content.\n[Image: image/jpeg]',
      );
    });
  });

  describe('shouldConfirmExecute', () => {
    it('should return false if trust is true', async () => {
      const trustedTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        true,
      );
      const invocation = trustedTool.build({ param: 'mock' });
      expect(
        await invocation.shouldConfirmExecute(new AbortController().signal),
      ).toBe(false);
    });

    it('should return false if server is allowlisted', async () => {
      const invocation = tool.build({ param: 'mock' }) as any;
      invocation.constructor.allowlist.add(serverName);
      expect(
        await invocation.shouldConfirmExecute(new AbortController().signal),
      ).toBe(false);
    });

    it('should return false if tool is allowlisted', async () => {
      const toolAllowlistKey = `${serverName}.${serverToolName}`;
      const invocation = tool.build({ param: 'mock' }) as any;
      invocation.constructor.allowlist.add(toolAllowlistKey);
      expect(
        await invocation.shouldConfirmExecute(new AbortController().signal),
      ).toBe(false);
    });

    it('should return confirmation details if not trusted and not allowlisted', async () => {
      const invocation = tool.build({ param: 'mock' });
      const confirmation = await invocation.shouldConfirmExecute(
        new AbortController().signal,
      );
      expect(confirmation).not.toBe(false);
      if (confirmation && confirmation.type === 'mcp') {
        // Type guard for ToolMcpConfirmationDetails
        expect(confirmation.type).toBe('mcp');
        expect(confirmation.serverName).toBe(serverName);
        expect(confirmation.toolName).toBe(serverToolName);
      } else if (confirmation) {
        // Handle other possible confirmation types if necessary, or strengthen test if only MCP is expected
        throw new Error(
          'Confirmation was not of expected type MCP or was false',
        );
      } else {
        throw new Error(
          'Confirmation details not in expected format or was false',
        );
      }
    });

    it('should add server to allowlist on ProceedAlwaysServer', async () => {
      const invocation = tool.build({ param: 'mock' }) as any;
      const confirmation = await invocation.shouldConfirmExecute(
        new AbortController().signal,
      );
      expect(confirmation).not.toBe(false);
      if (
        confirmation &&
        typeof confirmation === 'object' &&
        'onConfirm' in confirmation &&
        typeof confirmation.onConfirm === 'function'
      ) {
        await confirmation.onConfirm(
          ToolConfirmationOutcome.ProceedAlwaysServer,
        );
        expect(invocation.constructor.allowlist.has(serverName)).toBe(true);
      } else {
        throw new Error(
          'Confirmation details or onConfirm not in expected format',
        );
      }
    });

    it('should add tool to allowlist on ProceedAlwaysTool', async () => {
      const toolAllowlistKey = `${serverName}.${serverToolName}`;
      const invocation = tool.build({ param: 'mock' }) as any;
      const confirmation = await invocation.shouldConfirmExecute(
        new AbortController().signal,
      );
      expect(confirmation).not.toBe(false);
      if (
        confirmation &&
        typeof confirmation === 'object' &&
        'onConfirm' in confirmation &&
        typeof confirmation.onConfirm === 'function'
      ) {
        await confirmation.onConfirm(ToolConfirmationOutcome.ProceedAlwaysTool);
        expect(invocation.constructor.allowlist.has(toolAllowlistKey)).toBe(
          true,
        );
      } else {
        throw new Error(
          'Confirmation details or onConfirm not in expected format',
        );
      }
    });

    it('should handle Cancel confirmation outcome', async () => {
      const invocation = tool.build({ param: 'mock' }) as any;
      const confirmation = await invocation.shouldConfirmExecute(
        new AbortController().signal,
      );
      expect(confirmation).not.toBe(false);
      if (
        confirmation &&
        typeof confirmation === 'object' &&
        'onConfirm' in confirmation &&
        typeof confirmation.onConfirm === 'function'
      ) {
        // Cancel should not add anything to allowlist
        await confirmation.onConfirm(ToolConfirmationOutcome.Cancel);
        expect(invocation.constructor.allowlist.has(serverName)).toBe(false);
        expect(
          invocation.constructor.allowlist.has(
            `${serverName}.${serverToolName}`,
          ),
        ).toBe(false);
      } else {
        throw new Error(
          'Confirmation details or onConfirm not in expected format',
        );
      }
    });

    it('should handle ProceedOnce confirmation outcome', async () => {
      const invocation = tool.build({ param: 'mock' }) as any;
      const confirmation = await invocation.shouldConfirmExecute(
        new AbortController().signal,
      );
      expect(confirmation).not.toBe(false);
      if (
        confirmation &&
        typeof confirmation === 'object' &&
        'onConfirm' in confirmation &&
        typeof confirmation.onConfirm === 'function'
      ) {
        // ProceedOnce should not add anything to allowlist
        await confirmation.onConfirm(ToolConfirmationOutcome.ProceedOnce);
        expect(invocation.constructor.allowlist.has(serverName)).toBe(false);
        expect(
          invocation.constructor.allowlist.has(
            `${serverName}.${serverToolName}`,
          ),
        ).toBe(false);
      } else {
        throw new Error(
          'Confirmation details or onConfirm not in expected format',
        );
      }
    });
  });

  describe('DiscoveredMCPToolInvocation', () => {
    it('should return the stringified params from getDescription', () => {
      const params = { param: 'testValue', param2: 'anotherOne' };
      const invocation = tool.build(params);
      const description = invocation.getDescription();
      expect(description).toBe('{"param":"testValue","param2":"anotherOne"}');
    });
  });

  describe('output truncation for large MCP results', () => {
    const THRESHOLD = 1000;
    const TRUNCATE_LINES = 50;

    const mockConfigWithTruncation = {
      getTruncateToolOutputThreshold: () => THRESHOLD,
      getTruncateToolOutputLines: () => TRUNCATE_LINES,
      getUsageStatisticsEnabled: () => false,
      storage: {
        getProjectTempDir: () => '/tmp/test-project',
      },
      isTrustedFolder: () => true,
    } as any;

    it('should truncate large text results from direct client execution', async () => {
      const largeText = 'Line of text content\n'.repeat(25000); // ~525k chars, over the 500k MCP char budget
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(async () => ({
          content: [{ type: 'text', text: largeText }],
        })),
      };

      const truncTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true, // trust
        undefined,
        mockConfigWithTruncation,
        mockMcpClient,
      );

      const invocation = truncTool.build({ param: 'test' });
      const result = await invocation.execute(new AbortController().signal);

      // The text part in llmContent should be truncated
      const textParts = (result.llmContent as Part[]).filter(
        (p: Part) => p.text,
      );
      const combinedText = textParts.map((p: Part) => p.text).join('');
      expect(combinedText.length).toBeLessThan(largeText.length);
      expect(combinedText).toContain('CONTENT TRUNCATED');
      expect(result.returnDisplay).toContain('CONTENT TRUNCATED');
    });

    it('should truncate large text results from callable tool execution', async () => {
      const largeText = 'Line of text content\n'.repeat(25000);
      const mockMcpToolResponseParts: Part[] = [
        {
          functionResponse: {
            name: serverToolName,
            response: {
              content: [{ type: 'text', text: largeText }],
            },
          },
        },
      ];
      mockCallTool.mockResolvedValue(mockMcpToolResponseParts);

      const truncTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true,
        undefined,
        mockConfigWithTruncation,
      );

      const invocation = truncTool.build({ param: 'test' });
      const result = await invocation.execute(new AbortController().signal);

      const textParts = (result.llmContent as Part[]).filter(
        (p: Part) => p.text,
      );
      const combinedText = textParts.map((p: Part) => p.text).join('');
      expect(combinedText.length).toBeLessThan(largeText.length);
      expect(combinedText).toContain('CONTENT TRUNCATED');
      expect(result.returnDisplay).toContain('CONTENT TRUNCATED');
    });

    it('should not truncate small text results', async () => {
      const smallText = 'Small response';
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(async () => ({
          content: [{ type: 'text', text: smallText }],
        })),
      };

      const truncTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true,
        undefined,
        mockConfigWithTruncation,
        mockMcpClient,
      );

      const invocation = truncTool.build({ param: 'test' });
      const result = await invocation.execute(new AbortController().signal);

      expect(result.llmContent).toEqual([{ text: smallText }]);
      expect(result.returnDisplay).not.toContain('Output too long');
    });

    it('should not truncate non-text content (images, audio)', async () => {
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(async () => ({
          content: [
            {
              type: 'image',
              data: 'x'.repeat(5000), // large base64 data
              mimeType: 'image/png',
            },
          ],
        })),
      };

      const truncTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true,
        undefined,
        mockConfigWithTruncation,
        mockMcpClient,
      );

      const invocation = truncTool.build({ param: 'test' });
      const result = await invocation.execute(new AbortController().signal);

      // Image data should not be truncated
      const inlineDataParts = (result.llmContent as Part[]).filter(
        (p: Part) => p.inlineData,
      );
      expect(inlineDataParts[0].inlineData!.data).toBe('x'.repeat(5000));
    });

    it('should truncate only text parts in mixed content', async () => {
      const largeText = 'Line of text content\n'.repeat(25000);
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(async () => ({
          content: [
            { type: 'text', text: largeText },
            {
              type: 'image',
              data: 'IMAGE_DATA',
              mimeType: 'image/png',
            },
          ],
        })),
      };

      const truncTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true,
        undefined,
        mockConfigWithTruncation,
        mockMcpClient,
      );

      const invocation = truncTool.build({ param: 'test' });
      const result = await invocation.execute(new AbortController().signal);

      const parts = result.llmContent as Part[];
      // Text should be truncated
      const textPart = parts.find(
        (p: Part) => p.text && !p.text.startsWith('[Tool'),
      );
      expect(textPart!.text!.length).toBeLessThan(largeText.length);
      expect(textPart!.text).toContain('CONTENT TRUNCATED');
      // Image should be preserved
      const imagePart = parts.find((p: Part) => p.inlineData);
      expect(imagePart!.inlineData!.data).toBe('IMAGE_DATA');
    });

    it('should not truncate when config is not provided', async () => {
      const largeText = 'Line of text content\n'.repeat(200);
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(async () => ({
          content: [{ type: 'text', text: largeText }],
        })),
      };

      // No cliConfig provided
      const truncTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        undefined, // no config
        mockMcpClient,
      );

      const invocation = truncTool.build({ param: 'test' });
      const result = await invocation.execute(new AbortController().signal);

      // Without config, should return untouched
      expect(result.llmContent).toEqual([{ text: largeText }]);
    });
  });

  describe('streaming progress for long-running MCP tools', () => {
    it('should have canUpdateOutput set to true so the scheduler creates liveOutputCallback', () => {
      // For long-running MCP tools (e.g., browseruse), the scheduler needs
      // canUpdateOutput=true to create a liveOutputCallback. Without this,
      // users see no progress during potentially minutes-long operations.
      expect(tool.canUpdateOutput).toBe(true);
    });

    it('should forward MCP progress notifications to updateOutput callback during execution', async () => {
      const params = { param: 'https://example.com' };

      // Create a mock MCP direct client that simulates progress notifications.
      // When callTool is called with an onprogress callback, it invokes
      // the callback to simulate the MCP server sending progress updates.
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(async (_params, _schema, options) => {
          // Simulate 3 progress notifications from the MCP server
          for (let i = 1; i <= 3; i++) {
            await new Promise((resolve) => setTimeout(resolve, 10));
            options?.onprogress?.({
              progress: i,
              total: 3,
              message: `Step ${i} of 3`,
            });
          }
          return {
            content: [
              {
                type: 'text',
                text: 'Browser automation completed successfully.',
              },
            ],
          };
        }),
      };

      // Create a tool with the direct MCP client
      const streamingTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined, // trust
        undefined, // nameOverride
        undefined, // cliConfig
        mockMcpClient,
      );

      const invocation = streamingTool.build(params);
      const updateOutputSpy = vi.fn();

      const result = await invocation.execute(
        new AbortController().signal,
        updateOutputSpy,
      );

      // The final result should still be correct
      expect(result.llmContent).toEqual([
        { text: 'Browser automation completed successfully.' },
      ]);

      // The updateOutput callback SHOULD have been called at least once
      // with intermediate progress, so users can see what's happening
      // during the long wait.
      expect(updateOutputSpy).toHaveBeenCalled();
      expect(updateOutputSpy).toHaveBeenCalledTimes(3);
      // Verify progress data contains structured MCP progress info
      expect(updateOutputSpy).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'mcp_tool_progress',
          progress: 1,
          total: 3,
          message: 'Step 1 of 3',
        }),
      );
      expect(updateOutputSpy).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'mcp_tool_progress',
          progress: 3,
          total: 3,
          message: 'Step 3 of 3',
        }),
      );
    });

    it('should show incremental progress for multi-step browser automation', async () => {
      const params = { param: 'fill-form' };
      const steps = [
        'Navigating to page...',
        'Filling username field...',
        'Filling password field...',
        'Clicking submit...',
      ];

      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(async (_params, _schema, options) => {
          for (let i = 0; i < steps.length; i++) {
            await new Promise((resolve) => setTimeout(resolve, 10));
            options?.onprogress?.({
              progress: i + 1,
              total: steps.length,
              message: steps[i],
            });
          }
          return {
            content: [{ type: 'text', text: steps.join('\n') }],
          };
        }),
      };

      const streamingTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        undefined,
        mockMcpClient,
      );

      const invocation = streamingTool.build(params);
      const receivedUpdates: unknown[] = [];
      const updateOutputCallback = (output: unknown) => {
        receivedUpdates.push(output);
      };

      await invocation.execute(
        new AbortController().signal,
        updateOutputCallback,
      );

      // User should have received one update per step
      expect(receivedUpdates.length).toBeGreaterThan(0);
      expect(receivedUpdates).toHaveLength(steps.length);
      // Each update should be structured McpToolProgressData
      expect(receivedUpdates[0]).toEqual({
        type: 'mcp_tool_progress',
        progress: 1,
        total: steps.length,
        message: 'Navigating to page...',
      });
      expect(receivedUpdates[3]).toEqual({
        type: 'mcp_tool_progress',
        progress: 4,
        total: steps.length,
        message: 'Clicking submit...',
      });
    });
  });

  describe('auto-reconnect on connection error', () => {
    it('should attempt reconnect and retry on connection error', async () => {
      const params = { param: 'test' };
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(),
      };

      const successResult = {
        content: [{ type: 'text', text: 'Success after reconnect' }],
      };

      const newMockMcpClient: McpDirectClient = {
        callTool: vi.fn().mockResolvedValueOnce(successResult),
      };

      const newTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        undefined,
        newMockMcpClient,
      );

      const discoverToolsForServer = vi.fn().mockResolvedValue(undefined);
      const ensureTool = vi.fn().mockResolvedValue(newTool);
      const mockConfig = {
        isTrustedFolder: () => true,
        getToolRegistry: () => ({
          discoverToolsForServer,
          ensureTool,
        }),
        getTruncateToolOutputThreshold: () => 0,
        getTruncateToolOutputLines: () => 0,
      };

      const connectionError = new Error('Connection closed');

      updateMCPServerStatus(serverName, MCPServerStatus.CONNECTED);
      (mockMcpClient.callTool as any).mockRejectedValueOnce(connectionError);

      const reconnectTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        mockConfig as any,
        mockMcpClient,
      );

      const invocation = reconnectTool.build(params);
      const result = await invocation.execute(new AbortController().signal);

      expect(mockMcpClient.callTool).toHaveBeenCalledTimes(1);
      expect(newMockMcpClient.callTool).toHaveBeenCalledTimes(1);
      expect(discoverToolsForServer).toHaveBeenCalledWith(serverName);
      expect(result.llmContent).toEqual([{ text: 'Success after reconnect' }]);
    });

    it('should not retry on non-connection errors', async () => {
      const params = { param: 'test' };
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(),
      };

      const retryClient: McpDirectClient = {
        callTool: vi
          .fn()
          .mockResolvedValueOnce({ content: [{ type: 'text', text: 'OK' }] }),
      };
      const retryTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        undefined,
        retryClient,
      );

      const discoverToolsForServer = vi.fn().mockResolvedValue(undefined);
      const ensureTool = vi.fn().mockResolvedValue(retryTool);
      const mockConfig = {
        isTrustedFolder: () => true,
        getToolRegistry: () => ({
          discoverToolsForServer,
          ensureTool,
        }),
      };

      updateMCPServerStatus(serverName, MCPServerStatus.CONNECTED);

      const toolError = new Error('Invalid parameters');
      (mockMcpClient.callTool as any).mockRejectedValue(toolError);

      const reconnectTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        mockConfig as any,
        mockMcpClient,
      );

      const invocation = reconnectTool.build(params);
      await expect(
        invocation.execute(new AbortController().signal),
      ).rejects.toThrow('Invalid parameters');

      expect(mockMcpClient.callTool).toHaveBeenCalledTimes(1);
      expect(discoverToolsForServer).not.toHaveBeenCalled();
      expect(ensureTool).not.toHaveBeenCalled();
      expect(retryClient.callTool).not.toHaveBeenCalled();
    });

    it('should not retry aborted calls even when the server is disconnected', async () => {
      const params = { param: 'test' };
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(),
      };

      const retryClient: McpDirectClient = {
        callTool: vi
          .fn()
          .mockResolvedValueOnce({ content: [{ type: 'text', text: 'OK' }] }),
      };
      const retryTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        undefined,
        retryClient,
      );

      const discoverToolsForServer = vi.fn().mockResolvedValue(undefined);
      const ensureTool = vi.fn().mockResolvedValue(retryTool);
      const mockConfig = {
        isTrustedFolder: () => true,
        getToolRegistry: () => ({
          discoverToolsForServer,
          ensureTool,
        }),
      };

      updateMCPServerStatus(serverName, MCPServerStatus.DISCONNECTED);
      const abortError = new Error('The operation was aborted');
      abortError.name = 'AbortError';
      (mockMcpClient.callTool as any).mockRejectedValue(abortError);

      const reconnectTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        mockConfig as any,
        mockMcpClient,
      );

      const invocation = reconnectTool.build(params);
      await expect(
        invocation.execute(new AbortController().signal),
      ).rejects.toThrow('The operation was aborted');

      expect(mockMcpClient.callTool).toHaveBeenCalledTimes(1);
      expect(discoverToolsForServer).not.toHaveBeenCalled();
      expect(ensureTool).not.toHaveBeenCalled();
      expect(retryClient.callTool).not.toHaveBeenCalled();
    });

    it('should not retry after reconnection attempt fails', async () => {
      const params = { param: 'test' };
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn(),
      };

      const secondMockMcpClient: McpDirectClient = {
        callTool: vi.fn().mockRejectedValue(new Error('ECONNREFUSED')),
      };

      const secondTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        undefined,
        secondMockMcpClient,
      );

      const discoverToolsForServer = vi.fn().mockResolvedValue(undefined);
      const mockConfig = {
        isTrustedFolder: () => true,
        getToolRegistry: () => ({
          discoverToolsForServer,
          ensureTool: vi.fn().mockResolvedValue(secondTool),
        }),
      };

      const connectionError = new Error('ECONNREFUSED');
      updateMCPServerStatus(serverName, MCPServerStatus.CONNECTED);
      (mockMcpClient.callTool as any).mockRejectedValue(connectionError);

      const reconnectTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        mockConfig as any,
        mockMcpClient,
      );

      const invocation = reconnectTool.build(params);
      await expect(
        invocation.execute(new AbortController().signal),
      ).rejects.toThrow('ECONNREFUSED');

      expect(mockMcpClient.callTool).toHaveBeenCalledTimes(1);
      expect(secondMockMcpClient.callTool).toHaveBeenCalledTimes(3);
      expect(discoverToolsForServer).toHaveBeenCalledTimes(3);
    });

    it('should detect various connection error patterns', async () => {
      const connectionErrors = [
        'ECONNREFUSED',
        'ENOTFOUND',
        'ECONNRESET',
        'ETIMEDOUT',
        'connection closed',
        'Connection lost',
        'Not connected',
        'Disconnected',
        'Transport closed',
      ];

      for (const errorMsg of connectionErrors) {
        const params = { param: 'test' };
        const mockMcpClient: McpDirectClient = {
          callTool: vi.fn().mockRejectedValueOnce(new Error(errorMsg)),
        };

        const newMockMcpClient: McpDirectClient = {
          callTool: vi
            .fn()
            .mockResolvedValueOnce({ content: [{ type: 'text', text: 'OK' }] }),
        };

        const newTool = new DiscoveredMCPTool(
          mockCallableToolInstance,
          serverName,
          serverToolName,
          baseDescription,
          inputSchema,
          undefined,
          undefined,
          undefined,
          newMockMcpClient,
        );

        const discoverToolsForServer = vi.fn().mockResolvedValue(undefined);
        const mockConfig = {
          isTrustedFolder: () => true,
          getToolRegistry: () => ({
            discoverToolsForServer,
            ensureTool: vi.fn().mockResolvedValue(newTool),
          }),
          getTruncateToolOutputThreshold: () => 0,
          getTruncateToolOutputLines: () => 0,
        };

        const reconnectTool = new DiscoveredMCPTool(
          mockCallableToolInstance,
          serverName,
          serverToolName,
          baseDescription,
          inputSchema,
          undefined,
          undefined,
          mockConfig as any,
          mockMcpClient,
        );

        const invocation = reconnectTool.build(params);
        updateMCPServerStatus(serverName, MCPServerStatus.CONNECTED);
        await invocation.execute(new AbortController().signal);

        expect(discoverToolsForServer).toHaveBeenCalled();
      }
    });

    it('should reconnect when MCP error occurs and server is disconnected', async () => {
      const params = { param: 'test' };
      const mockMcpClient: McpDirectClient = {
        callTool: vi
          .fn()
          .mockRejectedValueOnce(
            new Error('MCP error -32602: Invalid request'),
          ),
      };

      const newMockMcpClient: McpDirectClient = {
        callTool: vi
          .fn()
          .mockResolvedValueOnce({ content: [{ type: 'text', text: 'OK' }] }),
      };

      const newTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        undefined,
        newMockMcpClient,
      );

      const discoverToolsForServer = vi.fn().mockResolvedValue(undefined);
      const mockConfig = {
        isTrustedFolder: () => true,
        getToolRegistry: () => ({
          discoverToolsForServer,
          ensureTool: vi.fn().mockResolvedValue(newTool),
        }),
        getTruncateToolOutputThreshold: () => 0,
        getTruncateToolOutputLines: () => 0,
      };

      updateMCPServerStatus(serverName, MCPServerStatus.DISCONNECTED);

      const reconnectTool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        undefined,
        undefined,
        mockConfig as any,
        mockMcpClient,
      );

      const invocation = reconnectTool.build(params);
      await invocation.execute(new AbortController().signal);

      expect(discoverToolsForServer).toHaveBeenCalled();
    });
  });

  describe('MCP Tool Idle Timeout', () => {
    it('should abort when MCP server does not respond within idle timeout', async () => {
      vi.useFakeTimers();

      const idleTimeoutMs = 1000; // 1 second for testing
      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn().mockImplementation(
          (_params, _schema, options) =>
            new Promise((_resolve, reject) => {
              // Simulate SDK behavior: reject when signal is aborted
              options?.signal?.addEventListener('abort', () => {
                const error = new Error(
                  (options?.signal as AbortSignal & { reason?: Error })?.reason
                    ?.message ?? 'The operation was aborted',
                );
                error.name = 'AbortError';
                reject(error);
              });
            }),
        ),
      };

      const tool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true,
        undefined,
        undefined,
        mockMcpClient,
        undefined,
        idleTimeoutMs,
      );

      const invocation = tool.build({ param: 'test' });
      const abortController = new AbortController();
      const executePromise = invocation.execute(abortController.signal);

      // Advance time to trigger the idle timeout
      vi.advanceTimersByTime(idleTimeoutMs + 100);

      await expect(executePromise).rejects.toThrow(
        /did not respond within.*idle timeout/,
      );
      // The external abort signal should not have been triggered
      expect(abortController.signal.aborted).toBe(false);

      vi.useRealTimers();
    });

    it('should reset idle timeout on progress updates', async () => {
      vi.useFakeTimers();

      const idleTimeoutMs = 1000;
      let onProgressCallback: ((progress: any) => void) | undefined;

      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn().mockImplementation((_params, _schema, options) => {
          onProgressCallback = options?.onprogress;
          return new Promise((resolve, reject) => {
            // Listen for abort signal to properly reject when timeout fires
            options?.signal?.addEventListener('abort', () => {
              reject(options.signal!.reason);
            });
            // Resolve after 2.5 seconds (would timeout without progress)
            setTimeout(() => {
              resolve({ content: [{ type: 'text', text: 'Success' }] });
            }, 2500);
          });
        }),
      };

      const tool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true,
        undefined,
        undefined,
        mockMcpClient,
        undefined,
        idleTimeoutMs,
      );

      const invocation = tool.build({ param: 'test' });
      const executePromise = invocation.execute(new AbortController().signal);

      // Send progress at 500ms, 1400ms, 2300ms to reset the timeout
      // Each progress must arrive BEFORE the 1000ms idle timeout fires
      vi.advanceTimersByTime(500);
      onProgressCallback?.({ progress: 0.25 });

      vi.advanceTimersByTime(900);
      onProgressCallback?.({ progress: 0.5 });

      vi.advanceTimersByTime(900);
      onProgressCallback?.({ progress: 0.75 });

      // Advance past the mock's 2500ms resolve time
      vi.advanceTimersByTime(200);

      const result = await executePromise;

      expect(result.error).toBeUndefined();
      expect(result.llmContent).toBeDefined();

      vi.useRealTimers();
    });

    it('should not apply idle timeout when set to 0 or undefined', async () => {
      vi.useFakeTimers();

      const mockMcpClient: McpDirectClient = {
        callTool: vi.fn().mockResolvedValue({
          content: [{ type: 'text', text: 'Success' }],
        }),
      };

      const tool = new DiscoveredMCPTool(
        mockCallableToolInstance,
        serverName,
        serverToolName,
        baseDescription,
        inputSchema,
        true,
        undefined,
        undefined,
        mockMcpClient,
        undefined,
        undefined, // No idle timeout
      );

      const invocation = tool.build({ param: 'test' });
      const result = await invocation.execute(new AbortController().signal);

      expect(result.error).toBeUndefined();
      expect(result.llmContent).toBeDefined();

      vi.useRealTimers();
    });
  });
});
