# agent-workflow

Rules for coding agents, shared by Claude Code and OpenCode: always loaded rules, skills loaded on demand, harness settings, and an install script. Process skills (brainstorming, planning, TDD, debugging, review, verification) come from [superpowers](https://github.com/obra/superpowers).

## Contents

```
agent-workflow/
├── core/AGENTS.md            always loaded: language, git, working rules, index of rules and skills
├── rules/                    always loaded
│   ├── general-secrets.md    credentials, .env gate
│   ├── general-sensitive-data.md real infrastructure names in chat, notes, commits
│   ├── code-design.md        design rules, English-only code text, no comments, docstrings
│   ├── code-negotiation.md   what is approved before implementing: tree, signatures, call site, payload
│   ├── code-docs.md          root README, docs/ layout
│   ├── code-report.md        report in the chat after implementing code
│   ├── general-wsl.md        WSL repos from a Windows host
│   └── general-writing.md    style of docs, notes and articles
├── skills/                   loaded on demand (SKILL.md format)
│   ├── autonomous-run/       unattended run from an approved plan
│   ├── describing-pipelines/ pipeline notes: flow diagram, payload notation
│   ├── obsidian-canvas/      .canvas layout rules and canvas-check.py
│   ├── mutation-testing/     tests from the spec by an isolated subagent, mutation run, survivor triage
│   ├── refactor/             refactor to the code rules: scope, inventory, approval, batches
│   ├── second-brain/         structure and rules of the knowledge base
│   └── beads/                task tracking in repos with .beads/
├── commands/                 slash commands, installed for both harnesses
│   ├── mutations-tests.md    /mutations-tests: skill mutation-testing
│   ├── refactor-all.md       /refactor-all: skill refactor on the whole repo
│   └── refactor-latest.md    /refactor-latest: skill refactor on the session's changes
├── harness/
│   ├── claude/               settings.json, subagents (leak-auditor, code-design-reviewer), compact hook
│   └── opencode/             opencode.json: permissions, superpowers plugin
├── second-brain-obsidian/    Obsidian CSS snippet (hides templates/)
├── second-brain-templates/   note templates for the knowledge base
├── install.py                installs the rules into ~/.claude and ~/.config/opencode
└── RESTORE.md                rebuild the setup on a clean machine
```

## How the harnesses load the rules

| Harness | Core | Rules | Skills | Commands |
|---|---|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/rules/*.md` | `~/.claude/skills/` | `~/.claude/commands/` |
| OpenCode | `~/.config/opencode/AGENTS.md` | `~/.claude/rules/*.md` (`instructions` in `opencode.json`) | `~/.claude/skills/` | `~/.config/opencode/commands/` |

`install.py` copies everything; nothing is linked.

## Usage

Rules and `core/AGENTS.md` are loaded in every session; nothing is run for them. Skills are loaded on demand: the agent sees each skill's `description` and loads the skill when the task matches it. Commands start a skill explicitly.

Commands start with `/`; skills without a command are referenced with `@` in the prompt. Text after either is optional and is passed to the agent as additional instructions.

```
# Refactor the whole repo to the code rules
/refactor-all

# Refactor the changes of the current session
/refactor-latest

# Tests from the spec by an isolated subagent, then mutation testing
/mutations-tests

# Unattended run of an approved plan
@autonomous-run

# Notes, decisions and session log in the knowledge base
@second-brain

# Document a pipeline or data flow
@describing-pipelines

# Obsidian .canvas diagram
@obsidian-canvas

# Task tracking in a repo with .beads/
@beads
```

## Change the rules

Edit this repo, run `py install.py`, review `git diff`, commit.

## Excluded

- Knowledge-base content: personal, local only.
- Conversation history, plugin caches, account data.
- Any secret, token, host name or personal identifier. `settings.json` uses the `{{HOME}}` placeholder, expanded by `install.py`.
