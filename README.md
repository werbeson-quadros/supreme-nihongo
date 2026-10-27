# Supreme Nihongo

A local Japanese N5/N4/N3 practice app for listening, sentence completion, and vocabulary review. The interface is in Brazilian Portuguese.

## Run locally

This project targets Windows with Python 3.8 or newer. Install the official VOICEVOX Engine and start the trainer:

```powershell
.\voicevox\install.ps1
.\treino-n5\iniciar.ps1
```

The installer automatically selects CUDA when it detects an NVIDIA GPU, or the CPU package otherwise. It downloads the pinned VOICEVOX Engine 0.26.0 release, verifies official SHA-256 hashes, extracts it, and starts the engine. It needs about 11 GB of free disk space for CUDA or 7 GB for CPU during installation, and skips the download when the selected edition is already present. Open <http://127.0.0.1:8765/> if the browser does not open automatically.

## Features

- 520 annotated N5 sentences, 1,200 annotated N4 sentences, and 300 short N3 sentences, with full Portuguese translations.
- Listening transcription and Japanese sentence completion exercises.
- Multiple VOICEVOX voices, play/pause, playback speed from 0.5× to 2×, and an optional 0.5-second pause after each identified particle.
- On-demand reading of selected Japanese text with a meaning tooltip and a save-for-review button.
- Separate listening and writing scores for words and grammar, stored in a local SQLite database.
- Level-specific review flashcards for the 20 most missed terms and saved words, excerpts, or sentences. Cards have readings, translations, personal notes, 0.85× audio, and a two-seconds-per-side automatic mode.
- Dark theme and a review ranking.

The sentence data lives in `treino-n5/Lista e Frases N5.json`, `treino-n5/Lista e Frases N4.json`, and `treino-n5/Lista e Frases N3.json`. See [app documentation](treino-n5/README.md) and [voice setup](voicevox/README.md) for details.

## Local data and dependencies

The VOICEVOX Engine distribution, generated WAV files, logs, and `treino-n5/desempenho.sqlite3` are excluded from Git. The SQLite file contains the user's practice history and is created locally. VOICEVOX voices may have their own usage rules; review them before publishing generated audio.
