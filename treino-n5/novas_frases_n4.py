"""Add 300 concise N4 sentences using annotated vocabulary themes."""

from cenarios_n4 import VOCAB, make_token, reading

# Each row has a short Japanese pattern, its N4 grammar focus and full translation.
PATTERNS = [
    ("X について 話してもいいですか", "てもいい", "Posso falar sobre {meaning}?"),
    ("X について 話そうと思います", "ようと思う", "Pretendo falar sobre {meaning}."),
    ("X について 話すことにしました", "ことにする", "Decidi falar sobre {meaning}."),
    ("X について 話すことになりました", "ことになる", "Ficou decidido que falarei sobre {meaning}."),
    ("X について 話してよかったです", "てよかった", "Foi bom ter falado sobre {meaning}."),
    ("X について 話したばかりです", "たばかり", "Acabei de falar sobre {meaning}."),
    ("X について 話したところです", "たところ", "Acabei de falar sobre {meaning}."),
    ("X について 話しているところです", "ているところ", "Estou falando sobre {meaning} agora."),
    ("X について 話し続けています", "続ける", "Continuo falando sobre {meaning}."),
    ("X について 話し始めました", "始める", "Comecei a falar sobre {meaning}."),
    ("X について 聞けば分かります", "ば", "Se perguntar sobre {meaning}, entenderá."),
    ("X について 調べておきます", "ておく", "Vou pesquisar {meaning} com antecedência."),
    ("X について 調べながら書きます", "ながら", "Escrevo enquanto pesquiso {meaning}."),
    ("X について 調べなければなりません", "なければならない", "Preciso pesquisar {meaning}."),
    ("X について 調べる必要があります", "必要がある", "É necessário pesquisar {meaning}."),
    ("X について 調べたはずです", "はずだ", "Acredito que pesquisei {meaning}."),
    ("X について 調べたことがあります", "たことがある", "Já pesquisei {meaning}."),
    ("X について 調べてしまいました", "てしまう", "Acabei pesquisando {meaning}."),
    ("X について 調べているところです", "ているところ", "Estou pesquisando {meaning} agora."),
    ("X について 調べたらどうですか", "たらどう", "Que tal pesquisar {meaning}?"),
    ("X について 教えてほしいです", "てほしい", "Quero que me conte sobre {meaning}."),
    ("X について 教えていただけませんか", "ていただけませんか", "Poderia me contar sobre {meaning}?"),
    ("X について 教えてもらいました", "てもらう", "Alguém me explicou sobre {meaning}."),
    ("X について 教えてくれました", "てくれる", "Alguém me contou sobre {meaning}."),
    ("X について 考えたことがあります", "たことがある", "Já pensei sobre {meaning}."),
    ("X について 考えながら歩きます", "ながら", "Caminho enquanto penso sobre {meaning}."),
    ("X について 考えているところです", "ているところ", "Estou pensando sobre {meaning} agora."),
    ("X について 考えても分かりません", "ても", "Mesmo pensando sobre {meaning}, não entendo."),
    ("X について 考えるようになりました", "ようになる", "Passei a pensar sobre {meaning}."),
    ("X について 考えようと思います", "ようと思う", "Pretendo pensar sobre {meaning}."),
]

GLOSS = {
    "について": ("について", "estrutura gramatical", ["sobre", "a respeito de"]),
    "話してもいいですか": ("はなしてもいいですか", "estrutura gramatical", ["posso falar?", "é permitido falar?"]),
    "話そうと思います": ("はなそうとおもいます", "estrutura gramatical", ["pretendo falar", "penso em conversar"]),
    "話すことにしました": ("はなすことにしました", "estrutura gramatical", ["decidi falar"]),
    "話すことになりました": ("はなすことになりました", "estrutura gramatical", ["ficou decidido que falarei"]),
    "話してよかったです": ("はなしてよかったです", "estrutura gramatical", ["foi bom falar"]),
    "話したばかりです": ("はなしたばかりです", "estrutura gramatical", ["acabei de falar", "falei há pouco"]),
    "話したところです": ("はなしたところです", "estrutura gramatical", ["acabei de falar"]),
    "話しているところです": ("はなしているところです", "estrutura gramatical", ["estou falando agora"]),
    "話し続けています": ("はなしつづけています", "estrutura gramatical", ["continuo falando"]),
    "話し始めました": ("はなしはじめました", "estrutura gramatical", ["comecei a falar"]),
    "聞けば分かります": ("きけばわかります", "estrutura gramatical", ["se perguntar, entenderá"]),
    "調べておきます": ("しらべておきます", "estrutura gramatical", ["pesquisarei antes", "deixarei pesquisado"]),
    "調べながら書きます": ("しらべながらかきます", "estrutura gramatical", ["escrevo enquanto pesquiso"]),
    "調べなければなりません": ("しらべなければなりません", "estrutura gramatical", ["preciso pesquisar", "devo pesquisar"]),
    "調べる必要があります": ("しらべるひつようがあります", "estrutura gramatical", ["é necessário pesquisar"]),
    "調べたはずです": ("しらべたはずです", "estrutura gramatical", ["devo ter pesquisado", "acredito que pesquisei"]),
    "調べたことがあります": ("しらべたことがあります", "estrutura gramatical", ["já pesquisei antes"]),
    "調べてしまいました": ("しらべてしまいました", "estrutura gramatical", ["acabei pesquisando"]),
    "調べているところです": ("しらべているところです", "estrutura gramatical", ["estou pesquisando agora"]),
    "調べたらどうですか": ("しらべたらどうですか", "estrutura gramatical", ["que tal pesquisar?"]),
    "教えてほしいです": ("おしえてほしいです", "estrutura gramatical", ["quero que me conte", "gostaria que me ensinasse"]),
    "教えていただけませんか": ("おしえていただけませんか", "estrutura gramatical", ["poderia me contar?", "poderia me ensinar?"]),
    "教えてもらいました": ("おしえてもらいました", "estrutura gramatical", ["recebi uma explicação", "alguém me ensinou"]),
    "教えてくれました": ("おしえてくれました", "estrutura gramatical", ["alguém me contou", "alguém me ensinou"]),
    "考えたことがあります": ("かんがえたことがあります", "estrutura gramatical", ["já pensei antes"]),
    "考えながら歩きます": ("かんがえながらあるきます", "estrutura gramatical", ["caminho enquanto penso"]),
    "考えているところです": ("かんがえているところです", "estrutura gramatical", ["estou pensando agora"]),
    "考えても分かりません": ("かんがえてもわかりません", "estrutura gramatical", ["mesmo pensando, não entendo"]),
    "考えるようになりました": ("かんがえるようになりました", "estrutura gramatical", ["passei a pensar"]),
    "考えようと思います": ("かんがえようとおもいます", "estrutura gramatical", ["pretendo pensar"]),
}


def grammar_token(surface):
    kana, kind, meanings = GLOSS[surface]
    return {"surface": surface, "reading": kana, "kind": kind,
            "meanings_pt": meanings, "note_pt": "Estrutura N4 usada nesta frase."}


def append_short_phrases(phrases):
    rows = [line.split("|", 1) for line in VOCAB.splitlines()]
    vocabulary = [(word, meaning, reading(word)) for word, meaning in rows]
    existing = {phrase["text"] for phrase in phrases}
    for index in range(300):
        word, meaning, kana = vocabulary[index % len(vocabulary)]
        for shift in range(len(PATTERNS)):
            pattern, grammar, translation = PATTERNS[(index + shift) % len(PATTERNS)]
            parts = pattern.split()
            tokens = [make_token("X", (word, meaning, kana)) if part == "X" else grammar_token(part) for part in parts]
            text = "".join(token["surface"] for token in tokens) + "。"
            if len(text) <= 25 and text not in existing:
                break
        else:
            raise ValueError(f"No short N4 sentence for {word}")
        existing.add(text)
        phrases.append({"id": 1901 + index, "level": "N4", "category": "gramática e vocabulário N4",
                        "grammar_point": grammar, "theme": f"{word} ({meaning})",
                        "text": text, "translation_pt": translation.format(meaning=meaning),
                        "tokens": tokens, "focus_token_indices": [0, len(tokens) - 1], "display_after": []})
    return phrases
