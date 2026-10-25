# Local Japanese Voice Engine

This project uses the Windows CUDA build of VOICEVOX Engine. Place the engine at `voicevox/engine/windows-nvidia/run.exe`. The engine distribution is not included in this repository.

Start the engine and try its command-line helper:

```powershell
.\iniciar.ps1
python .\speak.py --list-voices
python .\speak.py 'こんにちは。今日はいい天気ですね。' --speaker 2 --output .\sample.wav
```

Speaker IDs come from `--list-voices`. To stop the engine, close `run.exe` in Task Manager.

## Local performance check

On a GTX 1660 with 6 GB of VRAM, a 256-character Japanese sentence took 6.01 seconds for analysis and synthesis after engine startup, producing 47.9 seconds of audio. Speaker styles 2 and 3 were tested. Initial engine startup can take longer.

VOICEVOX speakers may have individual usage terms. Check those terms before publishing generated audio.
