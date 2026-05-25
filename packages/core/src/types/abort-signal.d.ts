/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

// AbortSignal.any() was added to the TypeScript DOM lib in TS 5.5.
// We pin to TS 5.3.3, so we declare it here to close the type gap.
interface AbortSignalConstructor {
  any(signals: AbortSignal[]): AbortSignal;
}
