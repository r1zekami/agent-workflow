## Language: HARD RULE, every approach

| Where | Language |
|---|---|
| Chat with the user | English, always, even when the user writes in another language (Cyrillic costs about 2-3x the tokens) |
| Code projects (everything: identifiers, comments, docstrings, log / print / error text, docs, OpenSpec specs, commit messages, beads issues and notes, PR texts) | English only |
| Instruction files (every `CLAUDE.md`, `instructions/*.md`, `agents/*.md`, skills) | English only, no other language, not even when quoting or referring to something |
| second-brain (everything: note content, structure such as folder and file names, tags, frontmatter, and `agents-data/`) | English; structure in kebab-case so it never drifts. Another language only for a note the user explicitly asks for |

- Applies in every approach, Easy included.
- Anything that goes to a remote repository is English, without exception.
- **Translation**: only on the user's explicit request, and only as a copy derived
  from the English original. Never write project text natively in another language,
  never translate without being asked. The English text stays the source of truth.
- **Log output**: English and ASCII only. Non-ASCII breaks Windows consoles
  (legacy ANSI code pages vs UTF-8, mojibake) regardless of the terminal's locale.
