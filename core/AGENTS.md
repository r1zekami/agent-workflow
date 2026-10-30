# Global agent rules

Loaded in every session of every harness (Claude Code, OpenCode), together with the rule files listed under Rules. Guides needed only for some work are skills, loaded on demand.

## Language

- Chat: the user's language.
- Everything persistent is English: code, comments, docs, specs, commit messages, issues, notes, instruction files, second-brain.
- Log and console output: English, ASCII only (non-ASCII breaks Windows consoles).
- Translation only on request, as a copy of the English original.

## Secrets and sensitive data: hard rules

Rules `general-secrets` and `general-sensitive-data` apply in every session without exception: never read or touch `.env`, never surface a secret, never show real infrastructure names.

## Git

- Never push without an explicit yes for that push. Before a push, read everything it sends (`git log -p <remote>/<branch>..HEAD`) for secrets and infrastructure details (Claude Code: the `leak-auditor` subagent; elsewhere: by hand); findings block the push.
- Commit only when asked. Title `type(scope): short description`, short factual body, the session's attribution trailer.
- Never commit agent artifacts (scratch files, logs, backups).

## Working

- Environment: work in the environment the session runs in. Install nothing without asking; commands that need `sudo` are run by the user.
- Ask only about decisions that are the user's (scope, interfaces, design, anything destructive); assume the rest and list assumptions in the report.
- Multi-step work keeps its plan and progress in a file (a plan file or beads), not only in the chat, so a compaction loses nothing.
- No claim of done, fixed or passing without a check run in this session. Nothing could be checked: say "not verified".
- Library and API facts come from current sources (official docs, release notes), not from memory.
- Before running, building, testing or deploying a project, read the documents that the repo's `AGENTS.md` table names for that task; without a table, read `README.md` and `docs/README.md`. Follow the documented way. Documentation that contradicts the code is reported, never silently bypassed.
- Destructive operations (deleting data, force operations, history rewrites) need an explicit yes.

## second-brain

A repo is tracked in second-brain when its `AGENTS.md` has a `second-brain:` line or its path is the `repo:` of an entity (`<scope>/projects|services|pipelines/<slug>/README.md`). Load skill `second-brain` before writing.

- A decision goes into the entity's `decisions.md` when it is made, not at the end of the session. A decision is a choice between alternatives that a later session needs: architecture, interface, tool, data format, an approach rejected and why. Routine edits and bug fixes are not decisions.
- The entity's `README.md` is rewritten when the project's state changes: a feature lands, a component appears or goes, the way to run or deploy the project changes.
- A milestone (a merged PR, a finished slice, a release) adds a file to the entity's `log/`.
- Every note about a project carries the tag `project/<slug>`. Creating a new project folder comes with a proposal of that tag to the user.
- A task that changed something or produced an artifact ends with a session-log entry; its `target` links the entity note when one exists.

## Rules

Always loaded next to this file (`~/.claude/rules/`):

| Rule | Covers |
|---|---|
| `general-secrets` | Credentials: how they reach programs, `.env` gate, prohibitions, local-sandbox exception |
| `general-sensitive-data` | Real infrastructure names: statistics, masking at extraction, pointwise values on request |
| `code-design` | Writing and designing code: simplicity, structure, names, English-only code text, no comments, docstrings |
| `code-negotiation` | What is approved before implementing: file tree, signatures, call site, payload |
| `code-docs` | Root README, `docs/` layout, docs and OpenSpec |
| `code-report` | Report in the chat after implementing code |
| `general-wsl` | WSL repos from a Windows host: commands inside WSL, Git Bash path rewriting, edits on the share |
| `general-writing` | READMEs, docs, regulations, articles, notes |

## Skills

Load the matching skill before the work, not after:

| Work | Skill |
|---|---|
| Unattended run from an approved plan | `autonomous-run` |
| Describing a pipeline or data flow | `describing-pipelines` |
| Obsidian `.canvas` files | `obsidian-canvas` |
| Anything in second-brain | `second-brain` |
| Repo with `.beads/` | `beads` |

Process skills (brainstorming, planning, TDD, debugging, review, verification) come from superpowers. A repo with `openspec/` follows native OpenSpec (`/opsx:*`) and its own `openspec/config.yaml`.

## Paths

- second-brain: `~/home/agents/second-brain` (local git, never a remote).
- These rules: `~/home/agents/agent-workflow`.
- A repo in WSL opened from a Windows host: rule `general-wsl`.
