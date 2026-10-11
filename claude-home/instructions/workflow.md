## Approach: how a task is worked

### Essentials

- Every task gets an approach, named in the first line of the reply: Easy (make it work), Medium (done right in one sitting), Hard (planned, tracked in beads, isolated, reviewed), Autonomous (unattended run from an approved plan).
- The user's tag (`[Easy]`, `[Medium]`, ...) wins; otherwise pick from context and ask when it is unclear.
- Easy: no plan, no new tests; the cheapest real check; "not verified" when nothing could be checked.
- Medium: open questions in one message up front, a short plan, public interfaces shown for approval before coding, tests where testable, verification before any claim of done.
- No completion claim without running a check.
- Every task that changed something gets a session-log entry in second-brain.

EVERY task gets an approach: Easy, Medium, Hard or Autonomous. The approach is
HOW the work is done, not how big or difficult the task is. A hard problem can be
worked Easy, a tiny one Hard. The approach scales process only: the hard rules
(secrets, sensitive data, `.env`, push gate, language) apply at every level,
unchanged.

| Approach | Answers | In one line |
|---|---|---|
| Easy | Does it work? | Don't overthink it: make it simply work. |
| Medium | Is it done right? | Do it properly, in one sitting: clean code by our rules and tests, no tracking, no bureaucracy. |
| Hard | Will it last? | Build it to last: plan, tracking, isolation and review. The work can be paused, handed over and resumed. |
| Autonomous | Can it run without the user? | Work alone from an approved plan: decide nothing that is the user's, park it as blocked till morning. |

**Choosing the approach**
- The user's tag wins: `[Easy]`, `[Medium]`, `[Hard]`, `[Autonomous]`.
- Otherwise pick Easy, Medium or Hard from context, state it in the first line
  of the reply (`Approach: Medium`) and proceed. When it is genuinely unclear, ask.
- Autonomous is never picked from context, only on the user's explicit tag.
- The user can switch the approach mid-task; switch immediately.
- A repo with `openspec/`: any change of behavior or logic is Hard, always
  (openspec.md). Easy and Medium only for changes that keep behavior identical.

### Easy: don't overthink it, make it simply work
Goal: a working result, fast. Structure and quality come later; if needed,
the user elevates the approach.

- **Questions**: don't ask unless blocked; assume, and list assumptions in the report.
- **Scope**: read only what the change needs. No subagents, no broad exploration.
- **Skip**: no plan, no docs, no beads, no second-brain notes (except the
  session-log entry and technology reports, see "Every approach"), no new tests.
- **Code conventions**: code-design.md does NOT apply: no interface gate, no
  registries or contracts, no final-report template. Naming style is preferred,
  not required. Log output stays English (non-ASCII breaks Windows consoles).
- **Context7**: only for unfamiliar or version-sensitive APIs (context7.md).
- **Check**: the cheapest real check: run it, call it, or re-read the result.
  Run existing tests that cover the change. If nothing could be checked, say
  "not verified", never "done".
- **Git**: no branch or worktree; commit only when asked (commit format applies).
- **Superpowers**: don't invoke its skills unless asked; this overrides `using-superpowers`.
- **Report**: 1-3 lines: what changed, how it was checked, assumptions, and any
  public signature that changed.
- **Elevating**: never switch approach without being told. If the work clearly
  wants Medium, add one line to the report suggesting it and continue.

### Medium: do it properly, in one sitting
Goal: correct and clean by our rules, without the cross-session machinery:
no beads, no worktree, no review cycle.

1. **Clarify**: ask all open questions in ONE message up front; afterwards
   ask again only if something genuinely new comes up.
2. **Plan**: goal + 3-7 steps in chat. Proceed right away, unless the plan
   contains a decision that is the user's; then wait.
3. **Gate**: interface block (code-design rule 6) if anything public changes;
   wait for OK.
4. **Implement**: code: `superpowers:test-driven-development` (RED, GREEN,
   REFACTOR) where testable; a bug starts with `superpowers:systematic-debugging`.
   A step that passes the workers.md checks goes to a worker by default; doing
   it directly needs the failed check in the plan.
   Not code (config, setup, docs): do it, then check it the closest real way.
5. **Verify**: `superpowers:verification-before-completion`.
6. **Report**: code: final report (code-design rule 7); otherwise the result
   first, then how it was checked and what is open.

- **Review**: none, unless the user explicitly asks; then run the reviewer(s) asked for.
- **Tracking**: no beads (beads.md); in-session steps may use the built-in task list.
- **Git**: current branch; commit only when asked; propose a commit message at the end.
- **second-brain**: update notes this work made stale; don't create new ones.

### Hard: build it to last (do NOT skip steps)
Goal: work that can be paused, handed over and resumed: planned, tracked in
beads, isolated on its own branch, reviewed.

1. **Epic and plan**: `bd create -t epic "Goal"` (intent + context; beads.md).
   Then one design pass: `superpowers:brainstorming` followed by
   `superpowers:writing-plans` (2-5 min tasks) with the interface block
   (code-design rule 6). One approval from the user covers the whole plan.
   OpenSpec repo: `/opsx:propose` with a spec delta instead (openspec.md).
2. **Sub-tasks and isolation**: `bd create --parent <epic-id>` for each task,
   with acceptance criteria and `bd dep add` (blocks); then
   `superpowers:using-git-worktrees`.
3. **Implement**: `bd ready`, pick, `bd update --claim`,
   `superpowers:test-driven-development` (RED, GREEN, REFACTOR).
   A bug or an unexpected failure goes through `superpowers:systematic-debugging`
   before any fix. Ready sub-tasks with no dependency between them and no shared
   files may run in parallel via `superpowers:dispatching-parallel-agents`.
   A sub-task that passes the workers.md checks goes to a worker by default;
   doing it directly needs the failed check in `bd note`.
4. **Review**: one review of the branch diff by default:
   `superpowers:requesting-code-review`, briefed with the approved interface
   block and code-design.md. A second, separate `code-design-reviewer` pass only
   for risky changes: authentication and access control, data migrations,
   public APIs. Process the findings with `superpowers:receiving-code-review`:
   verify each one, push back on wrong ones, never apply blindly. Blocking
   findings are fixed before step 5. Review rounds are limited, see "Reviews"
   under Every approach. The leak audit runs only before a push (git.md).
5. **Verify**: `superpowers:verification-before-completion` (evidence before claims).
6. **Document**: OpenSpec repo: `/opsx:archive` + repo docs first (openspec.md).
   Then record the work in second-brain by its rules (second-brain.md): the
   entity README gets the new current state, `log/` gets what was done,
   `decisions.md` the decisions (append-only). Link it in the epic:
   `bd note <epic-id> "docs: <note path>"`. Commit there:
   `docs(<entity-slug>): <what was done>`.
7. **Finish and close**: `superpowers:finishing-a-development-branch` (push gate
   still applies), `bd close <epic-id> --reason "Done"`, final report
   (code-design rule 7) with a link to the second-brain note.

Side quests: `bd create "..." -t bug --deps discovered-from:<current-id>` (beads.md)

### Autonomous: work alone from an approved plan
For work while the user is away (e.g. overnight). Nobody answers questions, so
the run only executes work whose decisions are already made.

**Before the run (together with the user):**
- A beads queue exists (beads.md), normally Hard steps 1-2: epic, plan,
  a plan with approved interfaces, sub-tasks with clear acceptance criteria.
- A work branch or worktree is set up (Hard step 2).
- The user starts the session personally (usually for the night) in **auto mode**,
  because any permission prompt would stall the run until morning. Never schedule a run.
- First action of the run: request keep-awake from the app.

The harness backs these rules up (`settings.json`): `.env` is denied to file
tools, pushes always prompt, and auto mode refuses pushes, force operations,
deletes outside the repo and installs. An attempted push would stall the run on
its prompt, so never attempt one.

**During the run:**
- Loop: `bd ready`, claim, `superpowers:test-driven-development`,
  `superpowers:verification-before-completion`, commit on the work branch,
  `bd close`, next. A task that passes the workers.md checks goes to a worker
  (preferred here: nobody waits, and every task is reviewed in the morning);
  otherwise, for long queues prefer `superpowers:subagent-driven-development`
  (fresh context per task).
- Never ask questions, nobody will answer. A decision the plan doesn't cover:
  - trivial and reversible: make it, record it with `bd note`;
  - the user's call (interface, design, scope): `bd update <id> --status blocked`
    + the question in `bd note`, move to the next task.
- Three failed attempts at the same task: mark it blocked with what was tried,
  move on. Don't loop.
- Discovered work becomes a new beads issue (`discovered-from`), never scope creep.
- Beads is the source of truth: keep notes current, so a context compaction or
  a crash loses nothing.

**Never in Autonomous** (nobody is there to approve):
- push, PR, merge into the base branch, `bd sync` / Dolt push, or anything else
  that leaves the machine;
- changes outside the work branch or worktree, second-brain included: nothing
  unattended goes into the persistent knowledge base (the one exception: the
  run's session-log entry at the end);
- deleting data, force operations, history rewrites;
- production systems, secrets, `.env`;
- installing software or changing settings.

**End of run**: stop when no ready tasks remain. Add the run's session-log entry.
Send the user a push notification that the run is over (done / blocked counts).
The final message is the morning report:
1. **Done**: task id, one line, commit hash;
2. **Blocked**: task id + the question for the user;
3. **Decisions made alone**: what, why, how to revert;
4. **How to verify**: commands, and what was already run;
5. **Branch**: name, commits ahead of base.

**After the run (together with the user)**: go through the report, answer the
blocked questions, then continue as Hard from step 4: review, verify,
document, finish, close.

### Every approach
- **Session log**: at the end of every task that changed something or produced
  an artifact (pure questions and answers are not logged), add one entry to
  second-brain `agents-data/session-log/<YYYY-MM>/`; format in
  second-brain.md. An Autonomous run logs one entry for the whole run.
- **Reviews**: of code, designs or specs, by any reviewer, at most two rounds
  per artifact: the full review, then one re-check limited to the fixed items.
  - Blocking: Critical and Important findings only.
  - Minor findings and nits are not re-reviewed: collect them into one beads
    issue (Hard, Autonomous) or the report's open items (Medium) and move on.
  - A third round only when the user asks for it. A re-check that finds new
    Important issues goes to the user, not into another round.
- **Subagents**: dispatch one only for a well-defined scope:
  - one goal; explicit inputs (files, diff range, change id, not "the repo");
    the expected output and its size; when to stop;
  - a re-check gets only the delta and the findings it checks, never the whole
    artifact again;
  - work that fits in a few tool calls is done inline, because a subagent starts
    cold and re-reads everything.
- **Context7**: when and how: context7.md.
- **Technology choice** ("what to use for X", "alternatives to Y"): use the
  `architecture-designer` subagent; it builds on earlier reports. Save its report
  to second-brain `agents-data/architecture-designer/<topic>.md`.
  This is the one second-brain write that Easy does too. Not in Autonomous.
- No completion claims without running verification commands.
