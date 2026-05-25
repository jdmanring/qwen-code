/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

/// <reference types="vitest" />
import { defineConfig } from 'vitest/config';
import path from 'node:path';

export default defineConfig({
  resolve: {
    alias: {
      '@qwen-code/qwen-code-core': path.resolve(__dirname, '../core/index.ts'),
      '@qwen-code/acp-bridge': path.resolve(__dirname, '../acp-bridge/src/index.ts'),
      '@qwen-code/acp-bridge/eventBus': path.resolve(__dirname, '../acp-bridge/src/eventBus.ts'),
      '@qwen-code/acp-bridge/inMemoryChannel': path.resolve(__dirname, '../acp-bridge/src/inMemoryChannel.ts'),
      '@qwen-code/acp-bridge/channel': path.resolve(__dirname, '../acp-bridge/src/channel.ts'),
      '@qwen-code/acp-bridge/permission': path.resolve(__dirname, '../acp-bridge/src/permission.ts'),
      '@qwen-code/acp-bridge/status': path.resolve(__dirname, '../acp-bridge/src/status.ts'),
      '@qwen-code/acp-bridge/workspacePaths': path.resolve(__dirname, '../acp-bridge/src/workspacePaths.ts'),
      '@qwen-code/acp-bridge/bridgeErrors': path.resolve(__dirname, '../acp-bridge/src/bridgeErrors.ts'),
      '@qwen-code/acp-bridge/bridgeTypes': path.resolve(__dirname, '../acp-bridge/src/bridgeTypes.ts'),
      '@qwen-code/acp-bridge/bridgeOptions': path.resolve(__dirname, '../acp-bridge/src/bridgeOptions.ts'),
    },
  },
  test: {
    include: ['**/*.{test,spec}.?(c|m)[jt]s?(x)', 'config.test.ts'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/cypress/**'],
    environment: 'jsdom',
    globals: true,
    reporters: ['default', 'junit'],
    silent: true,
    outputFile: {
      junit: 'junit.xml',
    },
    setupFiles: ['./test-setup.ts'],
    coverage: {
      enabled: true,
      provider: 'v8',
      reportsDirectory: './coverage',
      include: ['src/**/*.{ts,tsx,js,jsx,mts,cts,mjs,cjs}'],
      reporter: [
        ['text', { file: 'full-text-summary.txt' }],
        'html',
        'json',
        'lcov',
        'cobertura',
        ['json-summary', { outputFile: 'coverage-summary.json' }],
      ],
    },
    server: {
      deps: {
        inline: [/@qwen-code\/qwen-code-core/, /@qwen-code\/acp-bridge/],
      },
    },
  },
});
