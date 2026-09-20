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

# Verify required tools
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or not available on PATH."
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI is not installed or not available on PATH."
}

# Verify GitHub authentication
gh auth status

if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated. Run: gh auth login"
}

# Initialize Git only if needed
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

# Commit current project state if anything changed
git add .

git diff --cached --quiet

if ($LASTEXITCODE -eq 1) {
    Write-Host "Committing current changes..."

    git commit -m "Prepare Bhawna Skills v0.1.0"

    if ($LASTEXITCODE -ne 0) {
        throw "git commit failed."
    }
}
elseif ($LASTEXITCODE -ne 0) {
    throw "Could not inspect staged changes."
}
else {
    Write-Host "No uncommitted changes."
}

# Check whether origin already exists
$OriginUrl = git remote get-url origin 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Origin already exists:"
    Write-Host $OriginUrl
    Write-Host ""
    Write-Host "Pushing main..."

    git push -u origin main

    if ($LASTEXITCODE -ne 0) {
        throw "git push failed."
    }
}
else {
    Write-Host ""
    Write-Host "Creating public GitHub repository $FullName..."

    gh repo create $FullName `
        --public `
        --source=. `
        --remote=origin `
        --push `
        --description "Guardrails and reusable skills for reliable AI coding agents."

    if ($LASTEXITCODE -ne 0) {
        throw "GitHub repository creation failed."
    }
}

Write-Host ""
Write-Host "Published successfully:"
Write-Host "https://github.com/$FullName"
Write-Host ""