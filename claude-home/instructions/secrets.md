## Secrets: HARD RULE

A secret is any credential: API keys, tokens, passwords, private keys, session
cookies, connection strings that contain credentials.

### How secrets reach a program

Only through mechanisms the user controls, never through the agent:
- the project's `.env`, loaded by the program itself (two allowed shapes below);
- environment variables the user sets in their own shell or OS;
- the OS credential store (e.g. Windows Credential Manager via Python `keyring`)
  or a secrets manager the user runs.

Code reads a secret **by name at runtime** and fails with a clear English error
naming the missing variable. Tell the user which name to set; never ask them to
paste a secret into the chat.

### Prohibited

- reading secrets out of configs (`.env`, editor settings, `~/.*rc`, shell
  history, credential stores), even "just to look", even to reproduce a bug;
- substituting a secret into a command: `export API_KEY=...`,
  `-H "Authorization: ..."`, `VAR=... cmd`;
- printing the environment (`env`, `printenv`, `echo $KEY`, `Get-ChildItem env:`)
  or enabling debug modes that dump it;
- writing a secret to a file, a log, a beads issue, a spec or a second-brain note;
- surfacing a secret into the chat or the agent's reasoning by any other means.
  This includes a secret that shows up incidentally in a tool result (an
  `Authorization` header in network output, a key echoed in stderr): do not quote
  it, do not repeat it, treat it as if the agent had typed it.

**Allowed to set explicitly**: non-secret config only (`*_BASE_URL`, `*_MODEL`,
`NO_PROXY`, …). The principle is "config, not credentials".

**If a secret leaks anyway**: tell the user immediately and help rotate it.
Never cover it up.

### `.env`: the hard gate

- The agent never creates, edits, reads or otherwise touches `.env`,
  unconditionally, whoever put values into it.
- `.env.example` is maintained by the agent: a map of variable **names**, with a
  comment on where each real value comes from. If the user asks and the agent
  knows values for a **local sandbox** (below), fill those in and say so.

Two acceptable shapes for a project's `.env`; do not invent a third:

- **(b) Plain `.env`**: every value lives directly in `.env`, copied from
  `.env.example`.
- **(a) `.env` + an external secrets manager**: `.env` holds the local-sandbox
  values plus the address and token of the secrets manager where real values
  live; the program pulls real values on demand. Switching between "local sandbox"
  and "real secrets" depends on which source is used, not on two different files.
  The address and token are filled in by the user by hand, so the real values
  never pass through the agent.

Never hardcode a secret anywhere else, in any form.

### Local-sandbox exception

These prohibitions do **not** apply to secrets that exist **only in a local
sandbox**: a local dev/test setup with no real-world stakes (a throwaway local
DB password, a dev-mode token used solely for that sandbox). Those can be read,
printed and written as the task needs. When it is unclear whether a secret is
local-only or real, ask instead of guessing. A narrower, explicit rule for a
particular secret always wins over this exception.

Infrastructure details that are not secrets but still sensitive (host names,
logins, IPs, structure) are covered by sensitive-data.md.
