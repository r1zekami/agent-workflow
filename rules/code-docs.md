# Documenting code

## Final report after code work

Sections in this order. A section with nothing to say is omitted, never filled with "n/a".

1. **What changed**: per file, one line each: what and why.
2. **Signatures**: new and changed ones, in the interface format of rule `code-design` (rule 6).
3. **Pipeline**: a text diagram: from where, through what, to where.
4. **Payload**: if the pipeline builds one, shown whole with every possible field.
5. **How to verify**: command and expected result, plus what was already run.
6. **Not done**: assumptions and open questions.

## Payload notation

Keys are never duplicated; alternatives go in the value: `/` = alternative values; `[...]` = the field is a list; `<...>` = computed value.
```
"some_final_json_we_built": {
    "payload": "<some_computed_value>/N/A",
    "color": "RED/GREEN/N/A",
    "tags": ["<tag>", ...]
}
```

## Docstrings

A docstring is one short sentence on what the function does: the action and its result.

- Not included: parameters and types from the signature, exceptions, edge cases, implementation steps, history.
- No docstring when the name already says everything (`is_expired()`, getters).
- A change of behavior or signature updates the docstring in the same edit.

```python
def export_all_orders_to_csv(path: Path, *, since: date) -> int:
    """Write every order created on or after `since` to a CSV file and return the row count."""

def find_session(session_id: str) -> Session:
    """Load an active session from the cache, falling back to the database."""

def charge_order(order: Order, *, gateway: PaymentGateway) -> Receipt:
    """Charge the order total."""
```
```rust
/// Merges duplicate alerts from the same source into one, keeping the earliest timestamp.
pub fn deduplicate_alerts(alerts: Vec<Alert>) -> Vec<Alert>
```

## Repo docs

| What | Where |
|---|---|
| Install, run, configure, operate, architecture overview | `README.md`, `docs/` |
| Behavior contract (if the repo uses OpenSpec) | `openspec/specs/` |
| Context across repos, decisions, history | second-brain (skill `second-brain`) |

Docs follow rule `writing`. A change of install, run, config or architecture updates the docs in the same change.
