# agent-workflow

Rules for coding agents, shared by Claude Code and OpenCode: always loaded rules, skills loaded on demand, harness settings, and an install script. Process skills (brainstorming, planning, TDD, debugging, review, verification) come from [superpowers](https://github.com/obra/superpowers).

## Contents

```
agent-workflow/
├── core/AGENTS.md            always loaded: language, secrets, sensitive data, git, working rules
├── rules/                    always loaded
│   ├── code-design.md        design rules, English-only code text, no comments, docstrings
│   ├── code-negotiation.md   what is approved before implementing: tree, signatures, call site, payload
│   ├── code-docs.md          root README, docs/ layout
│   ├── code-report.md        report in the chat after implementing code
│   └── general-writing.md    style of docs, notes and articles
├── skills/                   loaded on demand (SKILL.md format)
│   ├── autonomous-run/       unattended run from an approved plan
│   ├── describing-pipelines/ pipeline notes: flow diagram, payload notation
│   ├── obsidian-canvas/      .canvas layout rules and canvas-check.py
│   ├── second-brain/         structure and rules of the knowledge base
│   └── beads/                task tracking in repos with .beads/
├── harness/
│   ├── claude/               settings.json, subagents (leak-auditor, code-design-reviewer), compact hook
│   └── opencode/             opencode.json: permissions, superpowers plugin
├── second-brain-obsidian/    Obsidian CSS snippet (hides templates/)
├── second-brain-templates/   note templates for the knowledge base
├── install.py                installs the rules into ~/.claude and ~/.config/opencode
└── RESTORE.md                rebuild the setup on a clean machine
```

## How the harnesses load the rules

| Harness | Core | Rules | Skills |
|---|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/rules/*.md` | `~/.claude/skills/` |
| OpenCode | `~/.config/opencode/AGENTS.md` | `~/.claude/rules/*.md` (`instructions` in `opencode.json`) | `~/.claude/skills/` |

`install.py` copies everything; nothing is linked.

## Change the rules

Edit this repo, run `py install.py`, review `git diff`, commit.

## Excluded

- Knowledge-base content: personal, local only.
- Conversation history, plugin caches, account data.
- Any secret, token, host name or personal identifier. `settings.json` uses the `{{HOME}}` placeholder, expanded by `install.py`.
