## Context7: current library documentation

Context7 is an MCP server (`resolve-library-id`, `query-docs`) that returns
up-to-date, version-specific docs and code examples. Training data may not
reflect recent changes, so Context7 is the source of truth for library APIs.

### When: depends on the approach (workflow.md)

- **Medium, Hard, Autonomous**: use it whenever the user asks about a library,
  framework, SDK, API, CLI tool, or cloud service, and before writing code
  against one, even well-known ones (React, Django, Prisma, ...) and even when
  the answer seems known. This covers API syntax, configuration, version
  migration, library-specific debugging, setup instructions, and CLI usage.
- **Easy**: only for unfamiliar or version-sensitive APIs: a niche library,
  anything that changed across major versions (Pydantic v1 to v2,
  SQLAlchemy 1.x to 2.0, ...), anything newer than the training data. Stable,
  familiar APIs are written from memory.
- **Never for**: refactoring, writing scripts from scratch, debugging business
  logic, code review, or general programming concepts.
- Prefer Context7 over web search for library docs.

### How

1. Start with `resolve-library-id`: the library name plus what to look up,
   unless the user gave an exact ID in `/org/project` format.
2. Pick the best match (`/org/project`) by: exact name match, description
   relevance, code snippet count, source reputation (High/Medium preferred),
   benchmark score (higher is better). If results look wrong, try alternate
   names or rephrase ("next.js", not "nextjs"). Use a version-specific ID when
   a version is known from the user or from the project's pinned dependencies.
3. `query-docs` with that ID and a specific question (not single words), scoped
   to ONE concept. Several distinct concepts (routing and auth and caching) get
   a separate `query-docs` call per concept with the same ID, unless the
   question is about how they interact: combined queries return shallow results.
4. Answer or write the code from the fetched docs.

### Privacy

Queries leave the machine. Never put secrets, internal host or domain names,
logins, IPs, or proprietary code into a query. Describe the API need
generically (sensitive-data.md applies).
