# Headless Stdout Bug Case Study Documentation

## Purpose
This file serves as a "worked example" for the `structured-debugging` skill. It documents a specific, non-obvious bug to illustrate key debugging principles.

## Logic & Structure
The case study is presented as a narrative:
- **The Bug**: A situation where a CLI command prints nothing in a zsh TTY but works perfectly when output is captured in a pipe.
- **The Cause**: A missing trailing newline in the output, which causes zsh's `PROMPT_SP` to erase the line before drawing the prompt.
- **The Lesson**: Highlights the importance of "reproduction contradiction"—the fact that the bug disappears in a pipe is the key piece of data that leads to the fix.
- **Mapping to SKILL.md**: The case is explicitly mapped to core debugging axioms:
    - *Reproduction contradiction is data*.
    - *Instrument the data flow, not just the code path*.
    - *Pipe $\neq$ TTY*.

## Usage
- **Onboarding**: Used to train new developers or AI agents on how to approach "invisible" bugs.
- **Reference**: Serves as a reminder to always check the environment (TTY vs Pipe) when debugging output issues.

## Original File
[config/skills/structured-debugging/examples/headless-bg-agent-empty-stdout.md](../../config/skills/structured-debugging/examples/headless-bg-agent-empty-stdout.md)
