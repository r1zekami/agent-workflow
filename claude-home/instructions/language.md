## Language — HARD RULE, every approach

| Where | Language |
|---|---|
| Chat with the user | The user's language — answer in the language they write in |
| Code projects — everything: identifiers, comments, docstrings, log / print / error text, docs, OpenSpec specs, commit messages, beads issues and notes, PR texts | English only |
| Instruction files — every `CLAUDE.md`, `instructions/*.md`, `agents/*.md`, skills | English only — no other language, not even when quoting or referring to something |
| second-brain — content of the user's notes (areas, projects, modules, knowledge-base) | Any language |
| second-brain — structure: folder and file names, tags, frontmatter keys and values | English, kebab-case — so the structure never drifts |
| second-brain — `agents-data/` (reports, session log) | English |

- Applies in every approach, Easy included.
- Anything that goes to a remote repository is English, without exception.
- **Translation** — only on the user's explicit request, and only as a copy derived
  from the English original. Never write project text natively in another language,
  never translate on your own initiative. The English text stays the source of truth.
- **Log output** — English and ASCII only: non-ASCII breaks Windows consoles
  (legacy ANSI code pages vs UTF-8, mojibake) regardless of the terminal's locale.
