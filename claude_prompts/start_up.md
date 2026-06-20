# Getting started 

## Goals

This repository will be used to develop the Holy Grail project, which is a set of tools to auto-identify and measure emission lines in arc-line spectra.

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
