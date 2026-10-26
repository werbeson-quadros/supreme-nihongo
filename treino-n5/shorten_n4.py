"""Replace the 200 longest generated N4 entries with short, annotated ones."""

from collections import defaultdict

# Only the source clauses above 20 characters need a new, shorter clause.
SHORT_CORES = {
    "間（あいだ）": ("先生 が 話している 間 書いていました", "enquanto o professor falava, eu escrevia"),
    "ことができる": ("漢字 を 覚える ことができる", "consigo memorizar kanji"),
    "ことになる": ("来月 から 勉強 する ことになりました", "ficou decidido que estudarei a partir do mês que vem"),
    "のに（目的）": ("言葉 を 覚える のに ノート を 使います", "uso um caderno para memorizar palavras"),
    "それでも": ("疲れましたが それでも 勉強 を 続けました", "estava cansado, mas mesmo assim continuei estudando"),
    "ということ": ("説明 が 大切だ ということ が 分かりました", "entendi que a explicação é importante"),
    "間に（あいだに）": ("先生 が いない 間に 宿題 を 終わらせました", "terminei a tarefa enquanto o professor estava fora"),
    "ことがある": ("漢字 を 読み間違える ことがある", "às vezes leio um kanji errado"),
    "の中で（のなかで）": ("三つ の 中で 説明 が 一番 分かりやすい", "entre os três, a explicação é a mais fácil de entender"),
    "そうに / そうな": ("友達 は 楽しそうに 本 を 読んでいます", "meu amigo lê um livro com ar de prazer"),
    "たらいいですか": ("だれ に 聞いたらいいですか", "a quem devo perguntar?"),
    "という": ("明日 試験 が ある という 話 を 聞きました", "ouvi dizer que haverá uma prova amanhã"),
    "ように / ような": ("上手に 話せる ように 練習 します", "pratico para conseguir falar bem"),
    "ぜひ": ("ぜひ 発表 を 聞きに来てください", "venha ouvir a apresentação, por favor"),
}

GLOSS = {
    "について": ("について", "estrutura gramatical", ["sobre", "a respeito de"]),
    "話してみます": ("はなしてみます", "estrutura gramatical", ["tentarei falar", "experimentarei conversar"]),
    "調べてみます": ("しらべてみます", "estrutura gramatical", ["tentarei pesquisar", "vou procurar saber"]),
    "の": ("の", "partícula", ["de", "liga substantivos"]),
    "話": ("はなし", "vocabulário N4", ["história", "conversa", "assunto"]),
    "を": ("を", "partícula", ["marca o objeto direto"]),
    "聞いたことがある": ("きいたことがある", "estrutura gramatical", ["já ouvi", "tenho experiência de ouvir"]),
    "なら": ("なら", "estrutura gramatical", ["se for", "quanto a"]),
    "先生": ("せんせい", "vocabulário N4", ["professor", "professora"]),
    "に": ("に", "partícula", ["a", "para", "marca o destinatário"]),
    "聞いてください": ("きいてください", "estrutura gramatical", ["pergunte, por favor", "escute, por favor"]),
    "考えています": ("かんがえています", "estrutura gramatical", ["estou pensando", "estou refletindo"]),
}

VOCAB_PATTERNS = [
    ("X について 話してみます", "てみる", "Vou tentar falar sobre {meaning}."),
    ("X について 調べてみます", "てみる", "Vou tentar pesquisar sobre {meaning}."),
    ("X の 話 を 聞いたことがある", "たことがある", "Já ouvi falar sobre {meaning}."),
    ("X なら 先生 に 聞いてください", "なら / てください", "Se for sobre {meaning}, pergunte ao professor."),
    ("X について 考えています", "ている", "Estou pensando sobre {meaning}."),
]


def vocab_token(surface):
    reading, kind, meanings = GLOSS[surface]
    return {"surface": surface, "reading": reading, "kind": kind,
            "meanings_pt": meanings, "note_pt": "Uso deste trecho na frase curta."}


def shorten_longest(phrases, rows, original_token):
    selected = sorted(phrases, key=lambda phrase: (-len(phrase["text"]), phrase["id"]))[:200]
    selected_ids = {phrase["id"] for phrase in selected}
    existing = {phrase["text"] for phrase in phrases if phrase["id"] not in selected_ids}
    original_counts = defaultdict(int)
    vocab_counts = defaultdict(int)

    for phrase in sorted(selected, key=lambda item: item["id"]):
        if phrase["id"] <= 1400:
            topic, source_core, source_pt = rows[(phrase["id"] - 1001) % len(rows)]
            core, translation = SHORT_CORES.get(topic, (source_core, source_pt))
            core_tokens = [original_token(part) for part in core.split()]
            occurrence = original_counts[topic]
            original_counts[topic] += 1
            prefix = None
            suffix = None
            question_or_command = core.endswith(("か", "かい", "かしら", "かな", "ください", "なさい"))
            if occurrence == 1:
                prefix = "あ" if question_or_command else None
                suffix = None if question_or_command else "ね"
            elif occurrence == 2:
                prefix = "ねえ" if question_or_command else None
                suffix = None if question_or_command else "よ"
            elif occurrence == 3:
                prefix = "あ"
            tokens = list(core_tokens)
            display_after = []
            if prefix:
                tokens.insert(0, {"surface": prefix, "reading": prefix, "kind": "interjeição",
                                  "meanings_pt": ["ah" if prefix == "あ" else "ei"],
                                  "note_pt": "Interjeição usada para iniciar a fala."})
                display_after = [{"index": 0, "text": "、"}]
                translation = ("Ah, " if prefix == "あ" else "Ei, ") + translation
            if suffix:
                tokens.append({"surface": suffix, "reading": suffix, "kind": "partícula final",
                               "meanings_pt": ["não é?" if suffix == "ね" else "viu", "ênfase na fala"],
                               "note_pt": "Partícula final da fala."})
                translation = translation.rstrip(".?!") + (", né?" if suffix == "ね" else ", viu.")
            comma = "、" if prefix else ""
            text = (prefix + comma if prefix else "") + "".join(token["surface"] for token in core_tokens) + (suffix or "") + "。"
            offset = 1 if prefix else 0
            focus = list(range(offset, offset + len(core_tokens)))
        else:
            anchor = next(token for token in phrase["tokens"] if token.get("note_pt", "").startswith("Tema desta cena"))
            meaning = anchor["meanings_pt"][0]
            occurrence = vocab_counts[anchor["surface"]]
            vocab_counts[anchor["surface"]] += 1
            for shift in range(len(VOCAB_PATTERNS)):
                pattern, topic, pt = VOCAB_PATTERNS[(occurrence + shift) % len(VOCAB_PATTERNS)]
                parts = pattern.split()
                tokens = [dict(anchor) if part == "X" else vocab_token(part) for part in parts]
                text = "".join(token["surface"] for token in tokens) + "。"
                if len(text) <= 20 and text not in existing:
                    break
            else:
                raise ValueError(f"No unique short sentence for {anchor['surface']}")
            translation = pt.format(meaning=meaning)
            phrase["grammar_point"] = topic
            phrase["category"] = "vocabulário N4"
            phrase["theme"] = f"{anchor['surface']} ({meaning})"
            display_after = []
            focus = [i for i, part in enumerate(parts) if part == "X" or tokens[i]["kind"] == "estrutura gramatical"]

        if len(text) > 20:
            raise ValueError(f"Short sentence exceeds 20 characters: {phrase['id']} ({len(text)})")
        if text in existing:
            raise ValueError(f"Duplicate short sentence: {phrase['id']} {text}")
        if len(focus) < 2:
            raise ValueError(f"Too few focus tokens: {phrase['id']}")
        existing.add(text)
        translation = translation[0].upper() + translation[1:] if translation else translation
        if translation and not translation.endswith((".", "?", "!")):
            translation += "."
        phrase.update(text=text, translation_pt=translation,
                      tokens=tokens, focus_token_indices=focus, display_after=display_after)

    return selected_ids
