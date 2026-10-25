"""Cenas adicionais N4, com vocabulário temático da lista enviada pelo usuário."""

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
VOCAB = """
アフリカ|África
挨拶|cumprimento
味|sabor
アジア|Ásia
赤ちゃん|bebê
アクセサリー|acessório
アメリカ|América
アナウンサー|locutor
案内|orientação
安心|tranquilidade
安全|segurança
アルバイト|trabalho de meio período
アルコール|álcool
遊び|brincadeira
番組|programa de televisão
場所|lugar
ベル|campainha
美術館|museu de arte
ビル|prédio
貿易|comércio exterior
部長|chefe de departamento
ぶどう|uva
文学|literatura
文化|cultura
文法|gramática
血|sangue
力|força
地理|geografia
中学校|escola secundária
注意|cuidado
注射|injeção
駐車場|estacionamento
大学生|universitário
暖房|aquecimento
電報|telegrama
電灯|lâmpada elétrica
泥棒|ladrão
動物園|zoológico
道具|ferramenta
枝|galho
遠慮|reserva; moderação
エスカレーター|escada rolante
ファックス|fax
復習|revisão
船|navio
布団|futon
ガラス|vidro
ガソリン|gasolina
ガソリンスタンド|posto de gasolina
原因|causa
下宿|pensão
技術|técnica
ごちそう|banquete
ごみ|lixo
具合|condição
葉|folha
歯医者|dentista
花見|observação das flores
ハンドバッグ|bolsa de mão
反対|oposição
発音|pronúncia
林|bosque
返事|resposta
火|fogo
髭|barba
光|luz
引き出し|gaveta
飛行場|aeródromo
昼休み|intervalo do almoço
翻訳|tradução
星|estrela
法律|lei
放送|transmissão
医学|medicina
意見|opinião
生き物|ser vivo
田舎|interior
糸|fio
ジャム|geleia
時代|época
事故|acidente
事務所|escritório
神社|santuário xintoísta
人口|população
人生|vida
地震|terremoto
辞典|dicionário
自由|liberdade
柔道|judô
住所|endereço
カーテン|cortina
壁|parede
科学|ciência
鏡|espelho
海岸|litoral
会議|reunião
会議室|sala de reuniões
会場|local do evento
会話|conversa
火事|incêndio
髪|cabelo
形|forma
着物|quimono
近所|vizinhança
絹|seda
季節|estação do ano
汽車|trem a vapor
規則|regra
国際|internacional
米|arroz
コンピュータ|computador
コンサート|concerto
故障|defeito
小鳥|passarinho
講堂|auditório
工場|fábrica
交通|trânsito
雲|nuvem
草|grama
空気|ar
空港|aeroporto
教育|educação
教会|igreja
競争|competição
漫画|mangá
港|porto
味噌|missô
湖|lago
木綿|algodão
森|floresta
虫|inseto
息子|filho
娘|filha
値段|preço
熱|febre
人形|boneca
匂い|cheiro
喉|garganta
乗り物|veículo
入学|ingresso na escola
入院|internação
踊り|dança
お祝い|comemoração
屋上|terraço
贈り物|presente
お祭り|festival
お見舞い|visita a um doente
お土産|lembrança de viagem
おもちゃ|brinquedo
オートバイ|motocicleta
お礼|agradecimento
音|som
お釣り|troco
泳ぎ方|modo de nadar
パソコン|computador pessoal
ピアノ|piano
プレゼント|presente
冷房|ar condicionado
レジ|caixa de loja
歴史|história
連絡|contato
レポート|relatório
理由|motivo
旅館|pousada japonesa
坂|ladeira
サンダル|sandália
サンドイッチ|sanduíche
産業|indústria
サラダ|salada
生物|ser vivo
政治|política
生活|vida cotidiana
生命|vida
生産|produção
世界|mundo
席|assento
背中|costas
先輩|colega mais experiente
戦争|guerra
社長|presidente da empresa
社会|sociedade
試合|partida
島|ilha
市民|cidadão
品物|mercadoria
新聞社|empresa jornalística
食料品|alimentos
小学校|escola primária
小説|romance
趣味|passatempo
習慣|hábito
卒業|formatura
相談|consulta
水道|abastecimento de água
水泳|natação
スクリーン|tela
砂|areia
スーツケース|mala
ステーキ|bife
ステレオ|aparelho de som
数学|matemática
スーツ|terno
台風|tufão
棚|prateleira
誕生|nascimento
畳|tatame
手袋|luva
テキスト|material didático
点|ponto
店員|funcionário de loja
テニス|tênis
天気予報|previsão do tempo
展覧会|exposição
寺|templo
特急|trem expresso
床屋|barbearia
都合|conveniência
月|lua
妻|esposa
腕|braço
受付|recepção
運転手|motorista
売り場|seção de vendas
忘れ物|objeto esquecido
割合|proporção
約束|promessa
予習|preparação da aula
予定|plano
用意|preparo
用事|compromisso
予約|reserva
湯|água quente
指|dedo
指輪|anel
夢|sonho
映画|filme
病院|hospital
銀行|banco
郵便局|correio
料理|culinária
旅行|viagem
仕事|trabalho
学校|escola
図書館|biblioteca
先生|professor
友達|amigo
家族|família
公園|parque
電車|trem
自転車|bicicleta
""".strip()

PARTS = {
    "学校": ("がっこう", "escola"), "帰りに": ("かえりに", "na volta"),
    "今日": ("きょう", "hoje"), "今度": ("こんど", "próximo; desta vez"),
    "きちんと": ("きちんと", "corretamente; com cuidado"), "夕ご飯": ("ゆうごはん", "jantar"),
    "後で": ("あとで", "depois de; mais tarde"),
    "昨日": ("きのう", "ontem"), "友達": ("ともだち", "amigo"), "と": ("と", "com; e"),
    "について": ("について", "sobre; a respeito de"), "話していたら": ("はなしていたら", "quando estava conversando; condicional たら"),
    "知らなかった": ("しらなかった", "não sabia"), "こと": ("こと", "coisa; fato; nominalizador"),
    "を": ("を", "marca o objeto direto"), "一つ": ("ひとつ", "um; uma coisa"),
    "教えてもらいました": ("おしえてもらいました", "recebi uma explicação; favor com てもらう"),
    "先生": ("せんせい", "professor"), "に": ("に", "a; para; marca o destinatário"),
    "の": ("の", "de; liga substantivos"), "聞いてみたかった": ("きいてみたかった", "queria experimentar perguntar; てみる + たい"),
    "のに": ("のに", "embora; apesar de"), "授業": ("じゅぎょう", "aula"),
    "が": ("が", "marca o sujeito; mas"), "終わる": ("おわる", "terminar"),
    "まで": ("まで", "até"), "質問できませんでした": ("しつもんできませんでした", "não consegui perguntar; forma potencial"),
    "週末": ("しゅうまつ", "fim de semana"), "は": ("は", "marca o tema"),
    "図書館": ("としょかん", "biblioteca"), "で": ("で", "em; local da ação"),
    "調べてから": ("しらべてから", "depois de pesquisar; sequência てから"),
    "妹": ("いもうと", "irmã mais nova"), "も": ("も", "também"),
    "分かりやすく": ("わかりやすく", "de modo fácil de entender; sufixo やすい"),
    "説明する": ("せつめいする", "explicar"), "つもりです": ("つもりです", "pretendo; planejo"),
    "母": ("はは", "minha mãe"), "話": ("はなし", "conversa; história"),
    "してくれた": ("してくれた", "fez para mim; favor com てくれる"),
    "ので": ("ので", "porque; já que"), "私": ("わたし", "eu"), "いつか": ("いつか", "algum dia"),
    "自分": ("じぶん", "si mesmo"), "目": ("め", "olho"), "確かめたい": ("たしかめたい", "quero confirmar"),
    "と思いました": ("とおもいました", "pensei que; achei que"), "駅": ("えき", "estação"),
    "会った": ("あった", "encontrei"), "伝えたら": ("つたえたら", "se/quando contei; condicional たら"),
    "来週": ("らいしゅう", "semana que vem"), "一緒に": ("いっしょに", "juntos"),
    "調べよう": ("しらべよう", "vamos pesquisar; forma volitiva"),
    "と言われました": ("といわれました", "foi dito a mim; voz passiva"),
}

TEMPLATES = [
    ("conversa entre amigos", "たら / てもらう", "Ontem, na volta da escola, enquanto conversava com um amigo sobre {x}, ele me ensinou algo que eu não sabia.",
     "昨日 学校 の 帰りに 友達 と X について 話していたら 知らなかった こと を 一つ 教えてもらいました"),
    ("dúvida na aula", "のに / potencial", "Hoje, na aula, queria perguntar ao professor sobre {x}, mas não consegui fazer a pergunta antes do fim da aula.",
     "今日 の 授業 で 先生 に X の こと を 聞いてみたかった のに 授業 が 終わる まで 質問できませんでした"),
    ("pesquisa na biblioteca", "てから / つもり", "No próximo fim de semana, pretendo pesquisar {x} na biblioteca e depois explicar direito à minha irmã.",
     "今度 の 週末 は 図書館 で X について 調べてから 妹 に も きちんと 分かりやすく 説明する つもりです"),
    ("história em família", "ので / たい", "Depois do jantar, minha mãe contou sobre {x}, então pensei que um dia gostaria de conferir pessoalmente.",
     "夕ご飯 の 後で 母 が X の 話 を してくれた ので 私 も いつか 自分 の 目 で 確かめたい と思いました"),
    ("encontro na estação", "たら / passiva / volitiva", "Ontem, na volta da escola, ao contar a um amigo que encontrei na estação sobre {x}, ele me disse para pesquisarmos juntos na próxima semana.",
     "昨日 学校 の 帰りに 駅 で 会った 友達 に X の こと を 伝えたら 来週 一緒に 調べよう と言われました"),
]


def reading(word):
    if not re.search(r"[一-龯]", word):
        return word
    url = "http://127.0.0.1:50021/audio_query?" + urllib.parse.urlencode({"text": word, "speaker": 2})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="POST"), timeout=5) as response:
            data = json.load(response)
        kana = "".join(m["text"] for p in data["accent_phrases"] for m in p["moras"])
        return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in kana)
    except Exception as exc:
        raise RuntimeError(f"Não foi possível obter a leitura de {word} pelo VOICEVOX") from exc


def make_token(surface, vocab):
    if surface == "X":
        word, meaning, kana = vocab
        return {"surface": word, "reading": kana, "kind": "vocabulário N4", "meanings_pt": meaning.split("; "),
                "note_pt": "Tema desta cena; vocabulário da lista enviada."}
    kana, meaning = PARTS[surface]
    return {"surface": surface, "reading": kana, "kind": "estrutura gramatical" if surface in
            {"について", "話していたら", "教えてもらいました", "のに", "調べてから", "分かりやすく", "つもりです", "してくれた", "ので", "伝えたら", "調べよう", "と言われました"} else "vocabulário N4",
            "meanings_pt": meaning.split("; "), "note_pt": "Significado no contexto desta frase."}


def extend(phrases):
    rows = [line.split("|", 1) for line in VOCAB.splitlines()]
    assert len(rows) == 250 and len({x[0] for x in rows}) == 250, len(rows)
    vocab = [(word, meaning, reading(word)) for word, meaning in rows]
    existing = {p["text"] for p in phrases}
    for index in range(500):
        word, meaning, kana = vocab[index % 250]
        template_index = (index % 5 + (2 if index >= 250 else 0)) % 5
        scene, grammar, pt, pattern = TEMPLATES[template_index]
        parts = pattern.split()
        tokens = [make_token(part, (word, meaning, kana)) for part in parts]
        text = "".join(t["surface"] for t in tokens) + "。"
        if text in existing:
            raise ValueError(f"Frase repetida: {text}")
        existing.add(text)
        focus = parts.index("X")
        grammar_focus = [i for i, part in enumerate(parts) if i != focus and
                         make_token(part, (word, meaning, kana))["kind"] == "estrutura gramatical"]
        focus_indices = sorted([focus] + grammar_focus[:3])
        phrases.append({"id": 1401 + index, "level": "N4", "category": scene, "grammar_point": grammar,
                        "theme": f"{word} ({meaning}) — {scene}", "text": text, "translation_pt": pt.format(x=meaning),
                        "tokens": tokens, "focus_token_indices": focus_indices, "display_after": []})
    return phrases
