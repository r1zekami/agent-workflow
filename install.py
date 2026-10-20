"""Install the agent rules from this repo into Claude Code and OpenCode on this machine.

Re-run after editing core/AGENTS.md or anything in harness/. Skills are
linked, so their edits apply without re-running.
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


def merge_values(live, template):
    """Objects merge recursively, lists are unioned, other template values win; nothing only in the live file is lost."""
    if isinstance(live, dict) and isinstance(template, dict):
        merged = dict(live)
        for key, value in template.items():
            merged[key] = merge_values(live[key], value) if key in live else value
        return merged
    if isinstance(live, list) and isinstance(template, list):
        return live + [item for item in template if item not in live]
    return template


def merge_json_file(template: pathlib.Path, destination: pathlib.Path, *, replacements: dict[str, str]) -> None:
    """Live values (provider keys, extra permissions) are kept and never printed; removed template entries stay in the live file."""
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
    merged = merge_values(live_data, template_data)
    if merged == live_data:
        return
    if destination.exists():
        backup_copy = BACKUP / destination.relative_to(HOME)
        backup_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(destination, backup_copy)
        log(f"backed up {destination} -> {backup_copy}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    log(f"merged {template.name} into {destination}")


def install_claude() -> None:
    for path in OBSOLETE_PATHS:
        if path.exists() and not is_link(path):
            backup(path)
    copy_file(REPO / "core" / "AGENTS.md", CLAUDE_HOME / "CLAUDE.md")
    for skill in sorted((REPO / "skills").iterdir()):
        link_directory(CLAUDE_HOME / "skills" / skill.name, skill)
    for agent in sorted((REPO / "harness" / "claude" / "agents").glob("*.md")):
        copy_file(agent, CLAUDE_HOME / "agents" / agent.name)
    replacements = {
        "{{HOME}}": str(HOME).replace("\\", "\\\\"),
        "{{REPO}}": str(REPO).replace("\\", "\\\\"),
    }
    merge_json_file(REPO / "harness" / "claude" / "settings.json", CLAUDE_HOME / "settings.json", replacements=replacements)


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
