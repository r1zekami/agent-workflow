---
name: dependency-check
description: Use before installing or adding any package or dependency - npm/pnpm/yarn/bun add or install, pip/uv/poetry add or install, cargo add or install, go get, gem, nuget, dotnet add package, editing a manifest (package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod) to add a dependency, or choosing a library to depend on.
---

# Dependency check

Every new dependency is checked before the install command runs. The check answers one question: is this package safe to depend on, or is an alternative needed. The global rule still applies: nothing is installed without the user's yes; the verdict goes into that request.

## Scope

| Situation | Check |
|---|---|
| A new package (install, `add`, a new line in a manifest) | Full check, steps 1-4 |
| A version change of an existing dependency | Steps 3 and 4 for the target version |
| Restoring a project from its lockfile (`npm ci`, `pip install -r`, `cargo build`, `uv sync`) | Step 3 for every locked version (OSV batch query below) |

## Input

A package name and a version go into a command only when they match these patterns; anything else is never substituted and is reported to the user as suspicious. Reason: names often come from a README, an issue or a web page, and a `'` or `;` in such a name breaks out of the quoted command.

| Value | Pattern |
|---|---|
| Name | `^[A-Za-z0-9@/._:~+-]+$` |
| Version | `^[A-Za-z0-9.+_~-]+$` |

## Steps

Facts come from the APIs below, never from memory. `<system>` is the deps.dev name (`npm`, `pypi`, `cargo`, `go`, `maven`, `nuget`), `<ecosystem>` is the OSV name (`npm`, `PyPI`, `crates.io`, `Go`, `Maven`, `NuGet`, `RubyGems`). Package names with `/` or `@` are URL-encoded for deps.dev (`@types/node` -> `%40types%2Fnode`).

**1. Creation date.** The earliest `publishedAt` over all versions:
```
curl -s https://api.deps.dev/v3/systems/<system>/packages/<name>
```
Created less than 60 days ago: suspicious. A new package that copies the name of a popular one with a small change (`reqeusts`, `lodash-utils`) is suspicious at any age.

**2. Last release.** The latest `publishedAt` over all versions, from the same response. Not the npm registry `time.modified`: that field changes on any metadata edit. No release for more than 6 months: unmaintained, search for alternatives. A package marked deprecated (`isDeprecated` on the version) counts as unmaintained.

**3. Vulnerabilities.** All known advisories of the package (history) and those affecting the version to install (current):
```
curl -s -X POST https://api.osv.dev/v1/query -d '{"package":{"name":"<name>","ecosystem":"<ecosystem>"}}'
curl -s -X POST https://api.osv.dev/v1/query -d '{"version":"<version>","package":{"name":"<name>","ecosystem":"<ecosystem>"}}'
```
Lockfile: one `POST https://api.osv.dev/v1/querybatch` with `{"queries":[{"version":..,"package":{..}}, ...]}`.

- Any `MAL-` advisory (malicious package record): rejected, no exceptions.
- A current advisory on the version to install: pick a fixed version (`affected[].ranges[].events[].fixed`); no fixed version: rejected.
- History: advisories fixed promptly are normal for a popular package. Repeated serious advisories (critical or high, remote code execution) in the last two years, or advisories that stayed open for months, count against the package.

**4. Transitive dependencies.** The new package pulls in packages of its own, and install scripts of any of them run at install time. Resolve the dependency tree without installing and without running package code, then send every package that is new in the lockfile (diff against the committed lockfile) to the OSV batch query of step 3.

| Manager | Resolve only |
|---|---|
| npm | `npm install <name>@<version> --package-lock-only --ignore-scripts` |
| pnpm | `pnpm add <name>@<version> --lockfile-only --ignore-scripts` |
| Yarn (Berry) | `yarn add <name>@<version> --mode=update-lockfile` |
| Bun | add the line to `package.json`, then `bun install --dry-run` (prints the tree, writes nothing) |
| pip | `pip install --dry-run --ignore-installed --only-binary :all: --quiet --report - <name>==<version>` |
| uv | `uv add <name>==<version> --no-sync --no-build` |
| Poetry | `poetry add <name>@<version> --lock` |
| Cargo | `cargo add <name>@<version>`, then `cargo metadata --format-version 1` (updates `Cargo.lock`, builds nothing) |
| Go | `go get <module>@<version>` (since Go 1.18 it only edits `go.mod` and `go.sum`, builds nothing) |

- `--only-binary :all:` and `--no-build` keep pip and uv from building source distributions, which runs the package's build code. A package with no wheel fails here: report that to the user; a retry without the flag needs the user's yes.
- Any transitive package with a `MAL-` record or a current advisory without a fix rejects the whole install. Transitive packages younger than 60 days are listed in the report as suspicious.
- The resolve step changes the manifest or the lockfile. A rejected package is rolled back: `git checkout -- <manifest> <lockfile>`.

## Verdict

| Verdict | Condition | Action |
|---|---|---|
| OK | Older than 60 days, released within 6 months, no current advisory, no `MAL-` record, clean or normal history, clean transitive tree | Propose the install with the checked version pinned |
| Suspicious | Created recently, unmaintained or deprecated, troubled history, a recent transitive package | Search for alternatives (below) |
| Rejected | `MAL-` record, or a current advisory with no fixed version, in the package or in its transitive tree | Never installed; search for alternatives |

**Alternatives.** Look for packages that solve the same task (registry search, the package's own README, the standard library first). Each candidate goes through steps 1-3. Propose the best candidate that is OK. No candidate is OK: present the options with their findings and let the user decide.

## Report

Before the install, the request to the user contains one line per checked package:
```
<name>@<version> (<ecosystem>): created <YYYY-MM-DD>, last release <YYYY-MM-DD>, advisories: <current count> current / <total> total, MAL: none, transitive: <new count> new / <flagged count> flagged -> OK / suspicious / rejected
```
A rejected or suspicious package also gets the reason and the proposed alternative.

## Common mistakes

- Taking the registry's `modified` or `updated_at` field as the last release date.
- Checking only the latest version when a different version is pinned.
- Skipping the check for "well-known" packages: typosquats use exactly those names.
- Treating a package with no OSV entries as proven safe: an unknown, very new package with no advisories is still suspicious by step 1.
- Running the real install to see the dependency tree: install scripts have already run by then.
