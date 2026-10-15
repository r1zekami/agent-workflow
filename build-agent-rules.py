"""Build the short rule files for OpenCode and Codex workers from the Essentials
blocks of ~/.claude/instructions/*.md. Run on the Windows host after any rule change:

    py build-agent-rules.py
"""
import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parent
INSTRUCTIONS = pathlib.Path.home() / ".claude" / "instructions"
DISTRO = "Ubuntu-26.04"

AUDIENCES = {
    "opencode": ["workflow", "language", "writing", "environment", "secrets", "sensitive-data",
                 "git", "code-style", "code-design", "second-brain", "beads", "openspec",
                 "canvas"],
    "worker": ["language", "secrets", "sensitive-data", "code-style", "code-design"],
}


def essentials(name):
    lines = (INSTRUCTIONS / f"{name}.md").read_text(encoding="utf-8").splitlines()
    title = lines[0].removeprefix("## ").split(":")[0]
    start = lines.index("### Essentials") + 1
    while not lines[start].strip():
        start += 1
    end = start
    while end < len(lines) and lines[end].strip():
        end += 1
    if end == start:
        raise SystemExit(f"{name}.md: empty Essentials block")
    return f"## {title}\n\n" + "\n".join(lines[start:end]) + "\n"


def build(preamble, audience):
    parts = [preamble.read_text(encoding="utf-8").rstrip() + "\n"]
    parts += [essentials(name) for name in AUDIENCES[audience]]
    return "\n".join(parts)


def wsl_home():
    out = subprocess.run(["wsl.exe", "-d", DISTRO, "--exec", "sh", "-c", "echo $HOME"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return pathlib.Path(rf"\\wsl.localhost\{DISTRO}" + out.replace("/", "\\"))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path} ({len(text.split())} words)")


write(pathlib.Path.home() / ".config" / "opencode" / "AGENTS.md",
      build(REPO / "harnesses" / "opencode" / "preamble.md", "opencode"))
write(wsl_home() / ".codex" / "instructions.md",
      build(REPO / "workers" / "codex" / "instructions.md", "worker"))
