## Environment: Windows host + WSL

| Where | What is located there |
|---|---|
| WSL, distro `Ubuntu-26.04` | ALL development: code repos in `~/wsl-dev/<repo>`, git, every toolchain (Rust, Go, C / C++, Node, Bun, ...), `bd`, `openspec` |
| Windows host | Routine only: Python 3 (`py` / `python`), PowerShell 7 (`pwsh`). Also host-side repos that never build (`~/home/agents/claude-code-setup`, `~/home/agents/second-brain`) with host git and host `bd`. Also Claude itself. |

### Rules

- **Never install a development toolchain on the Windows host.** A new toolchain
  goes into WSL. Ask before installing; anything that needs `sudo` the user runs.
- **Code repos are located in WSL** (`~/wsl-dev/<repo>`); from Windows they are
  `\\wsl.localhost\Ubuntu-26.04\home\<user>\wsl-dev\<repo>`. Best: open the
  session directly in that folder.
- **Every command for a WSL repo runs inside WSL**: git, builds, tests, linters,
  formatters, `bun`, `bd`, `openspec`.
- **Never run Windows `git.exe` or `bd.exe` on a WSL repo**: git refuses
  ("dubious ownership"), `bd` cannot lock files over the WSL share.
- **PATH for WSL tools goes into `~/.profile`, not `~/.bashrc`**: non-interactive
  login shells (the way commands are run) stop reading `.bashrc` at its first line.
- **Routine scripts on the host** use Python or PowerShell 7; run user scripts
  with `pwsh -NoProfile -File <script>`. The agent's own PowerShell tool is
  Windows PowerShell 5.1, so 7-only syntax must not be assumed there.

### Working on a WSL repo

- **Files**: Read / Edit / Write / Grep / Glob on the `\\wsl.localhost\...` path
  work normally. Glob does not skip build output, so exclude `target/`,
  `node_modules/` in patterns.
- **Commands**: from the Bash tool (Git Bash):

  ```bash
  wsl.exe -d Ubuntu-26.04 --exec bash -lc 'cargo test'
  ```

  - `--exec`, never `--`: with `--` the default shell expands `$variables` first
    and the command receives empty values.
  - `bash -lc` is a login shell, so `~/.profile` paths (`~/.cargo/bin`,
    `~/.local/bin`, `~/.bun/bin`) are on PATH.
  - If the session's working directory is the WSL repo, `wsl.exe` starts in the
    matching Linux directory by itself. Otherwise add `--cd <linux path>` and
    prefix the call with `MSYS_NO_PATHCONV=1`, because Git Bash rewrites Linux
    paths in arguments.
  - Not from PowerShell 5.1: it mangles inner double quotes for native programs.
- **Line endings**: WSL repos are LF natively; add a `.gitattributes` with
  `* text=auto eol=lf` to every new repo as insurance.
