---
name: code-docs
description: Use after any work on code to write the final report, and when writing docstrings, a repo README or docs for code. Holds the fixed report template and the payload notation.
---

# Documenting code

## Final report after code work

Sections in this order. A section with nothing to say is omitted, never filled
with "n/a".

1. **What changed**: per file, one line each: what and why.
2. **Signatures**: new and changed ones, in the interface format of skill
   `code-design` (rule 6).
3. **Pipeline**: a text diagram: from where, through what, to where.
4. **Payload**: if the pipeline builds one, shown whole with every possible field.
5. **How to verify**: command and expected result, plus what was already run.
6. **Not done**: assumptions and open questions.

## Payload notation

Keys are never duplicated; alternatives go in the value:
`/` = alternative values; `[...]` = the field is a list; `<...>` = computed value.
```
"some_final_json_we_built": {
    "payload": "<some_computed_value>/N/A",
    "color": "RED/GREEN/N/A",
    "tags": ["<tag>", ...]
}
```

## Docstrings

One line on the non-obvious why; never retell the signature. A signature change
updates its docstring in the same edit.

## Repo docs

| What | Where |
|---|---|
| Install, run, configure, operate, architecture overview | `README.md`, `docs/` |
| Behavior contract (if the repo uses OpenSpec) | `openspec/specs/` |
| Context across repos, decisions, history | second-brain (skill `second-brain`) |

Docs follow skill `writing`. A change of install, run, config or architecture
updates the docs in the same change.
