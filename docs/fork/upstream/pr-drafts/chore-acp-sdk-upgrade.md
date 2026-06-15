# PR Draft: chore/acp-sdk-upgrade → upstream/main

**Branch:** `chore/acp-sdk-upgrade`
**Issue:** #12
**Status:** Needs Verification

---

## Title

`chore(deps): upgrade @agentclientprotocol/sdk 0.14 → 0.22 to unlock session lifecycle methods`

## Description

Updates the Agent Client Protocol SDK to version 0.22. This upgrade is required to unlock critical session lifecycle methods (`resumeSession`, `closeSession`, `unstable_forkSession`) as requested in #4227, and supports the ACP Streamable HTTP transport upgrade plan in #4782.

## Testing

- [ ] SDK integration tests pass
- [ ] API compatibility verified
