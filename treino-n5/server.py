"""Local N5/N4/N3 trainer: static UI, VOICEVOX audio, and SQLite history."""
import json
import io
import hashlib
import random
import re
import sqlite3
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.parse
import urllib.request
import uuid
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = [json.loads((ROOT / f"Lista e Frases {level}.json").read_text(encoding="utf-8")) for level in ("N5", "N4", "N3")]
VIDEO_N4 = json.loads((ROOT / "Lista e Frases N4 - YouTube cy9P8f4lrEw.json").read_text(encoding="utf-8"))
ALL_DATA = DATA + [VIDEO_N4]
PHRASES = {p["id"]: p for corpus in ALL_DATA for p in corpus["phrases"]}
LEVEL_PHRASES = {level: [p for p in PHRASES.values() if p["level"] == level] for level in ("N5", "N4", "N3")}
LIST_PHRASES = {level:{"main":corpus["phrases"]} for level,corpus in zip(("N5","N4","N3"),DATA)}
LIST_PHRASES["N4"]["youtube:cy9P8f4lrEw"] = VIDEO_N4["phrases"]
DB = ROOT / "desempenho.sqlite3"
AUDIO_DIR = ROOT / "audio-cache"
VOICEVOX = "http://127.0.0.1:50021"
LOCK = threading.Lock()
SESSION_LOCK = threading.Lock()
SESSIONS = {}
ENGINE_PROCESS = None


def database():
    con = sqlite3.connect(DB, timeout=20)
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS attempts (
      id INTEGER PRIMARY KEY, phrase_id INTEGER NOT NULL, submitted TEXT NOT NULL,
      correct INTEGER NOT NULL, total INTEGER NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      detail_json TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS token_results (
      id INTEGER PRIMARY KEY, attempt_id INTEGER NOT NULL, token_key TEXT NOT NULL,
      surface TEXT NOT NULL, reading TEXT NOT NULL, kind TEXT NOT NULL,
      correct INTEGER NOT NULL, category TEXT NOT NULL DEFAULT 'Listening',
      FOREIGN KEY(attempt_id) REFERENCES attempts(id)
    );
    CREATE INDEX IF NOT EXISTS token_results_key ON token_results(token_key);
    CREATE TABLE IF NOT EXISTS review_saved (
      level TEXT NOT NULL, item_key TEXT NOT NULL, kind TEXT NOT NULL,
      text TEXT NOT NULL, reading TEXT NOT NULL, meaning TEXT NOT NULL,
      note TEXT NOT NULL DEFAULT '', phrase_id INTEGER,
      PRIMARY KEY(level, item_key)
    );
    CREATE TABLE IF NOT EXISTS review_removed (
      level TEXT NOT NULL, item_key TEXT NOT NULL,
      PRIMARY KEY(level, item_key)
    );
    """)
    attempt_columns = {row[1] for row in con.execute("PRAGMA table_info(attempts)")}
    token_columns = {row[1] for row in con.execute("PRAGMA table_info(token_results)")}
    if "mode" not in attempt_columns:
        con.execute("ALTER TABLE attempts ADD COLUMN mode TEXT NOT NULL DEFAULT 'Listening'")
    if "level" not in attempt_columns:
        con.execute("ALTER TABLE attempts ADD COLUMN level TEXT NOT NULL DEFAULT 'N5'")
    if "weight" not in token_columns:
        con.execute("ALTER TABLE token_results ADD COLUMN weight REAL NOT NULL DEFAULT 1.0")
    con.commit()
    return con


def norm(value):
    value = unicodedata.normalize("NFKC", value)
    return re.sub(r"[\s。、！？?!,.\-・「」『』]", "", value)


def review_key(kind, text):
    return f"{kind}:{norm(text)}"


def selected_review_item(phrase, selected):
    """Resolve a selection against stored phrase tokens, never client meanings."""
    selected = selected.strip()
    if not selected or len(selected) > 100 or not re.search(r"[\u3040-\u30ff\u3400-\u9fff]", selected):
        raise ValueError("Selecione até 100 caracteres japoneses da frase.")
    if norm(selected) == norm(phrase["text"]):
        return {"kind":"phrase", "text":phrase["text"],
                "reading":"".join(t["reading"] for t in phrase["tokens"]),
                "meaning":phrase["translation_pt"]}
    chosen = norm(selected)
    surfaces = norm("".join(t["surface"] for t in phrase["tokens"]))
    readings = norm("".join(t["reading"] for t in phrase["tokens"]))
    source = "surface" if chosen in surfaces else "reading" if chosen in readings else None
    if source is None:
        raise ValueError("O trecho selecionado não pertence à frase atual.")
    start = (surfaces if source == "surface" else readings).find(chosen)
    matching = []
    position = 0
    for token in phrase["tokens"]:
        end = position + len(norm(token[source]))
        if end > start and position < start + len(chosen):
            matching.append(token)
        position = end
    if not matching:
        raise ValueError("Nenhuma palavra correspondente foi encontrada.")
    return {"kind":"word" if len(matching) == 1 else "excerpt", "text":selected,
            "reading":"".join(t["reading"] for t in matching),
            "meaning":" · ".join("/".join(t["meanings_pt"]) for t in matching)}


def review_cards(level):
    """Return the 20 hardest active tokens plus saved words and sentences."""
    with database() as con:
        excluded = {row[0] for row in con.execute(
            "SELECT item_key FROM review_removed WHERE level=?", (level,))}
        ranked = con.execute("""SELECT tr.surface,tr.reading,tr.kind,
            COUNT(*)-SUM(tr.correct) AS errors,COUNT(*) AS attempts
            FROM token_results tr JOIN attempts a ON a.id=tr.attempt_id
            WHERE a.level=? GROUP BY tr.surface,tr.reading,tr.kind
            HAVING errors>0 ORDER BY errors DESC,
            1.0*SUM(tr.correct)/COUNT(*) ASC,attempts DESC""", (level,)).fetchall()
        saved = con.execute("""SELECT item_key,kind,text,reading,meaning,note
            FROM review_saved WHERE level=? ORDER BY rowid DESC""", (level,)).fetchall()
    glossary = {(t["surface"],t["reading"]): t for p in LEVEL_PHRASES[level] for t in p["tokens"]}
    cards = []
    seen = set()
    for surface,reading,kind,errors,attempts in ranked:
        key = review_key("word",surface)
        if key in excluded or key in seen: continue
        token = glossary.get((surface,reading))
        cards.append({"key":key,"kind":"word","text":surface,"reading":reading,
            "meaning":" · ".join(token["meanings_pt"]) if token else kind,
            "note":"","source":"mistakes","errors":errors,"attempts":attempts})
        seen.add(key)
        if len(cards) == 20: break
    saved_cards = []
    for key,kind,surface,reading,meaning,note in saved:
        if key in excluded: continue
        card = {"key":key,"kind":kind,"text":surface,"reading":reading,
                "meaning":meaning,"note":note,"source":"saved"}
        if key in seen:
            for existing in cards:
                if existing["key"] == key:
                    existing.update({"note":note,"meaning":meaning,"source":"mistakes + saved"})
                    break
        else:
            saved_cards.append(card)
            seen.add(key)
    return cards + saved_cards


def distance(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        row = [i]
        for j, cb in enumerate(b, 1):
            row.append(min(row[-1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = row
    return prev[-1]


def evaluate(phrase, submitted):
    """Align typed text to words; accept the written form or the kana reading."""
    typed = norm(submitted)
    tokens = phrase["tokens"]
    n = len(typed)
    # Each state stores (edit cost, number of exact tokens, previous position, token match).
    states = [{0: (0, 0, None, None)}]
    for token in tokens:
        alternatives = list(dict.fromkeys([norm(token["surface"]), norm(token["reading"])]))
        next_states = {}
        for start, (cost, exact_count, _, _) in states[-1].items():
            max_len = min(n - start, max(map(len, alternatives)) + 4)
            for length in range(max_len + 1):
                piece = typed[start:start + length]
                error = min(distance(piece, alt) for alt in alternatives)
                exact = error == 0 and bool(piece)
                score = (cost + error, -(exact_count + int(exact)))
                end = start + length
                old = next_states.get(end)
                if old is None or score < (old[0], -old[1]):
                    next_states[end] = (cost + error, exact_count + int(exact), start, {"typed":piece,"correct":exact,"distance":error})
        states.append(next_states)
    end = min(states[-1], key=lambda pos: (states[-1][pos][0] + n - pos, -states[-1][pos][1]))
    overflow = typed[end:]
    results = []
    for i in range(len(tokens), 0, -1):
        _, _, previous, match = states[i][end]
        results.append({**tokens[i - 1], **match})
        end = previous
    results.reverse()
    if overflow:
        results[-1]["typed"] += overflow
        results[-1]["correct"] = False
        results[-1]["distance"] += len(overflow)
    return results


def engine_request(path, data=None, content_type=None):
    headers = {"Content-Type":content_type} if content_type else {}
    req = urllib.request.Request(VOICEVOX + path, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def ensure_engine():
    global ENGINE_PROCESS
    try:
        engine_request("/version")
        return
    except Exception:
        pass
    with LOCK:
        try:
            engine_request("/version")
            return
        except Exception:
            pass
        gpu_exe = ROOT.parent / "voicevox" / "engine" / "windows-nvidia" / "run.exe"
        cpu_exe = ROOT.parent / "voicevox" / "engine" / "windows-cpu" / "run.exe"
        gpu_available = False
        try:
            result = subprocess.run(["nvidia-smi", "-L"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            gpu_available = result.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            pass
        if gpu_available and gpu_exe.exists():
            exe, use_gpu = gpu_exe, True
        elif cpu_exe.exists():
            exe, use_gpu = cpu_exe, False
        else:
            raise RuntimeError("VOICEVOX não encontrado. Execute voicevox/install.ps1.")
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        args = [str(exe), "--host", "127.0.0.1", "--port", "50021"]
        if use_gpu:
            args.append("--use_gpu")
        ENGINE_PROCESS = subprocess.Popen(args, cwd=str(exe.parent), creationflags=flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if ENGINE_PROCESS.poll() is not None:
                raise RuntimeError("O motor de áudio terminou durante a inicialização.")
            try:
                engine_request("/version")
                return
            except Exception:
                time.sleep(1)
        raise RuntimeError("O motor de áudio não respondeu em 60 segundos.")


def audio_for(phrase, speaker):
    AUDIO_DIR.mkdir(exist_ok=True)
    revision = "-" + hashlib.sha256(phrase["text"].encode("utf-8")).hexdigest()[:10] if phrase["level"] in ("N4", "N3") else ""
    path = AUDIO_DIR / f"{phrase['id']:03d}-voz-{speaker}{revision}.wav"
    if not path.exists():
        with LOCK:
            if not path.exists():
                query = engine_request("/audio_query?" + urllib.parse.urlencode({"speaker":speaker,"text":phrase["text"]}), data=b"")
                wav = engine_request("/synthesis?" + urllib.parse.urlencode({"speaker":speaker}), data=query, content_type="application/json")
                path.write_bytes(wav)
    return path.read_bytes()


PARTICLE_SURFACES = {"は", "が", "を", "に", "へ", "で", "と", "も", "の", "か", "ね", "よ", "や", "から", "まで", "だけ"}


def spaced_segments(phrase):
    """Keep each particle with the words before it, then mark a pause."""
    decorated = []
    position = 0
    for token in phrase["tokens"]:
        surface = token["surface"]
        start = phrase["text"].find(surface, position)
        if start < 0:
            raise ValueError(f"Texto e trechos não coincidem na frase {phrase['id']}.")
        punctuation = phrase["text"][position:start]
        if decorated:
            decorated[-1] += punctuation
        decorated.append(surface)
        position = start + len(surface)
    decorated[-1] += phrase["text"][position:]
    segments = []
    current = ""
    for index, token in enumerate(phrase["tokens"]):
        current += decorated[index]
        if index < len(phrase["tokens"]) - 1 and (token["surface"] in PARTICLE_SURFACES or token["kind"].startswith("partícula")):
            segments.append((current, True))
            current = ""
    if current:
        segments.append((current, False))
    return segments


def spaced_audio_for(phrase, speaker):
    AUDIO_DIR.mkdir(exist_ok=True)
    revision = hashlib.sha256(phrase["text"].encode("utf-8")).hexdigest()[:10]
    path = AUDIO_DIR / f"{phrase['id']:03d}-voz-{speaker}-{revision}-particulas-v2.wav"
    if not path.exists():
        with LOCK:
            if not path.exists():
                chunks = []
                audio_format = None
                for text, pause_after in spaced_segments(phrase):
                    query = json.loads(engine_request("/audio_query?" + urllib.parse.urlencode({"speaker": speaker, "text": text}), data=b""))
                    query["prePhonemeLength"] = 0
                    query["postPhonemeLength"] = 0
                    wav = engine_request("/synthesis?" + urllib.parse.urlencode({"speaker": speaker}),
                                         data=json.dumps(query, ensure_ascii=False).encode("utf-8"), content_type="application/json")
                    with wave.open(io.BytesIO(wav), "rb") as reader:
                        fmt = (reader.getnchannels(), reader.getsampwidth(), reader.getframerate())
                        if audio_format is not None and fmt != audio_format:
                            raise RuntimeError("Os trechos de áudio têm formatos incompatíveis.")
                        audio_format = fmt
                        chunks.append(reader.readframes(reader.getnframes()))
                        if pause_after:
                            chunks.append(b"\0" * round(reader.getframerate() * 0.5) * reader.getnchannels() * reader.getsampwidth())
                output = io.BytesIO()
                with wave.open(output, "wb") as writer:
                    writer.setnchannels(audio_format[0])
                    writer.setsampwidth(audio_format[1])
                    writer.setframerate(audio_format[2])
                    writer.writeframes(b"".join(chunks))
                path.write_bytes(output.getvalue())
    return path.read_bytes()


def selection_audio_for(text, speaker):
    """Small, cached audio clips for selected Japanese text."""
    AUDIO_DIR.mkdir(exist_ok=True)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]
    path = AUDIO_DIR / f"selection-{digest}-voz-{speaker}.wav"
    if not path.exists():
        with LOCK:
            if not path.exists():
                query = engine_request("/audio_query?" + urllib.parse.urlencode({"speaker":speaker,"text":text}), data=b"")
                wav = engine_request("/synthesis?" + urllib.parse.urlencode({"speaker":speaker}), data=query, content_type="application/json")
                path.write_bytes(wav)
    return path.read_bytes()


def voices():
    ensure_engine()
    speakers = json.loads(engine_request("/speakers"))
    return [{"id":style["id"],"label":f"{speaker['name']} · {style['name']}"}
            for speaker in speakers for style in speaker["styles"]
            if "talk" in style.get("type","talk")]


def skill_for(token):
    kind = token["kind"]
    if kind in ("partícula", "partícula final", "estrutura gramatical", "cópula polida"):
        return "Grammar", 1.5
    return "Vocabulary", 1.25


def choose_blanks(phrase):
    tokens = phrase["tokens"]
    indices = phrase.get("focus_token_indices", []) if phrase["level"] in ("N4", "N3") else list(range(len(tokens)))
    if not indices: indices = list(range(len(tokens)))
    grammar = [i for i in indices if skill_for(tokens[i])[0] == "Grammar"]
    vocabulary = [i for i in indices if skill_for(tokens[i])[0] == "Vocabulary"]
    maximum = min(4, len(indices), len(tokens) - 1)
    focus = [i for i in phrase.get("focus_token_indices", []) if i in indices]
    picked = {random.choice(focus)} if focus else set()
    if grammar and not (picked & set(grammar)) and len(picked) < maximum:
        picked.add(random.choice(grammar))
    if vocabulary and not (picked & set(vocabulary)) and len(picked) < maximum:
        picked.add(random.choice(vocabulary))
    count = random.randint(max(2,len(picked)),maximum)
    picked.update(random.sample([i for i in indices if i not in picked], count - len(picked)))
    return sorted(picked)


def cloze_choices(phrase, blanks):
    """Offer every missing surface among ten unique, same-level words."""
    answers = {phrase["tokens"][i]["surface"] for i in blanks}
    visible = {token["surface"] for i, token in enumerate(phrase["tokens"]) if i not in blanks}
    pool = {token["surface"] for item in LEVEL_PHRASES[phrase["level"]]
            for token in item["tokens"] if token["surface"] not in answers | visible}
    choices = list(answers) + random.sample(sorted(pool), 10 - len(answers))
    random.shuffle(choices)
    return choices


def save_attempt(phrase, submitted, results, mode):
    correct = sum(r["correct"] for r in results)
    with database() as con:
        cursor = con.execute("INSERT INTO attempts(phrase_id,submitted,correct,total,detail_json,mode,level) VALUES(?,?,?,?,?,?,?)",
            (phrase["id"], submitted, correct, len(results), json.dumps(results, ensure_ascii=False), mode, phrase["level"]))
        for result in results:
            category, weight = ("Listening", 1.0) if mode == "Listening" else skill_for(result)
            key = f"{result['surface']}|{result['reading']}|{result['kind']}"
            con.execute("""INSERT INTO token_results(attempt_id,token_key,surface,reading,kind,correct,category,weight)
                VALUES(?,?,?,?,?,?,?,?)""",
                (cursor.lastrowid,key,result["surface"],result["reading"],result["kind"],int(result["correct"]),category,weight))
    return cursor.lastrowid, correct


class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, code, data, content_type):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, code, value):
        self.send_bytes(code, json.dumps(value, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        try:
            path = urllib.parse.urlsplit(self.path).path
            if path in ("/", "/index.html"):
                return self.send_bytes(200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")
            if path == "/style.css":
                return self.send_bytes(200, (ROOT / "style.css").read_bytes(), "text/css; charset=utf-8")
            if path == "/app.js":
                return self.send_bytes(200, (ROOT / "app.js").read_bytes(), "application/javascript; charset=utf-8")
            if path == "/api/next":
                query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                level = query.get("level", ["N5"])[0]
                if level not in LEVEL_PHRASES: return self.send_json(400,{"error":"Nível inválido"})
                list_id = query.get("list", ["main"])[0]
                if list_id not in LIST_PHRASES[level]: return self.send_json(400,{"error":"Lista inválida"})
                with database() as con:
                    recent = [row[0] for row in con.execute("SELECT phrase_id FROM attempts WHERE level=? ORDER BY id DESC LIMIT 8",(level,))]
                options = [p for p in LIST_PHRASES[level][list_id] if p["id"] not in recent] or LIST_PHRASES[level][list_id]
                choice = random.choice(options)
                return self.send_json(200, {"id":choice["id"],"level":level,"list_id":list_id,"category":choice.get("grammar_point",choice["category"]),"glossary":choice["tokens"]})
            if path == "/api/cloze/next":
                query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                level = query.get("level", ["N5"])[0]
                if level not in LEVEL_PHRASES: return self.send_json(400,{"error":"Nível inválido"})
                list_id = query.get("list", ["main"])[0]
                if list_id not in LIST_PHRASES[level]: return self.send_json(400,{"error":"Lista inválida"})
                with database() as con:
                    recent = [row[0] for row in con.execute("SELECT phrase_id FROM attempts WHERE level=? AND mode='Writing' ORDER BY id DESC LIMIT 8",(level,))]
                options = [p for p in LIST_PHRASES[level][list_id] if p["id"] not in recent and len(p["tokens"]) >= 3]
                choice = random.choice(options or LIST_PHRASES[level][list_id])
                blanks = choose_blanks(choice)
                exercise_id = uuid.uuid4().hex
                with SESSION_LOCK:
                    SESSIONS[exercise_id] = (choice["id"], blanks, time.time())
                    for key, (_, _, created) in list(SESSIONS.items()):
                        if time.time() - created > 3600: SESSIONS.pop(key, None)
                display_parts=[]
                insertions={item["index"]:item["text"] for item in choice.get("display_after",[])}
                for i,word in enumerate(choice["tokens"]):
                    display_parts.append({"index":i,"surface":None if i in blanks else word["surface"],"blank":i in blanks})
                    if i in insertions: display_parts.append({"index":-1,"surface":insertions[i],"blank":False})
                return self.send_json(200, {"exercise_id":exercise_id,"id":choice["id"],"level":level,"list_id":list_id,"glossary":choice["tokens"],
                    "category":choice.get("grammar_point",choice["category"]),"translation_pt":choice["translation_pt"],
                    "punctuation":choice["text"][-1],
                    "parts":display_parts,"choices":cloze_choices(choice,blanks)})
            if path == "/api/voices":
                return self.send_json(200, {"voices":voices()})
            if path == "/api/metadata":
                levels = {level:{"phrase_count":len(items),"grammar_topics":len({p.get("grammar_point") for p in items if p.get("grammar_point")}),
                    "lists":[{"id":list_id,"title":DATA[("N5","N4","N3").index(level)]["title"] if list_id == "main" else VIDEO_N4["title"],
                              "phrase_count":len(phrases)} for list_id,phrases in LIST_PHRASES[level].items()]}
                    for level,items in LEVEL_PHRASES.items()}
                return self.send_json(200,{"phrase_count":len(PHRASES),"levels":levels})
            if path == "/api/review":
                level = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query).get("level", ["N5"])[0]
                if level not in LEVEL_PHRASES: return self.send_json(400,{"error":"Nível inválido"})
                return self.send_json(200,{"level":level,"cards":review_cards(level)})
            if path == "/api/stats":
                with database() as con:
                    summary = con.execute("""SELECT level,mode,COUNT(*),COALESCE(SUM(correct),0),COALESCE(SUM(total),0)
                        FROM attempts GROUP BY level,mode""").fetchall()
                    scores = con.execute("""SELECT attempts.level,attempts.mode,SUM(token_results.weight*token_results.correct),
                        SUM(token_results.weight) FROM token_results JOIN attempts ON attempts.id=token_results.attempt_id
                        GROUP BY attempts.level,attempts.mode""").fetchall()
                    rows = con.execute("""SELECT attempts.level,attempts.mode,token_results.surface,token_results.reading,
                        token_results.kind, COUNT(*), SUM(token_results.correct), token_results.category
                        FROM token_results JOIN attempts ON attempts.id=token_results.attempt_id
                        GROUP BY attempts.level,attempts.mode,token_results.token_key,token_results.category
                        HAVING SUM(token_results.correct) < COUNT(*)
                        ORDER BY (COUNT(*)-SUM(token_results.correct)) DESC,
                            (1.0*SUM(token_results.correct)/COUNT(*)) ASC""").fetchall()
                metrics = {(level,mode):{"attempts":count,"correct_tokens":correct,"total_tokens":total,
                    "earned_weight":0,"possible_weight":0,"needs_practice":[]}
                    for level,mode,count,correct,total in summary}
                for level,mode,earned,possible in scores:
                    metrics[(level,mode)]["earned_weight"] = earned or 0
                    metrics[(level,mode)]["possible_weight"] = possible or 0
                for level,mode,surface,reading,kind,count,correct,category in rows:
                    if len(metrics[(level,mode)]["needs_practice"]) < 20:
                        metrics[(level,mode)]["needs_practice"].append({"surface":surface,"reading":reading,
                            "kind":kind,"attempts":count,"correct":correct,"category":category})
                return self.send_json(200,{"levels":{level:{mode:metrics.get((level,mode)) for mode in ("Listening","Writing")} for level in LEVEL_PHRASES}})
            if path == "/api/selection-audio":
                query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                selected = query.get("text",[""])[0].strip()
                if not selected or len(selected) > 100 or not re.search(r"[\u3040-\u30ff\u3400-\u9fff]", selected):
                    return self.send_json(400,{"error":"Selecione até 100 caracteres japoneses"})
                try: speaker = int(query.get("speaker",[2])[0])
                except (ValueError,TypeError): return self.send_json(400,{"error":"Voz inválida"})
                if speaker not in {v["id"] for v in voices()}:
                    return self.send_json(400,{"error":"Voz indisponível"})
                return self.send_bytes(200,selection_audio_for(selected,speaker),"audio/wav")
            match = re.fullmatch(r"/api/audio/(\d+)", path)
            if match:
                phrase = PHRASES.get(int(match.group(1)))
                if phrase is None: return self.send_json(404,{"error":"Frase não encontrada"})
                query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                try: speaker = int(query.get("speaker",[2])[0])
                except (ValueError,TypeError): return self.send_json(400,{"error":"Voz inválida"})
                if speaker not in {v["id"] for v in voices()}:
                    return self.send_json(400,{"error":"Voz indisponível"})
                ensure_engine()
                spaced = query.get("spaced", ["0"])[0] == "1"
                return self.send_bytes(200, spaced_audio_for(phrase,speaker) if spaced else audio_for(phrase,speaker), "audio/wav")
            return self.send_json(404,{"error":"Rota não encontrada"})
        except Exception as exc:
            self.send_json(500,{"error":str(exc)})

    def do_POST(self):
        try:
            if self.path not in ("/api/submit", "/api/cloze/submit", "/api/review/save", "/api/review/note", "/api/review/remove"):
                return self.send_json(404,{"error":"Rota não encontrada"})
            length = int(self.headers.get("Content-Length","0"))
            if length > 8192: return self.send_json(413,{"error":"Resposta muito longa"})
            body = json.loads(self.rfile.read(length))
            if self.path.startswith("/api/review/"):
                level = body.get("level")
                if level not in LEVEL_PHRASES: return self.send_json(400,{"error":"Nível inválido"})
                if self.path == "/api/review/save":
                    phrase = PHRASES.get(body.get("phrase_id"))
                    if phrase is None or phrase["level"] != level:
                        return self.send_json(400,{"error":"Frase inválida para este nível"})
                    try: item = selected_review_item(phrase,str(body.get("text","")))
                    except ValueError as exc: return self.send_json(400,{"error":str(exc)})
                    key = review_key(item["kind"],item["text"])
                    with database() as con:
                        con.execute("""INSERT INTO review_saved(level,item_key,kind,text,reading,meaning,phrase_id)
                            VALUES(?,?,?,?,?,?,?) ON CONFLICT(level,item_key) DO UPDATE SET
                            reading=excluded.reading,meaning=excluded.meaning,phrase_id=excluded.phrase_id""",
                            (level,key,item["kind"],item["text"],item["reading"],item["meaning"],phrase["id"]))
                        con.execute("DELETE FROM review_removed WHERE level=? AND item_key=?",(level,key))
                    return self.send_json(200,{"saved":True,"key":key,"item":item})
                key = str(body.get("key",""))
                if not key or len(key)>120:
                    return self.send_json(400,{"error":"Cartão inválido"})
                card = next((c for c in review_cards(level) if c["key"] == key),None)
                if card is None: return self.send_json(404,{"error":"Cartão não encontrado"})
                if self.path == "/api/review/remove":
                    with database() as con:
                        con.execute("INSERT OR IGNORE INTO review_removed(level,item_key) VALUES(?,?)",(level,key))
                        con.execute("DELETE FROM review_saved WHERE level=? AND item_key=?",(level,key))
                    return self.send_json(200,{"removed":True})
                note = str(body.get("note",""))
                if len(note)>2000: return self.send_json(400,{"error":"Nota muito longa"})
                with database() as con:
                    con.execute("""INSERT INTO review_saved(level,item_key,kind,text,reading,meaning,note)
                        VALUES(?,?,?,?,?,?,?) ON CONFLICT(level,item_key) DO UPDATE SET note=excluded.note""",
                        (level,key,card["kind"],card["text"],card["reading"],card["meaning"],note))
                return self.send_json(200,{"saved":True,"note":note})
            if self.path == "/api/cloze/submit":
                exercise_id = str(body.get("exercise_id",""))
                with SESSION_LOCK:
                    session = SESSIONS.pop(exercise_id, None)
                if session is None or time.time() - session[2] > 3600:
                    return self.send_json(400,{"error":"Exercício expirado. Abra outra frase."})
                phrase_id, blanks, _ = session
                phrase = PHRASES[phrase_id]
                answers = body.get("answers",{})
                if not isinstance(answers,dict):
                    return self.send_json(400,{"error":"Respostas inválidas"})
                results = []
                for index in blanks:
                    token = phrase["tokens"][index]
                    typed = str(answers.get(str(index),""))[:100]
                    accepted = {norm(token["surface"]), norm(token["reading"])}
                    category, weight = skill_for(token)
                    results.append({**token,"index":index,"typed":typed,
                        "correct":bool(norm(typed)) and norm(typed) in accepted,
                        "category":category,"weight":weight})
                submitted = json.dumps(answers,ensure_ascii=False)
                attempt_id, correct = save_attempt(phrase,submitted,results,"Writing")
                return self.send_json(200,{"mode":"Writing","phrase":phrase,"results":results,
                    "correct":correct,"total":len(results),"attempt_id":attempt_id})
            phrase = PHRASES.get(int(body.get("id",0)))
            submitted = str(body.get("text",""))
            if phrase is None or not norm(submitted): return self.send_json(400,{"error":"Informe uma frase válida"})
            results = evaluate(phrase,submitted)
            attempt_id, correct = save_attempt(phrase,submitted,results,"Listening")
            self.send_json(200,{"mode":"Listening","phrase":phrase,"submitted":submitted,
                "results":results,"correct":correct,"total":len(results),"attempt_id":attempt_id})
        except Exception as exc:
            self.send_json(500,{"error":str(exc)})


class LocalHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = False


if __name__ == "__main__":
    database().close()
    server = LocalHTTPServer(("127.0.0.1",8765),Handler)
    print("Treino N5: http://127.0.0.1:8765",flush=True)
    server.serve_forever()
