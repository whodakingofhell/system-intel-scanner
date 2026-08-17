# Wrapper to run intel scan and push results to GitHub + Obsidian
param(
  [string[]]$Sources,
  [switch]$Push
)
$ErrorActionPreference='SilentlyContinue'
$hermesHome = "$env:LOCALAPPDATA\hermes"
$scriptPath = Join-Path $hermesHome "skills\system-intel-scanner\scripts\scan.py"
$python = Join-Path $hermesHome "hermes-agent\venv\Scripts\python.exe"
if (-not (Test-Path $scriptPath)) { Write-Error "Scanner script not found: $scriptPath"; exit 1 }
if (-not (Test-Path $python)) { Write-Error "Python not found: $python"; exit 1 }

$argsList = @()
if ($Sources) { $argsList += $Sources }

Push-Location $hermesHome
& $python $scriptPath @argsList
$scanExit = $LASTEXITCODE
Pop-Location

if ($Push -and $scanExit -eq 0) {
  $latestScan = Get-ChildItem "$hermesHome\data\intel-scans\scan-*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($latestScan) {
    # Push to Obsidian vaults
    $vaults = @(
      "$env:USERPROFILE\OneDrive\Desktop\AI-Ops-Vault",
      "$env:USERPROFILE\OneDrive\Desktop\PROMPT GUIDE AI",
      "$env:USERPROFILE\OneDrive\Desktop\PAIOS"
    )
    foreach ($v in $vaults) {
      if (Test-Path "$v\.git") {
        Push-Location $v
        git add -A 2>$null | Out-Null
        $status = git diff --cached --shortstat 2>$null
        if ($status) {
          git commit -m "chore(intel): auto-sync system intel $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>$null | Out-Null
          $branch = git rev-parse --abbrev-ref HEAD 2>$null
          git push origin $branch 2>$null | Out-Null
          Write-Host "Pushed intel to $v"
        }
        Pop-Location
      }
    }
  }
}
exit $scanExit
