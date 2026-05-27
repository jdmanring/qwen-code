/**
 * @license
 * Copyright 2025 Qwen
 * SPDX-License-Identifier: Apache-2.0
 */

import type {
  MCPServerConfig,
  MCPServerStatus,
} from '@qwen-code/qwen-code-core';

/**
 * MCP
 */
export const MCP_MANAGEMENT_STEPS = {
  SERVER_LIST: 'server-list',
  SERVER_DETAIL: 'server-detail',
  DISABLE_SCOPE_SELECT: 'disable-scope-select',
  TOOL_LIST: 'tool-list',
  TOOL_DETAIL: 'tool-detail',
  AUTHENTICATE: 'authenticate', // OAuth 
} as const;

export type MCPManagementStep =
  (typeof MCP_MANAGEMENT_STEPS)[keyof typeof MCP_MANAGEMENT_STEPS];

/**
 * MCP
 */
export interface MCPServerDisplayInfo {
  /**  */
  name: string;
  /**  */
  status: MCPServerStatus;
  /**  */
  source: 'user' | 'project' | 'extension';
  /**  */
  configPath?: string;
  /**  */
  config: MCPServerConfig;
  /**  */
  toolCount: number;
  /** namedescription */
  invalidToolCount?: number;
  /** Prompt */
  promptCount: number;
  /**  */
  errorMessage?: string;
  /**  */
  isDisabled: boolean;
  /**  OAuth  */
  hasOAuthTokens?: boolean;
}

/**
 * MCP
 */
export interface MCPToolDisplayInfo {
  /**  */
  name: string;
  /**  */
  description?: string;
  /**  */
  serverName: string;
  /** schema */
  schema?: object;
  /**  */
  annotations?: {
    title?: string;
    readOnlyHint?: boolean;
    destructiveHint?: boolean;
    idempotentHint?: boolean;
    openWorldHint?: boolean;
  };
  /** namedescriptionLLM */
  isValid: boolean;
  /** isValidfalse */
  invalidReason?: string;
}

/**
 * MCP Prompt
 */
export interface MCPPromptDisplayInfo {
  /** Prompt */
  name: string;
  /** Prompt */
  description?: string;
  /**  */
  serverName: string;
  /**  */
  arguments?: Array<{
    name: string;
    description?: string;
    required?: boolean;
  }>;
}

/**
 * 
 */
export interface GroupedServers {
  /**  */
  source: string;
  /**  */
  displayName: string;
  /**  */
  configPath?: string;
  /**  */
  servers: MCPServerDisplayInfo[];
}

/**
 * ServerListStep
 */
export interface ServerListStepProps {
  /**  */
  servers: MCPServerDisplayInfo[];
  /**  */
  onSelect: (index: number) => void;
}

/**
 * ServerDetailStep 
 */
export interface ServerDetailStepProps {
  /**  */
  server: MCPServerDisplayInfo | null;
  /**  */
  onViewTools: () => void;
  /**  */
  onReconnect?: () => void;
  /**  */
  onDisable?: () => void;
  /** OAuth  */
  onAuthenticate?: () => void;
  /**  */
  onClearAuth?: () => void;
  /**  */
  onBack: () => void;
}

/**
 * DisableScopeSelectStep
 */
export interface DisableScopeSelectStepProps {
  /**  */
  server: MCPServerDisplayInfo | null;
  /**  scope  */
  onSelectScope: (scope: 'user' | 'workspace') => void;
  /**  */
  onBack: () => void;
}

/**
 * ToolListStep
 */
export interface ToolListStepProps {
  /**  */
  tools: MCPToolDisplayInfo[];
  /**  */
  serverName: string;
  /**  */
  onSelect: (tool: MCPToolDisplayInfo) => void;
  /**  */
  onBack: () => void;
}

/**
 * ToolDetailStep 
 */
export interface ToolDetailStepProps {
  /**  */
  tool: MCPToolDisplayInfo | null;
  /**  */
  onBack: () => void;
}

/**
 * AuthenticateStep 
 */
export interface AuthenticateStepProps {
  /**  */
  server: MCPServerDisplayInfo | null;
  /**  */
  onBack: () => void;
}

/**
 * MCP
 */
export interface MCPManagementDialogProps {
  /**  */
  onClose: () => void;
}
