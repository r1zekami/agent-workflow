---
name: second-brain
description: Use for anything in the user's knowledge base second-brain (~/home/agents/second-brain) - reading, writing or reorganizing notes, session-log entries, Obsidian setup. Holds the structure, scopes, tags, frontmatter and update rules.
---

# second-brain

Markdown files at `~/home/agents/second-brain`: a local git repo with **no remote, ever**. Obsidian is the user's viewer and editor. Read and write with the file tools. Always called second-brain, never "vault" ("Vault" means HashiCorp Vault).

Two scopes:

| Scope | Holds |
|---|---|
| `work` | Job: external systems, pipelines, projects, regulations |
| `personal` | Own life: personal projects, research |

## Structure

```
second-brain/
├── README.md             the map, for the user
├── work/
│   ├── README.md         scope map
│   ├── domain-tags.md    every domain tag, one line of meaning
│   ├── scratchpad/       raw notes, prompts, ideas
│   ├── services/<slug>/  external systems
│   ├── pipelines/<slug>/ regular processes with a data flow
│   ├── projects/<slug>/  one-off work with a result
│   ├── knowledge-base/   articles, regulations, guides
│   ├── dashboards/       Dataview pages and generated summaries
│   ├── attachments/      originals: swagger, pdf, old DAGs
│   └── archive/          finished work, moved whole, never deleted
├── personal/
│   ├── README.md, domain-tags.md, scratchpad/
│   ├── projects/<slug>/  anything with a goal and an end
│   ├── knowledge-base/   own research articles
│   └── archive/
├── agents-data/
│   ├── <agent>/          agent reports, one file per topic
│   └── session-log/      one note per agent task, month folders + dashboard.md
└── templates/            note templates (source: agent-workflow repo)
```

- No `modules/`, `epics/` or `areas/` folders: a reusable thing is a project, an epic or area is a `domain/` tag.
- `scratchpad/` is the user's free space: read only when asked, never reorganized.
- Each scope keeps its full skeleton (empty folders hold `.gitkeep`).

An entity (service, pipeline, project) folder:
```
<slug>/
├── README.md             CURRENT state: rewrite as things change
├── decisions.md          append-only
└── log/YYYY-MM-DD-<slug>.md   one file per session or milestone
```

## Reading: by scope, top-down

1. **Resolve the scope first**: the user's tag (`[work]`, `[personal]`) -> the entity whose `repo:` matches the working directory -> the user's words. Still unclear: ask once; never read both "to be safe".
2. **Read only `<scope>/`**: scope every Grep, Glob or tag search by path. Never search the whole knowledge base.
3. **Cheapest first**: `README.md` -> `<scope>/README.md` -> `<scope>/domain-tags.md` -> Grep `tags:` for the domain -> entity `README.md` -> only the notes the task needs. `log/` and `decisions.md` on demand; `scratchpad/` and `archive/` only when asked.
4. Cross-scope reads only on an explicit request for that question.
5. No links across scopes. Something needed on both sides is a separate note in each scope.
6. Writes go into the session's scope; unsure: ask.

## Where things go

| It is... | Goes to |
|---|---|
| Unsure, a quick idea, a prompt | `<scope>/scratchpad/<slug>.md` |
| A work external system | `work/services/<slug>/` |
| A work process with a data flow | `work/pipelines/<slug>/` (skill `describing-pipelines`) |
| A goal with an end, or a reusable piece with its own context | `<scope>/projects/<slug>/` |
| A research article, regulation, guide | `<scope>/knowledge-base/<slug>.md` |
| An agent report | `agents-data/<agent>/<topic>.md` |
| A record of agent work | `agents-data/session-log/<YYYY-MM>/<entry>.md` |
| Finished work | the whole folder moves to `<scope>/archive/` |

Search the scope for an existing note before creating one; extend it instead of creating a near-duplicate.

## Tags and frontmatter

Obsidian tags, lowercase kebab-case, nested with `/`:
- `scope/<work|personal>`: on every note, first, equal to its top-level folder.
- `domain/<domain>[/<subject>]`: one level by default. Each scope's `domain-tags.md` lists the tags; a new tag is added there in the same edit.
- `agent/<agent-name>`: on agents-data reports.

| Type | Keys |
|---|---|
| service | `tags`, `status: active / deprecated` |
| pipeline | `tags`, `status: active / paused / done`, `repo: <path or none>` |
| project | `tags`, `status: idea / active / paused / done`, `repo: <path or none>` |
| knowledge-base | `tags`, `status: draft / done` |
| agents-data | `tags: [scope/…, agent/<name>, domain/…]` |

Templates: `templates/` in second-brain, sourced from `agent-workflow/second-brain-templates/`.

## Naming and language

English kebab-case for folders, files, tags and frontmatter. Note content is English and follows rule `writing`. A date prefix appears only in `log/` file names. Knowledge-base names go from general to specific, versions keep dots: `tls-ssl-1.3-1.2.md`.

## Update rules

- `README.md`: always the current state; rewrite outdated parts.
- `log/`: add a new file; never rewrite old ones.
- `decisions.md`: append at the bottom; a reversed decision is a new entry.
- `knowledge-base/`: the content belongs to the user. Add frontmatter, tags and `[[links]]`, suggest changes, never rewrite content unasked.
- `agents-data/<agent>/`: one file per topic; a repeated study updates it.

## Session log

At the end of a task that changed something or produced an artifact, add one note: `agents-data/session-log/<YYYY-MM>/<YYYY-MM-DD-HHMM>-<slug>.md`.

```markdown
---
tags: [agent/session-log, scope/work]   # or scope/personal
timestamp: YYYY-MM-DDTHH:MM
harness: claude-code / opencode
model: <model id>
target: [<repo or tool name>, "[[note]]"]
status: done / partial / blocked / not-verified / abandoned
---
<one line, English, generic: what was done>
```

Timestamp from the system clock, never guessed. Entries are never edited. Pure questions and answers are not logged.

## Links, git, safety

- Between notes: `[[wikilinks]]` within the scope. To code: the `repo:` path. Specs and docs stay in the code repo; link, never copy.
- Commit at the end of a task: `docs(<entity-slug>): <what was done>`; session-log only: `docs(session-log): <what>`.
- Never add a remote, never push. No secrets, no infrastructure specifics, no real people's data.

## Obsidian setup

- CSS snippet hiding `templates/`: `agent-workflow/second-brain-obsidian/hide-templates.css` -> `.obsidian/snippets/`.
- Canvas files: skill `obsidian-canvas`.
