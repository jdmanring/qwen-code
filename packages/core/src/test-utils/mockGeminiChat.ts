/**
 * @license
 * Copyright 2025 Qwen
 * SPDX-License-Identifier: Apache-2.0
 */

import { vi } from 'vitest';
import type { GeminiChatInterface } from '../core/geminiChat.js';
import { CompressionStatus } from '../core/turn.js';
import type { Config } from '../config/config.js';

/**
 * A type-safe mock of the GeminiChat class.
 * Implements GeminiChatInterface to satisfy type checks without using 'as any'
 * and to avoid recursive loops when GeminiChat is mocked.
 */
export class MockGeminiChat implements GeminiChatInterface {
  constructor(config: Config) {
    // No super() call needed as we no longer extend GeminiChat
  }

  sendMessageStream = vi.fn();
  setLastPromptTokenCount = vi.fn();
  getLastPromptTokenCount = vi.fn().mockReturnValue(0);
  tryCompress = vi.fn().mockResolvedValue({
    compressionStatus: CompressionStatus.NOOP,
    originalTokenCount: 0,
    newTokenCount: 0,
  });
  compressFast = vi.fn().mockReturnValue({
    info: {
      compressionStatus: CompressionStatus.NOOP,
      originalTokenCount: 0,
      newTokenCount: 0,
    },
  });
  setSystemInstruction = vi.fn();
  setSessionStartContext = vi.fn();
  applySessionStartContext = vi.fn();
  getHistory = vi.fn().mockReturnValue([]);
  setHistory = vi.fn();
  getHistoryShallow = vi.fn().mockReturnValue([]);
}
