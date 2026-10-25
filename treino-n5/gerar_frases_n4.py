"""Build 400 contextual N4 practice entries with token annotations."""
import json
from pathlib import Path
from gerar_frases import L
from gramatica_extra import EXTRA

N5_DATA=json.loads(Path(__file__).with_name("Lista e Frases N5.json").read_text(encoding="utf-8"))
N5_TOKENS={token["surface"]:token for phrase in N5_DATA["phrases"] for token in phrase["tokens"]}

# The focus clause is kept near the end so the four longer contexts still read as
# one sentence. Spaces mark the meaningful units shown in answer feedback.
ROWS = """
間（あいだ）|先生 が 話している 間 私 は 大切な 言葉 を 書いていました|enquanto o professor falava, eu anotava as palavras importantes
間に（あいだに）|先生 が いない 間に 私 は 宿題 を 終わらせました|terminei a tarefa enquanto o professor estava fora
あまり～ない|私 は あまり 難しい 本 を 読みません|não leio muitos livros difíceis
後で（あとで）|授業 の 後で 先生 に 質問 しました|perguntei ao professor depois da aula
ば|時間 が あれば もう 一度 説明 を 聞きます|se houver tempo, ouvirei a explicação mais uma vez
場合は（ばあいは）|雨 が 降る 場合は 発表 を 明日 に 延ばします|se chover, adiaremos a apresentação para amanhã
ばかり|最近 は 日本語 の 本 ばかり 読んでいます|ultimamente só tenho lido livros em japonês
だけで|この 説明 を 聞く だけで よく 分かります|entendo bem só de ouvir esta explicação
出す（だす）|友達 は 急に 笑い出しました|meu amigo começou a rir de repente
でございます|こちら が 今日 の 発表 の 資料 でございます|este é o material da apresentação de hoje
でも|難しい 本 でも 最後 まで 読んでみます|mesmo que seja um livro difícil, tentarei lê-lo até o fim
ではないか|この 方法 は とても 便利 ではないか|este método não é muito prático?
が必要（がひつよう）|発表 には 新しい 資料 が必要 です|a apresentação precisa de material novo
がする|教室 から いい 音 がする|ouço um som agradável vindo da sala de aula
がり|弟 は 寒がり なので 暖かい 服 を 着ます|meu irmão sente muito frio e por isso veste roupa quente
がる / がっている|妹 は 新しい 本 を 読みたがっています|minha irmã quer ler um livro novo
ございます|机 の 上 に 先生 の 本 がございます|há um livro do professor sobre a mesa
始める（はじめる）|私 は 毎朝 日本語 の 新聞 を 読み始めました|comecei a ler o jornal japonês todas as manhãs
はずだ|先生 は もう 学校 に いる はずだ|o professor já deve estar na escola
はずがない|この 短い 説明 だけ で 全部 分かる はずがない|não é possível entender tudo só com esta explicação curta
必要がある（ひつようがある）|私 は 漢字 を もっと 練習 する 必要がある|preciso praticar mais os kanji
意向形 （いこうけい）|明日 も 一緒に 図書館 へ 行こう|vamos à biblioteca juntos amanhã também
いらっしゃる|先生 は 午後 に 教室 へ いらっしゃいます|o professor virá à sala de aula à tarde
いたします|私 が 発表 の 準備 を いたします|eu prepararei a apresentação
じゃないか|この 本 は 思った より 面白い じゃないか|este livro é mais interessante do que eu pensava, não é?
かどうか|明日 先生 が 来る かどうか まだ 分かりません|ainda não sei se o professor virá amanhã
かしら|この 答え で 本当に いい かしら|será que esta resposta está mesmo correta?
かい|君 も 今日 の 授業 に 出る かい|você também vai participar da aula de hoje?
かもしれない|明日 の 発表 は 難しい かもしれない|a apresentação de amanhã talvez seja difícil
かな|この 言葉 の 意味 は 何 かな|qual será o significado desta palavra?
から作る（からつくる）|この 紙 は 古い 本 から作られています|este papel é feito de livros velhos
きっと|先生 は きっと 私 の 質問 に 答えてくれます|o professor certamente responderá à minha pergunta
頃（ころ / ごろ）|午後 三時 ごろ に 学校 へ 戻ります|voltarei à escola por volta das três da tarde
こと|毎日 少しずつ 勉強 する こと が 大切 です|estudar um pouco todos os dias é importante
ことがある|私 は ときどき 漢字 を 読み間違える ことがある|às vezes leio um kanji errado
ことができる|この 本 を 読めば 新しい 表現 を 覚える ことができる|se ler este livro, poderei aprender expressões novas
ことになる|来月 から 別 の 学校 で 勉強 する ことになりました|ficou decidido que estudarei em outra escola a partir do mês que vem
ことにする|今日 は 家 で 宿題 を する ことにします|decidi fazer a tarefa em casa hoje
くする|部屋 を 明るくして 本 を 読みます|deixo o quarto claro para ler o livro
急に（きゅうに）|急に 雨 が 降り始めた ので 窓 を 閉めました|como começou a chover de repente, fechei a janela
までに|明日 までに この 宿題 を 終わらせます|terminarei esta tarefa até amanhã
まま|窓 を 開けた まま 授業 を 受けました|assisti à aula com a janela aberta
または|発表 は 今日 または 明日 に 行います|a apresentação será hoje ou amanhã
みたいだ|あの 人 は 新しい 先生 みたいだ|aquela pessoa parece ser o novo professor
みたいな|この 絵 は 本物 みたいな 写真 です|este desenho é uma imagem que parece real
みたいに|先生 みたいに 上手に 日本語 を 話したい|quero falar japonês bem como o professor
も|私 も 今日 の 授業 に 出ます|eu também participarei da aula de hoje
な|そこ で 大きな 声 で 話す な|não fale alto aí
など|本 や 新聞 など を 読んで 勉強 します|estudo lendo livros, jornais e outras coisas
ながら|音楽 を 聞きながら 新しい 言葉 を 覚えます|aprendo palavras novas enquanto ouço música
なかなか～ない|この 漢字 は なかなか 覚えられません|não consigo memorizar este kanji facilmente
なければいけない|明日 までに 宿題 を 出さなければいけない|preciso entregar a tarefa até amanhã
なければならない|発表 の 前 に 練習 しなければならない|tenho de praticar antes da apresentação
なら|日本語 を 勉強 する なら この 本 が いい です|se for estudar japonês, este livro é bom
なさい|この 文 を もう 一度 読みなさい|leia esta frase mais uma vez
なさる|先生 は いつも 丁寧に 説明 なさいます|o professor sempre explica com cuidado
に気がつく（にきがつく）|私 は 本 の 間違い に気がつきました|percebi um erro no livro
に見える（にみえる）|この 漢字 は 別 の 字 に見えます|este kanji parece outro caractere
にする|今日 の 発表 は 短い 話 にします|farei da apresentação de hoje uma fala curta
にくい|この 古い 本 の 字 は 読みにくい です|as letras deste livro velho são difíceis de ler
の中で（のなかで）|この 三つ の 中で あの 説明 が 一番 分かりやすい|entre estas três, aquela explicação é a mais fácil de entender
のに（逆接）|一生懸命 勉強 した のに 試験 は 難しかった|embora eu tenha estudado muito, a prova foi difícil
のに（目的）|新しい 言葉 を 覚える のに この ノート を 使います|uso este caderno para aprender palavras novas
のは〜だ|私 が 一番 好き な のは 日本語 の 授業 だ|do que eu mais gosto é da aula de japonês
お～ください|どうぞ この 資料 を お読みください|por favor, leia este material
お～になる|先生 は この 本 を お読みになります|o professor lerá este livro
おきに|二日 おきに 図書館 へ 行きます|vou à biblioteca a cada dois dias
終わる（おわる）|私 は やっと 宿題 を 書き終わりました|finalmente terminei de escrever a tarefa
られる（可能）|私 は 朝 六時 に 起きられます|consigo acordar às seis da manhã
らしい|あの 人 は 新しい 日本語 の 先生 らしい|parece que aquela pessoa é o novo professor de japonês
さ|この 問題 の 難しさ を 先生 に 伝えます|contarei ao professor a dificuldade desta questão
さっき|さっき 先生 が 教室 に 入りました|o professor entrou na sala há pouco
させられる|弟 は 毎日 漢字 を 練習 させられています|meu irmão é obrigado a praticar kanji todos os dias
させる|先生 は 学生 に 新しい 文 を 書かせます|o professor faz os alunos escreverem uma frase nova
させてください|私 に もう 一度 説明 させてください|deixe-me explicar mais uma vez
さすが|さすが 先生 は 難しい 質問 に も 答えられます|como era de esperar, o professor consegue responder até a perguntas difíceis
し|この 本 は 安い し 説明 も 分かりやすい です|este livro é barato e sua explicação também é fácil de entender
そんなに|この 宿題 は そんなに 難しくありません|esta tarefa não é tão difícil
それでも|昨日 は 疲れましたが それでも 勉強 を 続けました|ontem eu estava cansado, mas mesmo assim continuei estudando
それに|この 本 は 安い し それに 読みやすい です|este livro é barato e, além disso, fácil de ler
そうだ（伝聞）|先生 の 話 では 明日 は 試験 が ある そうだ|segundo o professor, parece que haverá prova amanhã
そうだ（様態）|空 が 暗い ので 雨 が 降りそうだ|o céu está escuro, então parece que vai chover
そうに / そうな|友達 は 楽しそうに 日本語 の 本 を 読んでいます|meu amigo lê um livro em japonês com ar de prazer
たばかり|私 は この 漢字 を 覚えた ばかり です|acabei de aprender este kanji
たところ|今 宿題 を 終えた ところ です|acabei de terminar a tarefa agora
他動詞 & 自動詞（たどうし & じどうし）|私 が ドア を 開ける と ドア が 開きます|quando abro a porta, ela se abre
たがる|弟 は 私 の 日本語 の 本 を 読みたがります|meu irmão quer ler meu livro de japonês
たら|時間 が あったら 先生 に 質問 します|se eu tiver tempo, perguntarei ao professor
たらどう|この 本 を もう 一度 読んだらどう|que tal ler este livro mais uma vez?
たらいいですか|分からない とき は だれ に 聞いたらいいですか|quando eu não entender, a quem devo perguntar?
て / で|友達 に 会って 図書館 で 勉強 しました|encontrei um amigo e estudei na biblioteca
てあげる|弟 に この 漢字 の 読み方 を 教えてあげます|ensinarei a leitura deste kanji ao meu irmão
てほしい|先生 に もう 一度 説明 してほしい です|quero que o professor explique mais uma vez
ていく|これから も 毎日 日本語 を 勉強 していきます|continuarei estudando japonês todos os dias daqui em diante
ていた|昨日 は 家 で 日本語 の 本 を 読んでいました|ontem eu estava lendo um livro em japonês em casa
ていただけませんか|先生 この 文 を 読んでいただけませんか|professor, poderia ler esta frase para mim?
てくれる|友達 が 難しい 漢字 を 教えてくれました|meu amigo me ensinou um kanji difícil
てくる|新しい 学生 が 教室 に 入ってきました|um aluno novo entrou na sala vindo para cá
てみる|分からない 言葉 を 辞書 で 調べてみます|tentarei pesquisar no dicionário as palavras que não entendo
てもらう|友達 に 宿題 を 見てもらいました|pedi a um amigo que visse minha tarefa
ておく|発表 の 前 に この 資料 を 読んでおきます|lerei este material antes da apresentação
てしまう / ちゃう|大切な ノート を 家 に 忘れちゃいました|acabei esquecendo o caderno importante em casa
てすみません|授業 に 遅れてすみません|desculpe por ter chegado atrasado à aula
てやる|弟 に この 問題 の 答え を 教えてやります|vou ensinar a resposta desta questão ao meu irmão
てよかった|先生 に 質問 してよかった です|foi bom ter perguntado ao professor
ているところ|今 友達 と 発表 の 準備 を しているところ です|estou justamente preparando a apresentação com um amigo
ても|雨 が 降っても 学校 へ 行きます|mesmo se chover, irei à escola
と（条件）|この ボタン を 押す と 音 が 出ます|quando aperto este botão, sai um som
と言ってもいい（といってもいい）|この 本 は 日本語 の 入門書 と言ってもいい|pode-se dizer que este livro é uma introdução ao japonês
という|友達 は 明日 試験 が ある という 話 を 聞きました|meu amigo ouviu que haverá prova amanhã
ということ|先生 の 説明 が 大切だ ということ が 分かりました|entendi que a explicação do professor é importante
と言われている（といわれている）|毎日 の 練習 が 大切だ と言われています|dizem que praticar todos os dias é importante
と聞いた（ときいた）|明日 は 新しい 先生 が 来る と聞きました|ouvi dizer que um novo professor virá amanhã
と思う（とおもう）|この 方法 が 一番 いい と思います|acho que este método é o melhor
とか～とか|本 を 読む とか 音楽 を 聞く とか して休みます|descanso lendo livros, ouvindo música e coisas assim
ところ|今 から 宿題 を 始める ところ です|estou prestes a começar a tarefa
続ける（つづける）|これから も 日本語 の 勉強 を 続けます|continuarei estudando japonês daqui em diante
って|友達 は 明日 試験 が ある って 言いました|meu amigo disse que haverá prova amanhã
受身形（うけみけい）|私 は 先生 に 名前 を 呼ばれました|fui chamado pelo nome pelo professor
は〜が… は|日本語 は 漢字 が 難しい が 会話 は 楽しい|em japonês os kanji são difíceis, mas conversar é divertido
やすい|この 本 の 説明 は とても 分かりやすい です|a explicação deste livro é muito fácil de entender
やっと|やっと 難しい 漢字 を 覚えました|finalmente aprendi o kanji difícil
より|この 本 は あの 本 より 読みやすい です|este livro é mais fácil de ler do que aquele
予定だ（よていだ）|来週 先生 に 質問 する 予定です|pretendo perguntar ao professor na semana que vem
ようだ|先生 は もう 教室 に いる ようだ|parece que o professor já está na sala
ように / ような|先生 の ように 上手に 話せる ように 練習 します|pratico para conseguir falar tão bem quanto o professor
ようになる|少しずつ 漢字 が 読める ようになりました|passei a conseguir ler kanji aos poucos
ようにする|毎日 日本語 の 本 を 読む ようにしています|procuro ler um livro em japonês todos os dias
ようと思う（ようとおもう）|明日 先生 に この 問題 を 聞こうと思います|penso em perguntar sobre esta questão ao professor amanhã
ぜひ|ぜひ 友達 と 一緒に 発表 を 聞きに来てください|venha ouvir a apresentação com seus amigos, por favor
全然～ない（ぜんぜん～ない）|この 説明 は 全然 分かりませんでした|não entendi absolutamente nada desta explicação
づらい|この 小さい 字 は 読みづらい です|estas letras pequenas são difíceis de ler
""".strip().splitlines()

# Four study situations introduce the target sentence as a quoted example.
# This keeps every long entry coherent even when its N4 target changes topic.
CONTEXTS = [
  ("昨日 の 授業 を 思い出し", "Lembrando da aula de ontem, escrevi o exemplo", "という 例文 を 書きました", ""),
  ("友達 と 図書館 で 話し", "Depois de conversar com um amigo na biblioteca, anotei", "と ノート に 書きました", ""),
  ("日本語 の 宿題 の ために", "Para a tarefa de japonês, criei a frase", "という 文 を 作りました", ""),
  ("新しい 文法 の 練習 に", "Para praticar a nova gramática, li em voz alta", "と 声 に 出して 読みました", ""),
]

GLOSS = {
  "向けて":("むけて","estrutura gramatical",["em direção a","visando"]),
  "資料":("しりょう","substantivo",["material","documentos"]),
  "集め":("あつめ","verbo",["reunindo","coletando"]),
  "分からない":("わからない","verbo",["não entender","desconhecido"]),
  "言葉":("ことば","substantivo",["palavra","linguagem"]),
  "ノート":("ノート","substantivo",["caderno","anotações"]),
  "書いた":("かいた","verbo",["escrevi","anotei"]),
  "ので":("ので","estrutura gramatical",["porque","como"]),
  "授業":("じゅぎょう","substantivo",["aula","lição"]),
  "大切な":("たいせつな","adjetivo な",["importante","valioso"]),
  "した":("した","verbo",["fez","realizou"]),
  "帰って":("かえって","verbo",["voltando","retornando"]),
  "辞書":("じしょ","substantivo",["dicionário"]),
  "使い":("つかい","verbo",["usando","utilizando"]),
  "例文":("れいぶん","substantivo",["frase de exemplo"]),
  "読んで":("よんで","verbo",["lendo","depois de ler"]),
  "相談":("そうだん","substantivo/verbo",["consulta","conversa para decidir"]),
  "来月":("らいげつ","substantivo",["mês que vem"]),
  "予定":("よてい","substantivo",["plano","programação"]),
  "決める":("きめる","verbo",["decidir","definir"]),
  "ために":("ために","estrutura gramatical",["para","com a finalidade de"]),
  "長い":("ながい","adjetivo い",["longo","comprido"]),
  "話し":("はなし","verbo",["conversando","falando"]),
  "行きたい":("いきたい","verbo",["querer ir"]),
  "場所":("ばしょ","substantivo",["lugar","local"]),
  "今朝":("けさ","substantivo",["esta manhã"]),
  "降っていた":("ふっていた","verbo",["estava chovendo"]),
  "聞きながら":("ききながら","estrutura gramatical",["enquanto escuto"]),
  "読み":("よみ","verbo",["lendo"]),
  "ところ":("ところ","substantivo",["parte","ponto"]),
  "質問":("しつもん","substantivo/verbo",["pergunta","questionar"]),
  "してみた":("してみた","estrutura gramatical",["tentei fazer"]),
  "書いて":("かいて","verbo",["escrevendo","depois de escrever"]),
  "として":("として","estrutura gramatical",["como","na qualidade de"]),
  "作りました":("つくりました","verbo",["criei","fiz"]),
  "文法":("ぶんぽう","substantivo",["gramática","regra gramatical"]),
  "声":("こえ","substantivo",["voz"]),
  "出して":("だして","verbo",["emitindo","pondo para fora"]),
  "読みました":("よみました","verbo",["li","fiz a leitura"]),
  "話し合い":("はなしあい","verbo",["conversando para decidir","discutindo"]),
  "書く":("かく","verbo",["escrever"]),
  "とき":("とき","estrutura gramatical",["quando","no momento em que"]),
  "選びました":("えらびました","verbo",["escolhi","selecionei"]),
  "自分":("じぶん","pronome",["eu mesmo","si próprio"]),
  "書きました":("かきました","verbo",["escrevi","anotei"]),
  "思い出し":("おもいだし","verbo",["lembrando","recordando"]),
}

# Reading and contextual meanings for the additional N4 units. A slash separates
# related meanings; inflected forms are kept intact when their grammar matters.
GLOSS_TEXT = """
あったら|あったら|se houvesse / se tiver
あれば|あれば|se houver / caso exista
いたします|いたします|farei / realizarei humildemente
いない|いない|não estar / não haver ser vivo
いらっしゃいます|いらっしゃいます|vem / está (honorífico)
おきに|おきに|a cada / com intervalo de
お読みください|およみください|por favor leia (honorífico)
お読みになります|およみになります|lê / lerá (honorífico)
かい|かい|partícula interrogativa informal
かしら|かしら|será que / eu me pergunto
かどうか|かどうか|se ou não / se
かな|かな|será que / eu me pergunto
かもしれない|かもしれない|talvez / pode ser que
から作られています|からつくられています|é feito de / é produzido a partir de
がございます|がございます|há / existe (polido)
がする|がする|sentir / perceber som ou cheiro
が必要|がひつよう|é necessário / precisa de
きっと|きっと|certamente / com certeza
こちら|こちら|este lado / aqui / esta pessoa
こと|こと|ato de / fato de / coisa abstrata
ことがある|ことがある|às vezes acontece / já ocorreu
ことができる|ことができる|conseguir fazer / poder fazer
ことにします|ことにします|decido fazer
ことになりました|ことになりました|ficou decidido que
これから|これから|daqui em diante / agora
ごろ|ごろ|por volta de / aproximadamente
さすが|さすが|como esperado / digno de
させてください|させてください|deixe-me fazer / permita-me
させられています|させられています|está sendo obrigado a fazer
さっき|さっき|há pouco / agora mesmo
し|し|e / além disso / pois
していきます|していきます|continuarei fazendo
しているところ|しているところ|estar fazendo neste momento
してほしい|してほしい|quero que faça
してよかった|してよかった|foi bom ter feito
して休みます|してやすみます|faço e descanso
しなければならない|しなければならない|tenho de fazer / é obrigatório
しました|しました|fiz / realizou
じゃないか|じゃないか|não é? / expressão de descoberta
する|する|fazer / realizar
ぜひ|ぜひ|por favor / sem falta
そうだ|そうだ|dizem que / parece que
それでも|それでも|mesmo assim / apesar disso
それに|それに|além disso / e ainda
そんなに|そんなに|tanto assim / desse jeito
だけで|だけで|apenas com / só por
って|って|diz que / marcador informal de citação
でございます|でございます|é (forma muito polida)
では|では|segundo / quanto a
ではないか|ではないか|não é? / não seria?
という|という|chamado / que se diz
ということ|ということ|o fato de que / isso significa que
とか|とか|coisas como / ou
ときどき|ときどき|às vezes / de vez em quando
と思います|とおもいます|acho que / penso que
と聞きました|とききました|ouvi dizer que
と言ってもいい|といってもいい|pode-se dizer que
と言われています|といわれています|dizem que / é considerado
どうぞ|どうぞ|por favor / fique à vontade
なかなか|なかなか|não facilmente / bastante
なさいます|なさいます|faz (honorífico)
など|など|etcétera / entre outros
なので|なので|por isso / sendo assim
なら|なら|se for / quanto a
にします|にします|decido por / torno em
には|には|para / quanto a
に気がつきました|にきがつきました|percebi / notei
に見えます|にみえます|parece / é visto como
のに|のに|embora / para fazer
のは|のは|o que / quanto ao fato de
はずがない|はずがない|não é possível que
はずだ|はずだ|deve ser / é esperado que
ばかり|ばかり|somente / o tempo todo
または|または|ou / alternativamente
までに|までに|até o prazo de / antes de
まま|まま|do jeito que está / mantendo
みたいだ|みたいだ|parece / é como
みたいな|みたいな|parecido com / como se fosse
みたいに|みたいに|como / à maneira de
もっと|もっと|mais / ainda mais
やっと|やっと|finalmente / com dificuldade
ようだ|ようだ|parece que / é como
ように|ように|para que / como
ようにしています|ようにしています|procuro fazer / faço questão de
ようになりました|ようになりました|passei a conseguir / passou a ser
らしい|らしい|parece ser / ouvi dizer que
ボタン|ボタン|botão
一度|いちど|uma vez / novamente
一生懸命|いっしょうけんめい|com muito esforço / intensamente
丁寧に|ていねいに|cuidadosamente / educadamente
上手に|じょうずに|bem / habilmente
中で|なかで|dentre / dentro de
予定です|よていです|pretendo / está programado
二日|ふつか|dois dias / dia dois
会って|あって|encontrando / depois de encontrar
会話|かいわ|conversa / diálogo
伝えます|つたえます|contarei / transmitirei
使います|つかいます|uso / utilizo
便利|べんり|prático / conveniente
入ってきました|はいってきました|entrou vindo para cá
入りました|はいりました|entrou
入門書|にゅうもんしょ|livro introdutório / manual inicial
全然|ぜんぜん|absolutamente / nada (com negação)
全部|ぜんぶ|tudo / inteiro
出さなければいけない|ださなければいけない|preciso entregar / devo apresentar
出ます|でます|sair / participar
出る|でる|sair / participar
分かりました|わかりました|entendi / compreendi
分かりません|わかりません|não entendo / não sei
分かりませんでした|わかりませんでした|não entendi
分かりやすい|わかりやすい|fácil de entender / claro
分かる|わかる|entender / saber
別|べつ|outro / diferente
勉強|べんきょう|estudo / estudar
午後|ごご|tarde / período da tarde
受けました|うけました|assisti / recebi
君|きみ|você / tu
呼ばれました|よばれました|fui chamado / foi chamado
問題|もんだい|questão / problema
場合は|ばあいは|no caso de / se
声|こえ|voz
大きな|おおきな|grande / alto
大切|たいせつ|importante / valioso
大切だ|たいせつだ|é importante
始める|はじめる|começar / iniciar
字|じ|letra / caractere
宿題|しゅくだい|tarefa de casa / dever
寒がり|さむがり|pessoa que sente muito frio
少しずつ|すこしずつ|aos poucos / pouco a pouco
延ばします|のばします|adiarei / prolongarei
弟|おとうと|irmão mais novo
後で|あとで|depois / mais tarde
必要がある|ひつようがある|ser necessário / precisar
忘れちゃいました|わすれちゃいました|acabei esquecendo
思った|おもった|pensei / achei
急に|きゅうに|de repente / subitamente
意味|いみ|significado / sentido
戻ります|もどります|voltarei / regressarei
押す|おす|apertar / empurrar
教えてあげます|おしえてあげます|ensinarei a alguém
教えてくれました|おしえてくれました|ensinou para mim
教えてやります|おしえてやります|ensinarei a alguém (informal)
文|ぶん|frase / texto
方法|ほうほう|método / maneira
明るくして|あかるくして|deixando claro / iluminando
時間|じかん|tempo / hora
暖かい|あたたかい|quente / confortável
暗い|くらい|escuro / sombrio
書いていました|かいていました|estava escrevendo
書かせます|かかせます|faz escrever / deixa escrever
書き終わりました|かきおわりました|terminei de escrever
最後|さいご|fim / último
最近|さいきん|ultimamente / recentemente
服|ふく|roupa / vestimenta
本当に|ほんとうに|realmente / de verdade
本物|ほんもの|coisa verdadeira / original
楽しそうに|たのしそうに|com aparência de alegria
毎朝|まいあさ|todas as manhãs
準備|じゅんび|preparação / preparo
漢字|かんじ|kanji / ideograma japonês
疲れましたが|つかれましたが|estava cansado mas
発表|はっぴょう|apresentação / exposição
着ます|きます|veste / coloca roupa
短い|みじかい|curto / breve
窓|まど|janela
笑い出しました|わらいだしました|começou a rir
答え|こたえ|resposta
答えてくれます|こたえてくれます|responderá para mim
答えられます|こたえられます|pode responder
終えた|おえた|terminou / concluiu
終わらせました|おわらせました|terminei / concluí
終わらせます|おわらせます|terminarei / concluirei
続けました|つづけました|continuei
続けます|つづけます|continuarei / continuo
続ける|つづける|continuar / prosseguir
練習|れんしゅう|prática / treino
聞いたらいいですか|きいたらいいですか|a quem devo perguntar / seria bom perguntar?
聞きに来てください|ききにきてください|venha ouvir, por favor
聞きました|ききました|ouvi / perguntei
聞く|きく|ouvir / perguntar
聞こうと思います|きこうとおもいます|penso em perguntar
行います|おこないます|realizarei / farei
行こう|いこう|vamos ir / irei
表現|ひょうげん|expressão / forma de dizer
見てもらいました|みてもらいました|pedi que visse para mim
覚えた|おぼえた|aprendi / memorizei
覚えました|おぼえました|aprendi / memorizei
覚えます|おぼえます|aprendo / memorizo
覚えられません|おぼえられません|não consigo memorizar
覚える|おぼえる|aprender / memorizar
言いました|いいました|disse / falou
試験|しけん|prova / exame
話|はなし|história / conversa
話したい|はなしたい|quero falar / desejo conversar
話している|はなしている|está falando
話せる|はなせる|conseguir falar / poder conversar
説明|せつめい|explicação / explicar
読んだらどう|よんだらどう|que tal ler?
読んでいただけませんか|よんでいただけませんか|poderia ler para mim?
読んでいました|よんでいました|estava lendo
読んでおきます|よんでおきます|lerei antes / deixarei lido
読んでみます|よんでみます|tentarei ler
調べてみます|しらべてみます|tentarei pesquisar
近く|ちかく|perto / proximidade
遅れてすみません|おくれてすみません|desculpe o atraso
閉めました|しめました|fechei
開きます|あきます|abre-se / abre
開けた|あけた|abriu / deixei aberto
開ける|あける|abrir algo
間|あいだ|durante / intervalo
間に|あいだに|enquanto / durante
間違い|まちがい|erro / engano
降っても|ふっても|mesmo se chover
降りそうだ|ふりそうだ|parece que vai chover
降り始めた|ふりはじめた|começou a chover
降る|ふる|chover
難しかった|むずかしかった|era difícil / foi difícil
難しくありません|むずかしくありません|não é difícil
難しさ|むずかしさ|dificuldade
面白い|おもしろい|interessante / divertido
音|おと|som / ruído
起きられます|おきられます|consigo acordar / pode levantar-se
六時|ろくじ|seis horas
読めば|よめば|se ler
読み始めました|よみはじめました|comecei a ler
読み間違える|よみまちがえる|ler errado
読みにくい|よみにくい|difícil de ler
読みません|よみません|não leio
読みたがっています|よみたがっています|quer ler (outra pessoa)
読みたがります|よみたがります|quer ler (outra pessoa)
読みづらい|よみづらい|difícil de ler
読みなさい|よみなさい|leia (ordem)
読みやすい|よみやすい|fácil de ler
読める|よめる|conseguir ler / ser legível
""".strip().splitlines()

for entry in GLOSS_TEXT:
    key,reading,meanings=entry.split("|",2)
    kind="vocabulário N4"
    GLOSS.setdefault(key,(reading,kind,[meaning.strip() for meaning in meanings.split(" / ")]))

GRAMMAR_KEYS=set("""間 間に あまり 後で あれば 場合は ばかり だけで 笑い出しました でございます でも ではないか が必要 がする 寒がり 読みたがっています がございます 読み始めました はずだ はずがない 必要がある 行こう いらっしゃいます いたします じゃないか かどうか かしら かい かもしれない かな から作られています きっと ごろ こと ことがある ことができる ことになりました ことにします 明るくして 急に までに まま または みたいだ みたいな みたいに な など 聞きながら なかなか 出さなければいけない しなければならない なら 読みなさい なさいます に気がつきました に見えます にします 読みにくい 中で のに のは お読みください お読みになります おきに 書き終わりました 起きられます らしい 難しさ さっき させられています 書かせます させてください さすが し そんなに それでも それに そうだ 楽しそうに ばかり ところ 読みたがります あったら 読んだらどう 聞いたらいいですか 会って 教えてあげます してほしい していきます 読んでいました 読んでいただけませんか 教えてくれました 入ってきました 調べてみます 見てもらいました 読んでおきます 忘れちゃいました 遅れてすみません 教えてやります してよかった しているところ 降っても と と言ってもいい という ということ と言われています と聞きました と思います とか 続けます って 呼ばれました やすい やっと より 予定です ようだ ように ようになりました ようにしています 聞こうと思います ぜひ 全然 読みづらい""".split())
for key in GRAMMAR_KEYS:
    if key in GLOSS:
        reading,_,meanings=GLOSS[key]
        GLOSS[key]=(reading,"estrutura gramatical",meanings)

def token(key):
    if key in GLOSS:
        reading,kind,meanings=GLOSS[key]
        return {"surface":key,"reading":reading,"kind":kind,"meanings_pt":meanings,"note_pt":"Uso desta palavra ou estrutura no contexto da frase."}
    source = L.get(key) or EXTRA.get(key)
    if source:
        if isinstance(source,tuple):
            surface,reading,kind,meanings,note=source if len(source)==5 else (key,*source)
            return {"surface":surface,"reading":reading,"kind":kind,"meanings_pt":meanings,"note_pt":note}
    if key in N5_TOKENS: return dict(N5_TOKENS[key])
    raise KeyError(key)

def build():
    rows=[line.split("|",2) for line in ROWS]
    if len({x[0] for x in rows}) != len(rows): raise ValueError("Duplicate grammar label")
    missing={word for topic,jp,pt in rows for word in jp.split() if word not in GLOSS and word not in L and word not in EXTRA and word not in N5_TOKENS}
    missing |= {word for before,_,after,_ in CONTEXTS for word in (before+" "+after).split() if word not in GLOSS and word not in L and word not in EXTRA and word not in N5_TOKENS}
    missing |= {word for word in "今日 も 家 で もう 一度".split() if word not in GLOSS and word not in L and word not in EXTRA and word not in N5_TOKENS}
    if missing: raise ValueError("Missing glossary: " + ", ".join(sorted(missing)))
    phrases=[]
    for index in range(400):
        topic,core,translation=rows[index % len(rows)]
        context_index=(index // len(rows)) % 4
        context_jp,context_pt,ending_jp,_=CONTEXTS[context_index]
        before=[token(word) for word in context_jp.split()]
        focus=[token(word) for word in core.split()]
        core_length=len(core.replace(" ",""))
        supplement="今日 も 家 で もう 一度" if core_length<=13 else "もう 一度" if core_length<=17 else ""
        before += [token(word) for word in supplement.split()]
        after=[token(word) for word in ending_jp.split()]
        tokens=before+focus+after
        comma_index=len(context_jp.split())-1
        display_after=[{"index":comma_index,"text":"、"}]
        if supplement:
            display_after.append({"index":len(before)-1,"text":"「"})
        else:
            display_after[0]["text"]="、「"
        display_after.append({"index":len(before)+len(focus)-1,"text":"」"})
        punctuation={item["index"]:item["text"] for item in display_after}
        text="".join(t["surface"]+punctuation.get(i,"") for i,t in enumerate(tokens))+"。"
        if not 40<=len(text)<=50: raise ValueError(f"Wrong length: {topic}: {len(text)}")
        supplement_pt=" hoje, em casa, mais uma vez" if core_length<=13 else " mais uma vez" if core_length<=17 else ""
        translation_pt=context_pt+supplement_pt+" “"+translation+"”."
        phrases.append({"id":1001+index,"level":"N4","category":"gramática N4","grammar_point":topic,
            "text":text,"translation_pt":translation_pt,"tokens":tokens,
            "focus_token_indices":list(range(len(before),len(before)+len(focus))),
            "display_after":display_after})
    from cenarios_n4 import extend
    extend(phrases)
    path=Path(__file__).with_name("Lista e Frases N4.json")
    path.write_text(json.dumps({"title":"Lista e Frases N4","language":"ja","translation_language":"pt-BR","phrases":phrases},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"{path}: {len(phrases)} frases, {len(rows)} tópicos, {min(map(lambda p:len(p['text']),phrases))} caracteres mínimos")

if __name__=="__main__": build()
