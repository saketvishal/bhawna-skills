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
    if ($LASTEXITCODE -ne 0) { throw "git init failed." }
}

git add .
if ($LASTEXITCODE -ne 0) { throw "git add failed." }

if (git status --porcelain) {
    git commit -m "Initial Bhawna Skills release"
    if ($LASTEXITCODE -ne 0) { throw "git commit failed." }
}

$fullName = "$Owner/$Repo"
$visibilityFlag = if ($Visibility -eq "public") { "--public" } else { "--private" }

& gh repo view $fullName --json name *> $null
if ($LASTEXITCODE -ne 0) {
    $createArgs = @(
        "repo", "create", $fullName,
        $visibilityFlag,
        "--source=.",
        "--remote=origin",
        "--push",
        "--description", "Guardrails and reusable skills for reliable AI coding agents."
    )

    & gh @createArgs
    if ($LASTEXITCODE -ne 0) { throw "GitHub repository creation failed." }
} else {
    git remote get-url origin *> $null
    if ($LASTEXITCODE -ne 0) {
        git remote add origin "https://github.com/$fullName.git"
        if ($LASTEXITCODE -ne 0) { throw "Failed to add origin remote." }
    }

    git push -u origin main
    if ($LASTEXITCODE -ne 0) { throw "git push failed." }
}

Write-Host "Published: https://github.com/$fullName"
