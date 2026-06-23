# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**The Holy Grail** — a set of tools to auto-identify and measure emission lines
in arc-line spectra. "One solution to rule them all."

## Conventions

- **Git is handled by the user.** Do not run `git add`, `git commit`, `git push`,
  or any other state-changing git commands. The user will perform all git
  operations themselves. You may inspect history with read-only commands
  (e.g. `git status`, `git log`, `git diff`) when it helps with a task.
- This is a Python project. Follow standard Python conventions (PEP 8) and match
  the style of surrounding code.

## Workflow notes

- Prompts driving the initial setup live in [claude_prompts/](claude_prompts/).
- Work performed by Claude is logged under the "Logs" section of
  [claude_prompts/start_up.md](claude_prompts/start_up.md).
