## OpenSpec: behavior specs in the repo

OpenSpec keeps a written contract of how the system must behave, inside the
repo, and changes behavior only through a change proposal that edits that
contract first. A repo uses OpenSpec when it has an `openspec/` directory.

### A spec is not documentation

| What | Where | Answers |
|---|---|---|
| Spec: the behavior contract | `openspec/specs/` | What must the system do? (normative, checkable) |
| Change records | `openspec/changes/archive/` | Why and how did this behavior change? |
| Docs: install, run, configure, operate, architecture overview | repo `README.md`, `docs/` | How do I use / run / understand it? |
| Knowledge across repos: context, links between systems, decisions, history | second-brain (second-brain.md) | How does this fit into everything else? |

Second-brain links to specs and docs in the repo and never duplicates them.

### The rule: behavior changes only via Hard

In a repo with `openspec/`, ANY change of behavior or logic is Hard, with no
exceptions. Easy and Medium are allowed only for changes that keep behavior
identical: refactoring, typos, formatting, comments, config that does not change
behavior.

If an Easy or Medium task turns out to change behavior, STOP and propose
elevating to Hard. This overrides Easy's "don't stop" rule.

### OpenSpec inside the Hard steps (workflow.md)

- **3. Plan**: `/opsx:propose` produces `proposal.md` (why, scope), `design.md`
  (how, including the interface block, code-design rule 6) and the spec delta
  (`## ADDED / MODIFIED / REMOVED Requirements`). `openspec validate <change>`
  passes. Wait for the user's OK on the whole change.
- **4. Sub-tasks**: every item in `tasks.md` becomes a beads sub-task; its
  acceptance criteria are the matching spec scenarios. From here beads is the
  only state: `tasks.md` stays the approved plan and is not ticked item by item.
- **6. Implement**: through the beads loop, not `/opsx:apply`. Each scenario
  becomes a test first (RED, then GREEN).
- **9. Document**: tick all of `tasks.md` in one edit (every bead is closed),
  then `/opsx:archive` merges the delta into `openspec/specs/`. Update repo docs
  if install / run / config / architecture changed. Then the second-brain entry
  links the archived change.

### One change = one slice (Simplicity, code-design.md)

A change is the smallest slice that can be implemented, tested and archived on
its own, never a whole subsystem up front. A change must be split when it has
more than about 20 requirements, a `design.md` longer than about 300 lines, or
parts that could ship separately. Split it into an ordered series of changes;
the first one is specified in full, later ones are a list of titles in its
`proposal.md` ("Follow-up changes"). `design.md` holds contracts and
invariants (signatures, data, failure modes), never the code of call sites.

### Why this deviates from default OpenSpec

Default OpenSpec is built for a team on mixed AI tools: `tasks.md` checkboxes
are the tracker, `/opsx:apply` works through them, and the PR carries spec and
code together. This setup is solo, across long, interrupted sessions, so:
- beads replaces the checkboxes: dependencies, a ready queue and notes that
  survive compaction;
- every scenario becomes a test first; default apply does not require tests;
- reviews and second-brain links come from the Hard steps;
- OpenSpec stays local (below) until the user decides to share it.

### Spec format

```markdown
### Requirement: <name>
The <system> SHALL <behavior>.

#### Scenario: <case>
- **WHEN** <trigger>
- **THEN** <observable outcome>
```

- One requirement = one behavior. Every requirement has at least one scenario.
- Scenarios describe observable outcomes, never implementation details.
- No secrets and no infrastructure specifics in specs (sensitive-data.md);
  made-up names in examples.

### Setup and tooling

- `openspec` is installed in WSL only; run it inside WSL (environment.md).
- A repo without `openspec/`: ask before `openspec init`, and review every file
  it writes (commands, instruction blocks). They are subordinate to these rules.
- **Local by default**, like beads stealth: append `openspec/`,
  `.claude/commands/opsx/` and `.claude/skills/openspec-*/` to
  `.git/info/exclude` right after `openspec init`. Commit OpenSpec only when the
  user asks for it.
- **`openspec/config.yaml`**: OpenSpec injects `context` into every artifact it
  writes and `rules` into the matching one, so these conventions travel with the
  artifacts. Start every repo from this, then add the project's own context:

  ```yaml
  schema: spec-driven
  context: |
    <stack, layout, what exists now, short; no secrets, no infrastructure specifics>
    All text is English. Made-up names in examples.
  rules:
    proposal:
      - One change is one slice that ships on its own; list later slices under "Follow-up changes"
    specs:
      - One requirement is one behavior with at least one WHEN/THEN scenario
      - Scenarios state observable outcomes, never implementation details
    design:
      - Contracts and invariants only (signatures, data, failure modes), never call-site code
      - Include the interface block in the code-design rule 6 format
      - Simplicity: no speculative options, members or hooks
    tasks:
      - Every task names the spec scenarios that are its acceptance criteria
  ```
- Useful CLI: `openspec list`, `openspec show <item>`, `openspec validate <item>`,
  `openspec status`.
- Telemetry stays off (`openspec config set telemetry.enabled false`).
