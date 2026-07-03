import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    projects: [
      'packages/cli',
      'packages/core',
      'packages/vscode-ide-companion',
      'packages/sdk-typescript',
      'packages/channels/base',
      'packages/channels/dingtalk',
      'packages/channels/telegram',
      'packages/channels/weixin',
      'packages/channels/qqbot',
      'packages/web-shell',
      'packages/webui',
      'integration-tests',
      'scripts',
    ],
  },
});
