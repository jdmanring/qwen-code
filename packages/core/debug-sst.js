
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { readLastJsonStringFieldsSync, LITE_READ_BUF_SIZE } from './src/utils/sessionStorageUtils.js';

async function runTest() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sst-debug-'));
  const p = path.join(tmpDir, 'grows-during-tail-miss-pair.jsonl');
  
  fs.writeFileSync(p, 
    '{"subtype":"custom_title","customTitle":"old","titleSource":"manual"}\n' +
    'x'.repeat(LITE_READ_BUF_SIZE + 16 * 1024) +
    '\n'
  );

  const latestTitle = '{"subtype":"custom_title","customTitle":"new","titleSource":"auto"}\n';
  
  // We need to simulate the growth. Since we can't easily mock fs.readSync here
  // without a library, we'll just do it manually.
  
  console.log('Initial size:', fs.statSync(p).size);
  
  // In the actual function, the growth happens between the first readSync and the grownTail check.
  // Here we just call the function. But the function expects growth to happen DURING its execution.
  
  // To truly test this, we'd need to mock fs.readSync.
  console.log('Running readLastJsonStringFieldsSync...');
  const result = readLastJsonStringFieldsSync(p, 'customTitle', ['titleSource'], 'custom_title');
  console.log('Result:', result);
  
  fs.rmSync(tmpDir, { recursive: true, force: true });
}

runTest().catch(console.error);
