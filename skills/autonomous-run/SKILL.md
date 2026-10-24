---
name: autonomous-run
description: Use when the user starts an unattended run (overnight, "work alone", autopilot mode) to execute an already approved plan without anyone answering questions. Holds what may be decided alone, what is never done, and the morning report.
---

# Autonomous run

The run only executes work whose decisions are already made. Nobody answers questions until the user is back.

## Before the run (with the user)

- An approved plan exists as a queue of tasks with acceptance criteria: beads (skill `beads`) or a plan file in the repo.
- A work branch or worktree is set up; the run never works on the default branch.
- The user starts the session in a permission mode that does not prompt (Claude Code: `auto`; OpenCode: an agent whose permissions allow the work). Any prompt would stall the run until morning.
- First action of the run: request keep-awake if the harness offers it.

## During the run

- Loop: take the next ready task, test first, implement, verify, commit on the work branch, mark the task done, next.
- Never ask questions. A decision the plan does not cover:
  - trivial and reversible: make it and record it (task note or plan file);
  - the user's call (interface, design, scope): mark the task blocked with the question, move to the next task.
- Three failed attempts at one task: mark it blocked with what was tried, move on.
- Discovered work becomes a new task, never scope creep.
- Keep the task notes current, so a compaction or a crash loses nothing.

## Never during the run

- push, PR, merge into the base branch, `bd sync` / `bd dolt push`, anything that leaves the machine;
- changes outside the work branch or worktree (second-brain included, except the run's session-log entry at the end);
- deleting data, force operations, history rewrites;
- production systems, secrets, `.env`;
- installing software or changing settings.

## End of the run

Stop when no ready tasks remain. Add one session-log entry for the run (skill `second-brain`). Send a push notification if the harness offers it. The final message is the morning report:

1. **Done**: task id, one line, commit hash.
2. **Blocked**: task id and the question for the user.
3. **Decisions made alone**: what, why, how to revert.
4. **How to verify**: commands, and what was already run.
5. **Branch**: name, commits ahead of base.

After the run, with the user: go through the report, answer the blocked questions, then review, verify and finish the branch as usual.
