param(
    [Parameter(Mandatory = $true)]
    [string]$Owner
)

$ErrorActionPreference = "Stop"

$RepoName = "bhawna-skills"
$FullName = "$Owner/$RepoName"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host ""
Write-Host "Bhawna Skills - GitHub Publisher"
Write-Host "================================"
Write-Host "Repository: $FullName"
Write-Host ""

# ------------------------------------------------------------
# Required tools
# ------------------------------------------------------------

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or not available on PATH."
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI is not installed or not available on PATH."
}

# ------------------------------------------------------------
# GitHub authentication
# ------------------------------------------------------------

gh auth status

if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated. Run: gh auth login"
}

# ------------------------------------------------------------
# Git repository
# ------------------------------------------------------------

if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..."

    git init

    if ($LASTEXITCODE -ne 0) {
        throw "git init failed."
    }
}

git branch -M main

if ($LASTEXITCODE -ne 0) {
    throw "Could not set branch to main."
}

# ------------------------------------------------------------
# Commit pending changes
# ------------------------------------------------------------

git add .

if ($LASTEXITCODE -ne 0) {
    throw "git add failed."
}

git diff --cached --quiet

$DiffExitCode = $LASTEXITCODE

if ($DiffExitCode -eq 1) {
    Write-Host "Committing current changes..."

    git commit -m "Prepare Bhawna Skills v0.1.0"

    if ($LASTEXITCODE -ne 0) {
        throw "git commit failed."
    }
}
elseif ($DiffExitCode -eq 0) {
    Write-Host "No uncommitted changes."
}
else {
    throw "Could not inspect staged changes."
}

# ------------------------------------------------------------
# Check whether origin exists
# ------------------------------------------------------------

$Remotes = @(git remote)

if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect Git remotes."
}

$OriginExists = $Remotes -contains "origin"

# ------------------------------------------------------------
# Publish
# ------------------------------------------------------------

if ($OriginExists) {

    Write-Host ""
    Write-Host "Remote 'origin' already exists."
    Write-Host "Pushing main..."

    git push -u origin main

    if ($LASTEXITCODE -ne 0) {
        throw "git push failed."
    }
}
else {

    Write-Host ""
    Write-Host "Creating public GitHub repository $FullName..."

    $CreateArgs = @(
        "repo"
        "create"
        $FullName
        "--public"
        "--source=."
        "--remote=origin"
        "--push"
        "--description"
        "Guardrails and reusable skills for reliable AI coding agents."
    )

    & gh @CreateArgs

    if ($LASTEXITCODE -ne 0) {
        throw "GitHub repository creation failed."
    }
}

# ------------------------------------------------------------
# Verify
# ------------------------------------------------------------

Write-Host ""
Write-Host "Verifying remote..."

git remote -v

if ($LASTEXITCODE -ne 0) {
    throw "Could not verify Git remote."
}

Write-Host ""
Write-Host "Published successfully:"
Write-Host "https://github.com/$FullName"
Write-Host ""