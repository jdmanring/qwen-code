import path from 'node:path';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  resolve: {
    alias: {
      '@qwen-code/qwen-code/export': path.resolve(
        __dirname,
        '../cli/src/export/index.ts',
      ),
      '@qwen-code/qwen-code-core': path.resolve(__dirname, '../core/index.ts'),
      '@qwen-code/webui': path.resolve(__dirname, '../webui/src/index.ts'),
    },
  },
  test: {
    globals: true,
    clearMocks: true,
    environment: 'node',
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
    deps: {
      optimizer: {
        ssr: {
          include: [/@qwen-code\//],
        },
      },
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'clover'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts', 'src/**/*.d.ts'],
    },
  },
});
