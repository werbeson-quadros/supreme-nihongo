# N5 and N4 Listening and Writing Practice

Run `iniciar.ps1` in PowerShell. The interface opens at <http://127.0.0.1:8765/>.

The N5 corpus contains 520 sentences, including five examples for each of 84 requested grammar topics. The N4 corpus contains 900 sentences: 400 cover 132 grammar topics, and 500 additional sentences combine vocabulary themes with conversation, classroom, research, family, and travel scenarios. Each sentence has a full Brazilian Portuguese translation. Its tokens carry written forms, readings, types, meanings, and usage notes. The additional N4 sentences are 41–50 Japanese characters long.

`gerar_frases.py`, `gramatica_extra.py`, `gerar_frases_n4.py`, and `cenarios_n4.py` are the editable corpus generators. Regenerating the additional N4 sentences requires a running VOICEVOX Engine to obtain readings.

VOICEVOX generates the audio. The voice selector lists available speakers and styles. The player supports play/pause, speeds from 0.5× to 2×, and an optional 0.5-second pause after each identified particle. Generated audio is cached under `audio-cache/`. The selected speed and particle-pause setting persist in the browser.

The answer dialog also includes a Japanese audio player. Selecting Japanese text in an exercise or answer reads it aloud repeatedly until the selection is cleared. A small tooltip shows meanings from the current sentence's glossary. If the browser has no Japanese voice, the app uses a short locally generated audio clip.

In **Listening** mode, the learner transcribes the audio. Written forms and kana readings are accepted, while whitespace and punctuation are ignored. Token alignment is approximate when a response contains several errors.

In **Complete the sentence** mode, the Portuguese translation is the goal and two to four Japanese spans are blank. Only the blanks are scored. Grammar has a weight of 1.5, vocabulary 1.25, and listening 1. Results are stored by level and exercise mode in the local `desempenho.sqlite3` database.
