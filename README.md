# claude-code-setup

A complete, restorable setup for working with Claude Code (desktop app, Code
tab) on Windows + WSL: global agent instructions, subagents, settings, a
knowledge-base skeleton, and a step-by-step guide to rebuild everything on a
clean machine.

## What's inside

```
claude-code-setup/
├── README.md                 ← this file
├── RESTORE.md                ← rebuild the whole environment on a clean PC
├── CLAUDE.md                 ← how Claude works on this repo itself
├── sync-claude-config.ps1    ← mirror the config between ~/.claude and claude-home/
├── claude-home/              ← mirror of ~/.claude (whitelisted files only)
│   ├── CLAUDE.md             ← global instructions entry point (@imports)
│   ├── settings.json         ← user settings; {{HOME}} = your home folder
│   ├── instructions/         ← the rules, one topic per file
│   └── agents/               ← subagents: code-design-reviewer, leak-auditor, architecture-designer, Explore
├── services/
│   └── litellm/              ← local LLM gateway for worker agents (Docker in WSL)
└── second-brain-templates/   ← note templates for the knowledge base
```

| Instruction file | What it governs |
|---|---|
| `workflow.md` | The four approaches — Easy, Medium, Hard, Autonomous — and their steps |
| `language.md` | English for code, docs, specs, commits and instructions |
| `environment.md` | Windows host for routine, WSL for all development |
| `context7.md` | When and how to fetch current library docs |
| `beads.md` | Task tracking for Hard and Autonomous |
| `openspec.md` | Behavior specs in code repos; behavior changes only via Hard |
| `second-brain.md` | Structure and rules of the local knowledge base |
| `secrets.md`, `sensitive-data.md` | Hard rules for credentials and infrastructure details |
| `code-style.md`, `code-design.md` | How code is written and designed |
| `git.md` | Commit format, push gate |

## Restore on a new machine

Follow [RESTORE.md](RESTORE.md) — by hand, or open Claude desktop in this
folder and say: *"follow RESTORE.md"*.

## Back up changes

`~/.claude` is the live config; this repo is its versioned snapshot. After
changing anything there:

```powershell
pwsh -NoProfile -File .\sync-claude-config.ps1 -Direction ToRepo
git diff
```

Then commit and push.

## What is deliberately NOT here

- Knowledge-base content (notes, areas, session log) — personal, local only.
- Claude conversation history, plugin caches, account data.
- Any secret, token, host name or personal identifier — `settings.json` uses the
  `{{HOME}}` placeholder, expanded by the sync script on restore.
