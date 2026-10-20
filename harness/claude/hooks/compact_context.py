"""SessionStart hook (matcher "compact"): restores the working state that a compaction summary tends to lose.

Prints Claude Code hook JSON with the git state of the session's directory.
Usage in settings.json: py -I <path>/compact_context.py
"""

import json
import pathlib
import subprocess
import sys

MAX_STATUS_LINES = 30


def run_git(cwd: pathlib.Path, *arguments: str) -> str:
    command = ["git", *arguments]
    working_directory = cwd
    segments = str(cwd).replace("/", "\\").strip("\\").split("\\")
    if segments[0].lower() in ("wsl.localhost", "wsl$") and len(segments) > 1:
        # Windows git refuses repos on the WSL share; ask the distro's git instead.
        linux_path = "/" + "/".join(segments[2:])
        command = ["wsl.exe", "-d", segments[1], "--cd", linux_path, "--exec", *command]
        working_directory = None
    try:
        result = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def describe_git_state(cwd: pathlib.Path) -> str:
    branch = run_git(cwd, "branch", "--show-current")
    if not branch:
        return ""
    status_lines = run_git(cwd, "status", "--short").splitlines()
    shown_status = "\n".join(status_lines[:MAX_STATUS_LINES]) or "clean"
    if len(status_lines) > MAX_STATUS_LINES:
        shown_status += f"\n... {len(status_lines) - MAX_STATUS_LINES} more"
    recent_commits = run_git(cwd, "log", "--oneline", "-5")
    return (
        f"Git state after compaction in {cwd.name or cwd}:\n"
        f"Branch: {branch}\n"
        f"Working tree:\n{shown_status}\n"
        f"Recent commits:\n{recent_commits}"
    )


def main() -> int:
    hook_input = json.load(sys.stdin)
    cwd = pathlib.Path(hook_input.get("cwd") or ".")
    context = describe_git_state(cwd)
    if not context:
        return 0
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
