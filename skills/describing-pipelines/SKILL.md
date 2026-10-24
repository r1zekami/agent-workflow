---
name: describing-pipelines
description: Use when documenting a pipeline or data flow - a regular process that moves data between systems - in second-brain, repo docs or a code report. Holds the note layout, the flow diagram and the payload notation.
---

# Describing pipelines

A pipeline is a regular process with a data flow: data is taken from a source, transformed, and delivered somewhere. A work pipeline is an entity in second-brain: `work/pipelines/<slug>/` (skill `second-brain`), created from the template `templates/pipeline-readme.md`.

## README sections

| Section | Content |
|---|---|
| What it does | One or two sentences: the result and who consumes it |
| Data flow | Text diagram, below |
| Payload | Every payload the pipeline builds, in the notation below |
| Current state | Rewritten as things change: schedule, status, known issues |
| Open | Open questions and planned work |
| Links | Repo, `[[decisions]]`, related services (`services:` in frontmatter) |

## Data flow diagram

One line per hop, from source to destination; each hop names the system, the step and the format:
```
<source system> (<format>)
  -> <step: what is done> (<format>)
  -> <destination system> (<format>)
```
Branches are indented under the step they leave. Schedules and triggers go on the first line. A diagram with more than about ten hops, or with several branches that join again, goes to an Obsidian canvas (skill `obsidian-canvas`) and the README links it.

## Payload notation

Shown whole, with every possible field. Keys are never duplicated; alternatives go in the value: `/` = alternative values; `[...]` = the field is a list; `<...>` = computed value.
```
"order_export": {
    "order_id": "<int>",
    "status": "NEW/PAID/CANCELLED",
    "items": [{"sku": "<str>", "qty": "<int>"}, ...]
}
```
Example values are made up (no real hosts, ids or people).

## Style

Text follows rule `writing`. Names of systems, tables, fields and queues are in backticks. No real host names, IPs or credentials anywhere in the note.
