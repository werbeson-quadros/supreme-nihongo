"""Build 300 short N3 examples from distinct everyday scenario prompts.

Each row is an independently named situation. Vocabulary comes from the
existing N4 corpus, so N3 learners only meet words at or below their level.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = json.loads((ROOT / "Lista e Frases N4.json").read_text(encoding="utf-8"))
LEXICON = {token["surface"]: token for phrase in SOURCE["phrases"] for token in phrase["tokens"]}

# N3 patterns: (grammar point, fixed prefix, fixed suffix, Portuguese goal,
#               15 vocabulary-led situations). X is replaced with the focus noun.
SCENARIOS = [
    ("べきだ", "", "を大切にすべきです", "Devemos valorizar {the}.",
     "挨拶 文化 安全 時間 約束 家族 友達 教育 自由 生命 自然 意見 習慣 技術 生活"),
    ("べきではない", "", "を忘れるべきではない", "Não se deve esquecer {the}.",
     "返事 注意 お礼 予習 復習 住所 予約 用事 予定 原因 理由 文法 発音 歴史 法律"),
    ("代わりに", "", "の代わりに電話します", "Ligarei no lugar {of}.",
     "先生 友達 妹 弟 息子 娘 妻 部長 社長 先輩 店員 運転手 大学生 アナウンサー 歯医者"),
    ("結局", "結局", "を選びました", "No fim, escolhi {the}.",
     "着物 手袋 指輪 人形 おもちゃ 贈り物 お土産 サンダル スーツ サラダ ステーキ ジャム 米 味噌 ぶどう"),
    ("だらけ", "", "はごみだらけです", "{The} está com muito lixo.",
     "駐車場 海岸 公園 駅 屋上 港 島 林 森 道 教室 会議室 事務所 工場 旅館"),
    ("気味", "", "は疲れ気味です", "{The} apresenta sinais de cansaço.",
     "先生 友達 部長 社長 先輩 店員 大学生 アナウンサー 運転手 息子 娘 妻 妹 弟 赤ちゃん"),
    ("ごとに", "", "ごとに確認します", "Confiro cada {x}.",
     "席 部屋 教室 会議室 学校 病院 銀行 郵便局 図書館 美術館 動物園 工場 旅館 空港 駐車場"),
    ("ほど～ない", "", "ほど高くないです", "Isto não custa tanto quanto {the}.",
     "パソコン コンピュータ スーツケース ハンドバッグ オートバイ 自転車 テニス ステレオ ピアノ 指輪 アクセサリー 着物 スーツ 布団 カーテン"),
    ("一度に", "", "を一度に運びました", "Transportei {the} de uma só vez.",
     "本 辞典 テキスト レポート 新聞 写真 紙 絵 道具 食料品 品物 おもちゃ お土産 プレゼント サンドイッチ"),
    ("一方だ", "", "は増える一方です", "{The} continua aumentando.",
     "人口 値段 ごみ 事故 交通 熱 仕事 予定 用事 相談 競争 生産 貿易 連絡 放送"),
    ("ふりをする", "", "は寝たふりをしました", "{The} fingiu estar dormindo.",
     "赤ちゃん 息子 娘 妹 弟 友達 先輩 大学生 先生 部長 社長 店員 運転手 妻 泥棒"),
    ("かける", "", "を読みかけました", "Comecei a ler {the}, mas parei.",
     "本 辞典 テキスト レポート 新聞 小説 漫画 文学 歴史 文法 例文 資料 手紙 翻訳 説明"),
    ("おかげで", "", "のおかげで助かりました", "Consegui ajuda graças {to}.",
     "先生 友達 家族 先輩 妹 弟 息子 娘 妻 部長 店員 道具 技術 案内 連絡"),
    ("せいで", "", "のせいで遅れました", "Atrasei-me por causa {of}.",
     "雨 台風 地震 事故 交通 故障 雪 火事 霧 風 熱 病院 約束 会議 工事"),
    ("に関して", "", "に関して調べます", "Vou pesquisar sobre {the}.",
     "医学 科学 政治 経済 社会 教育 文化 文学 地理 歴史 法律 生物 生命 貿易 産業"),
    ("にとって", "", "にとって大切です", "Isto é importante para {the}.",
     "家族 友達 先生 大学生 先輩 市民 社長 部長 店員 運転手 赤ちゃん 息子 娘 妹 弟"),
    ("に対して", "", "に対して謝りました", "Pedi desculpas {to}.",
     "先生 友達 家族 先輩 部長 社長 店員 運転手 大学生 市民 妻 息子 娘 妹 弟"),
    ("によって", "", "によって変わります", "Isso muda conforme {the}.",
     "天気予報 季節 時代 場所 時間 値段 交通 予定 都合 文化 習慣 規則 原因 理由 技術"),
    ("うちに", "", "があるうちに買います", "Vou comprar enquanto ainda houver {x}.",
     "ぶどう 米 ジャム 味噌 サラダ ステーキ サンドイッチ 食料品 お土産 品物 指輪 手袋 サンダル 着物 布団"),
    ("につれて", "", "が増えるにつれて忙しい", "Conforme {the} aumenta, fico ocupado.",
     "仕事 人口 相談 連絡 予約 予定 用事 会議 旅行 生産 貿易 競争 交通 品物 お祝い"),
]

READINGS = {"駅": "えき", "道": "みち", "雪": "ゆき", "霧": "きり", "風": "かぜ",
            "工事": "こうじ", "経済": "けいざい", "自然": "しぜん", "手紙": "てがみ"}
MEANINGS = {"駅": "estação", "道": "estrada", "雪": "neve", "霧": "neblina",
            "風": "vento", "工事": "obra", "経済": "economia", "自然": "natureza",
            "手紙": "carta"}

FEMININE = {"mão", "luz", "flor", "viagem", "estação", "previsão", "reunião", "neve", "neblina", "obra", "economia",
            "natureza", "carta", "água", "lei", "sociedade", "liberdade", "saúde", "cidade",
            "voz", "tradução", "explicação", "produção", "educação", "competição", "opinião"}


def portuguese_forms(meaning):
    first = meaning.split()[0].lower()
    plural = first.endswith("s") and first not in {"país", "ônibus", "lápis"}
    feminine = first in FEMININE or first.endswith(("a", "ção", "dade", "gem", "ice"))
    article = ("as" if feminine else "os") if plural else ("a" if feminine else "o")
    of = {"o": "do", "a": "da", "os": "dos", "as": "das"}[article]
    to = {"o": "ao", "a": "à", "os": "aos", "as": "às"}[article]
    return {"x": meaning, "the": f"{article} {meaning}", "The": f"{article.capitalize()} {meaning}",
            "of": f"{of} {meaning}", "to": f"{to} {meaning}"}

GRAMMAR = {
    "べきだ": ("を大切にすべきです", "をたいせつにすべきです", "devemos valorizar"),
    "べきではない": ("を忘れるべきではない", "をわすれるべきではない", "não se deve esquecer"),
    "代わりに": ("の代わりに電話します", "のかわりにでんわします", "telefonar no lugar de"),
    "結局": ("結局", "けっきょく", "no fim", "を選びました", "をえらびました", "escolhi"),
    "だらけ": ("はごみだらけです", "はごみだらけです", "cheio de lixo"),
    "気味": ("は疲れ気味です", "はつかれぎみです", "um pouco cansado"),
    "ごとに": ("ごとに確認します", "ごとにかくにんします", "conferir a cada"),
    "ほど～ない": ("ほど高くないです", "ほどたかくないです", "não tão caro quanto"),
    "一度に": ("を一度に運びました", "をいちどにはこびました", "transportar de uma vez"),
    "一方だ": ("は増える一方です", "はふえるいっぽうです", "continua aumentando"),
    "ふりをする": ("は寝たふりをしました", "はねたふりをしました", "fingiu dormir"),
    "かける": ("を読みかけました", "をよみかけました", "começou a ler e parou"),
    "おかげで": ("のおかげで助かりました", "のおかげでたすかりました", "graças a"),
    "せいで": ("のせいで遅れました", "のせいでおくれました", "atrasado por causa de"),
    "に関して": ("に関して調べます", "にかんしてしらべます", "pesquisar sobre"),
    "にとって": ("にとって大切です", "にとってたいせつです", "importante para"),
    "に対して": ("に対して謝りました", "にたいしてあやまりました", "pedi desculpas a"),
    "によって": ("によって変わります", "によってかわります", "varia dependendo de"),
    "うちに": ("があるうちに買います", "があるうちにかいます", "comprar enquanto houver"),
    "につれて": ("が増えるにつれて忙しい", "がふえるにつれていそがしい", "mais ocupado à medida que aumenta"),
}


def make():
    phrases = []
    for grammar, prefix, suffix, translation, words in SCENARIOS:
        for word in words.split():
            source = LEXICON.get(word)
            if source is None and word not in READINGS:
                raise ValueError(f"Missing reading for {word}")
            reading = source["reading"] if source else READINGS[word]
            meaning = (source["meanings_pt"][0] if source else MEANINGS[word])
            text = prefix + word + suffix + "。"
            if len(text) > 20:
                raise ValueError(f"Sentence exceeds 20 characters: {text}")
            vocab = {"surface": word, "reading": reading, "kind": "vocabulário N3",
                     "meanings_pt": [meaning], "note_pt": "Palavra da situação apresentada."}
            info = GRAMMAR[grammar]
            if grammar == "結局":
                opening = {"surface": info[0], "reading": info[1], "kind": "estrutura gramatical",
                           "meanings_pt": [info[2]], "note_pt": "Marcador de conclusão N3."}
                ending = {"surface": info[3], "reading": info[4], "kind": "verbo",
                          "meanings_pt": [info[5]], "note_pt": "Ação no contexto da situação."}
                tokens = [opening, vocab, ending]
                focus = [0, 1]
            else:
                if suffix[0] in "はをのがに":
                    marker, remainder = suffix[0], suffix[1:]
                    marker_reading, remainder_reading = info[1][0], info[1][1:]
                    marker_kind = "partícula"
                else:
                    marker = "ごとに" if grammar == "ごとに" else "ほど"
                    remainder = suffix[len(marker):]
                    marker_reading, remainder_reading = info[1][:len(marker)], info[1][len(marker):]
                    marker_kind = "estrutura gramatical"
                marker_token = {"surface": marker, "reading": marker_reading, "kind": marker_kind,
                                "meanings_pt": ["ligação gramatical", info[2]],
                                "note_pt": f"Início da estrutura N3 {grammar}."}
                ending = {"surface": remainder, "reading": remainder_reading, "kind": "estrutura gramatical",
                          "meanings_pt": [info[2]], "note_pt": f"Uso da estrutura N3 {grammar} nesta situação."}
                tokens = [vocab, marker_token, ending]
                focus = [0, 1, 2]
            phrases.append({"id": 2201 + len(phrases), "level": "N3", "category": "gramática e vocabulário N3",
                            "grammar_point": grammar, "theme": f"{meaning}: {grammar}", "text": text,
                            "translation_pt": translation.format(**portuguese_forms(meaning)), "tokens": tokens,
                            "focus_token_indices": focus, "display_after": []})
    if len(phrases) != 300 or len({p["text"] for p in phrases}) != 300:
        raise ValueError("Expected 300 unique N3 sentences")
    return {"title": "Lista e Frases N3", "language": "ja", "translation_language": "pt-BR", "phrases": phrases}


if __name__ == "__main__":
    target = ROOT / "Lista e Frases N3.json"
    target.write_text(json.dumps(make(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {target.name} with 300 sentences")
