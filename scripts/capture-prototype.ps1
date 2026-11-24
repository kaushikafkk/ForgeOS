param(
  [string]$Output = "docs/screenshots/forgeos-prototype-live.png"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$page = Join-Path $root "config/includes.chroot/usr/share/forgeos/prototype/index.html"
$target = Join-Path $root $Output
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path -LiteralPath $edge)) { $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
if (-not (Test-Path -LiteralPath $edge)) { throw "Microsoft Edge was not found" }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
$uri = [System.Uri]::new($page).AbsoluteUri
& $edge --headless --disable-gpu --hide-scrollbars --window-size=1600,1000 --screenshot=$target $uri
for ($attempt = 0; $attempt -lt 40 -and -not (Test-Path -LiteralPath $target); $attempt++) {
  Start-Sleep -Milliseconds 250
}
if (-not (Test-Path -LiteralPath $target)) { throw "Screenshot was not created" }
Write-Output $target
