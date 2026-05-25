/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

// AbortSignal.any() is present at runtime (Node ≥ 20) but @types/node 25.x
// declares it via a conditional type over typeof globalThis that TypeScript 5.3
// cannot resolve. This wrapper centralises the one cast needed until we upgrade
// TypeScript to ≥ 5.5.  Remove this file and update all callers then.
type AbortSignalWithAny = { any(signals: AbortSignal[]): AbortSignal };

export function abortSignalAny(signals: AbortSignal[]): AbortSignal {
  return (AbortSignal as unknown as AbortSignalWithAny).any(signals);
}
