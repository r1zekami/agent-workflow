# WSL repos from a Windows host

Applies when the harness runs on Windows and the repo is located in WSL (a `\\wsl.localhost\<distro>\...` or `\\wsl$\<distro>\...` path).

## Rule of thumb

Windows tools only read the share. Commands and edits beyond a single file run inside WSL.

## Reading

Read, Grep and Glob on the share path work normally. Glob does not skip build output: exclude `target/`, `node_modules/` and similar in patterns.

## Commands

git, builds, tests, linters, formatters, package managers, `bd` and `openspec` run inside WSL:
```
wsl.exe -d <distro> --cd <linux path> --exec bash -lc '<command>'
```
- Windows `git.exe` refuses the repo ("dubious ownership"); Windows `bd` fails ("Incorrect function"), because its embedded database cannot lock or map files over the share.
- `--exec`, never `--`: with `--`, the default shell expands `$variables` before the command sees them.
- `bash -lc` starts a login shell, so the tool paths from `~/.profile` are on `PATH`.
- From Git Bash, prefix the call with `MSYS_NO_PATHCONV=1`: otherwise MSYS rewrites `--cd /home/...` to `C:/Program Files/Git/home/...` and WSL reports a missing path. From PowerShell, no prefix is needed.
- The command inside `bash -lc '...'` uses single quotes outside and double quotes inside; Windows PowerShell 5.1 mangles inner double quotes passed to native programs, so complex commands go through Git Bash or PowerShell 7.
- `wsl.exe -l -v` prints UTF-16LE text that reads as spaced letters; set `WSL_UTF8=1` before the call, or do not parse that output.

## Editing

Edit and Write save through a temporary file and a rename. On the WSL share the rename fails intermittently (`EPERM`, `EUNKNOWN ftruncate`), more often while a build or a language server holds the file open.
- One file, one change: Edit on the share path is fine. After any error, check the file (`git diff` inside WSL) before treating the edit as applied, then retry once.
- Several files, bulk or mechanical changes: run a script inside WSL (for example, Python through `wsl.exe`).
- Files in WSL repos keep LF line endings. A new repo gets a `.gitattributes` with `* text=auto eol=lf`.
