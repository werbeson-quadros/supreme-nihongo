$ErrorActionPreference = 'Stop'
$url = 'http://127.0.0.1:50021/version'
try {
    $version = Invoke-RestMethod $url -TimeoutSec 2
    Write-Host "VOICEVOX ja esta em execucao (versao $version)."
    exit 0
} catch {}

$engine = Join-Path $PSScriptRoot 'engine\windows-nvidia\run.exe'
if (-not (Test-Path $engine)) { throw "Motor nao encontrado: $engine" }
$process = Start-Process -FilePath $engine `
    -ArgumentList '--host','127.0.0.1','--port','50021','--use_gpu' `
    -WorkingDirectory (Split-Path $engine) `
    -WindowStyle Hidden -PassThru
for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 1
    try {
        $version = Invoke-RestMethod $url -TimeoutSec 2
        Write-Host "VOICEVOX $version iniciado na GPU (PID $($process.Id))."
        exit 0
    } catch {
        if ($process.HasExited) { throw "O motor terminou com codigo $($process.ExitCode)." }
    }
}
throw 'O motor nao respondeu em 60 segundos.'
