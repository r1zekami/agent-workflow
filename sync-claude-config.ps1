<#
.SYNOPSIS
Mirrors the Claude Code config between ~/.claude and claude-home/ in this repo.

.DESCRIPTION
Only whitelisted files are touched: CLAUDE.md, settings.json, instructions/*.md
and agents/*.md. In settings.json the home folder path is stored in the repo as
the {{HOME}} placeholder, so the repo never contains a user name.

  -Direction ToRepo    ~/.claude -> claude-home/. Files that no longer exist in
                       ~/.claude are removed from claude-home/.
  -Direction ToClaude  claude-home/ -> ~/.claude. Nothing is deleted in
                       ~/.claude; every file about to be overwritten is backed
                       up to ~/.claude/backups/restore-<timestamp>/ first.

.EXAMPLE
pwsh -NoProfile -File .\sync-claude-config.ps1 -Direction ToRepo
pwsh -NoProfile -File .\sync-claude-config.ps1 -Direction ToClaude -DryRun
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("ToRepo", "ToClaude")]
    [string]$Direction,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$claudeRoot = Join-Path $HOME ".claude"
$repoMirror = Join-Path $PSScriptRoot "claude-home"
$singleFiles = @("CLAUDE.md", "settings.json")
$mirroredFolders = @("instructions", "agents")
$homePlaceholder = "{{HOME}}"
$homeAsJson = $HOME.Replace("\", "\\")
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

if ($Direction -eq "ToRepo") {
    $sourceRoot = $claudeRoot
    $targetRoot = $repoMirror
} else {
    $sourceRoot = $repoMirror
    $targetRoot = $claudeRoot
}
$backupRoot = Join-Path $claudeRoot ("backups\restore-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
$counts = @{ copied = 0; unchanged = 0; removed = 0; backedUp = 0 }

if (-not (Test-Path -LiteralPath $sourceRoot)) {
    Write-Error "Source folder not found: $sourceRoot"
    exit 1
}

function Convert-ContentForTarget([string]$relativePath, [string]$content) {
    if ($relativePath -ne "settings.json") {
        return $content
    }
    if ($Direction -eq "ToRepo") {
        return $content.Replace($homeAsJson, $homePlaceholder)
    }
    return $content.Replace($homePlaceholder, $homeAsJson)
}

function Sync-File([string]$relativePath) {
    $sourcePath = Join-Path $sourceRoot $relativePath
    $targetPath = Join-Path $targetRoot $relativePath
    $content = Convert-ContentForTarget $relativePath ([System.IO.File]::ReadAllText($sourcePath))
    $targetExists = Test-Path -LiteralPath $targetPath
    if ($targetExists -and ([System.IO.File]::ReadAllText($targetPath) -ceq $content)) {
        $counts.unchanged++
        return
    }
    if ($targetExists -and $Direction -eq "ToClaude") {
        Write-Output "backup   $relativePath"
        if (-not $DryRun) {
            $backupPath = Join-Path $backupRoot $relativePath
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backupPath) | Out-Null
            Copy-Item -LiteralPath $targetPath -Destination $backupPath -Force
        }
        $counts.backedUp++
    }
    Write-Output "copy     $relativePath"
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetPath) | Out-Null
        [System.IO.File]::WriteAllText($targetPath, $content, $utf8NoBom)
    }
    $counts.copied++
}

foreach ($file in $singleFiles) {
    if (Test-Path -LiteralPath (Join-Path $sourceRoot $file)) {
        Sync-File $file
    }
}

foreach ($folder in $mirroredFolders) {
    $sourceFolder = Join-Path $sourceRoot $folder
    $sourceNames = @()
    if (Test-Path -LiteralPath $sourceFolder) {
        foreach ($sourceFile in Get-ChildItem -LiteralPath $sourceFolder -Filter "*.md" -File) {
            $sourceNames += $sourceFile.Name
            Sync-File (Join-Path $folder $sourceFile.Name)
        }
    }
    $targetFolder = Join-Path $targetRoot $folder
    if ($Direction -eq "ToRepo" -and (Test-Path -LiteralPath $targetFolder)) {
        foreach ($targetFile in Get-ChildItem -LiteralPath $targetFolder -Filter "*.md" -File) {
            if ($sourceNames -notcontains $targetFile.Name) {
                Write-Output "remove   $(Join-Path $folder $targetFile.Name)"
                if (-not $DryRun) {
                    Remove-Item -LiteralPath $targetFile.FullName
                }
                $counts.removed++
            }
        }
    }
}

function Find-PersonalIdentifierInRepo {
    # The repo is public: no login name, home path, machine name or git identity in it.
    $identifiers = @{
        "login name"   = $env:USERNAME
        "machine name" = $env:COMPUTERNAME
        "git name"     = (git config --global user.name 2>$null)
        "git e-mail"   = (git config --global user.email 2>$null)
    }
    $patterns = @{}
    foreach ($kind in $identifiers.Keys) {
        if ($identifiers[$kind]) {
            $patterns[$kind] = "(?i)(?<![a-z0-9])" + [regex]::Escape($identifiers[$kind]) + "(?![a-z0-9])"
        }
    }
    # Only what git could commit: tracked files plus untracked ones not ignored
    # (.gitignore, .git/info/exclude) - local tool data like .beads/ is never published.
    # LICENSE carries the copyright holder's name on purpose - the only exception.
    $repoFiles = git -C $PSScriptRoot ls-files --cached --others --exclude-standard |
        Where-Object { $_ -ne "LICENSE" }
    foreach ($relativePath in $repoFiles) {
        $fullPath = Join-Path $PSScriptRoot $relativePath
        if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) { continue }
        $lineNumber = 0
        foreach ($line in [System.IO.File]::ReadAllLines($fullPath)) {
            $lineNumber++
            foreach ($kind in $patterns.Keys) {
                if ($line -match $patterns[$kind]) {
                    $relativePath + ":" + $lineNumber + " ($kind)"
                }
            }
        }
    }
}

# Runs on every ToRepo sync, dry runs included: it guards the commit.
if ($Direction -eq "ToRepo") {
    $identifierHits = @(Find-PersonalIdentifierInRepo)
    foreach ($hit in $identifierHits) {
        Write-Output "PERSONAL IDENTIFIER  $hit"
    }
    if ($identifierHits.Count -gt 0) {
        Write-Output "Found $($identifierHits.Count) personal identifier(s) in the repo - fix before committing."
        exit 1
    }
}

$mode = if ($DryRun) { "Dry run" } else { "Done" }
Write-Output ("{0} ({1}). Copied: {2}, unchanged: {3}, removed: {4}, backed up: {5}." -f `
    $mode, $Direction, $counts.copied, $counts.unchanged, $counts.removed, $counts.backedUp)
if (-not $DryRun -and $counts.backedUp -gt 0) {
    Write-Output "Backups: $backupRoot"
}
