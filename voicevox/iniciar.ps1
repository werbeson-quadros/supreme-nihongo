$ErrorActionPreference = 'Stop'
$url = 'http://127.0.0.1:50021/version'
try {
    $version = Invoke-RestMethod $url -TimeoutSec 2
    Write-Host "VOICEVOX ja esta em execucao (versao $version)."
    exit 0
} catch {}

$cudaEngine = Join-Path $PSScriptRoot 'engine\windows-nvidia\run.exe'
$cpuEngine = Join-Path $PSScriptRoot 'engine\windows-cpu\run.exe'
$gpuTool = Get-Command nvidia-smi.exe -ErrorAction SilentlyContinue
$gpuAvailable = $false
if ($gpuTool) {
    & $gpuTool.Source -L *> $null
    $gpuAvailable = $LASTEXITCODE -eq 0
}
if ($gpuAvailable -and (Test-Path -LiteralPath $cudaEngine -PathType Leaf)) {
    $engine = $cudaEngine
    $arguments = @('--host','127.0.0.1','--port','50021','--use_gpu')
} elseif (Test-Path -LiteralPath $cpuEngine -PathType Leaf) {
    $engine = $cpuEngine
    $arguments = @('--host','127.0.0.1','--port','50021')
} else {
    throw 'VOICEVOX Engine was not found. Run voicevox/install.ps1 first.'
}
$process = Start-Process -FilePath $engine `
    -ArgumentList $arguments `
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
