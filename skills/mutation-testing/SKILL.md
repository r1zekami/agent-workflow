---
name: mutation-testing
description: Use when the user asks for tests written from the spec by an isolated agent and checked by mutation testing. Holds the spec and brief preparation, the test-writer subagent dispatch, the frozen-tests check, the mutation run and the triage of surviving mutants.
---

# Spec tests and mutation testing

Tests written by the agent that writes the code repeat that agent's understanding of the task: everything is green and the code still does the wrong thing. Here the tests come from the spec through a subagent that never sees the implementation, and a mutation testing tool checks that the tests detect changes in the code.

Roles:
- **Main session**: prepares the brief, implements the code, runs the mutation tool, triages survivors.
- **Test writer**: a fresh subagent. Input: the brief only. Writes tests, never reads source code.

## 1. Preconditions

- **Spec.** Scenarios in the default OpenSpec schema: a `#### Scenario: <name>` heading followed by `- **WHEN** ...` and `- **THEN** ...` steps. In a repo with `openspec/`: the scenarios of the change under `openspec/changes/<change>/specs/`, or of `openspec/specs/` for existing behavior. Without OpenSpec: a spec file in the same schema (`docs/specs/<feature>.md`). No spec: write it with the user first; the skill does not start without one.
  ```
  ### Requirement: Order cancellation
  The system SHALL cancel an unpaid order on request.

  #### Scenario: Unpaid order is cancelled
  - **WHEN** the owner cancels an order with status NEW
  - **THEN** the order status is CANCELLED
  ```
- **Interface.** The public signatures the tests call, approved by the user (rule `code-negotiation`). Tests are written against these signatures.
- **Test command.** Read the documents the repo's `AGENTS.md` names for tests; without a table, `README.md` and `docs/README.md`.
- **Mutation tool** for the language (table in section 6). Not installed: ask the user to add it as a dev dependency; never install without a yes.
- Work on a branch, never on the default branch.

## 2. Brief

Fill `test-writer-prompt.md` (in this skill's folder). The brief contains only:
- the scenarios, copied verbatim from the spec;
- the approved signatures, with their one-line docstrings;
- the test framework, the test folder, the naming of test files, the test command;
- the source paths the writer must not read.

Never in the brief: implementation code, file contents from source folders, the conversation, a plan, the main session's guesses about the solution. A term the scenarios use and do not define goes to the user as a spec gap, not into the brief as an explanation.

## 3. Test writer

Dispatch a fresh subagent with the filled brief as the whole prompt:
- Claude Code: the Agent tool, `subagent_type: "general-purpose"`. Never `fork`: a fork inherits the whole conversation.
- OpenCode: the `task` tool with the `general` subagent.

The writer returns the test files, a table "scenario -> test names", and the scenarios it could not test with the reason.

The main session then:
1. Runs the tests. New code: every test fails on the missing implementation or on an assertion. Changed code: the tests of new or modified scenarios fail, the rest pass. A test that fails on a syntax error or an import of a non-existent test helper goes back to the writer.
2. Checks the table: every scenario has at least one test. Gaps go back to the writer, or to the user when the writer reported the scenario as not testable.
3. Freezes the tests: `git add <test files>`. The staged state is the reference; the main session never stages test files after this point.

The main session never edits test files itself.

## 4. Implementation

Implement in the main session until the tests pass. Test files stay unchanged.

A test that looks wrong is compared with the spec:
- the test contradicts the scenario: a new writer subagent gets the same brief plus the scenario name and what the test asserts against the scenario text;
- the scenario is ambiguous or wrong: the question goes to the user; after the spec is fixed, the affected tests are rewritten by a new writer subagent.

## 5. Frozen-tests check

```
git diff --exit-code -- <test files>
```
Output must be empty: the test files equal the staged reference. Any difference is undone (`git checkout -- <test files>`) and the implementation is fixed instead.

## 6. Mutation run

Run the tool on the files changed by the implementation only. Long runs go to the background.

| Language | Tool | Scope to the changed code |
|---|---|---|
| Python | `mutmut` 3.x | `only_mutate` (globs) next to `source_paths` in `[tool.mutmut]`; in `pyproject.toml` every path option is an array; no diff mode, list the changed files; on Windows runs only inside WSL |
| Rust | `cargo-mutants` | `git diff <base> > changes.diff`, then `cargo mutants --in-diff changes.diff`; or `--file <glob>` (`-f`), repeatable |
| JavaScript, TypeScript | StrykerJS | `npx stryker run --mutate "<path or glob>"`; the CLI value replaces `mutate` of the config file |
| Java, Kotlin | PIT | `targetClasses` and `targetTests` in the build plugin configuration; core PIT has no diff mode, list the changed classes |
| Go | `gremlins` | `gremlins unleash --diff "<base branch or commit>"` |

Checked against the official docs in November 2026 (mutmut 3.8.1, cargo-mutants 27.1, StrykerJS 10.1, PIT 1.30.2, gremlins 0.6). Flags change between versions: check the tool's current documentation before the first run in a repo.

## 7. Triage of survivors

The gate: no surviving mutant left without a category. Every survivor gets exactly one:

| Category | Meaning | Action |
|---|---|---|
| Spec covers it | A scenario describes the behavior, no test detects the change. | A new writer subagent: the same brief plus the gap described in spec terms (scenario name, input, expected outcome). Never the mutant's code or diff. |
| Equivalent | The mutant does not change observable behavior (for example, a changed log message). | Recorded in the report with the reason; excluded through the tool's own ignore mechanism when it has one. |
| Spec is silent | The code has behavior no scenario describes. | A question to the user: add a scenario, or remove the behavior from the code. |

After new tests: freeze again (section 3, step 3) and repeat sections 5-7. Three rounds without closing all survivors: stop and report.

## 8. Report

The final message follows rule `code-report`, plus:
- mutation score before and after triage, with the tool and its version;
- the survivors per category, the equivalent ones with their reasons;
- the questions to the user about the spec.
