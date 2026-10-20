# Working on this repo

This repo is the source of truth for the agent rules of Claude Code and
OpenCode on this machine.

- Edit here, never in `~/.claude` or `~/.config/opencode`. Then run
  `py install.py` and check its output. Skill folders are linked, so skill edits
  apply without re-running.
- `core/AGENTS.md` stays short: only rules that must apply in every session.
  Anything loaded on demand is a skill in `skills/<name>/SKILL.md` (frontmatter
  `name` equal to the folder name, `description` saying when to use it).
- **The repo is public.** Nothing personal ever goes in: no user names (paths
  use `~` or the `{{HOME}}` placeholder), no e-mail addresses, host names, IPs,
  tokens, and no knowledge-base content. The leak audit runs before every push.
- Everything in this repo is English and follows the `writing` skill.
