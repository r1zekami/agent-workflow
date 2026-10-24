# Documenting code

All documentation follows rule `writing`. A change of install, deployment, configuration, architecture or behavior updates the affected docs in the same change.

## Final report after code work

Sections in this order. A section with nothing to say is omitted, never filled with "n/a". A list of changed files is never part of the report: changes per release go to the release notes.

1. **Signatures**: new and changed ones, in the format of rule `code-negotiation`.
2. **Pipeline**: a text diagram: from where, through what, to where.
3. **Payload**: if the pipeline builds one, shown whole in the notation of rule `code-negotiation`.
4. **How to verify**: command and expected result, plus what was already run.
5. **Not done**: assumptions and open questions.

## Root README.md

The root README is short: what the project is, and links to everything else. Sections in this order; a section with nothing real to say is omitted.

1. **Title and description**: the project name as the heading, then one or two sentences on what the project is. A distinction from a similar known project goes here when confusion is likely.
2. **Features**: a short list of what the project does that is notable or unique. Omitted when there is nothing notable.
3. **Installation** or **Deployment** (whichever fits the product): a quick start of a few lines (the shortest path to a working result: one command or one call), then links to the guides in `docs/`.
4. **Documentation**: links only: `docs/README.md` first, then the main documents.
5. **License**: one line with the license name and a link to `LICENSE`.

Example:
```markdown
# SCAMP

SCAMP is an extremely simplified, declarative agent management protocol, inspired by OpAMP. It is NOT an OpAMP implementation.

## Features

- One declarative document describes the desired state of every agent.
- ...

## Deployment

Run the server with Docker:

    docker run -p 8080:8080 example/scamp-server

- [Deploy with Docker](docs/deployment/deploy-in-docker.md)
- [Deploy in Kubernetes](docs/deployment/deploy-in-k8s.md)

## Documentation

- [Documentation index](docs/README.md)
- [Architecture](docs/architecture.md)
- [Protocol](docs/protocol.md)

## License

MIT, see [LICENSE](LICENSE).
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
