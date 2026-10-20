---
name: code-design
description: Use before writing, changing or designing code - interfaces, modules, families of variants, naming, imports, comments. Holds the user's design rules and the interface approval gate.
---

# Code design

Code follows object-oriented, policy-based design (C++ style) in any language.
Code is judged first by its call site: working code with a bad interface is not
done. Rules are language-agnostic.

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
Anything that is one of a kind that could plausibly get siblings (a check, a
transport, a format, a mode, a data source) gets a family contract and a
registry from the first implementation, even with one member. Adding the next
member is "new module + one registry line", never a refactor. A plain function
is only for genuinely one-off logic.

## 2. A family shares one contract

- Members are interchangeable: identical signatures.
- Options are keyword-only (or the language's equivalent).
- The contract includes the data generic code needs (e.g. a hash's block size).
- Generic code never checks which implementation it got; if it has to, extend
  the contract instead of adding an `if name == ...` branch.

## 3. Name hierarchy = file hierarchy

`something.from_something.from_another.hello()` beats
`something_from_something_from_another_hello()`. The same prefix on several
functions (`report_read_x`, `report_write_y`) is a missing namespace level.

## 4. Module boundaries by responsibility

- `utils` holds pure functions without I/O only. DB code goes to `db`,
  external-system clients to `clients`/`connectors`, settings to `config`.
- A client is transport to ONE system and speaks only that system's terms.
- Mapping data between formats of different systems belongs to the consumer.
- Dependencies are one-way: a lower layer never imports a higher one.

## 5. Names and imports

- A long clear name beats a short cryptic one.
- The scope of an operation is visible from the name:
  `export_all_orders_to_csv()` vs `find_order_by_id(order_id)`.
- Import by full path, no aliases, where the language allows it.

## 6. Interface first: approval gate

For everything visible from another module (new modules, classes, functions,
methods called outside their own file), show the user and wait for OK before
implementing:
1. file/module layout;
2. every such signature, in this form, with a blank line after each one:
   ```
   # one-liner: what it does, where it takes from, where it gives to
   package.module.Class.method(type, type, *, option: type) -> type
   ```
3. a call-site example from the consumer's side;
4. if the result is a payload, the full payload (format: skill `code-docs`).

Changing an approved signature needs the same approval. Private helpers inside
one file are not gated but follow rules 1-5.

## Style

- Comments only for a non-obvious why; no comment that narrates what.
- No emoji in code, comments or logs; no decorative banners (`# ===== X =====`).
- Docstrings: one line on the non-obvious why; never retell the signature.
- Log output: English, ASCII only.

## Linters and formatters

Run the project's own linters, formatters and type checkers on changed files
and fix findings in the same turn. The project's configuration wins. No tool in
the project: say so in the report and suggest one.
