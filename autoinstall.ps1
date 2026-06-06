<#
autoinstall.ps1 - Tam otomatik kurulum (Windows)

Kullanım:
  powershell -NoProfile -ExecutionPolicy Bypass -File .\autoinstall.ps1 [-Venv .venv] [-Port 8000] [-Host 127.0.0.1] [-CreateScheduledTask]

#>

param(
    [string]$Venv = ".venv",
    [int]$Port = 8000,
    [string]$Host = "127.0.0.1",
    [switch]$CreateScheduledTask
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Write-Host "Otomatik kurulum başlıyor..." -ForegroundColor Cyan

$setupScript = Join-Path $scriptDir "setup.ps1"
if (Test-Path $setupScript) {
    Write-Host "Sanal ortam oluşturuluyor ve bağımlılıklar yükleniyor..." -ForegroundColor Cyan
    & powershell -NoProfile -ExecutionPolicy Bypass -File $setupScript -VENV $Venv
} else {
    Write-Host "setup.ps1 bulunamadı; sanal ortam atlanıyor." -ForegroundColor Yellow
}

if ($CreateScheduledTask) {
    $schtScript = Join-Path $scriptDir "install_setup_schtask.ps1"
    if (Test-Path $schtScript) {
        Write-Host "Scheduled task kuruluyor (yönetici izni gerekebilir)..." -ForegroundColor Cyan
        & powershell -NoProfile -ExecutionPolicy Bypass -File $schtScript -TaskName "EgitimSetupServer" -Venv $Venv -Port $Port -HostName $Host
    } else {
        Write-Host "install_setup_schtask.ps1 bulunamadı; atlanıyor." -ForegroundColor Yellow
    }
}

# Resolve python executable inside venv or fallback to global python
$venvPath = Join-Path $scriptDir $Venv
$pyExe = $null
$pyInVenv = Join-Path $venvPath "Scripts\python.exe"
if (Test-Path $pyInVenv) { $pyExe = (Resolve-Path $pyInVenv).Path }

if (-not $pyExe) {
    $globalPy = Get-Command python -ErrorAction SilentlyContinue
    if ($globalPy) { $pyExe = $globalPy.Source }
}

if (-not $pyExe) {
    Write-Host "Hata: Python yürütücüsü bulunamadı; sunucu başlatılamıyor." -ForegroundColor Red
    exit 1
}

# Start setup server in background
$arguments = @('-m','uvicorn','setup_server:app','--host',$Host,'--port',$Port.ToString())
Write-Host "Kurulum sunucusu başlatılıyor (arka planda)..." -ForegroundColor Cyan
Start-Process -FilePath $pyExe -ArgumentList $arguments -WorkingDirectory $scriptDir -WindowStyle Hidden

Start-Sleep -Seconds 2

# Open browser
$url = "http://$Host`:$Port"
Write-Host "Tarayıcı açılıyor: $url" -ForegroundColor Green
Start-Process $url

Write-Host "Otomatik kurulum tamamlandı." -ForegroundColor Green
