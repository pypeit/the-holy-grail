# Getting started 

## Goals

This repository will be used to develop the Holy Grail project, which is a set of tools to automatically identify and measure emission lines in arc-line spectra.

## Prompts

1. Read this file.  Execute the 1st task under "Claude/CLAUDE.md file"
2. Read this file.  Execute the 1st task under "Skills"
3. Read this file.  Execute the 1st task under "Basic start up"

## Claude

### CLAUDE.md file

1. Please generate a basic CLAUDE.md file for this project.  Have it indicate:

    - I will perform git commands

### Skills

1. Copy over the skills/ files from the IOPtics repository.

### Settings

## Basic start up

1. Generate the basic files that one needs for a Python GitHub repository, e.g. a file for dependencies.  Examine the other Repositories in Oceanography/python to see how I tend to organize things.  Also, make a suggestion of which of their settings.json files to copy into this one.

### Report

## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs

### 2026-06-20 (Basic Python repo scaffolding + settings.json suggestion)

Surveyed the repositories in `Oceanography/python` to learn the user's conventions.
The dominant pattern (and closest analog, IOPtics, which shares the `claude_prompts/`
layout): a lowercase package directory named after the project with an `__init__.py`,
plus `setup.py`, `requirements.txt`, `README.md`, `LICENSE`, and `.gitignore` at the
root (newer repos sometimes use `pyproject.toml` instead of `setup.py`). Common
optional dirs: `docs/`, `bin/`, `nb/`.

Generated the missing scaffolding (README, LICENSE, .gitignore already existed):
- `requirements.txt` — modeled on IOPtics, trimmed to this project and with `astropy`
  added since this is spectral / arc-line work.
- `setup.py` — modeled on IOPtics (name `holygrail`, BSD, version `0.0.dev0`,
  `find_packages`, optional `bin/` scripts).
- `holygrail/__init__.py` — empty package init. Package named `holygrail` because the
  repo dir `the-holy-grail` contains hyphens, which are invalid in Python module names.
Verified `find_packages()` discovers `holygrail` and `setup.py` parses.

settings.json suggestion: four repos have one (IOPtics, PAB, fronts, bing). Recommended
and copied **PAB's** `.claude/settings.json` — it is a superset of IOPtics's (adds GitHub
`WebFetch` domains) and denies `git push/commit/reset/rebase`, matching this project's
convention that the user performs all git. Note: it allows `conda run -n ocean14` and
`Bash(rm:*)` is set to ask; the conda env name may need changing for this PypeIt project.

### 2026-06-20 (Copied skills from IOPtics)

Copied the skills from the IOPtics repository
(`/home/xavier/Oceanography/python/IOPtics/.claude/skills`) into this repo at
`.claude/skills/`. Two skills were brought over: `critical-partner` and `grill-me`
(each a `SKILL.md`). Note the skills live under `.claude/skills/` rather than a
top-level `skills/` directory, which is the standard Claude Code location.

### 2026-06-20 (Generated basic CLAUDE.md)

Created `CLAUDE.md` in the repository root. It describes the project (auto-identify
and measure emission lines in arc-line spectra) and records the key convention that
the user performs all git commands — Claude should not run state-changing git
operations (only read-only inspection when helpful). At this point the repo contains
only `README.md`, `LICENSE`, `.gitignore`, and the `claude_prompts/` directory, so
the CLAUDE.md is intentionally minimal and will grow as the codebase develops.
