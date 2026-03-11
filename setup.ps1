# NEXUS Security Division — Windows Setup Script
# Run this once to install everything needed to play the game.
# Right-click PowerShell > "Run as Administrator" is NOT required.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "  NEXUS SETUP" -ForegroundColor Green
Write-Host "  ===========" -ForegroundColor DarkGreen
Write-Host ""

# ── 1. Check Python ──────────────────────────────────────────────────────────

Write-Host "  [1/4] Checking for Python..." -ForegroundColor Cyan

$pythonCmd = $null
foreach ($cmd in @("python", "python3")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 10)) {
                $pythonCmd = $cmd
                Write-Host "        Found: $ver" -ForegroundColor Green
                break
            } else {
                Write-Host "        Found $ver but Python 3.10+ is required." -ForegroundColor Yellow
            }
        }
    } catch {
        # not found, try next
    }
}

if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "  Python 3.10 or later is not installed." -ForegroundColor Yellow
    Write-Host "  Attempting to install via winget (Windows 11 / updated Windows 10)..." -ForegroundColor Cyan
    Write-Host ""

    try {
        winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
        # Refresh PATH so python is available in this session
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
                    [System.Environment]::GetEnvironmentVariable("Path","User")
        $pythonCmd = "python"
        Write-Host ""
        Write-Host "        Python installed successfully." -ForegroundColor Green
    } catch {
        Write-Host ""
        Write-Host "  ERROR: Could not install Python automatically." -ForegroundColor Red
        Write-Host ""
        Write-Host "  Please install Python 3.10+ manually:" -ForegroundColor Yellow
        Write-Host "    1. Go to https://www.python.org/downloads/" -ForegroundColor White
        Write-Host "    2. Download and run the installer" -ForegroundColor White
        Write-Host "    3. IMPORTANT: tick 'Add Python to PATH' on the first screen" -ForegroundColor White
        Write-Host "    4. Re-run this script after installing" -ForegroundColor White
        Write-Host ""
        exit 1
    }
}

# ── 2. Fix execution policy if needed ────────────────────────────────────────

Write-Host "  [2/4] Checking execution policy..." -ForegroundColor Cyan

$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted" -or $policy -eq "Undefined") {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "        Execution policy set to RemoteSigned." -ForegroundColor Green
} else {
    Write-Host "        Policy OK ($policy)." -ForegroundColor Green
}

# ── 3. Create virtual environment ────────────────────────────────────────────

Write-Host "  [3/4] Creating virtual environment..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (Test-Path ".venv") {
    Write-Host "        .venv already exists, skipping." -ForegroundColor DarkGreen
} else {
    & $pythonCmd -m venv .venv
    Write-Host "        .venv created." -ForegroundColor Green
}

# ── 4. Install dependencies ───────────────────────────────────────────────────

Write-Host "  [4/4] Installing dependencies..." -ForegroundColor Cyan

& .\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
& .\.venv\Scripts\pip.exe install -r requirements.txt --quiet

Write-Host "        Dependencies installed." -ForegroundColor Green

# ── Done ──────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "  ============================================" -ForegroundColor DarkGreen
Write-Host "  SETUP COMPLETE. To play the game, run:" -ForegroundColor Green
Write-Host ""
Write-Host "      .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "      python main.py" -ForegroundColor White
Write-Host ""
Write-Host "  Or without activating the venv:" -ForegroundColor DarkGreen
Write-Host ""
Write-Host "      .venv\Scripts\python.exe main.py" -ForegroundColor White
Write-Host "  ============================================" -ForegroundColor DarkGreen
Write-Host ""
