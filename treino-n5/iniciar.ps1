$ErrorActionPreference = 'Stop'
$url = 'http://127.0.0.1:8765/api/stats'
try { Invoke-RestMethod $url -TimeoutSec 2 | Out-Null; $running = $true } catch { $running = $false }
if (-not $running) {
    $python = (Get-Command python -ErrorAction Stop).Source
    $process = Start-Process -FilePath $python -ArgumentList @('server.py') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru
    for ($i = 0; $i -lt 15; $i++) {
        Start-Sleep -Seconds 1
        try { Invoke-RestMethod $url -TimeoutSec 2 | Out-Null; $running = $true; break } catch {}
        if ($process.HasExited) { throw 'O servidor do treino terminou durante a inicialização.' }
    }
    if (-not $running) { throw 'O servidor do treino não respondeu em 15 segundos.' }
}
Start-Process 'http://127.0.0.1:8765'
