# Restore

Rebuilds the whole agent environment on a clean Windows PC. Written for a human
and for Claude alike: follow it by hand, or open Claude desktop in this repo's
folder and say *"follow RESTORE.md"*.

## For Claude

- Before each step run its **Check**. If it already passes, skip the step.
- Anything that installs software, needs administrator rights or `sudo`: print
  the exact command and wait for the user to run it. Never run installers yourself.
- Never ask for secrets, tokens or keys in the chat — GitHub access and sign-ins
  are the user's job.
- After the last step run the final verification table and report every row.

## Layout

| Path | What |
|---|---|
| `~/home/agents/claude-code-setup` | this repo (Windows) |
| `~/home/agents/second-brain` | the knowledge base — local git, no remote |
| `~/.claude/` | live Claude config: `CLAUDE.md`, `settings.json`, `instructions/`, `agents/` |
| WSL `~/wsl-dev/` | code repos |

Other locations work too — then update `second-brain.md`, `environment.md` and
`permissions.additionalDirectories` in `settings.json` after step 3.

## 1. Windows base tools — user

- Claude desktop: <https://claude.ai/download>, sign in.
- In a terminal:

  ```powershell
  winget install --id Git.Git -e
  winget install --id Microsoft.PowerShell -e
  winget install --id Python.Python.3.14 -e
  winget install --id Obsidian.Obsidian -e   # optional, viewer for the knowledge base
  ```

- Git identity and a GitHub SSH key — set them up yourself
  (`git config --global user.name / user.email`, GitHub docs for SSH keys).

**Check:** `git --version`, `pwsh -v`, `py --version` all print a version.

## 2. Clone this repo

```powershell
New-Item -ItemType Directory -Force "$HOME\home\agents" | Out-Null
git clone <this-repo-url> "$HOME\home\agents\claude-code-setup"
```

**Check:** `$HOME\home\agents\claude-code-setup\RESTORE.md` exists.

## 3. Install the Claude config

```powershell
cd "$HOME\home\agents\claude-code-setup"
pwsh -NoProfile -File .\sync-claude-config.ps1 -Direction ToClaude -DryRun
pwsh -NoProfile -File .\sync-claude-config.ps1 -Direction ToClaude
```

Copies `claude-home/` — `CLAUDE.md`, `settings.json` (with `{{HOME}}` expanded),
`instructions/`, `agents/` — into `~/.claude`. Files it would overwrite are backed up first to
`~/.claude/backups/restore-<timestamp>/`. Restart Claude desktop afterwards.

**Check:** `~/.claude/instructions/workflow.md` exists; in a new session the
first line of a reply names the approach (`Approach: …`).

## 4. Plugins — user, in Claude desktop

- **Superpowers** — `settings.json` already enables
  `superpowers@claude-plugins-official`; if it isn't installed after the restart,
  install it from the plugin directory.
- **Context7** — install the Context7 plugin from the plugin directory (a hosted
  MCP server; no Node needed). Signing in is optional — it only raises rate limits.

**Check:** a new session lists `superpowers:*` skills and `context7` tools.

## 5. beads on Windows — for host-side repos

```powershell
irm https://raw.githubusercontent.com/gastownhall/beads/main/install.ps1 | iex
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";$env:LOCALAPPDATA\Programs\bd", "User")
```

Restart Claude desktop. `settings.json` already contains the SessionStart hook
`bd prime --hook-json` — do **not** run `bd setup claude` (it writes a CLAUDE.md
into whatever folder it runs in).

**Check:** `bd version`.

## 6. WSL — all development tools

```powershell
wsl --install -d Ubuntu-26.04
```

A different Ubuntu release works too — then replace the distro name in
`environment.md`. Reboot if asked and create the Linux user. Then, inside WSL:

```bash
sudo apt update && sudo apt install -y git nodejs npm unzip build-essential pkg-config
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
npm config set prefix ~/.local
npm install -g @fission-ai/openspec@latest
openspec config set telemetry.enabled false
curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash
curl -fsSL https://bun.sh/install | bash
echo 'export BUN_INSTALL="$HOME/.bun"; export PATH="$BUN_INSTALL/bin:$PATH"' >> ~/.profile
mkdir -p ~/wsl-dev
git config --global user.name "<name>" && git config --global user.email "<email>"
exec bash -l
```

PATH entries go into `~/.profile`, not `~/.bashrc` — agent commands run in a
non-interactive login shell. Keep the `bd` version equal on Windows and in WSL.

**Check** (from Git Bash on Windows):

```bash
wsl.exe -d Ubuntu-26.04 --exec bash -lc 'cargo --version; node --version; bun --version; bd version; openspec --version'
```

## 7. Knowledge base (second-brain)

Claude creates it from `instructions/second-brain.md`:

```powershell
$sb = "$HOME\home\agents\second-brain"
foreach ($d in "inbox","areas","projects","modules","knowledge-base","agents-data\session-log","archive","templates") {
    New-Item -ItemType Directory -Force "$sb\$d" | Out-Null
}
Copy-Item .\second-brain-templates\*.md "$sb\templates\"
git -C $sb init -b main
```

Then Claude writes `CLAUDE.md` (a pointer to `second-brain.md`), `README.md`
(the map) and `.gitignore` (`.obsidian/workspace*.json`, `.obsidian/cache`,
`.trash/`), and creates the user's areas from `templates/area.md`.

Obsidian: open the folder as a vault, enable the core plugin **Templates**, set
its folder to `templates`.

The knowledge base has no remote by design — its content survives a lost machine
only if the user backs it up elsewhere (external drive, encrypted archive).

**Check:** the folders exist and `git -C $sb status` works.

## 8. Worker gateway — LiteLLM (optional)

A local, OpenAI-compatible gateway for worker agents; Claude Code itself never
goes through it. Docker runs inside WSL — no Docker Desktop. Inside WSL, the user runs:

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2 docker-buildx && sudo usermod -aG docker $USER
```

Then `wsl.exe --terminate Ubuntu-26.04` from Windows, so the group applies.
Everything after that — runtime folder, the generated `.env`, first start, the
worker key with a budget — is in [services/litellm/README.md](services/litellm/README.md).
The `.env` is written and filled by the user only.

**Check:** `docker compose ps` in WSL `~/services/litellm` shows both containers
`healthy`; `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4000/health/liveliness`
prints `200` from WSL and from Windows.

## 9. Final verification

| What | How | Expected |
|---|---|---|
| Instructions loaded | new session, ask anything | reply starts with `Approach: …` |
| Settings valid | `pwsh -c "Get-Content $HOME\.claude\settings.json -Raw \| ConvertFrom-Json"` | no error |
| Plugins | new session | `superpowers:*` skills and `context7` tools available |
| Subagents | new session | `code-design-reviewer`, `leak-auditor`, `architecture-designer`, `Explore` available |
| Windows bd | `bd version` | a version |
| WSL toolchain | the step 6 check | five versions |
| Knowledge base | `git -C $HOME\home\agents\second-brain status` | a clean repo |
| Worker gateway (if set up) | the step 8 check | `healthy`, `200` |
| WSL repo from Claude | open a session in `\\wsl.localhost\Ubuntu-26.04\home\<user>\wsl-dev\<repo>` | file tools work, commands run via `wsl.exe --exec` |
