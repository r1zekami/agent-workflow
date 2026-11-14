---
name: refactor
description: Use when the user asks to refactor code to the user's code rules (code-design, code-docs), for the whole repo or for the changes of the current session; started by the /refactor-all and /refactor-latest commands. Holds the scope, the violation inventory, the approval step and the batch loop.
---

# Refactor to the code rules

A refactor changes structure, never behavior. The target is the state described by rules `code-design` and `code-docs`. Public surface that changes is approved first (rule `code-negotiation`).

## 1. Scope

| Command | Scope |
|---|---|
| `/refactor-all` | Every tracked source file of the repo, excluding generated code, vendored code and build output. |
| `/refactor-latest` | Files changed in the current session: uncommitted changes plus the commits of the current branch since it left the default branch. On the default branch: the commits made in this session. An argument `<base>` (a commit or a branch) overrides both: `git diff <base>`. |

When the session boundary is unclear (after a compaction, on the default branch with earlier commits of the same day), show the commit list and ask which commits belong to the scope.

For `/refactor-latest`, code outside the scope is changed only when a refactor inside it requires that (a renamed function and its callers). Violations found outside the scope are listed in the report, not fixed.

## 2. Baseline

- Read the documents the repo's `AGENTS.md` names for tests and linters; without a table, `README.md` and `docs/README.md`.
- Run the tests and linters before any change and record the result. A red baseline is reported to the user before going on: a refactor cannot be verified against failing tests.
- A scope without tests: say so, and ask whether to write characterization tests for the touched code first or to continue without them.
- Work on a branch, never on the default branch. `/refactor-all` starts a new branch `refactor/<short-topic>`.

## 3. Inventory

List violations against the rules, each with file, line and rule:
- `code-design`: simplicity, rules 1-6, names and imports, comments, language in code, docstrings;
- `code-docs`: root `README.md`, `AGENTS.md` and `CLAUDE.md`, `docs/` layout;
- the project's own linters and formatters.

Claude Code: dispatch the `code-design-reviewer` subagent with the scope; it returns the list. OpenCode: read the rule files and go through the scope file by file. For `/refactor-all` on a large repo, inventory module by module.

## 4. Plan and approval

Group the violations into batches. One batch is one coherent change that can be verified on its own (one family with its registry, one module split, one renaming across callers). Order: the batches other batches depend on first.

Show the user:
1. The batches, each with the violations it fixes.
2. For every batch that changes visible surface: the proposal of rule `code-negotiation` (file tree, signatures, call site, payload).
3. What stays as is and why (for example, a public API with external consumers).

Implementation starts after the user's OK. `/refactor-all` keeps the plan in a file or in beads (skill `beads` in a repo with `.beads/`), so a compaction loses nothing.

## 5. Batch loop

For each approved batch:
1. Change the code. Behavior stays identical; a bug found on the way goes to the report, never fixed silently inside the refactor.
2. Update the docs the batch affects (rule `code-docs`).
3. Run the formatters, linters and tests. Red: fix within the batch or revert it; never move on with red tests.
4. Commit the batch only when the user asked for commits; otherwise leave it uncommitted and continue.

A batch that turns out to need a signature or a structure outside the approved plan stops the loop: show the change and wait for the OK.

## 6. Report

The final message follows rule `code-report`, plus:
- the baseline and the final result of tests and linters;
- violations left unfixed, each with the reason (outside the scope, needs a decision, external consumers).
