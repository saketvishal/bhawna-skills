param(
    [Parameter(Mandatory = $true)]
    [string]$Owner,
    [string]$Repo = "bhawna-skills",
    [ValidateSet("public", "private")]
    [string]$Visibility = "public"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required. Install it and run 'gh auth login' first."
}

if (-not (Test-Path ".git")) {
    git init -b main
}

git add .
if (git status --porcelain) {
    git commit -m "Initial Bhawna Skills release"
}

$fullName = "$Owner/$Repo"
$existing = gh repo view $fullName 2>$null
if ($LASTEXITCODE -ne 0) {
    gh repo create $fullName --$Visibility --source . --remote origin --push \
        --description "Guardrails and reusable skills for reliable AI coding agents."
} else {
    if (-not (git remote get-url origin 2>$null)) {
        git remote add origin "https://github.com/$fullName.git"
    }
    git push -u origin main
}

Write-Host "Published: https://github.com/$fullName"
