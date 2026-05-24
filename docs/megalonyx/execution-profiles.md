# Execution Profiles

An execution profile is a configuration file that tells the control-plane-daemon how to handle
a specific type of task. Profiles live in `.qwen/agents/` as Markdown files with YAML frontmatter.

---

## What a profile contains

Each profile specifies:
- **Which model to use** — a model ID from `settings.json`
- **Which skills to activate** — skill names from `.qwen/skills/`
- **System prompt emphasis** — what the model should prioritize for this task type
- **When to apply it** — file patterns and task keywords that trigger this profile

Example profile header:
```yaml
---
name: software-developer
model: gemini-3.1-pro-preview
skills:
  - developer
  - commit
  - lsp
triggers:
  file_patterns: ["*.py", "*.ts", "*.js"]
  task_keywords: ["implement", "fix", "refactor", "add"]
---
# Software Developer

You are working on a software implementation task...
```

The YAML frontmatter is parsed by `ExecutionProfileSelector`. The Markdown body becomes
the system prompt when this profile is active.

---

## Available profiles

The 20 profiles in `.qwen/agents/` cover the main task types:

| Profile | When it applies |
|---|---|
| `software-architect.md` | System design, architecture decisions, structural planning |
| `software-developer.md` | Code implementation, bug fixes, feature additions |
| `code-reviewer.md` | Code review, security audit, quality assessment |
| `test-engineer.md` | Writing and improving tests |
| `documentation-writer.md` | Writing or updating documentation |
| `researcher.md` | Gathering information, summarizing, synthesizing |
| `memory-manager.md` | Operations involving the memory service |
| `devops-engineer.md` | Infrastructure, CI/CD, deployment |
| `data-analyst.md` | Data processing, analysis, visualization |
| `security-analyst.md` | Security review, vulnerability assessment |
| And 10 more... | Run `ls .qwen/agents/` for the full list |

---

## How selection works

`ExecutionProfileSelector.select(job)` scores each profile against the job:

1. File patterns are matched against the files the job is expected to touch
2. Task keywords are matched against the job's instruction text
3. The profile with the highest combined score is selected
4. If no profile scores above a threshold, the default profile is used

File: `apps/control-plane-daemon/src/control_plane_daemon/execution_profile_selector.py`

---

## Adding a new profile

1. Create `.qwen/agents/<name>.md` with YAML frontmatter (model, skills, triggers) and a Markdown system prompt body
2. Ensure any skills listed in the profile exist in `.qwen/skills/`
3. The profile is picked up automatically on next daemon start — no code change required

Follow the naming standard: use plain engineering terms. `database-migration.md` is good;
`schema-evolution-wizard.md` is not.

---

## Profiles vs. skills

These are related but different:

| | Execution profile | Skill |
|---|---|---|
| Lives in | `.qwen/agents/` | `.qwen/skills/` |
| What it is | Model + tool configuration for a task type | Reusable instruction set |
| Who reads it | `ExecutionProfileSelector` (Python) | Qwen Code CLI (Node.js) |
| Scope | Determines how a job runs | Tells the model how to do a specific action |

A profile lists which skills to activate. Skills do the detailed work once the model is running.
