# Documenting code

All documentation follows rule `writing`. A change of install, deployment, configuration, architecture or behavior updates the affected docs in the same change.

## Root README.md

The root README is short: what the project is, and links to everything else. Sections in this order; a section with nothing real to say is omitted.

1. **Title and description**: the project name as the heading, then one or two sentences on what the project is. A distinction from a similar known project goes here when confusion is likely.
2. **Installation** or **Deployment** (whichever fits the product): a quick start of a few lines (the shortest path to a working result: one command or one call), then links to the guides in `docs/`.
3. **Documentation**: links only: `docs/README.md` first, then the main documents.
4. **License**: one line with the license name and a link to `LICENSE`.

Template:
```markdown
# <Project name>

<One or two sentences: what the project is. Optional: how it differs from a similar known project.>

## Installation

<Quick start: one command or one call that gives a working result.>

- [<Guide title>](docs/installation.md)

## Documentation

- [Documentation index](docs/README.md)
- [Architecture](docs/architecture.md)

## License

<License name>, see [LICENSE](LICENSE).
```

## docs/

Detailed documentation lives in `docs/`; the README only links to it.

| Document | Content | Required |
|---|---|---|
| `docs/README.md` | Index: every document in `docs/` with one line on its content | always |
| `docs/architecture.md` | Stack, components and how they connect | always |
| `docs/components/<component>.md` | One document per component: responsibility, interfaces, configuration | one per component |
| `docs/flows/<flow>.md` | A flow as ordered steps that can be reproduced (for example, one exchange of a protocol); a flow of one component may live in that component's document | when the project has flows worth describing |
| `docs/installation.md` or `docs/deployment.md` | Installation or deployment guide | when the project is installed or deployed |
| `docs/deployment/<variant>.md` | One guide per variant (`deploy-in-docker.md`, `deploy-in-k8s.md`), replacing the single file | when there are several variants |
| `docs/development.md` | Build, run locally, tests, linters and formatters, local environment | always for code projects |
| `docs/api.md` or `docs/protocol.md` | External interface: endpoints or messages, every field in the payload notation of rule `code-negotiation` | when the project has an API or a protocol |
| `docs/glossary.md` | Domain terms with one line of meaning each | when the domain has its own terms |

## OpenSpec

In a repo with `openspec/`, `openspec/specs/` holds the behavior contract and `docs/` explains how the system is built and operated. Docs link to the specs and never restate requirements or scenarios.

## Where else

| What | Where |
|---|---|
| Context across repos, decisions, history | second-brain (skill `second-brain`) |
