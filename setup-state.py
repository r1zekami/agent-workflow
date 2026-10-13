"""Machine state of the agent setup, compared with setup-reference.yaml.

    py setup-state.py scan   # probe this machine, write setup-state.yaml
    py setup-state.py diff   # compare that state with setup-reference.yaml

Only names, versions and presence are recorded; secret values are never read.
Nothing is filled in by hand: every field is probed.
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()
STATE_PATH = REPO / "setup-state.yaml"
REFERENCE_PATH = REPO / "setup-reference.yaml"
DISTRO = "Ubuntu-26.04"
MISSING_VALUES = (None, "absent", "unset", "unknown", "down")


def parse_yaml(text):
    """Two-level mapping of scalars: `section:` then indented `key: value`."""
    data, section = {}, None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        key, _, value = raw.strip().partition(":")
        value = value.strip().strip('"')
        if raw.startswith(" "):
            section[key] = value
        elif value:
            data[key] = value
        else:
            section = data.setdefault(key, {})
    return data


def dump_yaml(data):
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            lines += [f'  {k}: "{v}"' for k, v in value.items()]
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def run(args, timeout=30):
    try:
        done = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                              encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def wsl(command):
    return run(["wsl.exe", "-d", DISTRO, "--exec", "bash", "-lc", command], timeout=60)


def first_version(text):
    match = re.search(r"\d+\.\d+(\.\d+)?", text or "")
    return match.group(0) if match else "present"


def windows_tool(exe):
    path = shutil.which(exe)
    if not path:
        return "absent"
    return first_version(run([path, "--version"]))


def wsl_tool(exe):
    out = wsl(f"command -v {exe} >/dev/null && ({exe} --version 2>&1 | head -1)")
    return "absent" if out is None else first_version(out)


def present(path):
    return "present" if pathlib.Path(path).exists() else "absent"


def count(folder, pattern):
    folder = pathlib.Path(folder)
    return str(len(list(folder.glob(pattern)))) if folder.is_dir() else "0"


def wsl_file(path):
    return "present" if wsl(f"test -e {path} && echo y") == "y" else "absent"


def wsl_env_present(name):
    return "present" if wsl(f'[ -n "${name}" ] && echo y') == "y" else "unset"


def opencode_state():
    config = HOME / ".config" / "opencode" / "opencode.json"
    state = {"config": present(config), "agents_md": present(config.with_name("AGENTS.md"))}
    if config.exists():
        loaded = json.loads(config.read_text(encoding="utf-8"))
        state["default_model"] = loaded.get("model", "absent")
        state["permission_default"] = loaded.get("permission", {}).get("*", "absent")
        providers = loaded.get("provider", {}).values()
        state["models"] = ",".join(model for p in providers for model in p.get("models", {}))
    return state


def codex_state():
    model = wsl("sed -n 's/^model = \"\\(.*\\)\"/\\1/p' ~/.codex/config.toml | head -1")
    return {"config_toml": wsl_file("~/.codex/config.toml"),
            "models_json": wsl_file("~/.codex/models.json"),
            "instructions_md": wsl_file("~/.codex/instructions.md"),
            "default_model": model or "absent"}


def git_identity(read):
    name, email = read("user.name"), read("user.email")
    return "yes" if name and email else "no"


def windows_git_identity():
    return git_identity(lambda key: run(["git", "config", "--global", key]))


def wsl_git_identity():
    return git_identity(lambda key: wsl(f"git config --global {key}"))


def github_ssh_auth():
    """GitHub answers an authenticated SSH login with exit code 1 and this banner."""
    try:
        done = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", "-T", "git@github.com"],
                              capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return "no"
    return "yes" if "successfully authenticated" in done.stderr + done.stdout else "no"


def gateway_deepseek_key_loaded():
    """Asks the running container; prints only a flag, never the value."""
    command = "cd ~/services/litellm && docker compose exec -T litellm sh -c '[ -n \"$DEEPSEEK_KEY\" ] && echo y'"
    out = wsl(command)
    return "yes" if out == "y" else "no"


def gateway_liveness():
    try:
        with urllib.request.urlopen("http://127.0.0.1:4000/health/liveliness", timeout=5) as reply:
            return str(reply.status)
    except OSError:
        return "down"


def scan():
    claude = HOME / ".claude"
    wslenv = os.environ.get("WSLENV", "").split(":")
    return {
        "schema": "1",
        "windows_tools": {name: windows_tool(name) for name in ("git", "pwsh", "python", "bd", "opencode")},
        "wsl": {"distro": DISTRO if wsl("echo y") == "y" else "absent"},
        "wsl_tools": {name: wsl_tool(name) for name in
                      ("git", "cargo", "node", "bun", "bd", "openspec", "docker", "codex")},
        "claude_config": {"claude_md": present(claude / "CLAUDE.md"),
                          "settings_json": present(claude / "settings.json"),
                          "instructions_count": count(claude / "instructions", "*.md"),
                          "agents_count": count(claude / "agents", "*.md")},
        "opencode": opencode_state(),
        "codex": codex_state(),
        "litellm": {"runtime_dir": wsl_file("~/services/litellm"),
                    "compose_yaml": wsl_file("~/services/litellm/compose.yaml"),
                    "gateway_liveness": gateway_liveness(),
                    "deepseek_key_loaded": gateway_deepseek_key_loaded()},
        "git": {"identity_windows": windows_git_identity(), "identity_wsl": wsl_git_identity(),
                "github_ssh_auth": github_ssh_auth()},
        "env": {"UNIVERSAL_LOCAL_LITELLM_KEY": wsl_env_present("UNIVERSAL_LOCAL_LITELLM_KEY"),
                "UNIVERSAL_EXTERNAL_LITELLM_KEY": wsl_env_present("UNIVERSAL_EXTERNAL_LITELLM_KEY"),
                "wslenv_has_local_key": "yes" if "UNIVERSAL_LOCAL_LITELLM_KEY" in wslenv else "no"},
    }


def matches(expected, actual):
    if expected == "any":
        return True
    if expected == "present":
        return actual not in MISSING_VALUES and actual != "0"
    return expected == actual


def diff():
    if not STATE_PATH.exists():
        raise SystemExit(f"No state at {STATE_PATH}: run `py setup-state.py scan` first.")
    state = parse_yaml(STATE_PATH.read_text(encoding="utf-8"))
    reference = parse_yaml(REFERENCE_PATH.read_text(encoding="utf-8"))
    problems = 0
    for section, expected_map in reference.items():
        if not isinstance(expected_map, dict):
            continue
        for key, expected in expected_map.items():
            actual = state.get(section, {}).get(key)
            if not matches(expected, actual):
                problems += 1
                print(f"DRIFT  {section}.{key}: expected {expected}, found {actual}")
    print(f"{problems} difference(s) from setup-reference.yaml." if problems
          else "State matches the reference.")
    return 1 if problems else 0


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "scan":
        STATE_PATH.write_text(dump_yaml(scan()), encoding="utf-8", newline="\n")
        print(f"wrote {STATE_PATH}")
        return 0
    if command == "diff":
        return diff()
    raise SystemExit(__doc__)


sys.exit(main())
