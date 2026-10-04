## OpenSpec — behavior specs in the repo

OpenSpec keeps a written contract of how the system must behave, inside the repo,
and changes behavior only through a change proposal that edits that contract
first. A repo uses OpenSpec when it has an `openspec/` directory.

### A spec is not documentation

| What | Where | Answers |
|---|---|---|
| Spec — the behavior contract | `openspec/specs/` | What must the system do? (normative, checkable) |
| Change records | `openspec/changes/archive/` | Why and how did this behavior change? |
| Docs — install, run, configure, operate, architecture overview | repo `README.md`, `docs/` | How do I use / run / understand it? |
| Knowledge across repos — context, links between systems, decisions, history | second-brain (second-brain.md) | How does this fit into everything else? |

Second-brain links to specs and docs in the repo — it never duplicates them.

### The rule: behavior changes only via Hard

In a repo with `openspec/`, ANY change of behavior or logic is Hard — no exceptions.
Easy and Medium are allowed only for changes that keep behavior identical:
refactoring, typos, formatting, comments, config that doesn't change behavior.

If an Easy or Medium task turns out to change behavior — STOP and propose
elevating to Hard. This overrides Easy's "don't stop" rule.

### OpenSpec inside the Hard steps (workflow.md)

- **3. Plan** — `/opsx:propose`: `proposal.md` (why, scope), `design.md` (how,
  including the interface block — code-design rule 6), spec delta
  (`## ADDED / MODIFIED / REMOVED Requirements`). `openspec validate <change>`
  passes. Wait for the user's OK on the whole change.
- **4. Sub-tasks** — every item in `tasks.md` becomes a beads sub-task; its
  acceptance criteria are the matching spec scenarios.
- **6. Implement** — through the beads loop, not `/opsx:apply`: each scenario
  becomes a test first (RED → GREEN); tick the `tasks.md` item when its bead closes.
- **9. Document** — `/opsx:archive` merges the delta into `openspec/specs/`;
  update repo docs if install / run / config / architecture changed; then the
  second-brain entry links the archived change.

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
- No secrets and no infrastructure specifics in specs (sensitive-data.md) —
  made-up names in examples.

### Setup and tooling

- `openspec` is installed in WSL only — run it inside WSL (environment.md).
- A repo without `openspec/` → ask before `openspec init`; review every file it
  writes (commands, instruction blocks) — they are subordinate to these rules.
- Useful CLI: `openspec list`, `openspec show <item>`, `openspec validate <item>`,
  `openspec status`.
- Telemetry stays off (`openspec config set telemetry.enabled false`).
