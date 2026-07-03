/**
 * @license
 * Copyright 2025 Qwen Team
 * SPDX-License-Identifier: Apache-2.0
 */

import type { FC } from 'react';
import type { BaseToolCallProps, ToolCallData } from './shared/index.js';
import { AgentToolCall, isAgentExecutionToolCall } from './AgentToolCall.js';
import { GenericToolCall } from './GenericToolCall.js';
import { ThinkToolCall } from './ThinkToolCall.js';
import { EditToolCall } from './EditToolCall.js';
import { WriteToolCall } from './WriteToolCall.js';
import { SearchToolCall } from './SearchToolCall.js';
import { UpdatedPlanToolCall } from './UpdatedPlanToolCall.js';
import { ShellToolCall } from './ShellToolCall.js';
import { ReadToolCall } from './ReadToolCall.js';
import { WebFetchToolCall } from './WebFetchToolCall.js';

interface ToolCallRendererProps extends BaseToolCallProps {
  toolCall: ToolCallData;
}

const COMPONENT_MAP: Record<string, FC<BaseToolCallProps>> = {
  read: ReadToolCall,
  read_file: ReadToolCall,
  read_many_files: ReadToolCall,
  readmanyfiles: ReadToolCall,
  list_directory: ReadToolCall,
  listfiles: ReadToolCall,
  write: WriteToolCall,
  edit: EditToolCall,
  execute: ShellToolCall,
  bash: ShellToolCall,
  command: ShellToolCall,
  updated_plan: UpdatedPlanToolCall,
  updatedplan: UpdatedPlanToolCall,
  todo_write: UpdatedPlanToolCall,
  update_todos: UpdatedPlanToolCall,
  todowrite: UpdatedPlanToolCall,
  search: SearchToolCall,
  grep: SearchToolCall,
  glob: SearchToolCall,
  find: SearchToolCall,
  think: ThinkToolCall,
  thinking: ThinkToolCall,
  fetch: WebFetchToolCall,
  web_fetch: WebFetchToolCall,
  webfetch: WebFetchToolCall,
  web_search: WebFetchToolCall,
};

export const ToolCallRenderer: FC<ToolCallRendererProps> = ({
  toolCall,
  isFirst,
  isLast,
}) => {
  const Component = isAgentExecutionToolCall(toolCall)
    ? AgentToolCall
    : (COMPONENT_MAP[toolCall.kind.toLowerCase()] ?? GenericToolCall);
  return <Component toolCall={toolCall} isFirst={isFirst} isLast={isLast} />;
};
