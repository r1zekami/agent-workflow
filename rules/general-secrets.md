# Secrets: hard rule

A secret is any credential: API keys, tokens, passwords, private keys, session cookies, connection strings that contain credentials.

## How secrets reach a program

Only through mechanisms the user controls, never through the agent:
- the project's `.env`, loaded by the program itself (two allowed shapes below);
- environment variables the user sets in their own shell or OS;
- the OS credential store (for example, Python `keyring`) or a secrets manager the user runs.

Code reads a secret by name at runtime and fails with a clear error naming the missing variable. The user is told which name to set; the user is never asked to paste a secret into the chat.

## Using `.env`

The agent never reads `.env`; the program or the shell loads it. No attempt to "understand" the file, check a value or compare variables.

| Where | How |
|---|---|
| Python | `from dotenv import load_dotenv; load_dotenv()`, then `os.environ["NAME"]` (fails with the name when unset) |
| Node / Bun | `process.env.NAME` (Bun loads `.env` itself; Node: `node --env-file=.env app.js`) |
| Rust | `dotenvy::dotenv()`, then `std::env::var("NAME")` |
| Shell, one command | `set -a; . ./.env; set +a; <command>` (the shell loads it, nothing is printed) |
| Docker Compose | `env_file:` in `compose.yaml`, or `docker compose --env-file .env ...` |

A missing or empty variable: report its name and stop; do not investigate the file.

## `.env`: the hard gate

- The agent never creates, edits, reads or otherwise touches `.env`, whoever put values into it.
- `.env.example` is maintained by the agent: a map of variable names. Directly above each variable, a comment of at most two short lines says what the value is and where it comes from. On request, values of a local sandbox (below) may be filled in, and this is stated.
  ```
  # Token of the payment provider; from the provider's dashboard.
  PAYMENT_API_TOKEN=
  ```

Two acceptable shapes of a project's `.env`; no third one:
- **Plain `.env`**: every value is located directly in `.env`, copied from `.env.example`.
- **`.env` + an external secrets manager**: `.env` holds the local-sandbox values plus the address and token of the secrets manager; the program pulls real values on demand. Switching between sandbox and real secrets depends on the source, not on two different files. The address and token are filled in by the user by hand, so real values never pass through the agent.

A secret is never hardcoded anywhere else, in any form.

## Prohibited

- Reading secrets out of configs (`.env`, editor settings, `~/.*rc`, shell history, credential stores), even "just to look", even to reproduce a bug.
- Substituting a secret into a command: `export API_KEY=...`, `-H "Authorization: ..."`, `VAR=... cmd`.
- Printing the environment (`env`, `printenv`, `set` without arguments, `echo $KEY`, `$env:NAME`, `Get-ChildItem env:`) or enabling debug modes that dump it.
- Commands that print a container's environment: `docker inspect <container>` without `--format`, `docker inspect --format '{{.Config.Env}}'`, `docker exec <container> env`, `docker compose config` (it substitutes `.env` values into the output). Ask for the one non-secret field needed instead:
  ```
  printing Env:  docker inspect web-1
  safe:          docker inspect --format '{{.State.Status}} {{.State.Health.Status}}' web-1
  ```
- Writing a secret to a file, a log, an issue, a spec or a note.
- Surfacing a secret in the chat or in reasoning by any other means. A secret that shows up in a tool result (an `Authorization` header in network output, a key echoed in stderr) is not quoted and not repeated.

Allowed to set explicitly: non-secret config only (`*_BASE_URL`, `*_MODEL`, `NO_PROXY`). The principle is "config, not credentials".

A secret that leaks anyway is reported to the user at once, with help to rotate it. A leak is never covered up.

## Local-sandbox exception

The prohibitions do not apply to secrets that exist only in a local sandbox: a local dev or test setup with no real-world stakes (a throwaway local database password, a dev-mode token used solely there). Those may be read, printed and written as the task needs. When it is unclear whether a secret is local-only or real, ask instead of guessing. A narrower, explicit rule for a particular secret always wins over this exception.

Infrastructure details that are not secrets but still sensitive are covered by rule `general-sensitive-data`.
