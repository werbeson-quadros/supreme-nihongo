param(
    [ValidateSet('auto', 'cuda', 'cpu')]
    [string]$Edition = 'auto',
    [switch]$NoStart
)

$ErrorActionPreference = 'Stop'
$python = (Get-Command python -ErrorAction Stop).Source
& $python (Join-Path $PSScriptRoot 'install_engine.py') --edition $Edition
if ($LASTEXITCODE -ne 0) { throw 'VOICEVOX Engine installation failed.' }

if (-not $NoStart) {
    & (Join-Path $PSScriptRoot 'iniciar.ps1')
    $version = Invoke-RestMethod 'http://127.0.0.1:50021/version' -TimeoutSec 10
    Write-Host "VOICEVOX Engine is ready (version $version)."
}
