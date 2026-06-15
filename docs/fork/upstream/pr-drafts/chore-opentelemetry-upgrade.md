# PR Draft: chore/opentelemetry-upgrade → upstream/main

**Branch:** `chore/opentelemetry-upgrade`
**Issue:** #4
**Status:** Needs Verification

---

## Title

`chore(deps): upgrade OpenTelemetry 0.203 → 0.218 to enable hardening and OpenInference`

## Description

Updates OpenTelemetry dependencies to version 0.218. This upgrade is a critical prerequisite for the hardening of OpenTelemetry configuration, HTTP OTLP behavior, and runtime safety requested in #3731, as well as the implementation of OpenInference-compliant trace tracking for Phoenix visualization requested in #3917.

## Testing

- [ ] Telemetry spans verified
- [ ] No performance regressions
