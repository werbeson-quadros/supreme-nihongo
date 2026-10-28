# N5, N4, and N3 Listening and Writing Practice

Run `iniciar.ps1` in PowerShell. The interface opens at <http://127.0.0.1:8765/>.

The N5 corpus contains 520 sentences, including five examples for each of 84 requested grammar topics. The N4 corpus contains 1,200 sentences: 400 started from 132 grammar topics, 500 combine vocabulary themes with conversation, classroom, research, family, and travel scenarios, and 300 new entries practice short N4 structures with vocabulary themes. The 200 longest entries from the previous 900-sentence corpus were replaced by sentences of at most 20 Japanese characters; the newest 300 have at most 25. The N3 corpus contains 300 sentences across 20 grammar patterns and everyday situations; each is at most 20 Japanese characters. Each sentence has a full Brazilian Portuguese translation. Its tokens carry written forms, readings, types, meanings, and usage notes.

`gerar_frases.py`, `gramatica_extra.py`, `gerar_frases_n4.py`, `cenarios_n4.py`, `shorten_n4.py`, `novas_frases_n4.py`, and `gerar_frases_n3.py` are the editable corpus generators. Regenerating the additional N4 sentences requires a running VOICEVOX Engine to obtain readings. The N3 generator reuses the annotated N4 vocabulary and needs no voice engine.

The N3 grammar selection follows the [JLPT Sensei N3 study list](https://jlptsensei.com/jlpt-n3-grammar-list/). The JLPT does not publish a fixed official grammar or vocabulary list, so level labels are study classifications rather than guarantees about exam content.

The N4 list selector includes 55 sentences under the title of [JLPT N4 LISTENING PRACTICE TEST WITH ANSWERS 2026.ちょうかい](https://www.youtube.com/watch?v=cy9P8f4lrEw): 40 curated from its Japanese auto-generated captions and 15 supplied by the user for the same list. They are longer than 10 Japanese characters, end at `。`, and contain no exact duplicates within the video list or the original N4 corpus. Obvious transcription errors in the supplied text were corrected for study use. Captions with clear recognition errors or merged speakers were omitted. The raw caption download is kept locally at `treino-n5/imports/youtube-cy9P8f4lrEw-ja-auto.txt` and excluded from Git; `importar_legenda_n4.py` documents the selections and can regenerate the JSON when the local caption file and VOICEVOX are available.

VOICEVOX generates the audio. The voice selector lists available speakers and styles. The player supports play/pause, speeds from 0.5× to 2×, and an optional 0.5-second pause after each identified particle. Generated audio is cached under `audio-cache/`. The selected speed and particle-pause setting persist in the browser.

The answer dialog also includes a Japanese audio player. Selecting Japanese text in an exercise or answer reads it aloud repeatedly until the selection is cleared. A small tooltip shows meanings from the current sentence's glossary. If the browser has no Japanese voice, the app uses a short locally generated audio clip.

In **Listening** mode, the learner transcribes the audio. Written forms and kana readings are accepted, while whitespace and punctuation are ignored. Token alignment is approximate when a response contains several errors.

In **Complete the sentence** mode, the Portuguese translation is the goal and two to four Japanese spans are blank. Only the blanks are scored. Grammar has a weight of 1.5, vocabulary 1.25, and listening 1. Results are stored by level and exercise mode in the local `desempenho.sqlite3` database.

Selecting Japanese text in a phrase opens a meaning tooltip with a save button. **Review** opens level-specific flashcards: up to 20 terms with the most recorded mistakes, plus saved words, excerpts, and complete sentences. Flip a card to see its reading and Portuguese meaning, add a personal note, or play its audio at 0.85×. Automatic review shows the front for two seconds, flips and plays audio, then advances after another two seconds. Removing a card excludes it from future reviews until the same text is saved again. Review data stays in the local SQLite database.
