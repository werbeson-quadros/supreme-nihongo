"""Portuguese grammar notes shown for structures in the current sentence."""

import re


# label | meaning in context | formation / conjugation
_GUIDE = """
だ / です|Cópula que afirma identidade ou estado; です é polido e だ é informal.|Substantivo ou adjetivo な + です/だ; passado でした/だった; negativo ではありません/じゃない.
だけ|Limita a afirmação a uma quantidade ou opção: apenas, somente.|Substantivo ou forma simples do verbo + だけ; pode receber partículas depois: だけで, だけを.
だろう|Indica suposição ou probabilidade na fala informal.|Forma simples do verbo ou adjetivo + だろう; substantivo/adjetivo な + だろう. Forma polida: でしょう.
でしょう|Expressa suposição ou pede concordância de forma polida.|Forma simples do verbo/adjetivo + でしょう; substantivo/adjetivo な + でしょう, sem だ antes.
で|Marca lugar da ação, meio utilizado ou causa contextual.|Substantivo + で; depois de adjetivo な, で também liga descrições: 静かで.
でも|Introduz contraste: mas, porém; depois de substantivo pode significar até mesmo.|No início de uma oração, でも + frase. Como partícula, substantivo + でも.
が|Marca sujeito ou informação nova; também aparece em construções de preferência e capacidade.|Substantivo + が + predicado. Em orações de contraste, frase + が + frase.
は|Marca o tema sobre o qual se comenta algo; pronuncia-se わ.|Substantivo + は + comentário. Pode contrastar dois temas.
を|Marca o objeto direto afetado pela ação; pronuncia-se お.|Substantivo + を + verbo transitivo; também indica percurso com alguns verbos de movimento.
に|Marca destino, tempo específico, alvo ou resultado de mudança.|Substantivo + に + verbo; hora exata + に; adjetivo な + に + なる.
の|Liga substantivos e indica posse, origem ou especificação.|Substantivo + の + substantivo; no fim da frase, pode pedir ou dar explicação informal.
も|Acrescenta alguém ou algo: também.|Substantivo + も substitui は/が/を; depois de outras partículas pode aparecer como にも ou でも.
から|Indica ponto de partida ou razão: desde, de, porque.|Substantivo + から para origem; oração na forma simples ou polida + から para causa.
まで|Indica limite final de tempo ou lugar: até.|Substantivo de tempo/lugar + まで; difere de までに, que marca prazo.
と|Liga substantivos, cita fala/pensamento ou marca companhia.|Substantivo + と + substantivo; frase + と言う/思う; pessoa + と + verbo.
ね|Partícula final que busca concordância ou partilha uma observação.|Frase completa + ね; não muda a conjugação do predicado.
よ|Partícula final que informa ou enfatiza algo ao interlocutor.|Frase completa + よ; não muda a conjugação do predicado.
か|Transforma uma frase em pergunta ou apresenta alternativas.|Frase polida + か; AかBか para escolher entre alternativas.
な-adjectives|Adjetivo な descreve substantivo ou estado.|Raiz + な + substantivo; raiz + です no predicado; negativo ではない; passado でした.
い-adjectives|Adjetivo い descreve estado ou qualidade e flexiona seu final.|Raiz + い; negativo くない; passado かった; forma adverbial く.
ないで|Indica que uma ação não é feita antes ou enquanto outra ocorre.|Verbo na forma ない + で + outra ação; ないでください pede que não se faça algo.
ないでください|Pedido polido para não fazer uma ação.|Verbo na forma negativa ない + でください: 行かないでください.
なくてもいい|Diz que não é necessário fazer algo.|Verbo na forma ない sem い + くてもいい; 食べない → 食べなくてもいい.
ないといけない|Expressa necessidade ou obrigação.|Verbo na forma ない + といけない; em conversa, ないと pode ficar elíptico.
なくてはいけない|Expressa obrigação: é preciso fazer.|Verbo na forma ない sem い + くてはいけない; forma informal: なくちゃ.
なくてはならない|Expressa obrigação mais categórica.|Verbo na forma ない sem い + くてはならない.
ちゃいけない・じゃいけない|Proíbe uma ação em registro informal.|Forma て + はいけない → ちゃいけない; forma で + はいけない → じゃいけない.
てはいけない|Indica proibição: não se pode fazer.|Verbo na forma て + はいけない; com で: ではいけない.
てもいいです|Dá ou pede permissão para fazer algo.|Verbo na forma て + もいいです; pergunta: てもいいですか.
てください|Pedido direto e polido para fazer uma ação.|Verbo na forma て + ください; 読む → 読んでください.
ている|Expressa ação em andamento ou estado resultante.|Verbo na forma て + いる; polido ています; informal てる.
てから|Marca a ordem: depois de fazer a primeira ação.|Verbo na forma て + から + próxima ação.
たい|Expressa desejo do próprio falante de fazer uma ação.|Raiz da forma ます + たい; 食べます → 食べたい; flexiona como adjetivo い.
たことがある|Relata experiência anterior de fazer algo.|Verbo na forma passada simples た + ことがある; negativo たことがない.
たり～たり|Enumera ações como exemplos, sem exigir ordem rígida.|Verbos na forma た + り, repetidos, seguidos de する.
つもり|Indica intenção ou plano pessoal.|Verbo na forma de dicionário + つもり; para não fazer: forma ない + つもり.
ので|Apresenta uma razão de modo explicativo ou suave.|Verbo/adjetivo い na forma simples + ので; substantivo/adjetivo な + なので.
んです|Acrescenta explicação, contexto ou curiosidade.|Verbo/adjetivo い na forma simples + んです; substantivo/adjetivo な + なんです.
のです|Acrescenta explicação em estilo mais formal que んです.|Verbo/adjetivo い na forma simples + のです; substantivo/adjetivo な + なのです.
なる|Indica mudança de estado: tornar-se.|Adjetivo い sem い + くなる; adjetivo な ou substantivo + になる.
にする|Indica escolha ou mudança deliberada de estado.|Substantivo/adjetivo な + にする; adjetivo い sem い + くする.
間（あいだ）|Indica todo o período durante o qual uma situação continua.|Verbo na forma ている ou simples + 間; substantivo + の間; adjetivo な + な間.
間に（あいだに）|Marca uma ação que acontece em algum momento dentro de um período.|Verbo na forma simples + 間に; substantivo + の間に.
あまり～ない|Expressa baixa frequência ou intensidade: não muito.|あまり + verbo/adjetivo na forma negativa.
後で（あとで）|Localiza a ação depois de outra ação ou momento.|Verbo na forma た + 後で; substantivo + の後で.
ば|Condição hipotética: se determinada condição ocorrer.|Verbo grupo 1: som う → え + ば; grupo 2: retirar る + れば; い → ければ; な/名詞 → ならば.
場合は（ばあいは）|Apresenta uma situação ou hipótese: no caso de.|Verbo/adjetivo い na forma simples + 場合は; substantivo + の場合は; adjetivo な + な場合は.
ばかり|Indica predominância ou repetição: só, o tempo todo.|Substantivo + ばかり; verbo na forma て + ばかりいる para ação repetida.
だけで|Indica que apenas uma coisa basta ou é o meio usado.|Substantivo ou forma simples do verbo + だけで.
出す（だす）|Com verbo, indica começo repentino de uma ação.|Raiz da forma ます + 出す: 走ります → 走り出す.
でございます|Forma muito polida da cópula です.|Substantivo/adjetivo な + でございます; passado でございました.
ではないか|Propõe uma conclusão ou pede confirmação: não é que...?|Substantivo/adjetivo な + ではないか; verbo/adjetivo い na forma simples + のではないか.
が必要（がひつよう）|Indica que algo é necessário.|Substantivo + が必要だ/です; verbo na forma de dicionário + 必要がある.
がする|Indica percepção sensorial ou sensação.|Substantivo de som, cheiro, sabor ou sensação + がする.
がり|Forma substantivos para tendência ou desejo atribuído a outra pessoa.|Raiz de adjetivo い sem い + がり: 寒い → 寒がり.
がる / がっている|Descreve desejo ou sensação observável de outra pessoa.|Raiz de adjetivo い sem い + がる; たい sem い + がる; em andamento, がっている.
ございます|Forma muito polida de ある, usada para existência.|Substantivo + がございます; em atendimento, também em expressões fixas.
始める（はじめる）|Indica início de uma ação.|Raiz da forma ます + 始める: 読みます → 読み始める.
はずだ|Indica expectativa baseada em indícios: deve ser.|Verbo/adjetivo い na forma simples + はずだ; substantivo + のはず; adjetivo な + なはず.
はずがない|Nega uma possibilidade: não pode ser que.|Verbo/adjetivo い na forma simples + はずがない; substantivo + のはずがない.
必要がある（ひつようがある）|Indica necessidade de realizar uma ação.|Verbo na forma de dicionário + 必要がある; negativo 必要がない.
必要はありません|Indica que uma ação ou objeto não é necessário.|Substantivo + の必要はありません; verbo na forma de dicionário + 必要はありません.
意向形 （いこうけい）|Forma volitiva usada para convite ou intenção: vamos, vou.|Grupo 1: final う → おう; grupo 2: retirar る + よう; する → しよう; 来る → 来よう.
いらっしゃる|Forma honorífica de ir, vir ou estar para falar de outra pessoa.|Usa-se いらっしゃる no lugar de 行く/来る/いる; polido いらっしゃいます.
いたします|Forma humilde de します ao falar da própria ação.|Raiz verbal ou substantivo verbal + いたします; する → いたします.
じゃないか|Expressa surpresa, conclusão ou confirmação informal.|Forma simples + じゃないか; após substantivo/adjetivo な, liga-se diretamente.
かどうか|Indica uma pergunta indireta de sim ou não: se... ou não.|Oração na forma simples + かどうか + verbo como 知る/聞く.
かしら|Partícula final de dúvida ou reflexão, muitas vezes associada à fala feminina.|Frase na forma simples + かしら.
かい|Partícula final de pergunta informal.|Frase na forma simples + かい; comum em fala familiar.
かもしれない|Indica possibilidade incerta: talvez.|Verbo/adjetivo い na forma simples + かもしれない; substantivo/adjetivo な sem だ + かもしれない.
かな|Expressa dúvida pessoal: será que...?|Frase na forma simples + かな.
から作る（からつくる）|Indica material de origem transformado no produto final.|Material + から作る; se o material permanece reconhecível, usa-se frequentemente で作る.
きっと|Indica forte expectativa ou convicção: certamente.|きっと antes do predicado; não exige uma forma verbal específica.
頃（ころ / ごろ）|Indica época aproximada: por volta de.|Horário + ごろ; período ou oração + 頃.
こと|Nominaliza uma ação ou evento, permitindo tratá-lo como substantivo.|Verbo na forma simples + こと; pode receber partículas como が/を.
ことがある|Indica que algo às vezes acontece; com passado, experiência anterior.|Verbo na forma simples + ことがある; experiência: forma た + ことがある.
ことができる|Indica capacidade ou possibilidade de fazer algo.|Verbo na forma de dicionário + ことができる.
ことになる|Indica decisão ou resultado determinado por circunstâncias externas.|Verbo na forma de dicionário ou ない + ことになる.
ことにする|Indica decisão tomada pelo próprio falante.|Verbo na forma de dicionário ou ない + ことにする.
くする|Indica mudança deliberada de qualidade.|Adjetivo い sem い + くする: 大きい → 大きくする.
急に（きゅうに）|Marca mudança inesperada ou repentina.|急に vem antes da ação ou mudança; o verbo mantém a conjugação exigida pela frase.
までに|Marca prazo: até determinado momento.|Tempo + までに + ação concluída antes do limite; difere de まで, duração até o limite.
まま|Indica que um estado permanece inalterado durante outra ação.|Verbo na forma た + まま; substantivo + のまま; adjetivo な + なまま.
または|Liga alternativas: ou.|A または B; não exige conjugação especial.
みたいだ|Expressa semelhança ou impressão informal: parece.|Substantivo ou forma simples + みたいだ; como adjetivo な, みたいな + nome.
みたいな|Liga uma comparação a um substantivo: parecido com.|Substantivo ou forma simples + みたいな + substantivo.
みたいに|Liga uma comparação a verbo ou adjetivo: como se.|Substantivo ou forma simples + みたいに + verbo/adjetivo.
な|Partícula final informal de sentimento, ordem ou proibição conforme contexto.|Depois da frase, な expressa emoção; verbo no dicionário + な pode proibir.
など|Enumera exemplos não exaustivos: entre outros.|Substantivo + など; pode vir após uma lista.
ながら|Indica duas ações simultâneas com o mesmo sujeito.|Raiz da forma ます + ながら + ação principal.
なかなか～ない|Expressa que algo custa a acontecer: não facilmente.|なかなか + predicado negativo.
なければいけない|Expressa obrigação: tem que fazer.|Verbo na forma ない sem い + なければいけない.
なければならない|Expressa obrigação formal: é necessário fazer.|Verbo na forma ない sem い + なければならない.
なら|Estabelece condição com base no tema mencionado: se for.|Substantivo ou forma simples do verbo/adjetivo + なら.
なさい|Dá uma instrução direta, geralmente de alguém em posição de autoridade.|Raiz da forma ます + なさい: 読みます → 読みなさい.
なさる|Forma honorífica de する para ações de outra pessoa.|Substantivo verbal + なさる; forma polida なさいます.
に気がつく（にきがつく）|Indica perceber ou notar alguma coisa.|Substantivo + に気がつく; oração nominalizada + ことに気がつく.
に見える（にみえる）|Indica a aparência visual de algo.|Substantivo/adjetivo な + に見える; adjetivo い sem い + く見える.
にくい|Indica que uma ação é difícil de fazer.|Raiz da forma ます + にくい; flexiona como adjetivo い.
の中で（のなかで）|Delimita um grupo dentro do qual se faz comparação.|Grupo + の中で + avaliação ou superlativo.
のに（逆接）|Contrasta o resultado com o esperado: embora, apesar de.|Verbo/adjetivo い na forma simples + のに; substantivo/adjetivo な + なのに.
のに（目的）|Indica finalidade ou uso: para fazer algo.|Verbo na forma de dicionário + のに + 便利/使う/必要.
のは〜だ|Destaca uma parte da frase como tópico e a identifica.|Oração na forma simples + のは + substantivo/descrição + だ/です.
お～ください|Pedido respeitoso para a ação do interlocutor.|お + raiz da forma ます + ください; com palavras sinojaponesas, ご + substantivo verbal + ください.
お～になる|Forma honorífica para ação de outra pessoa.|お + raiz da forma ます + になる; com verbo sinojaponês, ご + substantivo verbal + になる.
おきに|Expressa intervalos regulares: a cada.|Número + unidade de tempo + おきに; por exemplo 一日おきに.
終わる（おわる）|Indica fim de uma atividade.|Raiz da forma ます + 終わる: 読みます → 読み終わる.
られる（可能）|Forma potencial que expressa capacidade ou possibilidade.|Grupo 2: retirar る + られる; grupo 1: final う → え + る; する → できる; 来る → 来られる.
らしい|Expressa inferência baseada em informação ou sinais: parece.|Verbo/adjetivo na forma simples + らしい; substantivo + らしい.
さ|Transforma adjetivo em substantivo de grau ou medida.|Adjetivo い sem い + さ; adjetivo な sem な + さ.
さっき|Indica passado recente: agora há pouco.|Advérbio antes da ação; o verbo costuma aparecer no passado.
させられる|Forma causativa passiva: ser obrigado a fazer.|Primeiro forme a causativa em させる/せる e depois a passiva: 食べさせられる.
させる|Forma causativa: fazer ou deixar outra pessoa agir.|Grupo 1: final う → あ + せる; grupo 2: retirar る + させる; する → させる.
させてください|Pedido para receber permissão de fazer algo.|Verbo na forma causativa させる → させて + ください.
さすが|Expressa admiração compatível com a reputação de alguém: como esperado.|さすが vem antes da avaliação; pode aparecer como さすがに.
し|Enumera razões ou qualidades, sugerindo que há outras.|Oração na forma simples + し; substantivo/adjetivo な + だし.
そんなに|Indica intensidade: tanto assim; frequentemente com negação.|そんなに antes do predicado; a forma negativa produz não tanto assim.
それでも|Contrasta com a situação anterior: mesmo assim.|Conector no início da frase seguinte; sem mudança de conjugação.
それに|Acrescenta outra informação ou razão: além disso.|Conector no início da frase seguinte; sem mudança de conjugação.
そうだ（伝聞）|Transmite uma informação ouvida de terceiros: dizem que.|Verbo/adjetivo い na forma simples + そうだ; substantivo/adjetivo な + だそうだ.
そうだ（様態）|Expressa aparência baseada no que se vê: parece que vai.|Raiz da forma ます + そう; adjetivo い sem い + そう; negativo そうにない.
そうに / そうな|Liga a aparência a verbo ou substantivo.|Raiz da forma ます ou adjetivo い sem い + そうに + verbo / そうな + substantivo.
たばかり|Indica que uma ação aconteceu há pouco, na percepção do falante.|Verbo na forma た + ばかり.
たところ|Indica conclusão imediata de uma ação: acabei de.|Verbo na forma た + ところ; em andamento: ているところ.
他動詞 & 自動詞（たどうし & じどうし）|Contrasta ação sobre um objeto e mudança que ocorre no sujeito.|Transitivo: objeto + を + verbo; intransitivo: sujeito + が + verbo. Compare 開ける/開く.
たがる|Expressa desejo observável de outra pessoa.|Raiz da forma ます + たがる; em andamento, たがっている.
たら|Condição ou sequência: se/quando acontecer.|Verbo/adjetivo na forma た + ら; substantivo/adjetivo な + だったら.
たらどう|Faz uma sugestão informal: que tal se...?|Verbo na forma た + らどう; forma polida たらどうですか.
たらいいですか|Pede conselho sobre o que fazer.|Verbo na forma た + らいいですか.
て / で|Liga ações em sequência ou combina estados.|Verbo na forma て/で + próxima ação; adjetivo い sem い + くて; adjetivo な + で.
てあげる|Indica que alguém faz uma ação em benefício de outra pessoa.|Verbo na forma て + あげる; cuidado com o contexto social.
てほしい|Expressa desejo de que outra pessoa faça algo.|Pessoa + に + verbo na forma て + ほしい.
ていく|Indica movimento para longe ou mudança que prossegue no futuro.|Verbo na forma て + いく; informal てく.
ていた|Marca ação em curso ou estado no passado.|Verbo na forma て + いた; polido ていました.
ていただけませんか|Pedido muito polido para que alguém faça algo.|Verbo na forma て + いただけませんか.
てくれる|Indica que alguém faz uma ação em benefício do falante.|Verbo na forma て + くれる; polido てくれます.
てくる|Indica movimento em direção ao falante ou mudança até o presente.|Verbo na forma て + くる; passado てきた.
てみる|Indica experimentar fazer algo.|Verbo na forma て + みる; passado てみた.
てもらう|Indica receber de alguém o favor de uma ação.|Pessoa + に + verbo na forma て + もらう.
ておく|Indica fazer algo antecipadamente ou deixar em certo estado.|Verbo na forma て + おく; informal とく.
てしまう / ちゃう|Indica conclusão total ou resultado indesejado.|Verbo na forma て + しまう; informal てしまう → ちゃう, でしまう → じゃう.
てすみません|Pedido de desculpas por uma ação.|Verbo na forma て + すみません.
てやる|Indica fazer algo em benefício de alguém de posição próxima/inferior; pode soar rude.|Verbo na forma て + やる.
てよかった|Expressa alívio ou satisfação por ter feito algo.|Verbo na forma て + よかった.
ているところ|Indica que a ação está acontecendo justamente agora.|Verbo na forma ている + ところ; polido ているところです.
ても|Indica concessão: mesmo que.|Verbo na forma て + も; adjetivo い sem い + くても; substantivo/adjetivo な + でも.
ても構いません|Dá permissão de modo polido: não há problema em fazer.|Verbo na forma て + も構いません; pergunta ても構いませんか.
と（条件）|Condição de resultado habitual ou automático: quando/se.|Oração na forma simples presente + と + consequência; normalmente não exprime vontade nessa consequência.
と言ってもいい（といってもいい）|Indica que uma descrição é aceitável: pode-se dizer que.|Oração ou termo + と言ってもいい.
という|Apresenta nome, citação ou definição: chamado, que.|Nome ou oração + という + substantivo.
ということ|Transforma uma informação citada em fato ou conclusão.|Oração na forma simples + ということ.
と言われている（といわれている）|Relata opinião ou informação geralmente aceita.|Oração na forma simples + と言われている.
と聞いた（ときいた）|Relata algo ouvido de outra pessoa.|Oração na forma simples + と聞いた.
と思う（とおもう）|Expressa opinião ou pensamento.|Oração na forma simples + と思う; substantivo/adjetivo な + だと思う.
とか～とか|Enumera exemplos informais sem lista completa.|AとかBとか; pode terminar em など.
ところ|Marca momento da ação: prestes a, em andamento ou recém concluída.|Dicionário + ところ: prestes a; ているところ: agora; たところ: acabou de.
続ける（つづける）|Indica continuidade de uma ação.|Raiz da forma ます + 続ける: 話します → 話し続ける.
って|Citação ou marcador de tema informal.|Oração + って + 言う/聞く; substantivo + って como tópico informal.
受身形（うけみけい）|Voz passiva: o sujeito recebe a ação.|Grupo 1: final う → あ + れる; grupo 2: retirar る + られる; する → される.
は〜が… は|Compara dois aspectos contrastantes de um mesmo tema.|Tema + は + aspecto + が + descrição; segundo aspecto + は + descrição contrastante.
やすい|Indica facilidade de realizar a ação.|Raiz da forma ます + やすい; flexiona como adjetivo い.
やっと|Indica que algo finalmente aconteceu após esforço ou demora.|やっと antes do verbo no resultado final; não exige conjugação especial.
より|Marca o termo de comparação: mais ... que.|AよりBのほうが + adjetivo; ou BはAより + adjetivo.
予定だ（よていだ）|Indica plano ou compromisso previsto.|Verbo na forma de dicionário + 予定だ; substantivo + の予定だ.
ようだ|Indica inferência ou aparência: parece.|Verbo/adjetivo い na forma simples + ようだ; substantivo + のようだ; adjetivo な + なようだ.
ように / ような|Liga comparação ou finalidade a verbo/substantivo.|Oração simples + ように + verbo; substantivo + のような + substantivo.
ようになる|Indica mudança gradual de capacidade ou hábito.|Verbo na forma de dicionário ou potencial + ようになる.
ようにする|Indica esforço deliberado para manter hábito.|Verbo na forma de dicionário ou ない + ようにする.
ようと思う（ようとおもう）|Expressa intenção formada pelo falante.|Verbo na forma volitiva + と思う: 行こうと思う.
ぜひ|Reforça convite ou desejo: com certeza, por favor.|ぜひ antes do verbo ou pedido; não exige conjugação especial.
全然～ない（ぜんぜん～ない）|Enfatiza negação: de jeito nenhum.|全然 + verbo ou adjetivo na forma negativa.
づらい|Indica dificuldade psicológica ou prática de realizar a ação.|Raiz da forma ます + づらい; flexiona como adjetivo い.
どんな|Pergunta que tipo de pessoa ou coisa é.|どんな + substantivo; a resposta descreve uma qualidade ou categoria.
どうして|Pergunta a razão: por que?|どうして + oração interrogativa; a resposta pode terminar em から ou ので.
どうやって|Pergunta o método: como se faz?|どうやって + verbo interrogativo; a resposta descreve etapas ou meios.
があります|Afirma a existência de coisas inanimadas.|Lugar + に + objeto + がある/あります; negativo ありません.
がほしい|Expressa desejo de possuir algo.|Objeto desejado + がほしい; negativo ほしくない; passado ほしかった.
がいます|Afirma a existência de pessoas ou animais.|Lugar + に + pessoa/animal + がいる/います; negativo いません.
一番（いちばん）|Marca grau máximo: o mais.|Grupo + の中で + Aが一番 + adjetivo; também 一番 antes de adjetivo.
一緒に（いっしょに）|Indica que uma ação é feita junto com alguém.|Pessoa + と一緒に + verbo; pode usar 一緒に antes do verbo.
いつも|Indica frequência habitual: sempre.|いつも antes do verbo ou predicado habitual; negativo いつも～わけではない para nem sempre.
じゃない・ではない|Nega substantivos e adjetivos な.|Substantivo/adjetivo な + じゃない (informal) ou ではありません (polido).
か～か|Apresenta duas ou mais alternativas.|AかBか; com orações, forma simples + か + forma simples + か.
方（かた）|Indica maneira de realizar uma ação.|Raiz da forma ます + 方: 読みます → 読み方.
けれども|Liga ideias em contraste de modo mais formal que けど.|Oração na forma simples ou polida + けれども.
まだ|Indica continuidade ou que algo ainda não ocorreu.|まだ + afirmativo: ainda; まだ + negativo: ainda não.
まだ～ていません|Diz que uma ação ainda não foi concluída.|まだ + verbo na forma て + いません.
前に（まえに）|Indica que uma ação ocorre antes de outra.|Verbo na forma de dicionário + 前に; substantivo + の前に.
ませんか|Convite polido formulado como pergunta negativa.|Raiz da forma ます + ませんか: 行きます → 行きませんか.
ましょう|Convite ou decisão conjunta: vamos.|Raiz da forma ます + ましょう: 食べます → 食べましょう.
ましょうか|Oferta ou proposta cortês: devo fazer?|Raiz da forma ます + ましょうか.
もう|Indica conclusão ou mudança já ocorrida: já.|もう + verbo passado/afirmativo; com negativo, もう～ない pode indicar não mais.
なあ|Partícula final que expressa sentimento ou admiração.|Frase na forma simples + なあ; não altera o verbo.
なくちゃ|Forma oral abreviada de obrigação.|Forma ない sem い + なくちゃ; abrevia なくてはいけない.
に行く（にいく）|Indica objetivo de um deslocamento: ir fazer algo.|Raiz da forma ます + に行く; substantivo de atividade + に行く.
に/へ|Indica direção ou destino.|Lugar + に/へ + verbo de movimento; へ pronuncia-se え como partícula.
のが下手（のがへた）|Diz que alguém não tem habilidade em uma ação.|Verbo na forma de dicionário + のが下手だ/です.
のが上手（のがじょうず）|Diz que alguém é bom em uma ação.|Verbo na forma de dicionário + のが上手だ/です.
のが好き（のがすき）|Expressa gosto por fazer uma ação.|Verbo na forma de dicionário + のが好きだ/です.
の中で[A]が一番（のなかで[A]がいちばん）|Identifica o melhor ou maior dentro de um grupo.|Grupo + の中で + Aが一番 + adjetivo.
お / ご|Prefixos honoríficos que tornam a expressão respeitosa.|お + palavra japonesa; ご + palavra sinojaponesa em usos habituais, como ご家族.
をください|Pedido para receber um objeto.|Substantivo + をください; para pedir uma ação, forma て + ください.
しかし|Conector de contraste formal: porém.|No começo da frase seguinte; não altera a conjugação.
それから|Conector de sequência: depois disso.|No início da próxima oração ou frase; o verbo mantém sua conjugação.
そして|Conector aditivo ou sequencial: e então.|No início da oração seguinte; não exige conjugação especial.
すぎる|Indica excesso: fazer ou ser demais.|Raiz da forma ます + すぎる; adjetivo い sem い + すぎる; adjetivo な sem な + すぎる.
てある|Indica estado resultante de uma ação intencional.|Verbo transitivo na forma て + ある; objeto frequentemente marcado por が.
とき|Marca o momento em que algo acontece.|Verbo/adjetivo い na forma simples + とき; substantivo + のとき; adjetivo な + なとき.
とても|Intensifica uma qualidade: muito.|とても antes de adjetivo ou predicado; não altera conjugação.
は〜より・・・です|Compara dois elementos, afirmando que um possui mais uma qualidade.|AはBより + adjetivo + です.
はどうですか|Pede opinião ou oferece algo: que tal?|Substantivo + はどうですか; verbo na forma て + はどうですか para sugestão.
や|Enumera alguns itens, sem esgotar a lista.|AやB; muitas vezes termina com など.
より～ほうが|Indica que uma alternativa supera a outra.|AよりBのほうが + adjetivo/descrição.
のに / potencial|Combina concessão e capacidade nesta frase.|Forma simples + のに indica contraste; verbo potencial expressa poder fazer (grupo 2: られる; grupo 1: som え + る).
てもいい|Indica permissão ou possibilidade aceitável.|Verbo na forma て + もいい; pergunta てもいいですか.
ようと思う|Expressa intenção.|Verbo na forma volitiva + と思う.
続ける|Indica continuidade.|Raiz da forma ます + 続ける.
始める|Indica início.|Raiz da forma ます + 始める.
必要がある|Indica necessidade.|Verbo na forma de dicionário + 必要がある.
てしまう|Indica conclusão ou arrependimento.|Verbo na forma て + しまう; informal ちゃう/じゃう.
べきだ|Expressa dever ou recomendação forte.|Verbo na forma de dicionário + べきだ; する → すべき/するべき.
べきではない|Expressa que não se deve fazer algo.|Verbo na forma de dicionário + べきではない.
代わりに|Indica substituição ou alternativa: em vez de.|Substantivo + の代わりに; verbo na forma simples + 代わりに.
結局|Resume um resultado final: no fim das contas.|Advérbio antes da conclusão; não muda a conjugação verbal.
だらけ|Indica que há muitas coisas indesejadas de um tipo.|Substantivo + だらけ: 間違いだらけ.
気味|Indica leve tendência ou sinal de um estado.|Substantivo ou raiz da forma ます + 気味: 疲れ気味.
ごとに|Indica repetição a cada intervalo ou unidade.|Substantivo ou número + ごとに.
ほど～ない|Comparação negativa: não tão ... quanto.|AはBほど + adjetivo/verbo negativo.
一度に|Indica simultaneidade: de uma vez.|一度に antes da ação; não requer conjugação especial.
一方だ|Indica tendência contínua em uma direção.|Verbo na forma de dicionário + 一方だ.
ふりをする|Indica fingir que faz ou é algo.|Verbo/adjetivo い na forma simples + ふりをする; substantivo/adjetivo な + の/なふり.
かける|Indica ação começada mas ainda não concluída.|Raiz da forma ます + かける; 読みかける.
おかげで|Indica causa favorável: graças a.|Substantivo + のおかげで; verbo na forma simples + おかげで.
せいで|Indica causa desfavorável: por culpa de.|Substantivo + のせいで; verbo na forma simples + せいで.
に関して|Indica o assunto tratado: sobre, em relação a.|Substantivo + に関して + comentário; に関する + substantivo.
にとって|Marca o ponto de vista de alguém: para.|Pessoa/grupo + にとって + avaliação.
に対して|Indica alvo de ação ou comparação: em relação a.|Substantivo + に対して + ação; に対する + substantivo.
によって|Indica agente, causa, meio ou variação conforme contexto.|Substantivo + によって + predicado; による + substantivo.
うちに|Indica que algo acontece enquanto uma condição dura.|Verbo na forma simples + うちに; substantivo + のうちに.
につれて|Indica mudança proporcional: à medida que.|Verbo na forma de dicionário ou substantivo + につれて.
"""

GUIDE = {}
for line in _GUIDE.strip().splitlines():
    label, meaning, formation = line.split("|", 2)
    GUIDE[label] = {"title": label, "meaning_pt": meaning, "formation_pt": formation}

# Check specific constructions before shorter overlapping expressions.
DETECT = [
    (r"ていただけませんか", "ていただけませんか"),
    (r"ても構いません", "ても構いません"),
    (r"なければいけな|おかなければ", "なければいけない"),
    (r"ないといけな|ないとね", "ないといけない"),
    (r"ことにな", "ことになる"),
    (r"ことができ", "ことができる"),
    (r"たことがあ", "たことがある"),
    (r"かもしれ", "かもしれない"),
    (r"らしい", "らしい"),
    (r"ながら", "ながら"),
    (r"より.*ほうが", "より～ほうが"),
    (r"より", "より"),
    (r"ほうが", "ほうがいい"),
    (r"てしま|ちゃっ|じゃっ", "てしまう / ちゃう"),
    (r"てお|とく", "ておく"),
    (r"てくれ|てくれた", "てくれる"),
    (r"てあげ|であげ", "てあげる"),
    (r"ていこ|ていく|っていこ|っていく", "ていく"),
    (r"てきま|てきた|ってきま|ってきた", "てくる"),
    (r"てみ", "てみる"),
    (r"てから", "てから"),
    (r"(?<!と)ても", "ても"),
    (r"じゃダめ|じゃダメ|ちゃいけない|てはいけない", "てはいけない"),
    (r"たら", "たら"),
    (r"てください", "てください"),
    (r"って(?=言|聞|。|、|よ|ね)", "って"),
    (r"間に", "間に（あいだに）"),
    (r"と思", "と思う（とおもう）"),
    (r"と考え", "と考える"),
    (r"だろう", "だろう"),
    (r"でしょう", "でしょう"),
    (r"までに", "までに"),
    (r"まで", "まで"),
    (r"のです|んです|なんだ|のよ", "んです"),
    (r"そうにない", "そうだ（様態）"),
    (r"ている|てる|ていま|ってて", "ている"),
    (r"(?<!それ)から", "から"),
    (r"けど|ですが", "けど"),
    (r"もら", "てもらう"),
    (r"なら(?!な)", "なら"),
    (r"じゃない", "じゃない・ではない"),
    (r"必要はありません", "必要はありません"),
    (r"必要", "必要がある（ひつようがある）"),
    (r"になった|になりま", "なる"),
    (r"だね|ですよ", "だ / です"),
    (r"によって", "によって"),
]

ALIASES = {
    "ほうがいい":"ほうがいい", "けど":"けど", "だろう":"だろう",
    "てくれる":"てくれる", "ちゃいけない・じゃいけない":"ちゃいけない・じゃいけない",
}

GUIDE.update({
    "ほうがいい":{"title":"ほうがいい","meaning_pt":"Compara alternativas e recomenda a mais adequada.",
        "formation_pt":"Verbo na forma た + ほうがいい para recomendar; forma ない + ほうがいい para aconselhar evitar."},
    "けど":{"title":"けど","meaning_pt":"Liga duas ideias em contraste: mas, embora.",
        "formation_pt":"Oração na forma simples + けど; substantivo/adjetivo な + だけど. けれども é mais formal."},
    "てくれる":{"title":"てくれる","meaning_pt":"Alguém faz algo em benefício do falante.",
        "formation_pt":"Verbo na forma て + くれる; passado てくれた; pedido てくれますか."},
    "と考える":{"title":"と考える","meaning_pt":"Introduz uma opinião ou interpretação: considerar que.",
        "formation_pt":"Oração na forma simples + と考える; progressivo と考えている; polido と考えます."},
})


def grammar_details(phrase):
    """Find the main corpus topic and additional constructions actually in text."""
    text = phrase["text"]
    primary = phrase.get("grammar_point", "")
    labels = []
    if primary and primary != "legenda de vídeo":
        if primary in GUIDE: labels.append(primary)
        labels.extend(part.strip() for part in primary.split(" / "))
    labels.extend(label for pattern,label in DETECT if re.search(pattern,text))
    found = []
    seen = set()
    for label in labels:
        if label == "まで" and "までに" in text: continue
        if label in ("より","ほうがいい") and re.search(r"より.*ほうが",text): continue
        if label == "ても" and "ても構いません" in text: continue
        if label == "必要がある（ひつようがある）" and "必要はありません" in text: continue
        key = label if label in GUIDE else primary if primary in GUIDE else None
        if not key or key in seen: continue
        seen.add(key)
        found.append({**GUIDE[key], "example_jp": text})
    if not found and phrase.get("grammar_explanation_pt"):
        found.append({"title":primary,"meaning_pt":phrase["grammar_explanation_pt"],
                      "formation_pt":"Observe na frase a forma ligada ao verbo, adjetivo ou substantivo anterior.","example_jp":text})
    if not found:
        fallback = GUIDE["だ / です"] if re.search(r"です|だ[。！？]",text) else GUIDE["は"]
        found.append({**fallback,"example_jp":text})
    return found
