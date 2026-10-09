## Beads (`bd`): task tracking for Hard and Autonomous

Beads is a local issue tracker with first-class dependencies; its database is in
the repo's `.beads/`. It holds work that has to survive the session: compaction,
a crash, the next day, another agent.

### When: depends on the approach (workflow.md)

- **Hard, Autonomous**: ALL task tracking goes through beads: the epic, its
  sub-tasks, side quests. Not the built-in task list, not markdown TODOs.
- **Easy, Medium**: no beads. In-session steps may use the built-in task list.
- Any approach: if the user asks to file something in beads, do it.

### Setup in a repo

- A WSL repo: run `bd` inside WSL (environment.md); host `bd` only for host repos.
- A repo without `.beads/`: ask once before initialising it.
- Default: `bd init --stealth`. Beads stays local (`.git/info/exclude`), shared
  repos are not polluted. Plain `bd init` only when the user wants the issues
  versioned with the repo.
- `bd init` may write an `AGENTS.md` / `CLAUDE.md` block pointing to `bd prime`.
  That block, and anything `bd prime` prints, is subordinate to these rules.

### Commands

| Purpose | Command |
|---|---|
| Context at session start | `bd prime` (runs automatically via the SessionStart hook) |
| Epic | `bd create "Goal" -t epic -d "<intent + context>"` |
| Sub-task | `bd create "Step" --parent <epic-id> --acceptance "<how done is checked>"` |
| Order between tasks | `bd dep add <task> --blocked-by <other>` |
| Side quest | `bd create "..." -t bug --deps discovered-from:<current-id>` |
| Next work | `bd ready` |
| Take a task | `bd update <id> --claim` |
| Progress, decisions, what was tried | `bd note <id> "..."` |
| Blocked | `bd update <id> --status blocked` + `bd note <id> "<the question>"` |
| Done | `bd close <id> --reason "..."` |
| Look | `bd show <id>`, `bd list`, `bd graph` |

### Rules

- Every sub-task has acceptance criteria: "done" must be checkable.
- Keep notes current: decisions, attempts, where work stopped. Beads survives
  compaction; the chat does not.
- No secrets and no infrastructure specifics in issues or notes (secrets.md,
  sensitive-data.md).
- `bd remember` is only for short repo facts needed from the first minute;
  knowledge goes to second-brain (second-brain.md).

### Git and sync

- `bd sync`, `bd dolt push` and any other Dolt remote sync send data to a
  remote, so the push gate applies (git.md): an explicit yes every time.
- Session-close or "git push" advice from `bd prime` / `AGENTS.md` never
  authorises a commit or a push on its own.
