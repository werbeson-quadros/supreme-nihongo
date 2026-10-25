# Local Japanese Voice Engine

The engine distribution is not included in this repository. Run `install.ps1` to download the pinned official VOICEVOX Engine 0.26.0 release, verify its SHA-256 hashes, extract it, and start it. The installer selects the CUDA edition when an NVIDIA GPU is detected, or the CPU edition otherwise. Use `-Edition cuda` or `-Edition cpu` to choose explicitly. Installation needs about 11 GB of free disk space for CUDA or 7 GB for CPU. Rerunning the script reuses an existing installation.

Start the engine and try its command-line helper:

```powershell
.\install.ps1
python .\speak.py --list-voices
python .\speak.py 'こんにちは。今日はいい天気ですね。' --speaker 2 --output .\sample.wav
```

Speaker IDs come from `--list-voices`. To stop the engine, close `run.exe` in Task Manager.

## Local performance check

On a GTX 1660 with 6 GB of VRAM, a 256-character Japanese sentence took 6.01 seconds for analysis and synthesis after engine startup, producing 47.9 seconds of audio. Speaker styles 2 and 3 were tested. Initial engine startup can take longer.

VOICEVOX speakers may have individual usage terms. Check those terms before publishing generated audio.
