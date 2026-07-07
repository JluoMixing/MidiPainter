param(
    [string]$Version = "0.1.0",
    [switch]$SkipTests,
    [switch]$BuildInstaller
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Dist = Join-Path $Root "dist"
$Build = Join-Path $Root "build"
$Spec = Join-Path $Root "packaging\windows\MidiPainter.spec"
$PortableName = "MidiPainter-$Version-win64-portable"
$PortableDir = Join-Path $Dist $PortableName
$ZipPath = Join-Path $Dist "$PortableName.zip"

Set-Location $Root

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

if (-not $SkipTests) {
    Invoke-Checked { python -m pytest }
}

python -m PyInstaller --version *> $null
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller is not installed. Run: python -m pip install pyinstaller"
}

Remove-Item -Recurse -Force $Build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force (Join-Path $Dist "MidiPainter") -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force $PortableDir -ErrorAction SilentlyContinue
Remove-Item -Force $ZipPath -ErrorAction SilentlyContinue

Invoke-Checked { python -m PyInstaller --noconfirm $Spec }

New-Item -ItemType Directory -Force $PortableDir | Out-Null
Copy-Item -Recurse -Force (Join-Path $Dist "MidiPainter\*") $PortableDir
Copy-Item -Force (Join-Path $Root "LICENSE") $PortableDir
Copy-Item -Force (Join-Path $Root "README.md") $PortableDir
Copy-Item -Force (Join-Path $Root "README.zh-CN.md") $PortableDir

Compress-Archive -Path (Join-Path $PortableDir "*") -DestinationPath $ZipPath -Force
Write-Host "Portable build: $PortableDir"
Write-Host "Portable zip:   $ZipPath"

if ($BuildInstaller) {
    $Iscc = Get-Command iscc -ErrorAction SilentlyContinue
    if (-not $Iscc) {
        throw "Inno Setup compiler 'iscc' was not found in PATH. Install Inno Setup and retry with -BuildInstaller."
    }
    & $Iscc.Source (Join-Path $Root "packaging\windows\MidiPainter.iss") "/DAppVersion=$Version" "/DSourceDir=$PortableDir" "/DOutputDir=$Dist"
}