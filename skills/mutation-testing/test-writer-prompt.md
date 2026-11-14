# Test writer brief

The main session fills the placeholders `<...>` and sends the whole text below as the subagent's prompt. Nothing else is added.

---

Write automated tests from a specification. The implementation is written by someone else, later or in parallel. The tests decide whether that implementation matches the specification, so they come from the specification alone.

## Rules

- Never read, open, search or list anything under these paths: `<source paths>`. This includes Read, Grep, Glob, `cat`, `ls`, `git show`, `git diff` and imports run for inspection. Running the test command is allowed; reading its stack traces into source files is not.
- Allowed to read: the test folder `<test folder>`, existing test helpers and fixtures in it, the test framework's configuration `<test config files>`.
- Write only inside `<test folder>`.
- Call the code only through the signatures below. Do not guess internals, private functions, file layout or data structures beyond them.
- One scenario gets at least one test. A test name states the scenario and the case (`test_<scenario>_<case>`, or the framework's naming).
- Assert observable outcomes: return values, raised errors, written data, emitted messages. Never assert how the result was produced.
- Cover the edges a scenario implies: boundaries, empty input, the error cases the scenario names.
- A scenario that cannot be tested through the given signatures, or whose expected outcome is ambiguous: do not invent the answer; report it.
- Do not run any code except the test command.

## Specification

<scenarios, copied verbatim>

## Signatures

```
<approved signatures, each with its one-line docstring>
```

## Test setup

- Framework: `<framework>`
- Test folder: `<test folder>`
- Test file naming: `<naming>`
- Test command: `<command>`

## Additional gaps to cover

<empty on the first dispatch; on later dispatches: the scenario name, the input and the expected outcome that no test checks yet>

## Return

1. The test files written or changed.
2. A table: scenario -> test names.
3. Scenarios not tested, each with the reason.
4. The output summary of one run of the test command (tests are expected to fail where the implementation is missing).
