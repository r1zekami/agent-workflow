# Code design

Code follows object-oriented, policy-based design in any language. Code is judged first by its call site: working code with a bad interface is not done. Rules are language-agnostic.

## Simplicity first: KISS and YAGNI

Simple means understandable; understandable means easy to debug.

**KISS: plain code, never clever code.**
```
clever: let user = sessions.iter().filter_map(|s| s.ok()).find(|s| s.id == id && !s.expired(now)).map(|s| s.user).ok_or(Error::NotFound)?;
plain:  let session = find_session(id)?;
        if session.is_expired(now) { return Err(Error::Expired); }
        Ok(session.user)
```
- Early returns instead of nesting; one step per line; no tricks to save lines.
- One way to do each thing in a codebase.
- No checks for states the types already rule out.
- The standard library before a new dependency.

**Self-documenting code: no comments.**
Code is written so that reading it is enough to understand what it does. Names, small functions and explicit types carry the meaning, not comments. When a comment seems needed, rename, extract a function or introduce a named value instead.
```
commented:  # skip orders older than 30 days that are not paid
            if o.st != 2 and (now - o.ts).days > 30: continue
readable:   if order.is_unpaid() and order.age_in_days(now) > MAX_UNPAID_ORDER_AGE_DAYS:
                continue
```
The only exception is a fact the code cannot express: a workaround for a bug in an external system, or a constraint imposed from outside. Such a comment names the source.

**YAGNI: build the axis, never the speculative members.**
```
stays:    trait PasswordHasher { ... }     registry: [Argon2id]
YAGNI:    struct Bcrypt;                                    // "for later", no caller
          HasherOptions { pepper: Option<..>, legacy: bool } // nobody sets them
          fn load_hasher_from_config(name)                   // only one hasher exists
```
- A registry holds only members that exist.
- An option, parameter, enum variant or hook appears together with its first caller.
- Designs and specs state contracts and invariants, not the code of every call site.

## 1. A variant is a parameter, never part of a name

```
wrong:  elgamal_sha256_sign(msg, key), rsa_sha512_sign(msg, key)   # N x M functions
right:  sign_message(msg, key, algorithm=Elgamal, hash=Sha256)     # new variant = new class
```
Design the axis up front. Anything that is one of a kind that could plausibly get siblings (a check, a transport, a format, a mode, a data source) gets a family contract and a registry from the first implementation, even with one member. Adding the next member is "new module + one registry line", never a refactor. A plain function is only for genuinely one-off logic.

## 2. A family shares one contract

- Members are interchangeable: identical signatures.
- Options are keyword-only (or the language's equivalent).
- The contract includes the data generic code needs (e.g. a hash's block size).
- Generic code never checks which implementation it got; if it has to, extend the contract instead of adding an `if name == ...` branch.

## 3. Name hierarchy = file hierarchy

`something.from_something.from_another.hello()` beats `something_from_something_from_another_hello()`. Every segment is its own module or class; anything new for `from_another` goes into its file. The same prefix on several functions (`report_read_x`, `report_write_y`) is a missing namespace level.

## 4. Module boundaries by responsibility

- `utils` holds pure functions without I/O only. DB code goes to `db`, external-system clients to `clients`/`connectors`, settings to `config`.
- A client is transport to ONE system and speaks only that system's terms.
- Mapping data between formats of different systems belongs to the consumer.
- Dependencies are one-way: a lower layer never imports a higher one.

## 5. Names and imports

- A long clear name beats a short cryptic one.
- The scope of an operation is visible from the name: `export_all_orders_to_csv()` vs `find_order_by_id(order_id)`.
- Import by full path, no aliases, where the language allows it.

## Language in code

Strictly English: identifiers, comments, docstrings, log messages, error and exception messages, commit messages, TODOs. Log output is also ASCII only. Another language appears only inside string literals that are part of the program's data or logic: user-facing UI text, localized messages, parsing patterns, test data. Such a string never carries a comment in that language.

## Style

- No comments, except the external facts named under Self-documenting code.
- No emoji in code, comments or logs; no decorative banners (`# ===== X =====`).

## Docstrings

A docstring is one short sentence on what the function does: the action and its result.

- Not included: parameters and types from the signature, exceptions, edge cases, implementation steps, history.
- No docstring when the name already says everything (`is_expired()`, getters).
- A change of behavior or signature updates the docstring in the same edit.
- The same sentence is the signature comment in the negotiation proposal (rule `code-negotiation`).

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

## Linters and formatters

Run the project's own linters, formatters and type checkers on changed files and fix findings in the same turn. The project's configuration wins. No tool in the project: say so in the report and suggest one.
