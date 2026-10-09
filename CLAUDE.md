# Working on this repo

This repo is the public, versioned snapshot of the live Claude Code config in
`~/.claude`, plus everything needed to restore it on a clean machine.

- **`~/.claude` is the source of truth.** After changing anything there, sync it
  here and review the diff:
  `pwsh -NoProfile -File .\sync-claude-config.ps1 -Direction ToRepo`, then `git diff`.
- Never edit `claude-home/` by hand: edit `~/.claude` and sync. Only when the user
  asks to change the repo first: edit here, then sync `-Direction ToClaude`.
- **Restoring on a new machine**: follow `RESTORE.md` step by step.
- **`services/`**: templates for local services (e.g. `services/litellm/`). The
  repo copy is the source of truth; the running copy is located in WSL
  `~/services/<name>/` together with its `.env`, which only the user writes.
  After a template change: copy it over, restart the service, verify it.
- **The repo is public.** Nothing personal ever goes in: no user names (paths use
  `~` or the `{{HOME}}` placeholder), no e-mail addresses, host names, IPs,
  tokens, and no knowledge-base content. Run the `leak-auditor` subagent on the
  staged diff before every commit.
- Everything in this repo is English.
