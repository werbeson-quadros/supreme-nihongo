"""Curate N4 practice sentences from a downloaded Japanese YouTube transcript.

The local auto-caption export is kept in imports/ and is intentionally not
committed. Only complete, legible caption sentences are included here.
"""

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEO_ID = "cy9P8f4lrEw"
TITLE = "JLPT N4 LISTENING PRACTICE TEST WITH ANSWERS 2026.ちょうかい"
SOURCE = f"https://www.youtube.com/watch?v={VIDEO_ID}"
TRANSCRIPT = ROOT / "imports" / f"youtube-{VIDEO_ID}-ja-auto.txt"
OUTPUT = ROOT / f"Lista e Frases N4 - YouTube {VIDEO_ID}.json"

# Each row is: exact sentence from the caption, Portuguese translation, token
# surfaces. Captions with obvious recognition errors, merged speakers, or
# incomplete clauses are not used.
ROWS = [
    ("問題用紙にメモを取っても構いません。", "Pode fazer anotações na folha da prova.", "問題用紙 に メモ を 取っても 構いません"),
    ("問題用紙を開けてください。", "Abra a folha da prova, por favor.", "問題用紙 を 開けてください"),
    ("問題1ではまず質問を聞いてください。", "Na questão 1, primeiro escute a pergunta.", "問題1 では まず 質問 を 聞いてください"),
    ("今週土日は予定が入ってしまったんです。", "Já surgiu um compromisso neste fim de semana.", "今週 土日 は 予定 が 入ってしまったんです"),
    ("バスならまだ動いてるらしいよ。", "Parece que os ônibus ainda estão funcionando.", "バス なら まだ 動いてる らしい よ"),
    ("電車が止まっているからみんなも同じことを考えていると思う。", "Como os trens pararam, acho que todos estão pensando a mesma coisa.", "電車 が 止まっている から みんな も 同じ こと を 考えている と 思う"),
    ("タクシーは楽だけどなかなか呼べないと思う。", "Táxi é cômodo, mas acho que será difícil chamar um.", "タクシー は 楽 だけど なかなか 呼べない と 思う"),
    ("でも鈴木さんと山本さんはその日は用事があって来られないって言っていたよね。", "Mas o Suzuki e o Yamamoto disseram que têm compromissos e não podem vir naquele dia, não foi?", "でも 鈴木さん と 山本さん は その日 は 用事 が あって 来られない って 言っていた よね"),
    ("すっかり忘れていました。", "Eu tinha esquecido completamente.", "すっかり 忘れて いました"),
    ("あと私の学校の友達も1人一緒に行くからその分もお願いしますね。", "Um amigo da minha escola também irá conosco, então inclua mais uma pessoa, por favor.", "あと 私 の 学校 の 友達 も 1人 一緒に 行く から その分 も お願いします ね"),
    ("さっき拾って戻しておいたよ。", "Eu peguei e coloquei de volta há pouco.", "さっき 拾って 戻しておいた よ"),
    ("それからお菓子を買っていこうか。", "Depois, que tal comprarmos doces para levar?", "それから お菓子 を 買っていこう か"),
    ("お菓子は田中さんが持ってくるって。", "Disseram que o Tanaka vai trazer os doces.", "お菓子 は 田中さん が 持ってくる って"),
    ("紙コップが少ないからそれもお願いね。", "Há poucos copos descartáveis, então cuide disso também, por favor.", "紙コップ が 少ない から それ も お願い ね"),
    ("じゃあ明日は早く起きないとね。", "Então amanhã temos que acordar cedo, não é?", "じゃあ 明日 は 早く 起きないと ね"),
    ("その後問題用紙を見てください。", "Depois disso, olhe a folha da prova.", "その後 問題用紙 を 見てください"),
    ("病気の時に飲んじゃダめでしょ。", "Não se deve beber quando está doente, certo?", "病気 の 時 に 飲んじゃ ダめ でしょ"),
    ("それはいいアイデアだね。", "Essa é uma boa ideia, não é?", "それ は いい アイデア だ ね"),
    ("でも僕は本より体にいいものを持っていきたいんだ。", "Mas eu quero levar algo saudável em vez de um livro.", "でも 僕 は 本 より 体 に いい もの を 持っていきたい んだ"),
    ("果物なら田中さんも食べやすいと思うし。", "Se for fruta, acho que também será fácil para o Tanaka comer.", "果物 なら 田中さん も 食べやすい と 思う し"),
    ("じゃあ私が本を持っていくね。", "Então eu vou levar um livro.", "じゃあ 私 が 本 を 持っていく ね"),
    ("実は母が来週こちらに来ることになって空港まで迎えに行かないといけないのよ。", "Na verdade, minha mãe virá para cá na semana que vem, e preciso buscá-la no aeroporto.", "実は 母 が 来週 こちら に 来ることになって 空港 まで 迎えに行かないといけない のよ"),
    ("まず服を入れて石鹸を入れてください。", "Primeiro coloque as roupas e o sabão.", "まず 服 を 入れて 石鹸 を 入れてください"),
    ("洗濯が終わったら服を取り出して干してください。", "Quando a lavagem terminar, retire as roupas e estenda-as.", "洗濯 が 終わったら 服 を 取り出して 干してください"),
    ("そして洗濯機は必ず蓋を開けておいてください。", "E deixe sempre a tampa da máquina de lavar aberta.", "そして 洗濯機 は 必ず 蓋 を 開けておいてください"),
    ("それから月に1度は中を掃除してください。", "Depois, limpe o interior uma vez por mês.", "それから 月 に 1度 は 中 を 掃除してください"),
    ("でも毎回する必要はありません。", "Mas não é necessário fazer isso toda vez.", "でも 毎回 する 必要 は ありません"),
    ("そういうわけじゃないの。", "Não é por esse motivo.", "そういう わけ じゃない の"),
    ("具合が悪いかなと思った。", "Achei que talvez você não estivesse se sentindo bem.", "具合 が 悪い かな と 思った"),
    ("それに僕が本当に好きなのは音楽なんだ。", "Além disso, o que eu realmente gosto é de música.", "それに 僕 が 本当に 好きな のは 音楽 なんだ"),
    ("街が綺麗でまた来たいと思っていたんだよ。", "A cidade era bonita e eu queria voltar.", "街 が 綺麗で また 来たい と 思っていた んだ よ"),
    ("大学でデザインを勉強していて、デザインの仕事が好きになったんだ。", "Eu estudava design na faculdade e passei a gostar de trabalhar com design.", "大学 で デザイン を 勉強していて デザイン の 仕事 が 好きに なったんだ"),
    ("日本のデザインは有名だからここでもっと勉強したいと思ってきたんだよ。", "Como o design japonês é famoso, vim querendo estudar mais aqui.", "日本 の デザイン は 有名 だから ここ で もっと 勉強したい と 思ってきたんだ よ"),
    ("できれば日本で仕事をしたいと思ってる。", "Se possível, quero trabalhar no Japão.", "できれば 日本 で 仕事 を したい と 思ってる"),
    ("問題3では絵を見ながら質問を聞いてください。", "Na questão 3, escute a pergunta enquanto olha a imagem.", "問題3 では 絵 を 見ながら 質問 を 聞いてください"),
    ("3番歩いている間に急に雨が降ってきました。", "Na questão 3, começou a chover de repente enquanto caminhavam.", "3番 歩いている 間 に 急に 雨 が 降ってきました"),
    ("でも友達は傘を持っていません。", "Mas meu amigo não tem guarda-chuva.", "でも 友達 は 傘 を 持っていません"),
    ("まず文を聞いてください。", "Primeiro escute a frase.", "まず 文 を 聞いてください"),
    ("木村さんは来週結婚するらしいよ。", "Parece que o Kimura vai se casar na semana que vem.", "木村さん は 来週 結婚する らしい よ"),
    ("今日はいい天気ですよ。", "Hoje o tempo está bom.", "今日 は いい 天気 です よ"),
]

EXTRA_MEANINGS = {
    "問題用紙":"folha da prova", "メモ":"anotação", "取っても":"mesmo fazendo", "構いません":"não há problema",
    "問題1":"questão 1", "では":"em; quanto a", "まず":"primeiro", "今週":"esta semana", "土日":"sábado e domingo",
    "入ってしまったんです":"acabou surgindo", "バス":"ônibus", "なら":"se for", "動いてる":"está funcionando",
    "らしい":"parece que", "止まっている":"está parado", "みんな":"todos", "同じ":"mesmo", "こと":"coisa",
    "考えている":"está pensando", "思う":"acho", "タクシー":"táxi", "楽":"cômodo", "だけど":"mas",
    "なかなか":"dificilmente", "呼べない":"não consegue chamar", "鈴木さん":"senhor Suzuki", "山本さん":"senhor Yamamoto",
    "その日":"aquele dia", "あって":"havendo", "来られない":"não pode vir", "って":"disse que",
    "言っていた":"estava dizendo", "よね":"não é?", "すっかり":"completamente", "忘れて":"esquecer", "いました":"estava",
    "あと":"além disso", "1人":"uma pessoa", "一緒に":"junto", "行く":"ir", "その分":"essa parte",
    "お願いします":"por favor", "さっき":"há pouco", "拾って":"pegando do chão", "戻しておいた":"deixei de volta",
    "お菓子":"doces", "買っていこう":"vamos comprar e levar", "田中さん":"senhor Tanaka", "持ってくる":"trará",
    "紙コップ":"copo descartável", "少ない":"poucos", "お願い":"pedido", "じゃあ":"então", "早く":"cedo",
    "起きないと":"precisa acordar", "その後":"depois disso", "病気":"doença", "時":"quando", "飲んじゃ":"beber; acabar bebendo",
    "ダめ":"não pode", "でしょ":"não é?", "アイデア":"ideia", "僕":"eu (masculino)", "より":"em vez de; mais que",
    "体":"corpo", "もの":"coisa", "持っていきたい":"quero levar", "んだ":"explicação; é que", "果物":"fruta",
    "食べやすい":"fácil de comer", "持っていく":"levar", "実は":"na verdade", "母":"mãe", "こちら":"aqui",
    "来ることになって":"ficou decidido que virá", "迎えに行かないといけない":"preciso buscar", "のよ":"ênfase explicativa",
    "入れて":"coloque", "石鹸":"sabão", "入れてください":"coloque, por favor", "洗濯":"lavagem", "終わったら":"quando terminar",
    "取り出して":"retire", "干してください":"estenda, por favor", "洗濯機":"máquina de lavar", "必ず":"sem falta",
    "蓋":"tampa", "開けておいてください":"deixe aberto, por favor", "1度":"uma vez", "掃除してください":"limpe, por favor",
    "毎回":"toda vez", "必要":"necessidade", "ありません":"não há", "そういう":"desse tipo", "わけ":"motivo",
    "じゃない":"não é", "具合":"condição", "悪い":"ruim", "かな":"talvez", "思った":"achei",
    "それに":"além disso", "本当に":"realmente", "好きな":"gostar de", "のは":"o que", "音楽":"música",
    "なんだ":"é que", "街":"cidade", "綺麗で":"bonita e", "また":"de novo", "来たい":"querer vir",
    "思っていた":"pensava", "勉強していて":"estudava e", "デザイン":"design", "好きに":"passou a gostar",
    "なったんだ":"tornou-se", "有名":"famoso", "ここ":"aqui", "もっと":"mais", "勉強したい":"quero estudar",
    "思ってきたんだ":"vim pensando", "できれば":"se possível", "したい":"quero fazer", "思ってる":"estou pensando",
    "問題3":"questão 3", "見ながら":"enquanto olha", "3番":"número 3", "歩いている":"está caminhando",
    "間":"enquanto", "急に":"de repente", "降ってきました":"começou a chover", "傘":"guarda-chuva",
    "持っていません":"não tem", "文":"frase", "木村さん":"senhor Kimura", "結婚する":"vai se casar",
    "天気":"tempo; clima", "です":"é; está", "開けてください":"abra, por favor",
    "聞いてください":"escute, por favor", "それから":"depois", "か":"partícula de pergunta",
    "それ":"isso", "見てください":"olhe, por favor", "そして":"e então", "中":"interior",
    "大学":"universidade", "日本":"Japão", "だから":"por isso; porque",
}


def caption_sentences():
    if not TRANSCRIPT.exists():
        raise FileNotFoundError(f"Download the Japanese captions to {TRANSCRIPT}")
    lines = []
    for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\[\d+:\d+\] (.*)$", line)
        if match and not re.fullmatch(r"\[[^]]+\]", match.group(1)):
            lines.append(match.group(1).strip())
    return set(part.strip() + "。" for part in "".join(lines).split("。")[:-1])


def reading_for(text):
    query = urllib.parse.urlencode({"text":text,"speaker":2})
    request = urllib.request.Request(f"http://127.0.0.1:50021/audio_query?{query}",data=b"")
    with urllib.request.urlopen(request,timeout=30) as response:
        data = json.load(response)
    katakana = "".join(mora["text"] for phrase in data["accent_phrases"] for mora in phrase["moras"])
    return "".join(chr(ord(c)-96) if "ァ" <= c <= "ヶ" else c for c in katakana)


def make():
    source = caption_sentences()
    existing = {p["text"] for p in json.loads((ROOT / "Lista e Frases N4.json").read_text(encoding="utf-8"))["phrases"]}
    lexicon = {t["surface"]:t for p in json.loads((ROOT / "Lista e Frases N4.json").read_text(encoding="utf-8"))["phrases"] for t in p["tokens"]}
    phrases = []
    cache = {}
    for text,translation,split in ROWS:
        if text not in source or len(text) <= 10 or text in existing:
            continue
        surfaces = split.split()
        if "".join(surfaces) != text[:-1].replace("、", ""):
            raise ValueError(f"Tokens do not reconstruct {text}")
        tokens = []
        for surface in surfaces:
            base = lexicon.get(surface)
            meaning = EXTRA_MEANINGS.get(surface) or (base["meanings_pt"][0] if base else None)
            if not meaning:
                raise ValueError(f"Missing meaning: {surface}")
            if surface not in cache:
                cache[surface] = base["reading"] if base and base["reading"] else reading_for(surface)
            kind = base["kind"] if base else ("partícula" if surface in {"は","が","を","に","で","と","の","も","から","まで","ね","よ","か"} else "vocabulário N4")
            tokens.append({"surface":surface,"reading":cache[surface],"kind":kind,
                           "meanings_pt":base["meanings_pt"] if base and surface not in EXTRA_MEANINGS else meaning.split("; "),
                           "note_pt":base.get("note_pt", "Trecho da legenda japonesa.") if base else "Trecho da legenda japonesa."})
        insertions = []
        cursor = 0
        for index,token in enumerate(tokens):
            start = text.find(token["surface"],cursor)
            if start < 0: raise ValueError(f"Missing token in text: {text}")
            if start > cursor and index:
                insertions.append({"index":index-1,"text":text[cursor:start]})
            cursor = start+len(token["surface"])
        phrases.append({"id":2501+len(phrases),"level":"N4","list_id":f"youtube:{VIDEO_ID}",
                        "category":"legenda de vídeo N4","grammar_point":"legenda de vídeo",
                        "text":text,"translation_pt":translation,"tokens":tokens,
                        "focus_token_indices":list(range(len(tokens))),"display_after":insertions})
        existing.add(text)
    if len(phrases) < 30:
        raise ValueError(f"Only {len(phrases)} suitable sentences found")
    return {"title":TITLE,"source_url":SOURCE,"source_language":"ja","captions":"auto-generated",
            "language":"ja","translation_language":"pt-BR","phrases":phrases}


if __name__ == "__main__":
    data = make()
    OUTPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {len(data['phrases'])} caption sentences to {OUTPUT.name}")
