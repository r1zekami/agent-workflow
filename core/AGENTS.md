# Global agent rules

Loaded in every session of every harness (Claude Code, OpenCode), together with the rule files listed under Rules. Guides needed only for some work are skills, loaded on demand.

## Language

- Chat: the user's language.
- Everything persistent is English: code, comments, docs, specs, commit messages, issues, notes, instruction files, second-brain.
- Log and console output: English, ASCII only (non-ASCII breaks Windows consoles).
- Translation only on request, as a copy of the English original.

## Secrets: hard rule

- Never read, print, create or edit `.env` or any file holding credentials. `.env.example` (variable names only) is maintained instead.
- Code reads secrets by name at runtime (`os.environ["NAME"]`, `process.env.NAME`) and fails with an error naming the missing variable. To run with `.env`, let the program or the shell load it (`set -a; . ./.env; set +a; <command>`); never open it. A missing or empty variable: report its name and stop; do not investigate the file.
- Never ask the user to paste a secret into the chat; name the variable to set.
- Never read secrets out of configs, shell history or credential stores, not even "just to look".
- Never put a secret into a command line (`export KEY=...`, an `Authorization` header), file, log, issue, note or the chat. Never dump the environment (`env`, `printenv`, `Get-ChildItem env:`). Setting non-secret config explicitly (`*_BASE_URL`, `*_MODEL`) is fine.
- A secret that shows up in a tool result is not quoted or repeated; a leaked secret is reported to the user at once.
- Exempt: throwaway values of a purely local sandbox. Unsure: ask.

## Sensitive infrastructure data: hard rule

- Real host names, IPs, domains, user names and inventory structure never go into the chat, commits, specs, issues or notes.
- Prefer bare statistics; mask inside the extracting script; show a real value only when the user asks for that item.
- Test fixtures and examples use made-up names.

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
- Destructive operations (deleting data, force operations, history rewrites) need an explicit yes.
- A task that changed something or produced an artifact ends with a session-log entry in second-brain (skill `second-brain`).

## Rules

Always loaded next to this file (`~/.claude/rules/`):

| Rule | Covers |
|---|---|
| `code-design` | Writing and designing code, English-only code text, interface approval gate |
| `code-docs` | Final report after code work, docstrings, repo docs |
| `writing` | READMEs, docs, regulations, articles, notes |

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
- A repo on a `\\wsl.localhost\<distro>\...` path: git, builds and tests run inside WSL (`wsl.exe -d <distro> --cd <linux path> --exec bash -lc '<command>'`); Windows `git.exe` refuses such repos.
