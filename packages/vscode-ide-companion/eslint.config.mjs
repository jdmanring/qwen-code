/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import typescriptEslint from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import eslintReact from '@eslint-react/eslint-plugin';
import importPlugin from 'eslint-plugin-import-x';

export default [
  {
    files: ['**/*.ts', '**/*.tsx'],
  },
  {
    files: ['**/*.js', '**/*.cjs', '**/*.mjs'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'commonjs',
      globals: {
        module: 'readonly',
        require: 'readonly',
        __dirname: 'readonly',
        __filename: 'readonly',
        process: 'readonly',
        console: 'readonly',
      },
    },
  },
  {
    plugins: {
      '@typescript-eslint': typescriptEslint,
      '@eslint-react': eslintReact,
      'import-x': importPlugin,
    },

    languageOptions: {
      parser: tsParser,
      ecmaVersion: 2022,
      sourceType: 'module',
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },

    rules: {
      '@typescript-eslint/naming-convention': [
        'warn',
        {
          selector: 'import',
          format: ['camelCase', 'PascalCase'],
        },
      ],
      '@eslint-react/rules-of-hooks': 'error',
      '@eslint-react/exhaustive-deps': 'error',
      // Restrict deep imports but allow known-safe exceptions used by the webview
      // - react-dom/client: required for React 18's createRoot API
      // - ./styles/**: local CSS modules loaded by the webview
      'import-x/no-internal-modules': [
        'error',
        {
          allow: [
            'react-dom/client',
            './styles/**',
            '@modelcontextprotocol/sdk/**',
            '@qwen-code/acp-bridge/**',
            '@qwen-code/channel-weixin/**',
            '@qwen-code/qwen-code/export',
            '@qwen-code/webui/tailwind.preset',
            'vitest/config',
          ],
        },
      ],

      curly: 'warn',
      eqeqeq: ['warn', 'always', { null: 'ignore' }],
      'no-throw-literal': 'warn',
      semi: 'warn',
    },
  },
];
