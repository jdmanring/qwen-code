# README Style Guide

This guide defines the structure, tone, and formatting requirements for Megalonyx README files.
It applies to the public-facing README (the one end users read) and any package-level READMEs
in the monorepo.

There are two distinct README audiences with different needs. They get different documents.

---

## Two types of README

### User-facing README (public release repo)

The README that lives in the public repository root. This is what someone sees when they find
Megalonyx on GitHub or follow a link. It answers four questions in this order:

1. What is this?
2. What does it do for me?
3. How do I install it?
4. Where do I find out more?

It does not describe the development pipeline, branch strategy, upstream sync, or internal
tooling. Those are not the user's concern.

Template: `docs/templates/readme-public-draft.md`

### Developer README (monorepo)

The README in this monorepo (`README.md` on `develop`/`integration`). Aimed at maintainers
and contributors. Describes the internal architecture, branch strategy, quality checks, and
where things live.

The developer README follows the same structural and tone rules below, but the audience
and content are different.

---

## Structure (user-facing README)

Sections in order. Do not reorder. Remove a section only if it genuinely doesn't apply —
don't leave it empty.

```
1. Header block (centered)
   - Logo image
   - Project name (H1)
   - Badge row
   - Tagline (bold, one sentence)
   - Demo GIF or screenshot

2. Short description (1–2 sentences, not centered)

3. What it does
   - 4–6 bullet points, each starting with a bold label
   - One concrete claim per bullet — no vague superlatives

4. Requirements
   - Numbered or bulleted list
   - Each item: what it is + link to install it

5. Install
   - One-command quick install (curl | bash or equivalent)
   - Optional: manual install for users who want to inspect first

6. Quick start
   - 3–5 shell commands showing the most common usage
   - Brief comment on each

7. Configuration
   - Where config lives
   - The 1–2 things users actually need to change
   - Link to full reference docs

8. Model providers
   - Table: provider | what it's good for
   - Link to setup guide

9. Memory (if the product has memory)
   - Where data is stored
   - How to clear it

10. Privacy
    - What leaves the machine and where it goes
    - What Megalonyx itself does with data

11. Contributing
    - Issue link
    - Discussions link
    - Link to CONTRIBUTING.md
    - Security reporting note

12. License
    - SPDX license name, linked to LICENSE file
```

---

## Header block requirements

The header block is centered using `<div align="center">`. It contains, in order:

1. **Logo** — SVG or PNG, max 200px wide. `alt` text = project name.
2. **H1 heading** — project name only, no tagline
3. **Badge row** — all badges on one line, no line breaks between them
4. **Tagline** — bold, one sentence, in `**...**`. No period at the end.
5. **Demo GIF** — `alt` = "Megalonyx demo", width = 700px

Badges to include (in this order):
- CI status (GitHub Actions)
- Latest release version (GitHub releases)
- License
- Platform support

Badge format: use `img.shields.io`. All badges should link somewhere useful (CI run, releases
page, license file, etc.).

When assets don't exist yet (logo, demo GIF): add a commented-out placeholder line with a
description of what goes there. Do not use a broken image link.

---

## Tone rules

**Say what it does, not what it is.** "Remembers what you tell it across sessions" is better
than "features persistent memory." The first describes behavior; the second describes a
category.

**No superlatives.** "Lightning fast", "incredibly powerful", "seamlessly integrated" — cut
these. Every product claims them. They carry no information.

**No AI hype vocabulary.** Banned words and phrases in user-facing READMEs:

| Banned | Why |
|---|---|
| Agentic | Jargon that means nothing to most users |
| Autonomous | Sounds like it's out of control |
| Cognitive / cognitive architecture | AI-speak |
| Orchestration layer | Infrastructure jargon |
| Sovereign | Sounds grandiose and unclear |
| Synergy, seamless, revolutionary | Marketing filler |
| "AI-native" | Meaningless descriptor |
| "at scale" | What scale? |
| Self-healing, self-correcting | Overpromises |

**Describe the failure behavior, not just the success.** "When something fails, it tells you
why" is more trustworthy than "handles errors gracefully." Users who have been burned by tools
that fail silently will notice and appreciate this.

**Be specific about privacy.** Don't say "we take your privacy seriously." Say exactly what
data goes where, and what happens to it. Vague privacy claims are worse than saying nothing
because they signal that you're hiding something.

**Don't qualify everything.** Avoid "may", "might", "in some cases", "depending on your setup"
unless the qualification is genuinely necessary. Pick the common case and describe it.

---

## What "AI-readable" means

An AI reading this README should be able to:
- Predict the contents of every file it references, from the description alone
- Understand the product's boundaries (what it does and what it explicitly does not do)
- Identify the command to install and start using it immediately
- Know what data leaves the machine and what stays local

Achieving this requires:
- Concrete nouns, not category labels ("stores memory in a local Qdrant database" not "provides a memory subsystem")
- Exact paths and commands, not approximate ones ("~/.config/megalonyx/providers.json" not "your config directory")
- Explicit scope ("works with OpenAI-compatible APIs" — a specific, testable claim)

---

## What "human-readable" means alongside that

AI-readable and human-readable are not in tension. Both benefit from:
- Short sentences
- Active voice
- Concrete examples
- Tables for comparisons
- Code blocks for anything you'd actually type

The place they can diverge: AI benefits from exhaustive enumeration (every provider listed,
every config key named). Humans benefit from progressive disclosure (lead with the common case,
link to the full reference). Resolve this by leading with the common case in the README and
linking to complete documentation for the full detail.

---

## Placeholders

When an asset or piece of information doesn't exist yet, add a commented-out placeholder:

```html
<!-- PLACEHOLDER: Replace with actual logo once finalized -->
<!-- <img src="docs/assets/megalonyx-logo.svg" alt="Megalonyx" width="200" /> -->
```

or in a DRAFT NOTES block at the bottom of the file, listing every placeholder with what
it needs. See `docs/templates/readme-public-draft.md` for an example of this pattern.

Do not publish a README with broken image links, placeholder URLs, or `TODO` text visible
to users. The DRAFT NOTES section is HTML-commented — it is invisible in rendered Markdown.

---

## When to update this guide

Update this guide when:
- A new section type is needed across multiple READMEs
- A tone rule is added or removed based on experience
- The badge set changes (e.g., adding a Docker badge)
- The public repo structure changes in a way that affects README conventions

This guide is enforced by review, not by an automated linter. Keep it short enough that
reviewers will actually read it.
