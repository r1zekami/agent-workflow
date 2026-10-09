## Workers: delegating code to cheap models

A worker is Codex CLI in WSL, running a cheap model through the local LiteLLM
gateway (`claude-code-setup/services/litellm`, config in `workers/codex`). It
writes code. Claude stays the orchestrator: it scopes the task, reviews the diff
and is responsible for the result. A worker saves Claude's output tokens and
never replaces its judgment.

### When: delegation is the default

In Medium, Hard and Autonomous, a coding task **goes to a worker by default**
when every check holds (not in Easy, where briefing costs more than it saves):

1. **Decided**: the interface is approved (code-design rule 6) or nothing
   public changes; no design or scope decision is left open.
2. **Checkable**: acceptance criteria exist as tests the worker can run.
3. **Offline**: it builds and tests without network or a live service once
   dependencies are fetched.
4. **Clean**: no secrets, `.env`, credentials or real production data in the
   files it needs; the repo's code may leave the machine (ask when unsure).
5. **Worth it**: more than a few edits. Anything smaller is done directly,
   because briefing and reviewing cost more than writing it.

If any check fails, Claude does the task directly and gives the failed check as
the reason (Hard and Autonomous: `bd note`; Medium: the plan). Typical delegates:
implementing an approved interface, tests for given scenarios, a mechanical
change across files, a bug with a reproducing test. Never delegated: decisions,
reviews, git operations. WSL repos only.

Every final report says which tasks went to workers (alias, cost) and which
did not, with the failed check.

### Models

The aliases are `worker-<provider>-<model>`, defined in the gateway's
`services/litellm/config.yaml`; each also needs its entry in
`workers/codex/models.json`. Default: the cheapest alias (`worker-deepseek-flash`);
a stronger one for multi-file work or a retry after a failed run.

Adding a model: a `config.yaml` entry with prices (its key goes into `.env`, by
the user), a copied `models.json` entry with the new slug, restart the gateway.
Adding another worker CLI: its own `workers/<name>/` folder and a section here;
the gateway, key, budget and cost tracking stay shared.

### Run

1. **Brief**: write the task to `~/.codex-runs/<task>/task.md` (WSL) with the
   file tool (`\\wsl.localhost\…` path), not a shell heredoc, because code quotes
   break it. The brief contains: goal; files to touch; approved signatures
   (code-design rule 6) to implement exactly; acceptance criteria as tests; the
   commands that check it; out of scope. One task per brief.
2. **Isolate**: a worktree from the current branch:
   `git worktree add .worktrees/worker-<task> -b worker/<task>` (inside WSL).
   The sandbox has no network: fetch dependencies first (`cargo fetch`,
   `bun install`, …) so builds and tests run offline.
3. **Start**: as a background Bash task, so it shows in the Tasks pane; its
   description names the task and the alias (`Worker <task> (<alias>)`):

   ```bash
   MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu-26.04 --cd <worktree> --exec bash -lc 'R=~/.codex-runs/<task>; codex exec --ephemeral -m worker-deepseek-flash -o $R/final.txt - < $R/task.md > $R/log.txt 2>&1'
   ```

   Independent tasks may run in parallel, each in its own worktree.
4. **Collect**: read only `final.txt` (at most 15 lines: `DONE` / `PARTIAL` /
   `BLOCKED`, files, checks, open questions), `git status --short` and
   `git diff --stat`. Read `log.txt` only on failure, from the tail.
5. **Review**: read the full diff; run the tests, linters and formatters
   directly, because the worker's own claims are not evidence. Our rules apply
   to the worker's code as if Claude wrote it.
6. **Land**: fixes are made directly (small) or go into a follow-up brief (large).
   Then commit on the worker branch and merge it into the work branch; remove the
   worktree. Delete the worker branch only after `git branch --merged <work-branch>`
   lists it: `git branch -d` compares with the current checkout, not the work branch.
   A failed run gets one retry with a sharper brief or the stronger model, then
   Claude does the task directly.
7. **Report**: name the alias and the run's cost in the task report:
   `bash ~/.codex/run-cost.sh <task>` (WSL) prints calls, tokens and USD from the
   gateway's spend log; no key needed. Codex's own "tokens used" is not the bill:
   every call resends the conversation, so billed input is many times larger.

### Safety

- The worker never gets the master key, provider keys or any secret: Codex reads
  only `LITELLM_WORKER_KEY` (budgeted, set by the user) and never shows it.
- The worker never commits, pushes or installs (its prompt forbids it; the
  sandbox blocks network and writes outside the worktree). Landing is Claude's job.
- The sandbox is the `worker` permission profile in `workers/codex/config.toml`:
  the worktree is writable; `~/services`, `~/.ssh`, `/mnt` and other secret
  paths are unreadable; commands get no `*KEY*` / `*TOKEN*` / `*SECRET*` variables;
  no network. Never pass `-s`, it would replace the profile.
- No network means no database or service: a task whose tests need one fails
  check 3 and is done directly.
