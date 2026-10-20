"""Install the agent rules from this repo into Claude Code and OpenCode on this machine.

Re-run after editing core/AGENTS.md or harness settings. Skills and Claude
subagents are linked, so their edits apply without re-running.
Usage: py install.py
"""

import datetime
import json
import os
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()
CLAUDE_HOME = HOME / ".claude"
OPENCODE_HOME = HOME / ".config" / "opencode"
BACKUP = HOME / ".agent-workflow-backup" / datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Paths left by the previous layout of this repo; moved to the backup folder.
OBSOLETE_PATHS = [
    CLAUDE_HOME / "instructions",
    CLAUDE_HOME / "skills" / "context7-mcp",
    CLAUDE_HOME / "agents" / "Explore.md",
    CLAUDE_HOME / "agents" / "architecture-designer.md",
]


def log(message: str) -> None:
    print(message)


def backup(path: pathlib.Path) -> None:
    target = BACKUP / path.relative_to(HOME)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(target))
    log(f"backed up {path} -> {target}")


def is_link(path: pathlib.Path) -> bool:
    return path.is_symlink() or path.is_junction()


def link_directory(link: pathlib.Path, target: pathlib.Path) -> None:
    if is_link(link) and link.resolve() == target.resolve():
        return
    if is_link(link):
        # rmdir removes a junction or a directory symlink without touching its target.
        os.rmdir(link)
    elif link.exists():
        backup(link)
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        # A junction needs no admin rights or developer mode, unlike a symlink.
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)
    else:
        link.symlink_to(target, target_is_directory=True)
    log(f"linked {link} -> {target}")


def copy_file(source: pathlib.Path, destination: pathlib.Path) -> None:
    if destination.exists() and destination.read_bytes() == source.read_bytes():
        return
    if destination.exists():
        backup(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    log(f"copied {source.name} -> {destination}")


def merge_json_file(template: pathlib.Path, destination: pathlib.Path, *, replacements: dict[str, str]) -> None:
    """Template keys win at the top level; keys only in the live file (keys, providers) are kept and never printed."""
    text = template.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    template_data = json.loads(text)
    live_data = {}
    if destination.exists():
        try:
            live_data = json.loads(destination.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            log(f"SKIPPED {destination}: not plain JSON (comments?); merge the keys of {template} by hand")
            return
    merged = {**live_data, **template_data}
    if merged == live_data:
        return
    if destination.exists():
        shutil.copyfile(destination, destination.with_suffix(destination.suffix + ".bak"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    log(f"merged {template.name} into {destination} (previous copy: {destination.name}.bak)")


def install_claude() -> None:
    for path in OBSOLETE_PATHS:
        if path.exists() and not is_link(path):
            backup(path)
    copy_file(REPO / "core" / "AGENTS.md", CLAUDE_HOME / "CLAUDE.md")
    for skill in sorted((REPO / "skills").iterdir()):
        link_directory(CLAUDE_HOME / "skills" / skill.name, skill)
    for agent in sorted((REPO / "harness" / "claude" / "agents").glob("*.md")):
        copy_file(agent, CLAUDE_HOME / "agents" / agent.name)
    home_for_json = str(HOME).replace("\\", "\\\\")
    merge_json_file(REPO / "harness" / "claude" / "settings.json", CLAUDE_HOME / "settings.json", replacements={"{{HOME}}": home_for_json})


def install_opencode() -> None:
    # Skills come from ~/.claude/skills; the documented ~/.claude/CLAUDE.md fallback is not loaded by OpenCode 2.x.
    copy_file(REPO / "core" / "AGENTS.md", OPENCODE_HOME / "AGENTS.md")
    merge_json_file(REPO / "harness" / "opencode" / "opencode.json", OPENCODE_HOME / "opencode.json", replacements={})


def main() -> int:
    install_claude()
    install_opencode()
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
