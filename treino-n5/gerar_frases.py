"""Build the self-contained N5 sentence bank from reviewed lexical entries."""
import json
from pathlib import Path

# surface, reading, class, Portuguese meanings, grammar/usage note
L = {
"私":("私","わたし","pronome",["eu","meu/minha (com の)"],"Pronome pessoal neutro."),
"あなた":("あなた","あなた","pronome",["você"],"Em japonês, muitas vezes é omitido quando o contexto identifica a pessoa."),
"彼":("彼","かれ","pronome",["ele","namorado"],"O contexto determina o sentido."),
"彼女":("彼女","かのじょ","pronome",["ela","namorada"],"O contexto determina o sentido."),
"これ":("これ","これ","demonstrativo",["isto","este objeto"],"Objeto perto de quem fala."),
"それ":("それ","それ","demonstrativo",["isso","esse objeto"],"Objeto perto de quem ouve."),
"あれ":("あれ","あれ","demonstrativo",["aquilo","aquele objeto"],"Objeto longe dos dois."),
"この":("この","この","determinante",["este","esta"],"Vem antes de um substantivo."),
"その":("その","その","determinante",["esse","essa"],"Vem antes de um substantivo."),
"どの":("どの","どの","determinante",["qual"],"Vem antes de um substantivo."),
"ここ":("ここ","ここ","advérbio",["aqui","este lugar"],"Lugar perto de quem fala."),
"そこ":("そこ","そこ","advérbio",["aí","esse lugar"],"Lugar perto de quem ouve."),
"どこ":("どこ","どこ","advérbio",["onde","qual lugar"],"Pergunta por lugar."),
"だれ":("だれ","だれ","pronome interrogativo",["quem"],"Pergunta por pessoa."),
"何":("何","なに","pronome interrogativo",["o quê","qual coisa"],"Antes de です, comumente lido なん."),
"いつ":("いつ","いつ","advérbio interrogativo",["quando"],"Pergunta por tempo."),
"いくら":("いくら","いくら","advérbio interrogativo",["quanto custa","quanto"],"Pergunta por preço."),
"は":("は","わ","partícula",["tópico da frase","quanto a"],"Escrita は, pronunciada わ quando partícula."),
"が":("が","が","partícula",["sujeito","ênfase no sujeito"],"Marca sujeito ou informação nova; também acompanha 好き e 分かる."),
"を":("を","お","partícula",["objeto direto","percurso"],"Pronunciada お; marca o objeto da ação."),
"に":("に","に","partícula",["destino","momento","local de existência","beneficiário"],"O sentido depende do verbo e do contexto."),
"で":("で","で","partícula",["local da ação","meio","instrumento"],"Indica onde ocorre a ação ou o meio usado."),
"へ":("へ","え","partícula",["em direção a","para"],"Pronunciada え quando partícula."),
"の":("の","の","partícula",["posse","ligação entre substantivos","de"],"Liga dois substantivos."),
"と":("と","と","partícula",["e","com","citação"],"Une substantivos ou indica companhia."),
"も":("も","も","partícula",["também","até"],"Substitui は/が/を conforme a função."),
"から":("から","から","partícula",["de","desde","porque"],"Marca origem, início ou motivo."),
"まで":("まで","まで","partícula",["até"],"Marca limite de tempo ou lugar."),
"か":("か","か","partícula",["pergunta","ou"],"No fim da frase forma pergunta."),
"ね":("ね","ね","partícula final",["não é?","né?"],"Pede concordância ou compartilha percepção."),
"よ":("よ","よ","partícula final",["ênfase","informação nova"],"Reforça o que se informa ao ouvinte."),
"です":("です","です","cópula polida",["é","sou","está"],"Forma polida não passada; a tradução depende do predicado."),
"でした":("でした","でした","cópula polida",["era","foi","estava"],"Passado polido de です."),
"ではありません":("ではありません","ではありません","estrutura gramatical",["não é","não sou"],"Negação polida de substantivos e adjetivos な."),
"でしたか":("でしたか","でしたか","estrutura gramatical",["era?","foi?"],"Cópula passada polida com pergunta."),
"あります":("あります","あります","verbo",["há","existe","tenho"],"Existência de objetos e plantas; forma polida."),
"います":("います","います","verbo",["há","está","existe"],"Existência de seres animados; forma polida."),
"ありません":("ありません","ありません","verbo",["não há","não tenho"],"Negação polida de あります."),
"いません":("いません","いません","verbo",["não está","não há"],"Negação polida de います."),
"行きます":("行きます","いきます","verbo",["vou","vai","ir"],"Forma polida não passada de 行く."),
"来ます":("来ます","きます","verbo",["venho","vem","vir"],"Forma polida não passada de 来る."),
"帰ります":("帰ります","かえります","verbo",["volto","regresso"],"Forma polida não passada de 帰る."),
"食べます":("食べます","たべます","verbo",["como","come","comer"],"Forma polida não passada."),
"飲みます":("飲みます","のみます","verbo",["bebo","bebe","beber"],"Forma polida não passada."),
"見ます":("見ます","みます","verbo",["vejo","assisto","olho"],"Forma polida não passada."),
"聞きます":("聞きます","ききます","verbo",["ouço","pergunto","escuto"],"O contexto diferencia ouvir e perguntar."),
"読みます":("読みます","よみます","verbo",["leio","ler"],"Forma polida não passada."),
"書きます":("書きます","かきます","verbo",["escrevo","escrever"],"Forma polida não passada."),
"買います":("買います","かいます","verbo",["compro","comprar"],"Forma polida não passada."),
"話します":("話します","はなします","verbo",["falo","converso"],"Forma polida não passada."),
"勉強します":("勉強します","べんきょうします","verbo",["estudo","estudar"],"Substantivo verbal 勉強 + します."),
"働きます":("働きます","はたらきます","verbo",["trabalho","trabalhar"],"Forma polida não passada."),
"寝ます":("寝ます","ねます","verbo",["durmo","vou dormir"],"Forma polida não passada."),
"起きます":("起きます","おきます","verbo",["acordo","levanto"],"Forma polida não passada."),
"待ちます":("待ちます","まちます","verbo",["espero","aguardo"],"Forma polida não passada."),
"分かります":("分かります","わかります","verbo",["entendo","sei"],"O objeto entendido costuma ser marcado por が."),
"できません":("できません","できません","verbo",["não consigo","não posso fazer"],"Negação polida de できる."),
"食べました":("食べました","たべました","verbo",["comi","comeu"],"Passado polido de 食べる."),
"飲みました":("飲みました","のみました","verbo",["bebi","bebeu"],"Passado polido de 飲む."),
"行きました":("行きました","いきました","verbo",["fui","foi"],"Passado polido de 行く."),
"見ました":("見ました","みました","verbo",["vi","assisti"],"Passado polido de 見る."),
"買いました":("買いました","かいました","verbo",["comprei","comprou"],"Passado polido de 買う."),
"読みました":("読みました","よみました","verbo",["li","leu"],"Passado polido de 読む."),
"食べません":("食べません","たべません","verbo",["não como","não come"],"Negação polida de 食べる."),
"飲みません":("飲みません","のみません","verbo",["não bebo","não bebe"],"Negação polida de 飲む."),
"行きません":("行きません","いきません","verbo",["não vou","não vai"],"Negação polida de 行く."),
"見ません":("見ません","みません","verbo",["não vejo","não assisto"],"Negação polida de 見る."),
"ください":("ください","ください","estrutura gramatical",["por favor, dê","por favor, faça"],"Pedido polido; com objeto, significa 'dê-me'."),
"ましょう":("ましょう","ましょう","estrutura gramatical",["vamos","que tal fazermos"],"Forma volitiva polida, ligada à base verbal."),
"食べましょう":("食べましょう","たべましょう","verbo",["vamos comer"],"Convite polido: base de 食べる + ましょう."),
"行きましょう":("行きましょう","いきましょう","verbo",["vamos ir"],"Convite polido: base de 行く + ましょう."),
"飲みましょう":("飲みましょう","のみましょう","verbo",["vamos beber"],"Convite polido: base de 飲む + ましょう."),
"今日":("今日","きょう","substantivo",["hoje"],"Expressão de tempo; geralmente dispensa に."),
"明日":("明日","あした","substantivo",["amanhã"],"Expressão de tempo; geralmente dispensa に."),
"昨日":("昨日","きのう","substantivo",["ontem"],"Expressão de tempo; geralmente dispensa に."),
"毎日":("毎日","まいにち","substantivo",["todos os dias","diariamente"],"Frequência diária."),
"朝":("朝","あさ","substantivo",["manhã"],"Período do dia."),
"昼":("昼","ひる","substantivo",["meio-dia","dia"],"Período diurno."),
"夜":("夜","よる","substantivo",["noite"],"Período do dia."),
"今":("今","いま","substantivo",["agora"],"Momento atual."),
"七時":("七時","しちじ","expressão de tempo",["sete horas"],"Hora marcada por に quando indica momento da ação."),
"八時":("八時","はちじ","expressão de tempo",["oito horas"],"Hora marcada por に quando indica momento da ação."),
"九時":("九時","くじ","expressão de tempo",["nove horas"],"九時 lê-se くじ."),
"三時":("三時","さんじ","expressão de tempo",["três horas"],"Hora do relógio."),
"月曜日":("月曜日","げつようび","substantivo",["segunda-feira"],"Dia da semana."),
"日曜日":("日曜日","にちようび","substantivo",["domingo"],"Dia da semana."),
"学校":("学校","がっこう","substantivo",["escola"],"Local de estudo."),
"大学":("大学","だいがく","substantivo",["universidade","faculdade"],"Instituição de ensino superior."),
"家":("家","いえ","substantivo",["casa","lar"],"Pode ler うち em outros contextos."),
"駅":("駅","えき","substantivo",["estação"],"Estação ferroviária no contexto usual."),
"店":("店","みせ","substantivo",["loja","estabelecimento"],"Loja ou ponto comercial."),
"図書館":("図書館","としょかん","substantivo",["biblioteca"],"Local de livros e leitura."),
"公園":("公園","こうえん","substantivo",["parque"],"Espaço público de lazer."),
"病院":("病院","びょういん","substantivo",["hospital"],"Local de atendimento médico."),
"部屋":("部屋","へや","substantivo",["quarto","cômodo"],"Espaço interno de uma casa."),
"教室":("教室","きょうしつ","substantivo",["sala de aula"],"Sala onde ocorre a aula."),
"日本":("日本","にほん","nome próprio",["Japão"],"Nome de país."),
"東京":("東京","とうきょう","nome próprio",["Tóquio"],"Nome de cidade."),
"先生":("先生","せんせい","substantivo",["professor","mestre","doutor"],"Tratamento para professor e alguns profissionais."),
"学生":("学生","がくせい","substantivo",["estudante","aluno"],"Pessoa que estuda."),
"友達":("友達","ともだち","substantivo",["amigo","amiga"],"Amizade."),
"母":("母","はは","substantivo",["minha mãe","mãe"],"Forma usada para falar da própria mãe a terceiros."),
"父":("父","ちち","substantivo",["meu pai","pai"],"Forma usada para falar do próprio pai a terceiros."),
"兄":("兄","あに","substantivo",["meu irmão mais velho"],"Forma usada para falar do próprio irmão mais velho."),
"妹":("妹","いもうと","substantivo",["minha irmã mais nova"],"Forma usada para falar da própria irmã mais nova."),
"子供":("子供","こども","substantivo",["criança","filho"],"O contexto define se é criança em geral ou filho."),
"猫":("猫","ねこ","substantivo",["gato","gata"],"Animal."),
"犬":("犬","いぬ","substantivo",["cachorro","cão"],"Animal."),
"本":("本","ほん","substantivo",["livro","origem"],"Nesta lista, normalmente 'livro'."),
"新聞":("新聞","しんぶん","substantivo",["jornal"],"Publicação de notícias."),
"映画":("映画","えいが","substantivo",["filme","cinema"],"Obra audiovisual."),
"写真":("写真","しゃしん","substantivo",["foto","fotografia"],"Imagem fotográfica."),
"手紙":("手紙","てがみ","substantivo",["carta"],"Correspondência escrita."),
"名前":("名前","なまえ","substantivo",["nome"],"Identificação de pessoa ou coisa."),
"日本語":("日本語","にほんご","substantivo",["língua japonesa","japonês"],"Idioma."),
"英語":("英語","えいご","substantivo",["língua inglesa","inglês"],"Idioma."),
"水":("水","みず","substantivo",["água"],"Bebida ou substância."),
"お茶":("お茶","おちゃ","substantivo",["chá"],"Bebida; お é prefixo de cortesia."),
"コーヒー":("コーヒー","コーヒー","substantivo",["café"],"Bebida."),
"ご飯":("ご飯","ごはん","substantivo",["arroz cozido","refeição"],"O contexto define o sentido."),
"パン":("パン","パン","substantivo",["pão"],"Alimento."),
"魚":("魚","さかな","substantivo",["peixe"],"Animal ou alimento."),
"肉":("肉","にく","substantivo",["carne"],"Alimento."),
"野菜":("野菜","やさい","substantivo",["verdura","legume","vegetal"],"Alimento vegetal."),
"りんご":("りんご","りんご","substantivo",["maçã"],"Fruta."),
"卵":("卵","たまご","substantivo",["ovo"],"Alimento."),
"車":("車","くるま","substantivo",["carro","veículo"],"Meio de transporte."),
"電車":("電車","でんしゃ","substantivo",["trem"],"Meio de transporte."),
"自転車":("自転車","じてんしゃ","substantivo",["bicicleta"],"Meio de transporte."),
"机":("机","つくえ","substantivo",["escrivaninha","mesa de estudo"],"Móvel."),
"椅子":("椅子","いす","substantivo",["cadeira"],"Móvel."),
"かばん":("かばん","かばん","substantivo",["bolsa","mochila","mala"],"Objeto para carregar coisas."),
"時計":("時計","とけい","substantivo",["relógio"],"Objeto que mostra as horas."),
"傘":("傘","かさ","substantivo",["guarda-chuva","sombrinha"],"Objeto para chuva ou sol."),
"新しい":("新しい","あたらしい","adjetivo い",["novo","nova"],"Modifica substantivo diretamente."),
"古い":("古い","ふるい","adjetivo い",["velho","antigo"],"Para objetos; não costuma descrever idade de pessoa."),
"大きい":("大きい","おおきい","adjetivo い",["grande"],"Tamanho."),
"小さい":("小さい","ちいさい","adjetivo い",["pequeno"],"Tamanho."),
"高い":("高い","たかい","adjetivo い",["caro","alto"],"O contexto define preço ou altura."),
"安い":("安い","やすい","adjetivo い",["barato"],"Preço baixo."),
"おいしい":("おいしい","おいしい","adjetivo い",["gostoso","delicioso"],"Sabor agradável."),
"暑い":("暑い","あつい","adjetivo い",["quente"],"Calor do tempo/clima."),
"寒い":("寒い","さむい","adjetivo い",["frio"],"Frio do tempo/clima."),
"忙しい":("忙しい","いそがしい","adjetivo い",["ocupado"],"Falta de tempo."),
"楽しい":("楽しい","たのしい","adjetivo い",["divertido","agradável"],"Experiência prazerosa."),
"難しい":("難しい","むずかしい","adjetivo い",["difícil"],"Dificuldade."),
"いい":("いい","いい","adjetivo い",["bom","boa"],"Forma cotidiana de よい."),
"きれい":("きれい","きれい","adjetivo な",["bonito","limpo"],"O contexto define beleza ou limpeza."),
"静か":("静か","しずか","adjetivo な",["silencioso","calmo"],"Antes de substantivo, usa な."),
"元気":("元気","げんき","adjetivo な",["bem","saudável","animado"],"Estado físico ou ânimo."),
"好き":("好き","すき","adjetivo な",["gostar de","preferido"],"O objeto de gosto costuma ser marcado por が."),
"嫌い":("嫌い","きらい","adjetivo な",["não gostar de","detestar"],"O objeto costuma ser marcado por が."),
"とても":("とても","とても","advérbio",["muito","bastante"],"Intensifica adjetivos."),
"少し":("少し","すこし","advérbio",["um pouco","pouco"],"Quantidade ou grau pequeno."),
"よく":("よく","よく","advérbio",["frequentemente","bem"],"O contexto indica frequência ou qualidade."),
"あまり":("あまり","あまり","advérbio",["não muito"],"Usado normalmente com predicado negativo."),
"一緒に":("一緒に","いっしょに","advérbio",["juntos","junto"],"Ação feita em companhia."),
"ゆっくり":("ゆっくり","ゆっくり","advérbio",["devagar","sem pressa"],"Modo da ação."),
"もう":("もう","もう","advérbio",["já","mais"],"Com afirmativo, frequentemente 'já'."),
"まだ":("まだ","まだ","advérbio",["ainda"],"Com negativo, 'ainda não'."),
"一つ":("一つ","ひとつ","contador",["um","uma unidade"],"Contagem geral japonesa."),
"二つ":("二つ","ふたつ","contador",["dois","duas unidades"],"Contagem geral japonesa."),
"三人":("三人","さんにん","contador",["três pessoas"],"Contagem de pessoas."),
"一人":("一人","ひとり","contador",["uma pessoa","sozinho"],"Contagem de pessoas; leitura irregular."),
"二人":("二人","ふたり","contador",["duas pessoas"],"Contagem de pessoas; leitura irregular."),
"たくさん":("たくさん","たくさん","advérbio",["muitos","bastante"],"Quantidade grande."),
"くださいね":("くださいね","くださいね","estrutura gramatical",["por favor","por favor, tá?"],"Pedido com partícula final de suavização."),
"右":("右","みぎ","substantivo",["direita"],"Direção ou posição."),
"左":("左","ひだり","substantivo",["esquerda"],"Direção ou posição."),
"上":("上","うえ","substantivo",["em cima","acima"],"Posição; costuma aparecer com の e に."),
"下":("下","した","substantivo",["embaixo","abaixo"],"Posição; costuma aparecer com の e に."),
"前":("前","まえ","substantivo",["frente","antes"],"Posição espacial ou tempo, conforme contexto."),
"後ろ":("後ろ","うしろ","substantivo",["atrás"],"Posição espacial."),
}

# token keys | translation | category. Punctuation is stored separately.
ROWS = """
これ は 本 です|Isto é um livro.|identificação
それ は 私 の かばん です|Essa é a minha bolsa.|identificação
あれ は 学校 です|Aquilo é uma escola.|identificação
この 本 は 新しい です|Este livro é novo.|identificação
その 時計 は 高い です|Esse relógio é caro.|identificação
どの かばん が あなた の です か|Qual bolsa é sua?|identificação
ここ は 図書館 です|Aqui é a biblioteca.|identificação
そこ は 教室 です か|Aí é a sala de aula?|identificação
あれ は 私 の 車 ではありません|Aquele não é meu carro.|identificação
だれ が 先生 です か|Quem é o professor?|identificação
私 は 学生 です|Eu sou estudante.|pessoas
彼 は 先生 です|Ele é professor.|pessoas
彼女 は 私 の 友達 です|Ela é minha amiga.|pessoas
母 は 元気 です|Minha mãe está bem.|pessoas
父 は 今日 忙しい です|Meu pai está ocupado hoje.|pessoas
兄 は 大学 に 行きます|Meu irmão mais velho vai à universidade.|pessoas
妹 は 日本語 を 勉強します|Minha irmã mais nova estuda japonês.|pessoas
子供 が 公園 に います|Há uma criança no parque.|pessoas
先生 と 学生 が 教室 に います|O professor e o aluno estão na sala de aula.|pessoas
私 の 友達 も 学生 です|Meu amigo também é estudante.|pessoas
毎日 七時 に 起きます|Acordo às sete todos os dias.|rotina
朝 パン を 食べます|Como pão de manhã.|rotina
八時 に 学校 へ 行きます|Vou à escola às oito.|rotina
昼 ご飯 を 食べます|Como uma refeição ao meio-dia.|rotina
夜 本 を 読みます|Leio um livro à noite.|rotina
九時 に 寝ます|Durmo às nove.|rotina
今日 家 で 勉強します|Hoje estudo em casa.|rotina
明日 学校 に 行きます|Amanhã vou à escola.|rotina
昨日 図書館 に 行きました|Ontem fui à biblioteca.|rotina
月曜日 から 働きます|Trabalho a partir de segunda-feira.|rotina
水 を 飲みます|Bebo água.|comida
お茶 を 飲みました|Bebi chá.|comida
コーヒー は 飲みません|Não bebo café.|comida
りんご を 一つ 食べます|Como uma maçã.|comida
魚 と ご飯 を 食べました|Comi peixe e arroz.|comida
肉 は 食べません|Não como carne.|comida
野菜 は おいしい です|Os vegetais são gostosos.|comida
卵 を 二つ ください|Dois ovos, por favor.|comida
この パン は 安い です|Este pão é barato.|comida
一緒に ご飯 を 食べましょう|Vamos comer juntos.|comida
駅 に 行きます|Vou à estação.|lugares
電車 で 東京 へ 行きます|Vou a Tóquio de trem.|lugares
自転車 で 学校 に 行きます|Vou à escola de bicicleta.|lugares
公園 で 友達 と 話します|Converso com um amigo no parque.|lugares
病院 は どこ です か|Onde fica o hospital?|lugares
店 は 駅 の 前 に あります|A loja fica em frente à estação.|lugares
図書館 は 学校 の 右 に あります|A biblioteca fica à direita da escola.|lugares
猫 は 机 の 下 に います|O gato está embaixo da mesa.|lugares
本 は 机 の 上 に あります|O livro está sobre a mesa.|lugares
犬 は 家 の 後ろ に います|O cachorro está atrás da casa.|lugares
この 部屋 は 大きい です|Este quarto é grande.|descrições
その 部屋 は 小さい です|Esse quarto é pequeno.|descrições
今日 は 暑い です|Hoje está quente.|descrições
昨日 は 寒かったです|Ontem estava frio.|descrições
この 写真 は きれい です|Esta foto é bonita.|descrições
ここ は とても 静か です|Aqui é muito silencioso.|descrições
日本語 は 難しい です|Japonês é difícil.|descrições
この 映画 は 楽しい です|Este filme é divertido.|descrições
あの 本 は 古い です|Aquele livro é antigo.|descrições
今日 は いい 日 です|Hoje é um bom dia.|descrições
私は 日本語 が 好き です|Eu gosto de japonês.|preferências
彼 は 魚 が 好き です|Ele gosta de peixe.|preferências
彼女 は コーヒー が 嫌い です|Ela não gosta de café.|preferências
母 は お茶 が 好き です|Minha mãe gosta de chá.|preferências
父 は 映画 が 好き です|Meu pai gosta de filmes.|preferências
私 は 野菜 が あまり 好き ではありません|Eu não gosto muito de vegetais.|preferências
あなた は 何 が 好き です か|Do que você gosta?|preferências
この 本 が 好き です|Gosto deste livro.|preferências
私 は 猫 も 犬 も 好き です|Gosto tanto de gatos quanto de cachorros.|preferências
兄 は 英語 が よく 分かります|Meu irmão mais velho entende bem inglês.|preferências
本 を 読みます|Leio um livro.|ações
新聞 を 読みました|Li o jornal.|ações
手紙 を 書きます|Escrevo uma carta.|ações
写真 を 見ます|Olho uma foto.|ações
映画 を 見ました|Assisti a um filme.|ações
音楽 を 聞きます|Ouço música.|ações
先生 に 名前 を 聞きます|Pergunto o nome ao professor.|ações
店 で かばん を 買いました|Comprei uma bolsa na loja.|ações
友達 を 待ちます|Espero um amigo.|ações
日本語 を 話します|Falo japonês.|ações
今 何時 です か|Que horas são agora?|perguntas
駅 は どこ です か|Onde fica a estação?|perguntas
この 本 は いくら です か|Quanto custa este livro?|perguntas
明日 は 何 を 食べます か|O que você vai comer amanhã?|perguntas
日曜日 に どこ へ 行きます か|Aonde você vai no domingo?|perguntas
あなた の 名前 は 何 です か|Qual é seu nome?|perguntas
この 時計 は だれ の です か|De quem é este relógio?|perguntas
いつ 日本 に 行きます か|Quando você vai ao Japão?|perguntas
学校 に 学生 が います か|Há estudantes na escola?|perguntas
何 を 飲みます か|O que você vai beber?|perguntas
この 傘 を ください|Este guarda-chuva, por favor.|prática
ゆっくり 話します|Falo devagar.|prática
一緒に 公園 へ 行きましょう|Vamos ao parque juntos.|prática
お茶 を 飲みましょう|Vamos tomar chá.|prática
もう ご飯 を 食べました|Já comi uma refeição.|prática
まだ 本 を 読んでいません|Ainda não li o livro.|prática
この 部屋 に 椅子 が 三つ あります|Há três cadeiras neste quarto.|prática
公園 に 子供 が たくさん います|Há muitas crianças no parque.|prática
ここ から 駅 まで 行きます|Vou daqui até a estação.|prática
この 手紙 を 母 に 書きます|Escrevo esta carta para minha mãe.|prática
""".strip().splitlines()

# A few common N5 words needed by the rows above.
L.update({
"あの":("あの","あの","determinante",["aquele","aquela"],"Antes de substantivo; distante de ambos."),
"日":("日","ひ","substantivo",["dia","sol"],"Nesta frase, 'dia'."),
"音楽":("音楽","おんがく","substantivo",["música"],"Arte sonora."),
"何時":("何時","なんじ","expressão interrogativa",["que horas"],"Pergunta pelas horas."),
"三つ":("三つ","みっつ","contador",["três unidades"],"Contagem geral japonesa."),
"読んでいません":("読んでいません","よんでいません","verbo",["ainda não li","não estou lendo"],"Forma て + いません; com まだ, indica ação ainda não realizada."),
})

# Correct minor morphology: 寒い uses 寒かったです in the past.
L["寒かったです"]=("寒かったです","さむかったです","adjetivo い",["estava frio","fez frio"],"Passado polido de 寒い: い → かった + です.")

def build():
    phrases=[]
    for index,line in enumerate(ROWS,1):
        words,translation,category=line.split("|")
        keys=words.split()
        if keys[0]=="私は": keys[:1]=["私","は"]
        tokens=[]
        for position,key in enumerate(keys):
            if key not in L: raise ValueError(f"Unknown {key} in {index}")
            surface,reading,kind,meanings,note=L[key]
            if key=="何" and position+1<len(keys) and keys[position+1]=="です": reading="なん"
            tokens.append({"surface":surface,"reading":reading,"kind":kind,"meanings_pt":meanings,"note_pt":note})
        question=keys[-1]=="か"
        text="".join(t["surface"] for t in tokens)+( "？" if question else "。")
        phrases.append({"id":index,"level":"N5","category":category,"text":text,"translation_pt":translation,"tokens":tokens})
    assert len(phrases)==100, len(phrases)
    from gramatica_extra import extend
    phrases=extend(phrases,L)
    path=Path(__file__).with_name("Lista e Frases N5.json")
    path.write_text(json.dumps({"title":"Lista e Frases N5","language":"ja","translation_language":"pt-BR","phrases":phrases},ensure_ascii=False,indent=2),encoding="utf-8")
    print(path, len(phrases))

if __name__=="__main__": build()
