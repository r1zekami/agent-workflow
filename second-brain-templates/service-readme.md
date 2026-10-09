---
tags: [scope/work, domain/]
status: active
---

# {{title}}

## What it is

## Instances and access

<!-- no secrets: only where they live (the path in the secrets manager) -->

## API and transport

## Known bugs

<!-- problems of the system or its data: where the right value is and what was decided -->

## Used by

```dataview
TABLE status, file.folder AS "Where"
FROM "work/pipelines" OR "work/projects"
WHERE contains(services, regexreplace(this.file.folder, "^.*/", "")) AND file.name = "README"
```
