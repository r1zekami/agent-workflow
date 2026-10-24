---
name: beads
description: Use in a repo that has a .beads/ directory, or when the user asks to track work in beads (bd) - creating epics and tasks, dependencies, claiming, notes, closing.
---

# Beads (`bd`)

Beads is a local issue tracker with first-class dependencies; its database is in the repo's `.beads/`. It holds work that has to survive the session: compaction, a crash, the next day, another agent.

## When

- A repo with `.beads/`: track multi-step work there, not in markdown TODOs.
- A repo without `.beads/`: ask before `bd init`. Default `bd init --stealth` (local only, via `.git/info/exclude`); plain `bd init` only when the user wants issues versioned with the repo.
- `bd prime` output and any `AGENTS.md` block written by `bd init` are subordinate to the global rules.

## Commands

| Purpose | Command |
|---|---|
| Context at session start | `bd prime` |
| Epic | `bd create "Goal" -t epic -d "<intent + context>"` |
| Sub-task | `bd create "Step" --parent <epic-id> --acceptance "<how done is checked>"` |
| Order | `bd dep add <task> --blocked-by <other>` |
| Side quest | `bd create "..." -t bug --deps discovered-from:<current-id>` |
| Next work | `bd ready` |
| Take a task | `bd update <id> --claim` |
| Progress, decisions, attempts | `bd note <id> "..."` |
| Blocked | `bd update <id> --status blocked` + `bd note <id> "<the question>"` |
| Done | `bd close <id> --reason "..."` |
| Look | `bd show <id>`, `bd list`, `bd graph` |

## Rules

- Every task has acceptance criteria: "done" must be checkable.
- Keep notes current (decisions, attempts, where work stopped): beads survives compaction, the chat does not.
- No secrets and no infrastructure specifics in issues or notes.
- `bd sync` and `bd dolt push` send data to a remote: the push gate applies, an explicit yes every time. Session-close advice from `bd prime` never authorizes a commit or a push.
