# Restore

Rebuilds the agent setup on a clean machine. Followed by hand, or by a harness opened in this repo's folder with the prompt *"follow RESTORE.md"*.

## For the agent

- Before each step run its **Check**; if it already passes, skip the step.
- Anything that installs software, needs administrator rights or `sudo`: print the exact command and wait for the user to run it.
- Never ask for secrets, tokens or keys in the chat; sign-ins and provider keys are set up by hand.
- After the last step run the final verification and report every row.

## Layout

| Path | What |
|---|---|
| `~/home/agents/agent-workflow` | this repo |
| `~/home/agents/second-brain` | the knowledge base (local git, no remote) |
| `~/.claude/` | Claude Code config; OpenCode reads its `skills/` too |
| `~/.config/opencode/` | OpenCode config (`AGENTS.md`, `opencode.json`, provider keys) |

The harnesses run where the user works; the environment (OS, toolchains, WSL) is set up separately. Other locations work too, then update the paths in `core/AGENTS.md`, `skills/second-brain/SKILL.md` and `permissions.additionalDirectories` in `harness/claude/settings.json`.

## 1. Base tools

- Git, Python 3.12+, and (Windows) PowerShell 7.
- Obsidian, optional: viewer for the knowledge base.
- Git identity and a GitHub SSH key are set up by the user.

**Check:** `git --version` and `py --version` (or `python3 --version`) print a version.

## 2. Clone this repo

```powershell
New-Item -ItemType Directory -Force "$HOME\home\agents" | Out-Null
git clone <this-repo-url> "$HOME\home\agents\agent-workflow"
```

**Check:** `~/home/agents/agent-workflow/install.py` exists.

## 3. Harnesses

- Claude Code CLI, native installer: `irm https://claude.ai/install.ps1 | iex` (Windows) or `curl -fsSL https://claude.ai/install.sh | bash`. Add `~/.local/bin` to `PATH`. Sign in with `claude` -> `/login`.
- Claude desktop, optional: <https://claude.ai/download>.
- OpenCode 2.x CLI: see <https://opencode.ai/docs/>. Windows package managers are not supported; on Windows use npm (`npm install -g @opencode/cli`, and allow its install script). Desktop, optional: <https://opencode.ai/download>.
- Provider keys for OpenCode (`/connect`, or `provider` in `~/.config/opencode/opencode.json`) are added by the user.

**Check:** `claude --version` and `opencode --version` print a version.

## 4. Install the rules

```powershell
cd "$HOME\home\agents\agent-workflow"
py install.py
```

`install.py` does the following:
- copies `core/AGENTS.md` to `~/.claude/CLAUDE.md` and `~/.config/opencode/AGENTS.md`;
- copies `rules/*.md` into `~/.claude/rules/` and removes rules that were installed from the repo and are no longer in it;
- copies every `skills/<name>` into `~/.claude/skills/` and removes skills that were installed from the repo and are no longer in it;
- copies `harness/claude/agents/*.md` into `~/.claude/agents/` and `harness/claude/hooks/*.py` into `~/.claude/hooks/`;
- merges `harness/claude/settings.json` into `~/.claude/settings.json` (`{{HOME}}` expanded);
- merges `harness/opencode/opencode.json` into `~/.config/opencode/opencode.json`.

The merge is recursive: objects are merged, lists are unioned, and anything only in the live file (providers, keys, extra permissions) is kept. An entry removed from a template stays in the live file and is removed there by hand.

Replaced and merged files are first copied to `~/.agent-workflow-backup/<timestamp>/`. Nothing is linked: re-run after any edit in the repo.

**Check:** `~/.claude/CLAUDE.md` starts with `# Global agent rules`, and `~/.claude/rules/general-writing.md` exists.

## 5. Plugins

- **Claude Code**: `settings.json` enables `superpowers@claude-plugins-official`; if it is not installed after a restart: `claude plugin install superpowers@claude-plugins-official`.
- **OpenCode**: the template adds superpowers to `plugins`; restart OpenCode.

**Check:** a new session in each harness lists the superpowers skills (ask: "Tell me about your superpowers").

## 6. beads (optional, per repo)

Install `bd` where the repos are (see <https://github.com/gastownhall/beads>). `settings.json` runs `bd prime --hook-json` at session start. Do **not** run `bd setup claude`: it writes a `CLAUDE.md` into the folder it runs in.

**Check:** `bd version`.

## 7. Knowledge base (second-brain)

Structure and rules: `skills/second-brain/SKILL.md`. Create the skeleton:

```powershell
$sb = "$HOME\home\agents\second-brain"
foreach ($d in "work\scratchpad","work\services","work\pipelines","work\projects","work\knowledge-base","work\dashboards","work\attachments","work\archive",
                "personal\scratchpad","personal\projects","personal\knowledge-base","personal\archive",
                "agents-data\session-log","templates") {
    New-Item -ItemType Directory -Force "$sb\$d" | Out-Null
}
Copy-Item .\second-brain-templates\*.md "$sb\templates\"
git -C $sb init -b main
```

Then the agent writes `AGENTS.md` (a pointer to the `second-brain` skill), `README.md` (the map), a `README.md` and an empty `domain-tags.md` in each scope, and `.gitignore` (`.obsidian/workspace*.json`, `.obsidian/cache`, `.obsidian/plugins/`, `.trash/`). Empty folders get a `.gitkeep`.

Obsidian: open the folder as a vault, enable the core plugin **Templates** with folder `templates`, add `templates/` to **Files and links** -> **Excluded files**, copy `second-brain-obsidian/hide-templates.css` to `<vault>/.obsidian/snippets/` and enable it under **Appearance** -> **CSS snippets**.

The knowledge base has no remote by design; it survives a lost machine only through the user's own backup.

**Check:** the folders exist and `git -C $sb status` works.

## Final verification

| Row | Check |
|---|---|
| Claude Code | `claude --version` |
| OpenCode | `opencode --version` |
| Rules | `~/.claude/CLAUDE.md` starts with `# Global agent rules` |
| Skills | `~/.claude/skills/<name>/SKILL.md` exists for every folder in `skills/` |
| Rule files | `~/.claude/rules/<name>.md` exists for every file in `rules/` |
| superpowers | listed in a new session of each harness |
| second-brain | `git -C ~/home/agents/second-brain status` works |
