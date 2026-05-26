/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { defineConfig } from 'vitest/config';
import path from 'node:path';

export default defineConfig({
  resolve: {
    alias: {
      '@qwen-code/qwen-code-core': path.resolve(__dirname, './index.ts'),
    },
  },
  test: {
    reporters: ['default', 'junit'],
    silent: true,
    clearMocks: true,
    setupFiles: ['./test-setup.ts'],
    outputFile: {
      junit: 'junit.xml',
    },
    coverage: {
      enabled: true,
      provider: 'v8',
      reportsDirectory: './coverage',
      reportOnFailure: true,
      include: ['src/**/*.{ts,tsx,js,jsx,mts,cts,mjs,cjs}'],
      reporter: [
        ['text', { file: 'full-text-summary.txt' }],
        'html',
        'json',
        'lcov',
        'cobertura',
        ['json-summary', { outputFile: 'coverage-summary.json' }],
      ],
      thresholds: {
        statements: 75,
        branches: 78,
        functions: 77,
        lines: 75,
      },
    },
    deps: {
      optimizer: {
        ssr: {
          include: [/@qwen-code\/qwen-code-core/],
        },
      },
    },
  },
});
