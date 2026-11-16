---
name: dependency-check
description: Use before installing or adding any package or dependency - npm/pnpm/yarn/bun add or install, pip/uv/poetry add or install, cargo add or install, go get, gem, nuget, dotnet add package, editing a manifest (package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod) to add a dependency, or choosing a library to depend on.
---

# Dependency check

Every new dependency is checked before the install command runs. The check answers one question: is this package safe to depend on, or is an alternative needed. The global rule still applies: nothing is installed without the user's yes; the verdict goes into that request.

## Scope

| Situation | Check |
|---|---|
| A new package (install, `add`, a new line in a manifest) | Full check, steps 1-3 |
| A version change of an existing dependency | Step 3 for the target version |
| Restoring a project from its lockfile (`npm ci`, `pip install -r`, `cargo build`, `uv sync`) | Step 3 for every locked version (OSV batch query below) |

A check of a direct dependency covers that package only; transitive dependencies are covered by the lockfile scan.

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

## Verdict

| Verdict | Condition | Action |
|---|---|---|
| OK | Older than 60 days, released within 6 months, no current advisory, no `MAL-` record, clean or normal history | Propose the install with the checked version pinned |
| Suspicious | Created recently, unmaintained or deprecated, troubled history | Search for alternatives (below) |
| Rejected | `MAL-` record, or a current advisory with no fixed version | Never installed; search for alternatives |

**Alternatives.** Look for packages that solve the same task (registry search, the package's own README, the standard library first). Each candidate goes through steps 1-3. Propose the best candidate that is OK. No candidate is OK: present the options with their findings and let the user decide.

## Report

Before the install, the request to the user contains one line per checked package:
```
<name>@<version> (<ecosystem>): created <YYYY-MM-DD>, last release <YYYY-MM-DD>, advisories: <current count> current / <total> total, MAL: none -> OK / suspicious / rejected
```
A rejected or suspicious package also gets the reason and the proposed alternative.

## Common mistakes

- Taking the registry's `modified` or `updated_at` field as the last release date.
- Checking only the latest version when a different version is pinned.
- Skipping the check for "well-known" packages: typosquats use exactly those names.
- Treating a package with no OSV entries as proven safe: an unknown, very new package with no advisories is still suspicious by step 1.
