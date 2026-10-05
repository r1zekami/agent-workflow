## Workers — delegating code to cheap models

A worker is Codex CLI in WSL, running a cheap model through the local LiteLLM
gateway (`claude-code-setup/services/litellm`, config in `workers/codex`). It
writes code; I stay the orchestrator: I scope the task, review the diff and own
the result. A worker saves my output tokens — it never replaces my judgment.

### When

- **Medium, Hard, Autonomous** — not Easy (setup costs more than it saves).
- **Delegate**: well-scoped code with a check — implementing an approved
  interface, tests for given scenarios, a mechanical change across files, a
  bug with a reproducing test. A Hard sub-task with acceptance criteria is the
  ideal unit.
- **Never delegate**: decisions (interfaces, design, scope), reviews, anything
  touching secrets, `.env` or credentials, git operations, and tasks that fit in
  a few edits — doing those myself is cheaper than briefing and reviewing.
- WSL repos only. The worker's code leaves the machine to the model provider —
  never for a repo whose code must stay private (ask when unsure).

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

1. **Brief** — write the task to `~/.codex-runs/<task>/task.md` (WSL):
   goal; files to touch; approved signatures (code-design rule 6) to implement
   exactly; acceptance criteria as tests; the commands that check it; out of
   scope. One task per brief.
2. **Isolate** — a worktree from the current branch:
   `git worktree add .worktrees/worker-<task> -b worker/<task>` (inside WSL).
   The sandbox has no network: fetch dependencies first (`cargo fetch`,
   `bun install`, …) so builds and tests run offline.
3. **Start** — as a background Bash task, so it shows in the Tasks pane; its
   description names the task and the alias (`Worker <task> (<alias>)`):

   ```bash
   MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu-26.04 --cd <worktree> --exec bash -lc 'R=~/.codex-runs/<task>; codex exec --ephemeral -s workspace-write -m worker-deepseek-flash -o $R/final.txt - < $R/task.md > $R/log.txt 2>&1'
   ```

   Independent tasks may run in parallel, each in its own worktree.
4. **Collect** — read only `final.txt` (at most 15 lines: `DONE` / `PARTIAL` /
   `BLOCKED`, files, checks, open questions), `git status --short` and
   `git diff --stat`. Read `log.txt` only on failure, from the tail.
5. **Review** — read the full diff; run the tests, linters and formatters
   myself — the worker's own claims are not evidence. Our rules apply to the
   worker's code as if I wrote it.
6. **Land** — fixes are mine (small) or a follow-up brief (large). Then commit
   on the worker branch and merge it into the work branch; remove the worktree.
   A failed run: one retry with a sharper brief or the stronger model, then I
   do it myself.
7. **Report** — name the alias and the run's cost (LiteLLM spend log) in the
   task report.

### Safety

- The worker never gets the master key, provider keys or any secret: Codex reads
  only `LITELLM_WORKER_KEY` (budgeted, set by the user) and never shows it.
- The worker never commits, pushes or installs (its prompt forbids it; the
  sandbox blocks network and writes outside the worktree). Landing is my job.
