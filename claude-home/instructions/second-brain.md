## second-brain — the user's knowledge base

Naming: always **second-brain**, never "vault" — "Vault" means HashiCorp Vault only.

Markdown files at `~/home/agents/second-brain`: a local git repo with **no remote,
ever**. Obsidian is the user's viewer and editor. Both the user and agents write
here — keep it readable for a human first. Read and write it directly with the
file tools (it is in `permissions.additionalDirectories`; no MCP, no running
Obsidian needed). This section is the authority for its structure and rules.

### Structure

```
second-brain/
├── CLAUDE.md             ← pointer to this file
├── README.md             ← the map, for the user
├── inbox/                ← quick capture, unsorted
├── areas/                ← life zones, one file per area; each defines one tag
├── projects/<slug>/      ← anything with a goal and an end
├── modules/<slug>/       ← anything reusable and pluggable: libraries, scripts, configs, templates
├── knowledge-base/       ← the user's own research articles
├── agents-data/
│   ├── <agent>/          ← subagent output, one file per topic
│   └── session-log/      ← one table per month of agent work
├── templates/            ← note templates (source: claude-code-setup repo)
└── archive/              ← finished projects, moved whole, never deleted
```

Projects and modules share one skeleton:

```
<slug>/
├── README.md             ← CURRENT state — rewrite it as things change
├── decisions.md          ← append-only, never edit past entries
└── log/
    └── YYYY-MM-DD-<slug>.md   ← one file per work session / milestone
```

Areas, knowledge-base articles and agents-data reports are single files.

### Where things go

| It is… | Goes to |
|---|---|
| Unsure where it belongs, a quick idea | `inbox/<slug>.md` |
| A zone of life with no end | `areas/<slug>.md` |
| Something with a goal and an end | `projects/<slug>/` |
| Something reusable that plugs into other things | `modules/<slug>/` |
| A pipeline | built as its own goal → project; a piece reused in several places → module |
| The user's research article | `knowledge-base/<slug>.md` |
| A subagent's output (e.g. `architecture-designer`) | `agents-data/<agent>/<topic>.md` |
| A record of agent work | `agents-data/session-log/<YYYY-MM>.md` |
| A finished project | move the whole folder to `archive/` |

Before creating anything, search for an existing note (Glob by path, Grep by
title and tags) and extend it instead of creating a near-duplicate.

### Tags

Lowercase kebab-case, nested with `/`:
- `area/<area-slug>` — on projects, modules and articles; this is how an area
  finds everything related to it. Every area file defines exactly one.
- `topic/<topic>` — on knowledge-base articles and agents-data reports; an
  article may have several.
- `agent/<agent-name>` — on agents-data reports.

No folders by topic — tags do that job. List existing tags first (Grep `tags:`)
before inventing a new one.

### Frontmatter

| Type | Keys |
|---|---|
| area | `tags: [area/<slug>]` |
| project | `tags: [area/…]`, `status: idea / active / paused / done`, `repo: <path or none>` |
| module | `tags: [area/…]`, `status: active / deprecated`, `repo: <path or none>`, `used-in: [[…]]` |
| knowledge-base | `tags: [topic/…, area/…]`, `status: draft / done` |
| agents-data | `tags: [agent/<name>, topic/…]` |

### Naming and language (language.md)

- Structure is English kebab-case: folder and file names, tags, frontmatter keys
  and values, template headings. Knowledge-base articles go from general to
  specific, versions keep their dots: `tls-ssl-1.3-1.2.md`.
- A date prefix appears only in `log/` file names; decision entries carry their
  date in the heading.
- Content of the user's notes: any language. `agents-data/`: English.

### Update rules

- `README.md` — always the current state; rewrite outdated parts.
- `log/` — add a new file; never rewrite old ones.
- `decisions.md` — append at the bottom; never edit or delete old entries. A
  reversed decision is a new entry that references the old one.
- `knowledge-base/` — **the content belongs to the user.** Add frontmatter, tags
  and `[[links]]`, suggest renames and splits — never rewrite the content unasked.
- `agents-data/<agent>/` — one file per topic; a repeated study updates it (git
  keeps the previous version).

### Session log

`agents-data/session-log/<YYYY-MM>.md` — one file per month. Create it with:

```markdown
# Session log — YYYY-MM

| Timestamp | Approach | Description | Targeted projects or systems | Status |
|---|---|---|---|---|
```

- One row per task that changed something or produced an artifact; pure
  questions and answers are not logged. An Autonomous run is one row.
- **Timestamp** — local time at the end of the task, `YYYY-MM-DD HH:MM`, from the
  system clock (never guessed). **Approach** — Easy / Medium / Hard / Autonomous.
  **Description** — one line, English, generic. **Targets** — `[[wikilinks]]` to
  notes, or a repo / tool name. **Status** — `done`, `partial`, `blocked`,
  `not verified`, `abandoned`.
- Rows are appended, never edited. No secrets, no infrastructure specifics.

### Links

- Between notes: `[[wikilinks]]`. To code: the `repo:` path.
- Specs (`openspec/specs/`) and docs (`docs/`, `README.md`) stay in the code repo —
  link to them, never copy them here.
- A beads epic links its note: `bd note <epic-id> "docs: <note path>"`.

### Git and safety

- Commit at the end of a task: `docs(<entity-slug>): <what was done>`. Session-log
  rows go into the task's commit; when they are the only change, at most one
  `docs(session-log): <what>` commit per session.
- Never add a remote, never push.
- No secrets, no infrastructure specifics, no real people's data
  (secrets.md, sensitive-data.md).

### Memory layers

| What | Where |
|---|---|
| Rules — how to work | the global `CLAUDE.md` and its imported files, or a project `CLAUDE.md` |
| Knowledge — projects, modules, decisions, history, research | second-brain |
| Behavior specs and code docs | the code repo (`openspec/specs/`, `docs/`, `README.md`) — linked from second-brain |
| Tasks | beads in the repo |
| A short repo fact needed from the first minute | `bd remember` |

Claude's own auto-memory is disabled (`autoMemoryEnabled: false`) — never create
memory files; put the fact in one of the places above.
