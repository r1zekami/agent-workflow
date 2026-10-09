## second-brain: the user's knowledge base

Naming: always **second-brain**, never "vault". "Vault" means HashiCorp Vault only.

Markdown files at `~/home/agents/second-brain`: a local git repo with **no remote,
ever**. Obsidian is the user's viewer and editor. Both the user and agents write
here, so keep it readable for a human first. Read and write it directly with the
file tools (it is in `permissions.additionalDirectories`; no MCP, no running
Obsidian needed). This section is the authority for its structure and rules.

One vault serves two kinds of work, split by **scope** (`work` / `personal`):

| Scope | What it holds |
|---|---|
| `work` | Job: external systems, pipelines, projects, regulations |
| `personal` | Own life: personal projects, research |

### Structure

```
second-brain/
├── CLAUDE.md             ← pointer to this file
├── README.md             ← the map, for the user
├── work/
│   ├── README.md         ← the scope map
│   ├── domain-tags.md        ← registry: every domain tag, one line of meaning
│   ├── scratchpad/       ← raw notes, prompts, ideas, unstructured
│   ├── services/<slug>/  ← external systems, one per vault
│   ├── pipelines/<slug>/ ← regular processes with a data flow
│   ├── projects/<slug>/  ← one-off work with a result
│   ├── knowledge-base/   ← articles, regulations, guides
│   ├── dashboards/       ← Dataview pages and generated summaries
│   ├── attachments/      ← originals: swagger, pdf, old DAGs
│   └── archive/          ← finished work, moved whole, never deleted
├── personal/
│   ├── README.md         ← the scope map
│   ├── domain-tags.md        ← registry: every domain tag, one line of meaning
│   ├── scratchpad/       ← raw notes, prompts, ideas, unstructured
│   ├── projects/<slug>/  ← anything with a goal and an end
│   ├── knowledge-base/   ← the user's own research articles
│   └── archive/          ← finished projects, moved whole, never deleted
├── agents-data/
│   ├── <agent>/          ← subagent output, one file per topic
│   └── session-log/      ← one note per agent task, month folders + dashboard.md
└── templates/            ← note templates (source: claude-code-setup repo)
```

- There are no `modules/`, `epics/` or `areas/` folders. A reusable thing is a
  project (its README is the context, `repo:` points at the code); an epic or an
  area is a `domain/` tag.
- `archive/` and `scratchpad/` exist once per scope, never at the vault root.
- `scratchpad/` is the user's free space: unstructured notes, prompts, ideas. Agents
  read it only when asked and never reorganize it unasked.
- Each scope keeps its full skeleton from the start (empty folders hold a
  `.gitkeep`). A scope does not mirror the other scope's folders (`services/`,
  `pipelines/`, `dashboards/` and `attachments/` are work-only).
- A service, pipeline or project is an entity folder with one skeleton:

```
<slug>/
├── README.md             ← CURRENT state: rewrite it as things change
├── decisions.md          ← append-only, never edit past entries
└── log/
    └── YYYY-MM-DD-<slug>.md   ← one file per work session / milestone
```

Knowledge-base articles and agents-data reports are single files.

### Reading directives: segmentation by scope

The vault is read in slices, never as a whole. These rules apply to every read
(Read, Glob, Grep, Obsidian search) in every approach.

1. **Resolve the scope first.** In order: the user's tag (`[work]`, `[personal]`)
   -> the entity whose `repo:` matches the working directory -> the user's words.
   Still unclear -> ask once; never guess, never read both "to be safe".
2. **Read only `<scope>/`.** The other scope does not exist for the
   session. Scope the tool call itself (`path: second-brain/work`); a tag search
   (`#domain/...`) always carries the same path filter. Never run a vault-wide
   Grep, Glob or tag search.
3. **Top-down, cheapest first.** vault `README.md` -> `<scope>/README.md` ->
   `<scope>/domain-tags.md` (pick the domain) -> Grep `tags:` for that domain on the
   scope path -> entity `README.md` -> note bodies, only those the task needs.
   `log/` and `decisions.md` are read on demand, `scratchpad/` and `archive/` only
   when asked.
4. **Cross-scope reads need an explicit request** from the user for that
   specific question. The request covers that question, not the session.
5. **No links across scopes.** `work` and `personal` notes link only within
   their own scope. Something needed on both sides is a separate note in each
   scope, never a link or a shared copy.
6. **Writes follow the same slice.** A note goes into the session's scope.
   Unsure about the scope -> ask the user; never park a note outside a scope.
7. **Agent output carries the scope too.** Session-log entries and agents-data
   reports get the `scope/` tag of the session's scope.

### Where things go

| It is... | Goes to |
|---|---|
| Unsure where it belongs, a quick idea, a prompt | `<scope>/scratchpad/<slug>.md` |
| A work external system | `work/services/<slug>/` |
| A work regular process with a data flow | `work/pipelines/<slug>/` |
| A goal with an end, or a reusable piece with its own context | `<scope>/projects/<slug>/` |
| A research article, regulation, guide | `<scope>/knowledge-base/<slug>.md` |
| A subagent's output (e.g. `architecture-designer`) | `agents-data/<agent>/<topic>.md` |
| A record of agent work | `agents-data/session-log/<YYYY-MM>/<entry>.md` |
| Finished work | move the whole folder to `<scope>/archive/` |

Before creating anything, search the scope for an existing note (Glob by path,
Grep by title and tags) and extend it instead of creating a near-duplicate.

### Tags

Obsidian-native, lowercase kebab-case, nested with `/`:
- `scope/<work|personal>`: on every note, equal to its top-level folder.
  A mismatch is a bug: fix the note, not the folder.
- `domain/<domain>[/<subject>]`: the field of work or life a note belongs to:
  an epic (`domain/inventory`), a life zone (`domain/health`), or a finer
  subject (`domain/security/tls`). One level by default; the second level only
  when a domain has too many notes to scan by one tag. A note may have several.
- `agent/<agent-name>`: on agents-data reports.

Each scope's `domain-tags.md` lists its domain tags with one line of meaning; a new
domain tag is added there in the same edit. No folders by domain, tags serve that
purpose. Read `domain-tags.md` before inventing a tag.

### Frontmatter

Every note starts with `tags:` holding its `scope/` tag first.

| Type | Keys |
|---|---|
| service | `tags: [scope/…, domain/…]`, `status: active / deprecated` |
| pipeline | `tags: […]`, `status: active / paused / done`, `repo: <path or none>` |
| project | `tags: […]`, `status: idea / active / paused / done`, `repo: <path or none>` |
| knowledge-base | `tags: […]`, `status: draft / done` |
| agents-data | `tags: [scope/…, agent/<name>, domain/…]` |

### Naming and language (language.md)

- Structure is English kebab-case: folder and file names, tags, frontmatter keys
  and values, template headings. Knowledge-base articles go from general to
  specific, versions keep their dots: `tls-ssl-1.3-1.2.md`.
- All note content is English too. A note in another language exists only when
  the user explicitly asks for that note.
- A date prefix appears only in `log/` file names; decision entries carry their
  date in the heading.

### Update rules

- `README.md`: always the current state; rewrite outdated parts.
- `log/`: add a new file; never rewrite old ones.
- `decisions.md`: append at the bottom; never edit or delete old entries. A
  reversed decision is a new entry that references the old one.
- `knowledge-base/`: **the content belongs to the user.** Add frontmatter, tags
  and `[[links]]`, suggest renames and splits, never rewrite the content unasked.
- `agents-data/<agent>/`: one file per topic; a repeated study updates it (git
  keeps the previous version).

### Session log

One note per entry, so Dataview and Charts can query it:
`agents-data/session-log/<YYYY-MM>/<YYYY-MM-DD-HHMM>-<slug>.md`, slug = the
first words of the description, kebab-case. `dashboard.md` next to the month
folders shows the table (newest first) and the charts.

```markdown
---
tags: [agent/session-log, scope/work]   # or scope/personal
timestamp: YYYY-MM-DDTHH:MM
approach: easy / medium / hard / autonomous
effort: low / medium / high / xhigh / max / unknown
target: [<repo or tool name>, "[[note]]"]
status: done / partial / blocked / not-verified / abandoned
---
<one line, English, generic: what was done>
```

- One entry per task that changed something or produced an artifact; pure
  questions and answers are not logged. An Autonomous run is one entry.
- Entries are never edited afterwards.
- **timestamp**: local time at the end of the task, from the system clock
  (never guessed). **effort**: the session's reasoning effort if known.
  **target**: wikilinks are quoted inside the list.
- No secrets, no infrastructure specifics.

### Links

- Between notes: `[[wikilinks]]`, within the scope (directive 5).
  To code: the `repo:` path.
- Specs (`openspec/specs/`) and docs (`docs/`, `README.md`) stay in the code repo.
  Link to them, never copy them here.
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
| Rules: how to work | the global `CLAUDE.md` and its imported files, or a project `CLAUDE.md` |
| Knowledge: projects, decisions, history, research | second-brain |
| Behavior specs and code docs | the code repo (`openspec/specs/`, `docs/`, `README.md`), linked from second-brain |
| Tasks | beads in the repo |
| A short repo fact needed from the first minute | `bd remember` |

Claude's own auto-memory is disabled (`autoMemoryEnabled: false`). Never create
memory files; put the fact in one of the places above.
