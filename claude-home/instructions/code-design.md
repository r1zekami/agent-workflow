## Code design: extensible interfaces — REQUIRED

Scope: applies to the Medium, Hard and Autonomous approaches. The Easy approach
skips this file entirely (see workflow.md).

Code follows object-oriented, policy-based design (C++ style) in any language.
Code is judged first by its call site: working code
with a bad interface is not done. These rules are language-agnostic. Examples from
the user's own projects live in the second-brain note
`knowledge-base/code-style-examples.md` (once it exists) — read it before
designing any new interface.

### Simplicity — KISS and YAGNI, above every rule below
Simple means understandable; understandable means easy to debug; easy to debug
means fewer bugs. The rules below give code its *structure*; Simplicity keeps
everything inside that structure minimal.

**KISS — plain code, never clever code.**
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

**YAGNI — build the axis, never the speculative members.**
A family contract and a registry for something that will plausibly get siblings
(rule 1) is structure — it stays. What YAGNI forbids is code nobody calls yet:
```
stays:    trait PasswordHasher { ... }     registry: [Argon2id]
YAGNI:    struct Bcrypt;                                    // "for later", no caller
          HasherOptions { pepper: Option<..>, legacy: bool } // nobody sets them
          fn load_hasher_from_config(name)                   // only one hasher exists
          enum Verb { ..., Execute }                         // used nowhere
```
- A registry holds only members that exist.
- An option, parameter, enum variant or hook appears together with its first caller.

**Designs and specs too.** A design states contracts and invariants — signatures,
data, failure modes — not the code of every call site. Code belongs to
implementation, where it compiles and is tested.

### 1. A variant is a parameter, never part of a name
About to write a second function whose name encodes a variant — stop: the varying
part is an axis, and an axis is a parameter.
```
wrong:  elgamal_sha256_sign(msg, key), rsa_sha512_sign(msg, key)   # N x M functions
right:  sign_message(msg, key, algorithm=Elgamal, hash=Sha256)     # new variant = new class
```
Design the axis up front. As soon as something is one of a kind that could plausibly get
siblings (a check, a transport, a format, a mode, a data source), give it a family
contract and a registry from the very first implementation — even with one member.
The registry holds only members that exist (Simplicity).
Adding the next member must be "new module + one registry line", never a refactor.
A plain function is only for genuinely one-off logic (a helper, a formula).

### 2. A family shares one contract
- Family members are interchangeable: identical signatures. Changing a variant means
  changing its body; the signature stays.
- Options are keyword-only (or the language's equivalent), so a new option never
  breaks existing callers.
- The contract includes the data the generic code needs (e.g. a hash's block size),
  not only methods.
- If generic code has to check which implementation it received, the contract is
  incomplete. Extend the contract; never add an `if name == ...` branch.

### 3. Name hierarchy = file hierarchy
`something.from_something.from_another.hello()` beats
`something_from_something_from_another_hello()`. Every segment is its own module or
class; anything new for `from_another` goes into its file. The same prefix on several
functions (`report_read_x`, `report_write_y`) is a missing namespace level.

### 4. Module boundaries by responsibility
- `utils` = pure functions without I/O only. DB goes to `db`, external-system
  clients to `clients`/`connectors`, settings to `config`.
- A client is transport to ONE system and speaks only that system's terms.
- Mapping data between formats of different systems belongs to the consumer.
- One-way dependencies: a lower layer never imports a higher one.

### 5. Names and imports
- A long clear name beats a short cryptic one.
- The scope of an operation is visible from the name itself, without knowing a
  convention: `export_all_orders_to_csv()` vs `find_order_by_id(order_id)`.
- Import by full path, no aliases, where the language allows it.

### 6. Interface first — a hard gate
For everything visible after the dot from another module (new modules, classes,
functions, methods called outside their own file, including internal calls between
modules of the same project), show the user and wait for OK before implementing:
1. file/module layout;
2. every such signature, strictly in this form, with a blank line after each one:
   ```
   # one-liner: what it does, where it takes from, where it gives to
   package.module.Class.method(type, type, *, option: type) -> type

   # next one-liner
   package.module.other(type) -> type
   ```
3. a call-site example from the consumer's side;
4. if the result is a payload — the full payload (format: rule 7).

Changing an approved signature needs the same approval. Private helpers inside one
file (`_name`) are not gated, but still follow rules 1–5.

### 7. Final report on code work — fixed template
After any work on code, the final report has these sections, in this order. A
section with nothing to say is omitted, never filled with "n/a".
1. **What changed** — per file, one line each: what and why.
2. **Signatures** — new and changed ones, in the rule 6 format.
3. **Pipeline** — a text diagram: from where → through what → to where.
4. **Payload** — if the pipeline builds one, shown whole with every possible field.
   Keys are never duplicated; alternatives go in the value:
   `/` = alternative values; `[...]` = the field really is a list; `<...>` = computed value.
   ```
   "some_final_json_we_built": {
       "payload": "<some_computed_value>/N/A",
       "color": "RED/GREEN/N/A",
       "tags": ["<tag>", ...]
   }
   ```
5. **How to verify** — command and expected result, plus what was already run.
6. **Not done** — assumptions and open questions.

### 8. Docstrings
One line on the non-obvious *why*; never retell the signature. A signature change
updates its docstring in the same edit.

### Linters and formatters
Part of Verify, not optional: run the project's own linters, formatters and
type checkers on the changed files and fix the findings in the same turn —
inside WSL for WSL toolchains (environment.md).
The project's configuration always wins. No configuration and no tool in the
project → say so in the report and suggest one; don't silently skip.
