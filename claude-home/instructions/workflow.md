## Approach — how a task is worked

EVERY task gets an approach: Easy, Medium, Hard or Autonomous. The approach is
HOW we work, not how big or difficult the task is — a hard problem can be worked
Easy, a tiny one Hard. The approach scales process only: the hard rules (secrets,
sensitive data, `.env`, push gate, language) apply at every level, unchanged.

| Approach | Answers | In one line |
|---|---|---|
| Easy | Does it work? | Don't overthink it — make it simply work. |
| Medium | Is it done right? | Do it properly, in one sitting: clean code by our rules and tests, no tracking, no bureaucracy. |
| Hard | Will it last? | Build it to last: plan, tracking, isolation and review — the work can be paused, handed over and resumed. |
| Autonomous | Can it run without the user? | Work alone from an approved plan: decide nothing that is the user's — park it as blocked till morning. |

**Choosing the approach**
- The user's tag wins: `[Easy]`, `[Medium]`, `[Hard]`, `[Autonomous]`.
- Otherwise pick Easy, Medium or Hard from context, state it in the first line
  of the reply — `Approach: Medium` — and proceed. When it's genuinely unclear, ask.
- Autonomous is never picked from context — only on the user's explicit tag.
- The user can switch the approach mid-task; switch immediately.
- A repo with `openspec/`: any change of behavior or logic is Hard, always
  (openspec.md). Easy and Medium only for changes that keep behavior identical.

### Easy — don't overthink it, make it simply work
Goal: a working result, fast. Structure and quality come later — if needed,
the user elevates the approach.

- **Questions** — don't ask unless blocked; assume, and list assumptions in the report.
- **Scope** — read only what the change needs. No subagents, no broad exploration.
- **Skip** — no plan, no docs, no beads, no second-brain notes (except the
  session-log entry and technology reports, see "Every approach"), no new tests.
- **Code conventions** — code-design.md does NOT apply: no interface gate, no
  registries or contracts, no final-report template. Naming style is preferred,
  not required. Log output stays English (non-ASCII breaks Windows consoles).
- **Context7** — only for unfamiliar or version-sensitive APIs (context7.md).
- **Check** — the cheapest real check: run it, call it, or re-read the result.
  Run existing tests that cover the change. If nothing could be checked, say
  "not verified" — never "done".
- **Git** — no branch or worktree; commit only when asked (commit format applies).
- **Superpowers** — don't invoke its skills unless asked; this overrides `using-superpowers`.
- **Report** — 1–3 lines: what changed, how it was checked, assumptions, and any
  public signature that changed.
- **Elevating** — never switch approach on my own. If the work clearly wants
  Medium, add one line to the report suggesting it — don't stop.

### Medium — do it properly, in one sitting
Goal: correct and clean by our rules, without the cross-session machinery —
no beads, no worktree, no review cycle.

1. **Clarify** — ask all open questions in ONE message up front; afterwards
   ask again only if something genuinely new comes up.
2. **Plan** — goal + 3–7 steps in chat. Proceed right away, unless the plan
   contains a decision that is the user's — then wait.
3. **Gate** — interface block (code-design rule 6) if anything public changes;
   wait for OK.
4. **Implement** — code: `superpowers:test-driven-development` (RED → GREEN →
   REFACTOR) where testable; a bug starts with `superpowers:systematic-debugging`.
   A step that passes the workers.md checks goes to a worker by default; doing
   it myself needs the failed check in the plan.
   Not code (config, setup, docs): do it, then check it the closest real way.
5. **Verify** — `superpowers:verification-before-completion`.
6. **Report** — code: final report (code-design rule 7); otherwise the result
   first, then how it was checked and what is open.

- **Review** — none, unless the user explicitly asks; then run the reviewer(s) asked for.
- **Tracking** — no beads (beads.md); in-session steps may use the built-in task list.
- **Git** — current branch; commit only when asked; propose a commit message at the end.
- **second-brain** — update notes this work made stale; don't create new ones.

### Hard — build it to last (do NOT skip steps)
Goal: work that can be paused, handed over and resumed — planned, tracked in
beads, isolated on its own branch, reviewed.

1. **Epic** — `bd create -t epic "Goal"` (container for intent + context; beads.md)
2. **Brainstorm** — `superpowers:brainstorming` (design before code)
3. **Plan** — `superpowers:writing-plans` (2-5 min tasks), including the interface
   block (code-design rule 6); wait for OK. OpenSpec repo: `/opsx:propose` with a
   spec delta instead (openspec.md)
4. **Sub-tasks** — `bd create --parent <epic-id>` for each, with acceptance
   criteria + `bd dep add` (blocks)
5. **Isolate** — `superpowers:using-git-worktrees`
6. **Implement** — `bd ready` → pick → `bd update --claim` →
   `superpowers:test-driven-development` (RED → GREEN → REFACTOR).
   A bug or an unexpected failure → `superpowers:systematic-debugging` before
   any fix. Ready sub-tasks with no dependency between them and no shared files →
   may run in parallel via `superpowers:dispatching-parallel-agents`.
   A sub-task that passes the workers.md checks goes to a worker by default;
   doing it myself needs the failed check in `bd note`.
7. **Review** — three independent reviews of the branch diff:
   `superpowers:requesting-code-review` (correctness), `code-design-reviewer`
   (our rules, with the approved interface block), `leak-auditor` (secrets and
   infrastructure specifics). Process the findings with
   `superpowers:receiving-code-review` — verify each one, push back on wrong
   ones, never apply blindly. Blocking findings are fixed before step 8.
   Review rounds are limited — see "Reviews" under Every approach.
8. **Verify** — `superpowers:verification-before-completion` (evidence before claims)
9. **Document** — OpenSpec repo: `/opsx:archive` + repo docs first (openspec.md).
   Then record the work in second-brain by its rules (second-brain.md):
   find the entity (project or module) or create it per second-brain.md;
   README → the new current state, `log/` → what was done, decisions
   made (append-only). Link it in the epic: `bd note <epic-id> "docs: <note path>"`.
   `leak-auditor` on the second-brain changes, then commit there:
   `docs(<entity-slug>): <what was done>`.
10. **Finish** — `superpowers:finishing-a-development-branch` (push gate still applies)
11. **Close** — `bd close <epic-id> --reason "Done"` + final report (code-design rule 7)
    with a link to the second-brain note

Side quests: `bd create "..." -t bug --deps discovered-from:<current-id>` (beads.md)

### Autonomous — work alone from an approved plan
For work while the user is away (e.g. overnight). Nobody answers questions, so
the run only executes work whose decisions are already made.

**Before the run (together with the user):**
- A beads queue exists (beads.md) — normally Hard steps 1–4: epic, brainstorm,
  a plan with approved interfaces, sub-tasks with clear acceptance criteria.
- A work branch or worktree is set up (Hard step 5).
- The user starts the session themselves (usually for the night) in **auto mode** —
  any permission prompt would stall the run until morning. Never schedule a run.
- First action of the run: request keep-awake from the app.

The harness backs these rules up (`settings.json`): `.env` is denied to file
tools, pushes always prompt, and auto mode refuses pushes, force operations,
deletes outside the repo and installs. An attempted push would stall the run on
its prompt — so never attempt one.

**During the run:**
- Loop: `bd ready` → claim → `superpowers:test-driven-development` →
  `superpowers:verification-before-completion` → commit on the work branch →
  `bd close` → next. A task that passes the workers.md checks goes to a worker
  (preferred here: nobody waits, and every task is reviewed in the morning);
  otherwise, for long queues prefer `superpowers:subagent-driven-development`
  (fresh context per task).
- Never ask questions — nobody will answer. A decision the plan doesn't cover:
  - trivial and reversible → make it, record it with `bd note`;
  - the user's call (interface, design, scope) → `bd update <id> --status blocked`
    + the question in `bd note`, move to the next task.
- Three failed attempts at the same task → mark it blocked with what was tried,
  move on. Don't loop.
- Discovered work → a new beads issue (`discovered-from`), never scope creep.
- Beads is the source of truth: keep notes current, so a context compaction or
  a crash loses nothing.

**Never in Autonomous** — nobody is there to approve:
- push, PR, merge into the base branch, `bd sync` / Dolt push, or anything else
  that leaves the machine;
- changes outside the work branch or worktree — second-brain included: nothing
  unattended goes into the persistent knowledge base (the one exception: the
  run's session-log entry at the end);
- deleting data, force operations, history rewrites;
- production systems, secrets, `.env`;
- installing software or changing settings.

**End of run** — stop when no ready tasks remain. Run `leak-auditor` on the
branch diff; its findings go into the report. Add the run's session-log entry.
Send the user a push notification that the run is over (done / blocked counts).
The final message is the morning report:
1. **Done** — task id, one line, commit hash;
2. **Blocked** — task id + the question for the user;
3. **Decisions made alone** — what, why, how to revert;
4. **How to verify** — commands, and what was already run;
5. **Branch** — name, commits ahead of base.

**After the run (together with the user)** — go through the report, answer the
blocked questions, then continue as Hard from step 7: review → verify →
document → finish → close.

### Every approach
- **Session log** — at the end of every task that changed something or produced
  an artifact (pure questions and answers are not logged), add one entry to
  second-brain `agents-data/session-log/<YYYY-MM>/` — format in
  second-brain.md. An Autonomous run logs one entry for the whole run.
- **Reviews** — of code, designs or specs, by any reviewer — at most two rounds
  per artifact: the full review, then one re-check limited to the fixed items.
  - Blocking: Critical and Important findings only.
  - Minor findings and nits are not re-reviewed: collect them into one beads
    issue (Hard, Autonomous) or the report's open items (Medium) and move on.
  - A third round only when the user asks for it. A re-check that finds new
    Important issues goes to the user, not into another round.
- **Subagents** — dispatch one only for a well-defined scope:
  - one goal; explicit inputs (files, diff range, change id — not "the repo");
    the expected output and its size; when to stop;
  - a re-check gets only the delta and the findings it checks, never the whole
    artifact again;
  - work that fits in a few tool calls is done inline — a subagent starts cold
    and re-reads everything.
- **Context7** — when and how: context7.md.
- **Technology choice** — "what to use for X", "alternatives to Y" → the
  `architecture-designer` subagent; it builds on earlier reports. Save its report
  to second-brain `agents-data/architecture-designer/<topic>.md` (after `leak-auditor`) — the one
  second-brain write that Easy does too. Not in Autonomous.
- No completion claims without running verification commands.
