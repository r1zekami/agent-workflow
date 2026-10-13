## Workers: delegating code to cheap models

### Essentials

- Workers are Codex CLI runs in WSL, using a cheap model through the local LiteLLM gateway; the orchestrator briefs, reviews and lands their work.
- Delegation is the default for a coding task that passes five checks: decided, checkable, offline, clean, worth it (large volume: about 400+ lines or a mechanical change across many files).
- Substantial tasks below that size may go to a Sonnet subagent; small edits stay in the main session.
- Workers never get secrets, never commit, push or install; their sandbox has no network.

A worker is Codex CLI in WSL, running a cheap model through the local LiteLLM
gateway (`agent-workflow/services/litellm`, config in `workers/codex`). It
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
5. **Worth it**: large code volume: roughly 400 or more new or changed lines,
   or a mechanical change across many files. Below that, the brief and the
   review cost as much as writing the code (measured: worker-bench, below).

If any check fails, Claude does the task directly and gives the failed check as
the reason (Hard and Autonomous: `bd note`; Medium: the plan). Typical delegates:
implementing an approved interface, tests for given scenarios, a mechanical
change across files, a bug with a reproducing test. Never delegated: decisions,
reviews, git operations. WSL repos only.

Every final report says which tasks went to workers (alias, cost) and which
did not, with the failed check.

### Sonnet subagents for mid-size tasks

A task that fails only check 5 but is still substantial (a module with tests, a
feature across a few files) may go to a `general-purpose` subagent with
`model: sonnet` instead of being written in the main session. Same brief, same
review; no sandbox, so check 4 still applies. A subagent starts with about 75k
tokens of fixed context, so small edits stay in the main session.

### Measured: worker-bench (2026-10)

Python and Rust, three task sizes (about 20 to 300 lines), each done by an Opus
subagent directly, by an Opus subagent with a DeepSeek Flash worker, and by a
Sonnet subagent directly; 18 runs scored with hidden tests.
- All 18 runs passed every hidden test. The worker made 1 real defect in 6
  runs; the review caught it.
- Orchestrator tokens were 74k to 81k in every mode: the fixed context
  dominates, and a worker did not reduce them at these sizes.
- Worker cost: 0.7 to 2.7 US cents per run, plus 30 to 60 s of wall time.
- Sonnet matched Opus in quality and time at a lower price per token.
Details: second-brain `personal/projects/agent-workflow/log/2026-10-11-worker-bench.md`.

### Models

The aliases are the provider's model names (`deepseek-flash`), defined in the gateway's
`services/litellm/config.yaml`; each also needs its entry in
`workers/codex/models.json`. Default: the cheapest alias (`deepseek-flash`);
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
   MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu-26.04 --cd <worktree> --exec bash -lc 'R=~/.codex-runs/<task>; codex exec --ephemeral -m deepseek-flash -o $R/final.txt - < $R/task.md > $R/log.txt 2>&1'
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
  only `UNIVERSAL_LOCAL_LITELLM_KEY` (budgeted, set by the user) and never shows it.
- The worker never commits, pushes or installs (its prompt forbids it; the
  sandbox blocks network and writes outside the worktree). Landing is Claude's job.
- The sandbox is the `worker` permission profile in `workers/codex/config.toml`:
  the worktree is writable; `~/services`, `~/.ssh`, `/mnt` and other secret
  paths are unreadable; commands get no `*KEY*` / `*TOKEN*` / `*SECRET*` variables;
  no network. Never pass `-s`, it would replace the profile.
- No network means no database or service: a task whose tests need one fails
  check 3 and is done directly.
