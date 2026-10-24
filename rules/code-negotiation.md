# Code negotiation

Before implementing anything visible from another module (new modules, classes, functions, methods called outside their own file, including calls between modules of the same project), the proposal is shown to the user, and implementation starts only after the user's OK. Private helpers inside one file are not negotiated but follow rule `code-design`. Changing an approved file structure, signature or payload needs the same approval.

## What the proposal contains

Every item is a fenced code block in the chat.

### 1. File structure

The new and changed files as a tree:
```
orders/
├── export/
│   ├── __init__.py
│   ├── csv_exporter.py      new
│   └── registry.py          changed
└── models.py
```

### 2. Signatures

Every public signature, each with a one-line comment above it. The comment is the same text that becomes the function's docstring (rule `code-design`, Docstrings). A blank line follows each signature.
```
# Write every order created on or after `since` to a CSV file and return the row count.
orders.export.csv_exporter.CsvExporter.export_all_orders(path: Path, *, since: date) -> int

# Load an active session from the cache, falling back to the database.
auth.sessions.find_session(session_id: str) -> Session
```

### 3. Call site

A short example of the consumer's code calling the new interface:
```
row_count = CsvExporter().export_all_orders(Path("orders.csv"), since=date(2026, 1, 1))
```

### 4. Payload

When the work builds a payload (an API response, a message, a file record), its full format with every possible field. Keys are never duplicated; alternatives go in the value: `/` = alternative values; `[...]` = the field is a list; `<...>` = computed value.
```
"order_export": {
    "order_id": "<int>",
    "status": "NEW/PAID/CANCELLED",
    "items": [{"sku": "<str>", "qty": "<int>"}, ...],
    "note": "<str>/N/A"
}
```
