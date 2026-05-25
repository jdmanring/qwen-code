# Security Policy

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

To report a security vulnerability, email: **james_manring@yahoo.com**

Include in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fix (optional)

You will receive acknowledgment within 48 hours and a status update within 7 days.

## Scope

This repository contains:
- The Megalonyx sovereign AI stack (private, not publicly distributed)
- Customizations of the QwenLM/qwen-code CLI tool

Security reports are relevant for:
- Credential exposure or secret leakage in code or CI
- Dependency vulnerabilities with a known exploit path
- Authentication or authorization bypasses in the control plane

## Out of Scope

- Vulnerabilities in QwenLM/qwen-code upstream — report those directly at https://github.com/QwenLM/qwen-code/security
- Speculative or theoretical vulnerabilities without a concrete attack path

## Credential Files

The following files must never be committed:
- `config/settings.json` — API keys and model credentials
- `config/megalonyx/secrets.json` — internal secrets
- Any `*.env.local` or `*.env.production` file

These are listed in `.gitignore`. If you discover a credential exposure in git history, contact the email above immediately.
