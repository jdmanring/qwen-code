<div align="center">

<!-- PLACEHOLDER: Replace with actual logo once finalized -->
<!-- <img src="docs/assets/megalonyx-logo.svg" alt="Megalonyx" width="200" /> -->

# Megalonyx

[![CI](https://img.shields.io/github/actions/workflow/status/megalonyx/megalonyx/ci.yml?branch=main&label=CI)](https://github.com/megalonyx/megalonyx/actions)
[![Version](https://img.shields.io/github/v/release/megalonyx/megalonyx)](https://github.com/megalonyx/megalonyx/releases)
[![License](https://img.shields.io/github/license/megalonyx/megalonyx)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-blue)](#install)

**An AI agent for your terminal and browser.**

<!-- PLACEHOLDER: Replace with actual demo GIF once captured -->
<!-- <img src="docs/assets/demo.gif" alt="Megalonyx demo" width="700" /> -->

</div>

---

Megalonyx remembers what you tell it, handles complex tasks by breaking them into steps, works
with the model providers you already have, and gets out of your way when you don't need it.

It is honest about what it can and can't do. When something fails, it tells you why. It doesn't
silently retry until it guesses its way to a plausible-looking result.

---

## What it does

**Persistent memory.** Megalonyx remembers what matters across sessions — project context,
decisions you've made, things you've told it. You don't repeat yourself. It doesn't start
from zero every time.

**Handles complex tasks.** Give it a goal, not a list of steps. It figures out what needs to
happen, in what order, and does it. If a step fails, it tells you exactly why and what to do
about it.

**Connects to your tools.** It can read and write files, search the web, interact with GitHub,
and query your codebase. Everything it does is explicit — it tells you what it's about to do
before it does anything that changes something.

**Works with your providers.** Bring your own API keys. Megalonyx works with OpenAI-compatible
APIs, Google Gemini, and local models running on your machine. You decide which model handles
which type of task.

**Terminal and browser.** A full-featured command-line interface today, with a web interface
in active development.

---

## Requirements

- Linux or macOS
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- Node.js 22 or later
- An API key for at least one [supported model provider](#model-providers)

---

## Install

```bash
bash -c "$(curl -fsSL https://megalonyx.io/install)"
```

<!-- PLACEHOLDER: Confirm installer URL once the release infrastructure is in place -->

This installs the Megalonyx CLI and background services, sets up local memory storage, and
walks you through configuring your first API key. The whole process takes about two minutes.

**Manual install** (if you prefer to inspect the script first):
```bash
git clone https://github.com/megalonyx/megalonyx.git
cd megalonyx
bash scripts/install.sh
```

---

## Quick start

```bash
# Open an interactive session
megalonyx

# Ask it something
megalonyx "what does this project do"

# Give it a task
megalonyx "add input validation to the signup form in src/auth/login.py"

# Check what's running
megalonyx status
```

The first time you run it, it will ask for your API key if you haven't configured one.
Everything else is automatic.

---

## Configuration

All configuration lives in `~/.config/megalonyx/`. The installer creates it with sensible
defaults. The two things you're most likely to change:

- **API keys**: `~/.config/megalonyx/providers.json` — add or change your model provider keys
- **Default model**: set in `providers.json` under `"defaultModel"`

Full configuration reference: [megalonyx.io/docs/configuration](https://megalonyx.io/docs/configuration)

<!-- PLACEHOLDER: Confirm config path matches the released installer -->

---

## Model providers

Megalonyx works with any provider that supports the OpenAI chat completions API format,
plus native support for Google Gemini.

| Provider | What it's good for |
|---|---|
| OpenAI (GPT-4o, o3) | General purpose, strong coding and reasoning |
| Google Gemini 2.5 Pro | Long context, fast throughput |
| Google Gemini 2.5 Flash | Fast, low cost — good for lightweight steps |
| Groq | Very fast inference for supported open models |
| OpenRouter | Access to many models through one API key |
| Local (Ollama, vLLM, LM Studio) | Private, runs on your hardware, no API cost |

You can configure multiple providers and set rules for which model handles which type of
task — for example, use a fast model for reading and summarizing, and a stronger model for
writing or changing code.

Setup guide: [megalonyx.io/docs/providers](https://megalonyx.io/docs/providers)

---

## Memory

Megalonyx stores memory in a local [Qdrant](https://qdrant.tech/) vector database. Qdrant is
installed automatically — you don't set it up separately. Your data stays on your machine by
default.

If you want memory available across multiple machines, you can configure a Qdrant Cloud
instance. See [megalonyx.io/docs/memory](https://megalonyx.io/docs/memory).

To clear all stored memory:
```bash
megalonyx memory clear
```

---

## Privacy

**What leaves your machine:** The text of your prompts and any file content you ask Megalonyx
to read is sent to whichever model provider you configure. Read your provider's privacy policy
to understand how they handle that data. If privacy is a concern, use a local provider (Ollama,
vLLM) — nothing leaves your machine.

**What Megalonyx does with your data:** Nothing beyond what's needed to run. Memory is stored
locally in Qdrant. No usage data, no telemetry.

---

## Contributing

Bug reports and pull requests are welcome.

- [Open an issue](https://github.com/megalonyx/megalonyx/issues) — bugs, feature requests, questions
- [Discussions](https://github.com/megalonyx/megalonyx/discussions) — ideas and open-ended questions
- [CONTRIBUTING.md](./CONTRIBUTING.md) — how to set up a development environment and submit changes

If you find a security issue, please report it privately via GitHub's security advisory feature
rather than opening a public issue.

---

## License

[Apache 2.0](./LICENSE)

<!-- PLACEHOLDER: Confirm license before publishing -->

---

<!--
DRAFT NOTES — remove this section before publishing
=====================================================
Placeholders that need real values before this README goes live:

1. Logo           — docs/assets/megalonyx-logo.svg (or .png)
2. Demo GIF       — docs/assets/demo.gif
3. Installer URL  — https://megalonyx.io/install (confirm domain and path)
4. CLI command    — "megalonyx" used throughout; confirm or change to "mega" or other
5. Config path    — ~/.config/megalonyx/ (confirm this matches the installer)
6. GitHub org/repo — megalonyx/megalonyx (confirm the public repo name)
7. Docs site      — megalonyx.io/docs/... (confirm the domain)
8. License        — Apache 2.0 assumed; confirm and update SPDX identifier if different
9. Badge URLs     — update once the public repo exists and CI is configured
10. CONTRIBUTING.md — needs to be written for the public repo
-->
