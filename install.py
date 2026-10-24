"""Install the agent rules from this repo into Claude Code and OpenCode on this machine.

Everything is copied, nothing is linked: re-run after any edit in this repo.
Usage: py install.py
"""

import datetime
import json
import os
import pathlib
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()
CLAUDE_HOME = HOME / ".claude"
OPENCODE_HOME = HOME / ".config" / "opencode"
BACKUP = HOME / ".agent-workflow-backup" / datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Marks a skill folder as installed from this repo, so it is removed once the repo drops it.
INSTALLED_SKILL_MARKER = ".installed-by-agent-workflow"

# Lists the rule files installed from this repo, so a rule dropped from the repo is removed.
INSTALLED_RULES_MANIFEST = ".installed-by-agent-workflow"

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


def read_tree(root: pathlib.Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and path.name != INSTALLED_SKILL_MARKER and "__pycache__" not in path.parts
    }


def copy_skill(source: pathlib.Path, destination: pathlib.Path) -> None:
    if is_link(destination):
        # rmdir removes a junction or a directory symlink without touching its target.
        os.rmdir(destination)
    elif destination.exists():
        if (destination / INSTALLED_SKILL_MARKER).exists() and read_tree(destination) == read_tree(source):
            return
        backup(destination)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__"))
    (destination / INSTALLED_SKILL_MARKER).write_text("", encoding="utf-8")
    log(f"copied skill {source.name} -> {destination}")


def remove_skills_dropped_from_repo() -> None:
    skills_home = CLAUDE_HOME / "skills"
    if not skills_home.exists():
        return
    for installed in skills_home.iterdir():
        if (REPO / "skills" / installed.name).exists():
            continue
        if is_link(installed):
            os.rmdir(installed)
            log(f"removed link {installed}")
        elif (installed / INSTALLED_SKILL_MARKER).exists():
            backup(installed)


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


def install_rules() -> None:
    rules_home = CLAUDE_HOME / "rules"
    manifest = rules_home / INSTALLED_RULES_MANIFEST
    repo_rules = sorted((REPO / "rules").glob("*.md"))
    previously_installed = manifest.read_text(encoding="utf-8").split() if manifest.exists() else []
    for name in previously_installed:
        dropped_rule = rules_home / name
        if dropped_rule.exists() and not (REPO / "rules" / name).exists():
            backup(dropped_rule)
    for rule in repo_rules:
        copy_file(rule, rules_home / rule.name)
    manifest.write_text("\n".join(rule.name for rule in repo_rules) + "\n", encoding="utf-8")


def install_claude() -> None:
    for path in OBSOLETE_PATHS:
        if path.exists() and not is_link(path):
            backup(path)
    copy_file(REPO / "core" / "AGENTS.md", CLAUDE_HOME / "CLAUDE.md")
    install_rules()
    remove_skills_dropped_from_repo()
    for skill in sorted((REPO / "skills").iterdir()):
        copy_skill(skill, CLAUDE_HOME / "skills" / skill.name)
    for hook in sorted((REPO / "harness" / "claude" / "hooks").glob("*.py")):
        copy_file(hook, CLAUDE_HOME / "hooks" / hook.name)
    for agent in sorted((REPO / "harness" / "claude" / "agents").glob("*.md")):
        copy_file(agent, CLAUDE_HOME / "agents" / agent.name)
    replacements = {"{{HOME}}": str(HOME).replace("\\", "\\\\")}
    merge_json_file(REPO / "harness" / "claude" / "settings.json", CLAUDE_HOME / "settings.json", replacements=replacements)


def install_opencode() -> None:
    # Skills come from ~/.claude/skills; the documented ~/.claude/CLAUDE.md fallback is not loaded by OpenCode 2.x.
    copy_file(REPO / "core" / "AGENTS.md", OPENCODE_HOME / "AGENTS.md")
    replacements = {"{{HOME}}": HOME.as_posix()}
    merge_json_file(REPO / "harness" / "opencode" / "opencode.json", OPENCODE_HOME / "opencode.json", replacements=replacements)


def main() -> int:
    install_claude()
    install_opencode()
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
