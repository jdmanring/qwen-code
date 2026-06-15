
import { describe, it } from 'vitest';
import { extractCommandRules } from './shellAstParser.js';

describe('extractCommandRules Debug', () => {
  it('tests specific failing cases', async () => {
    console.log('Testing "cd packages/core && npm run build"');
    console.log(await extractCommandRules('cd packages/core && npm run build'));

    console.log('Testing "npm run build 2>&1 | head -100"');
    console.log(await extractCommandRules('npm run build 2>&1 | head -100'));

    console.log('Testing "git add /tmp/file && git commit -m "msg"');
    console.log(await extractCommandRules('git add /tmp/file && git commit -m "msg"'));
  });
});
