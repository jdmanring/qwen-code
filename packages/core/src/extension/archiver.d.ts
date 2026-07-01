/**
 * @license
 * Copyright 2025 Qwen Team
 * SPDX-License-Identifier: Apache-2.0
 */

declare module 'archiver' {
  import { Readable } from 'node:stream';

  interface ArchiverOptions {
    zlib?: { level?: number };
    [key: string]: unknown;
  }

  interface EntryData {
    name: string;
    prefix?: string;
    stats?: { [key: string]: unknown };
    [key: string]: unknown;
  }

  class Archiver extends Readable {
    constructor(format: string, options?: ArchiverOptions);
    append(source: Readable | Buffer | string, data?: EntryData): this;
    directory(dirpath: string, destpath?: string | false, data?: EntryData | ((entry: EntryData) => EntryData)): this;
    file(filepath: string, data?: EntryData): this;
    glob(pattern: string, cwd?: string, data?: EntryData): this;
    symlink(filepath: string, target: string): this;
    finalize(): Promise<void>;
    on(event: string, listener: (...args: unknown[]) => void): this;
    pipe(destination: NodeJS.WritableStream): NodeJS.WritableStream;
  }

  export = Archiver;
}
