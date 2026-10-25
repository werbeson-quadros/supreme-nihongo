"""Five curated examples per requested grammar topic.

Each example is written as space-separated meaningful Japanese units, followed by
its full Brazilian Portuguese translation. The shared lexicon annotates every unit.
"""

GROUPS = [
('ちゃいけない・じゃいけない', '''
ここ で 食べちゃいけない|Você não pode comer aqui.
図書館 で 話しちゃいけない|Você não pode falar na biblioteca.
この 水 を 飲んじゃいけない|Você não pode beber esta água.
学校 で 遊んじゃいけない|Você não pode brincar na escola.
ここ に 入っちゃいけない|Você não pode entrar aqui.
'''),
('だ / です', '''
これ は 私 の 本 だ|Este é meu livro.
その 人 は 先生 です|Aquela pessoa é professor.
ここ は 駅 だ|Aqui é a estação.
あれ は 新しい 車 です|Aquilo é um carro novo.
私 の 妹 は 学生 だ|Minha irmã mais nova é estudante.
'''),
('だけ', '''
水 だけ を 飲みます|Bebo somente água.
今日 だけ 家 に います|Fico em casa somente hoje.
この 本 だけ を 読みます|Leio somente este livro.
私 だけ が 行きます|Somente eu vou.
りんご だけ を 買います|Compro somente maçãs.
'''),
('だろう', '''
明日 は 暑い だろう|Amanhã provavelmente fará calor.
彼 は 学生 だろう|Ele provavelmente é estudante.
この 本 は 高い だろう|Este livro provavelmente é caro.
母 は 家 に いる だろう|Minha mãe provavelmente está em casa.
今日 は 雨 だろう|Hoje provavelmente vai chover.
'''),
('で', '''
家 で 本 を 読みます|Leio um livro em casa.
電車 で 学校 に 行きます|Vou à escola de trem.
図書館 で 勉強します|Estudo na biblioteca.
日本語 で 話します|Falo em japonês.
店 で パン を 買います|Compro pão na loja.
'''),
('でも', '''
お茶 でも 飲みましょう|Vamos tomar um chá ou algo assim.
日曜日 でも 働きます|Trabalho até no domingo.
水 でも いい です|Água também serve.
子供 でも 分かります|Até uma criança entende.
ここ でも 勉強します|Estudo aqui também.
'''),
('でしょう', '''
明日 は 寒い でしょう|Amanhã provavelmente fará frio.
この 映画 は 楽しい でしょう|Este filme provavelmente é divertido.
先生 は 来る でしょう|O professor provavelmente virá.
東京 は 大きい でしょう|Tóquio provavelmente é grande.
彼女 は 元気 でしょう|Ela provavelmente está bem.
'''),
('どんな', '''
どんな 本 が 好き です か|De que tipo de livro você gosta?
どんな 映画 を 見ます か|Que tipo de filme você assiste?
どんな 人 です か|Que tipo de pessoa é?
どんな 音楽 が 好き です か|De que tipo de música você gosta?
どんな 店 で 買います か|Em que tipo de loja você compra?
'''),
('どうして', '''
どうして 学校 に 行きません か|Por que você não vai à escola?
どうして この 本 が 好き です か|Por que você gosta deste livro?
どうして 今日 は 忙しい です か|Por que você está ocupado hoje?
どうして 猫 が いません か|Por que não há um gato?
どうして 水 を 飲みません か|Por que você não bebe água?
'''),
('どうやって', '''
どうやって 駅 に 行きます か|Como se vai à estação?
どうやって 日本語 を 勉強します か|Como você estuda japonês?
どうやって この 本 を 読みます か|Como você lê este livro?
どうやって 東京 に 行きます か|Como você vai a Tóquio?
どうやって この 料理 を 作ります か|Como você prepara este prato?
'''),
('が', '''
猫 が 部屋 に います|Há um gato no quarto.
私 が 行きます|Eu é que vou.
この 本 が おもしろい です|Este livro é interessante.
母 が 来ます|Minha mãe vem.
だれ が 日本語 を 話します か|Quem fala japonês?
'''),
('があります', '''
机 の 上 に 本 が あります|Há um livro sobre a mesa.
駅 の 前 に 店 が あります|Há uma loja em frente à estação.
部屋 に 椅子 が あります|Há uma cadeira no quarto.
家 の 後ろ に 公園 が あります|Há um parque atrás da casa.
学校 の 右 に 図書館 が あります|Há uma biblioteca à direita da escola.
'''),
('がほしい', '''
新しい 本 が ほしい です|Quero um livro novo.
私 は 水 が ほしい です|Eu quero água.
彼女 は かばん が ほしい です|Ela quer uma bolsa.
この 時計 が ほしい です|Quero este relógio.
子供 は りんご が ほしい です|A criança quer uma maçã.
'''),
('がいます', '''
公園 に 犬 が います|Há um cachorro no parque.
教室 に 先生 が います|Há um professor na sala de aula.
家 に 妹 が います|Minha irmã mais nova está em casa.
駅 の 前 に 友達 が います|Há um amigo em frente à estação.
机 の 下 に 猫 が います|Há um gato embaixo da mesa.
'''),
('ほうがいい', '''
水 を 飲んだ ほうがいい です|É melhor beber água.
早く 寝た ほうがいい です|É melhor dormir cedo.
この 本 を 読んだ ほうがいい です|É melhor ler este livro.
病院 に 行った ほうがいい です|É melhor ir ao hospital.
野菜 を 食べた ほうがいい です|É melhor comer vegetais.
'''),
('い-adjectives', '''
この りんご は 赤い です|Esta maçã é vermelha.
今日 の 空 は 青い です|O céu de hoje é azul.
この 本 は おもしろい です|Este livro é interessante.
あの 山 は 高い です|Aquela montanha é alta.
この 水 は 冷たい です|Esta água está fria.
'''),
('一番（いちばん）', '''
この 本 が 一番 おもしろい です|Este livro é o mais interessante.
母 の 料理 が 一番 おいしい です|A comida da minha mãe é a mais gostosa.
この 車 が 一番 高い です|Este carro é o mais caro.
この 部屋 が 一番 大きい です|Este quarto é o maior.
あの 公園 が 一番 きれい です|Aquele parque é o mais bonito.
'''),
('一緒に（いっしょに）', '''
一緒に 映画 を 見ましょう|Vamos assistir a um filme juntos.
友達 と 一緒に 本 を 読みます|Leio um livro junto com um amigo.
一緒に お茶 を 飲みませんか|Vamos tomar chá juntos?
母 と 一緒に 店 に 行きます|Vou à loja junto com minha mãe.
一緒に 日本語 を 勉強しましょう|Vamos estudar japonês juntos.
'''),
('いつも', '''
私 は いつも 七時 に 起きます|Eu sempre acordo às sete.
母 は いつも お茶 を 飲みます|Minha mãe sempre toma chá.
彼 は いつも 電車 で 行きます|Ele sempre vai de trem.
日曜日 は いつも 家 に います|Aos domingos, sempre fico em casa.
先生 は いつも 元気 です|O professor está sempre bem.
'''),
('じゃない・ではない', '''
これ は 私 の 本 じゃない|Este não é meu livro.
彼 は 先生 ではない|Ele não é professor.
ここ は 駅 じゃない|Aqui não é a estação.
あの 人 は 学生 ではない|Aquela pessoa não é estudante.
この 水 は お茶 じゃない|Esta água não é chá.
'''),
('か', '''
今日 は 月曜日 です か|Hoje é segunda-feira?
これ は あなた の 本 です か|Este é o seu livro?
先生 は 教室 に います か|O professor está na sala de aula?
明日 も 学校 に 行きます か|Você também vai à escola amanhã?
この りんご は おいしい です か|Esta maçã é gostosa?
'''),
('か～か', '''
お茶 か コーヒー か 選んでください|Escolha chá ou café.
今日 か 明日 か 教えてください|Diga se é hoje ou amanhã.
本 か 新聞 か 教えてください|Diga se é livro ou jornal.
電車 か 車 か 教えてください|Diga se é trem ou carro.
水 か お茶 か 選んでください|Escolha água ou chá.
'''),
('から', '''
九時 から 勉強します|Estudo a partir das nove.
家 から 学校 へ 行きます|Vou de casa até a escola.
今日 から 日本語 を 話します|A partir de hoje, falo japonês.
暑い から 水 を 飲みます|Bebo água porque está quente.
先生 から 本 を もらいました|Recebi um livro do professor.
'''),
('方（かた）', '''
この 本 の 読み方 を 教えてください|Por favor, ensine como ler este livro.
日本語 の 書き方 を 勉強します|Estudo como escrever em japonês.
駅 へ の 行き方 が 分かります|Sei como chegar à estação.
この 料理 の 作り方 を 聞きます|Pergunto como preparar este prato.
名前 の 書き方 を 教えてください|Por favor, ensine como escrever o nome.
'''),
('けど', '''
この 本 は 高い けど おもしろい です|Este livro é caro, mas interessante.
今日 は 寒い けど 公園 に 行きます|Hoje está frio, mas vou ao parque.
彼 は 学生 だ けど 働きます|Ele é estudante, mas trabalha.
この 部屋 は 小さい けど きれい です|Este quarto é pequeno, mas bonito.
日本語 は 難しい けど 楽しい です|Japonês é difícil, mas divertido.
'''),
('けれども', '''
雨 です けれども 学校 に 行きます|Está chovendo, mas vou à escola.
この 車 は 古い けれども いい です|Este carro é antigo, mas é bom.
彼女 は 忙しい けれども 元気 です|Ela está ocupada, mas está bem.
この 本 は 長い けれども おもしろい です|Este livro é longo, mas interessante.
今日 は 暑い けれども 水 が ありません|Hoje está quente, mas não há água.
'''),
('まだ', '''
まだ 三時 です|Ainda são três horas.
母 は まだ 家 に います|Minha mãe ainda está em casa.
この 店 は まだ 新しい です|Esta loja ainda é nova.
私 は まだ 学生 です|Ainda sou estudante.
友達 は まだ 来ていません|Meu amigo ainda não chegou.
'''),
('まだ～ていません', '''
まだ 朝 ご飯 を 食べていません|Ainda não tomei café da manhã.
まだ この 本 を 読んでいません|Ainda não li este livro.
まだ 映画 を 見ていません|Ainda não assisti ao filme.
まだ 手紙 を 書いていません|Ainda não escrevi a carta.
まだ 水 を 飲んでいません|Ainda não bebi água.
'''),
('まで', '''
五時 まで 働きます|Trabalho até as cinco.
駅 まで 歩きます|Caminho até a estação.
日曜日 まで 家 に います|Fico em casa até domingo.
ここ から 公園 まで 行きます|Vou daqui até o parque.
夜 まで 勉強します|Estudo até a noite.
'''),
('前に（まえに）', '''
寝る 前に 本 を 読みます|Leio um livro antes de dormir.
学校 に 行く 前に 朝 ご飯 を 食べます|Como antes de ir à escola.
映画 を 見る 前に お茶 を 飲みます|Tomo chá antes de assistir ao filme.
七時 の 前に 起きます|Acordo antes das sete.
勉強する 前に 水 を 飲みます|Bebo água antes de estudar.
'''),
('ませんか', '''
一緒に 映画 を 見ませんか|Vamos assistir a um filme juntos?
お茶 を 飲みませんか|Quer tomar chá?
明日 公園 に 行きませんか|Vamos ao parque amanhã?
この 本 を 読みませんか|Quer ler este livro?
日本語 を 勉強しませんか|Vamos estudar japonês?
'''),
('ましょう', '''
明日 学校 に 行きましょう|Vamos à escola amanhã.
この 映画 を 見ましょう|Vamos assistir a este filme.
一緒に 日本語 を 話しましょう|Vamos falar japonês juntos.
ここ で 少し 休みましょう|Vamos descansar um pouco aqui.
野菜 を 食べましょう|Vamos comer vegetais.
'''),
('ましょうか', '''
私 が 手紙 を 書きましょうか|Quer que eu escreva a carta?
一緒に 駅 まで 行きましょうか|Vamos juntos até a estação?
お茶 を 飲みましょうか|Vamos tomar chá?
この 本 を 読みましょうか|Vamos ler este livro?
ここ で 待ちましょうか|Vamos esperar aqui?
'''),
('も', '''
私 も 日本語 を 勉強します|Eu também estudo japonês.
母 も 公園 に 行きます|Minha mãe também vai ao parque.
この 本 も おもしろい です|Este livro também é interessante.
お茶 も 飲みます|Também bebo chá.
明日 も 働きます|Amanhã também trabalho.
'''),
('もう', '''
もう 昼 ご飯 を 食べました|Já almocei.
先生 は もう 来ました|O professor já chegou.
この 映画 は もう 見ました|Já assisti a este filme.
もう 九時 です|Já são nove horas.
友達 は もう 家 に 帰りました|Meu amigo já voltou para casa.
'''),
('な-adjectives', '''
この 公園 は 静か です|Este parque é tranquilo.
私 の 母 は 元気 です|Minha mãe está bem.
この 部屋 は きれい です|Este quarto está limpo.
あの 先生 は 親切 です|Aquele professor é gentil.
この 映画 は 有名 です|Este filme é famoso.
'''),
('なあ', '''
今日 は いい 天気 だ なあ|Que tempo bom hoje!
この りんご は おいしい なあ|Como esta maçã é gostosa!
あの 山 は 大きい なあ|Como aquela montanha é grande!
日本語 は おもしろい なあ|Como japonês é interessante!
もう 夜 だ なあ|Nossa, já é noite.
'''),
('ないで', '''
朝 ご飯 を 食べないで 学校 に 行きました|Fui à escola sem comer de manhã.
傘 を 持たないで 家 を 出ました|Saí de casa sem levar guarda-chuva.
本 を 読まないで 寝ました|Dormi sem ler o livro.
電車 に 乗らないで 歩きました|Caminhei sem pegar o trem.
水 を 飲まないで 働きました|Trabalhei sem beber água.
'''),
('ないでください', '''
ここ で 食べないでください|Por favor, não coma aqui.
この 本 を 読まないでください|Por favor, não leia este livro.
部屋 で 話さないでください|Por favor, não fale no quarto.
あの 水 を 飲まないでください|Por favor, não beba aquela água.
学校 に 行かないでください|Por favor, não vá à escola.
'''),
('ないといけない', '''
今日 は 勉強しないといけない|Preciso estudar hoje.
七時 に 起きないといけない|Preciso acordar às sete.
この 本 を 読まないといけない|Preciso ler este livro.
母 に 手紙 を 書かないといけない|Preciso escrever uma carta para minha mãe.
今日 は 早く 帰らないといけない|Preciso voltar cedo hoje.
'''),
('なくてもいい', '''
今日 は 学校 に 行かなくてもいい です|Hoje não preciso ir à escola.
この 本 は 読まなくてもいい です|Não preciso ler este livro.
朝 ご飯 を 食べなくてもいい です|Não preciso tomar café da manhã.
ここ で 待たなくてもいい です|Não preciso esperar aqui.
明日 は 働かなくてもいい です|Amanhã não preciso trabalhar.
'''),
('なくちゃ', '''
今日 は もう 行かなくちゃ|Já preciso ir hoje.
七時 に 起きなくちゃ|Preciso acordar às sete.
この 本 を 読まなくちゃ|Preciso ler este livro.
母 に 電話しなくちゃ|Preciso ligar para minha mãe.
明日 は 勉強しなくちゃ|Preciso estudar amanhã.
'''),
('なくてはいけない', '''
野菜 を 食べなくてはいけない|Preciso comer vegetais.
明日 学校 に 行かなくてはいけない|Preciso ir à escola amanhã.
毎日 日本語 を 勉強しなくてはいけない|Preciso estudar japonês todos os dias.
この 手紙 を 書かなくてはいけない|Preciso escrever esta carta.
八時 に 家 を 出なくてはいけない|Preciso sair de casa às oito.
'''),
('なくてはならない', '''
今日 は 働かなくてはならない|Tenho de trabalhar hoje.
先生 に 話さなくてはならない|Tenho de falar com o professor.
この 本 を 読まなくてはならない|Tenho de ler este livro.
七時 に 起きなくてはならない|Tenho de acordar às sete.
病院 に 行かなくてはならない|Tenho de ir ao hospital.
'''),
('なる', '''
彼 は 先生 に なります|Ele vai se tornar professor.
妹 は 学生 に なりました|Minha irmã mais nova se tornou estudante.
今日 は 暑く なります|Hoje vai ficar quente.
この 部屋 は 静か に なります|Este quarto vai ficar silencioso.
私 は 元気 に なりました|Fiquei melhor.
'''),
('んです', '''
今日 は 忙しい んです|É que estou ocupado hoje.
私 は 日本語 を 勉強している んです|É que estou estudando japonês.
この 本 が 好き な んです|É que eu gosto deste livro.
明日 は 学校 に 行く んです|É que vou à escola amanhã.
母 は 家 に いる んです|É que minha mãe está em casa.
'''),
('ね', '''
今日 は いい 天気 です ね|Hoje o tempo está bom, não é?
この りんご は おいしい です ね|Esta maçã é gostosa, não é?
もう 九時 です ね|Já são nove horas, não é?
あの 公園 は きれい です ね|Aquele parque é bonito, não é?
日本語 は 楽しい です ね|Japonês é divertido, não é?
'''),
('に', '''
明日 東京 に 行きます|Amanhã vou a Tóquio.
八時 に 起きます|Acordo às oito.
母 に 手紙 を 書きます|Escrevo uma carta para minha mãe.
部屋 に 猫 が います|Há um gato no quarto.
机 の 上 に 時計 が あります|Há um relógio sobre a mesa.
'''),
('に行く（にいく）', '''
本 を 買い に 行きます|Vou comprar um livro.
友達 に 会い に 行きます|Vou encontrar um amigo.
公園 へ 遊び に 行きます|Vou brincar no parque.
映画 を 見 に 行きます|Vou assistir a um filme.
駅 へ 母 を 迎え に 行きます|Vou buscar minha mãe na estação.
'''),
('にする', '''
私 は お茶 に します|Vou escolher chá.
昼 ご飯 は パン に します|Vou escolher pão para o almoço.
この かばん に します|Vou ficar com esta bolsa.
今日 は 電車 に します|Hoje vou escolher o trem.
飲み物 は 水 に します|Vou escolher água como bebida.
'''),
('に/へ', '''
私 は 学校 に 行きます|Vou à escola.
友達 は 学校 へ 行きます|Meu amigo vai em direção à escola.
母 は 店 に 行きます|Minha mãe vai à loja.
彼 は 東京 へ 行きます|Ele vai em direção a Tóquio.
明日 日本 に 行きます|Amanhã vou ao Japão.
'''),
('の', '''
これ は 先生 の 本 です|Este é o livro do professor.
あれ は 母 の 車 です|Aquele é o carro da minha mãe.
この 学校 の 学生 は 元気 です|Os alunos desta escola estão bem.
友達 の 猫 は 小さい です|O gato do meu amigo é pequeno.
日本 の 映画 が 好き です|Gosto de filmes do Japão.
'''),
('のです', '''
今日 は 忙しい のです|É que estou ocupado hoje.
私 は 日本語 を 勉強している のです|É que estou estudando japonês.
明日 東京 に 行く のです|É que vou a Tóquio amanhã.
この 部屋 は 静か な のです|É que este quarto é silencioso.
母 は 家 に いる のです|É que minha mãe está em casa.
'''),
('のが下手（のがへた）', '''
私 は 歌う のが下手 です|Sou ruim em cantar.
彼 は 料理する のが下手 です|Ele é ruim em cozinhar.
妹 は 泳ぐ のが下手 です|Minha irmã mais nova é ruim em nadar.
私 は 絵 を 描く のが下手 です|Sou ruim em desenhar.
兄 は 日本語 を 話す のが下手 です|Meu irmão mais velho é ruim em falar japonês.
'''),
('のが上手（のがじょうず）', '''
母 は 料理する のが上手 です|Minha mãe cozinha bem.
彼女 は 歌う のが上手 です|Ela canta bem.
兄 は 泳ぐ のが上手 です|Meu irmão mais velho nada bem.
先生 は 日本語 を 話す のが上手 です|O professor fala japonês bem.
妹 は 絵 を 描く のが上手 です|Minha irmã mais nova desenha bem.
'''),
('のが好き（のがすき）', '''
私 は 本 を 読む のが好き です|Eu gosto de ler livros.
母 は 料理する のが好き です|Minha mãe gosta de cozinhar.
彼 は 泳ぐ のが好き です|Ele gosta de nadar.
妹 は 歌う のが好き です|Minha irmã mais nova gosta de cantar.
友達 は 映画 を 見る のが好き です|Meu amigo gosta de assistir a filmes.
'''),
('の中で[A]が一番（のなかで[A]がいちばん）', '''
果物 の中で りんご が 一番 好き です|Entre as frutas, gosto mais de maçã.
この 三つ の中で この 本 が 一番 おもしろい です|Entre estes três, este livro é o mais interessante.
飲み物 の中で お茶 が 一番 好き です|Entre as bebidas, gosto mais de chá.
家族 の中で 妹 が 一番 若い です|Na família, minha irmã mais nova é a mais jovem.
この 店 の中で この パン が 一番 安い です|Nesta loja, este pão é o mais barato.
'''),
('ので', '''
今日 は 寒い ので 家 に います|Como hoje está frio, fico em casa.
雨 な ので 公園 に 行きません|Como está chovendo, não vou ao parque.
母 が 忙しい ので 私 が 料理します|Como minha mãe está ocupada, eu cozinho.
この 本 は 高い ので 買いません|Como este livro é caro, não o compro.
明日 は 学校 が ある ので 早く 寝ます|Como amanhã há aula, vou dormir cedo.
'''),
('お / ご', '''
お 水 を ください|Água, por favor.
お 名前 は 何 です か|Qual é o seu nome?
ご 家族 は 元気 です か|Sua família está bem?
お 茶 を 飲みます|Bebo chá.
ご 飯 を 食べます|Como uma refeição.
'''),
('を', '''
私 は 手紙 を 書きます|Escrevo uma carta.
父 は 新聞 を 読みます|Meu pai lê o jornal.
子供 は 水 を 飲みます|A criança bebe água.
妹 は 写真 を 見ます|Minha irmã mais nova olha uma foto.
母 は 野菜 を 買います|Minha mãe compra vegetais.
'''),
('をください', '''
この 本 を ください|Este livro, por favor.
水 を ください|Água, por favor.
新しい かばん を ください|Uma bolsa nova, por favor.
りんご を 二つ ください|Duas maçãs, por favor.
あの 時計 を ください|Aquele relógio, por favor.
'''),
('しかし', '''
この 本 は 高い です しかし おもしろい です|Este livro é caro. Entretanto, é interessante.
今日 は 暑い です しかし 水 が ありません|Hoje faz calor. Entretanto, não há água.
彼 は 学生 です しかし 働きます|Ele é estudante. Entretanto, trabalha.
この 店 は 小さい です しかし いい です|Esta loja é pequena. Entretanto, é boa.
日本語 は 難しい です しかし 楽しい です|Japonês é difícil. Entretanto, é divertido.
'''),
('それから', '''
朝 ご飯 を 食べます それから 学校 に 行きます|Tomo café da manhã e depois vou à escola.
本 を 読みます それから 寝ます|Leio um livro e depois durmo.
店 に 行きます それから パン を 買います|Vou à loja e depois compro pão.
水 を 飲みます それから 働きます|Bebo água e depois trabalho.
映画 を 見ます それから 友達 と 話します|Assisto a um filme e depois converso com um amigo.
'''),
('そして', '''
母 は 元気 です そして 先生 です|Minha mãe está bem e é professora.
この 本 は 安い です そして おもしろい です|Este livro é barato e interessante.
朝 起きます そして ご飯 を 食べます|Acordo de manhã e então como.
彼 は 学生 です そして 働きます|Ele é estudante e também trabalha.
東京 に 行きます そして 映画 を 見ます|Vou a Tóquio e então assisto a um filme.
'''),
('すぎる', '''
この 本 は 高すぎます|Este livro é caro demais.
今日 は 食べすぎました|Hoje comi demais.
彼 は 働きすぎます|Ele trabalha demais.
この かばん は 大きすぎます|Esta bolsa é grande demais.
昨日 は 寝すぎました|Ontem dormi demais.
'''),
('たことがある', '''
私 は 日本 に 行ったことがある|Já fui ao Japão.
この 映画 を 見たことがある|Já assisti a este filme.
魚 を 食べたことがある|Já comi peixe.
電車 で 東京 に 行ったことがある|Já fui a Tóquio de trem.
あの 本 を 読んだことがある|Já li aquele livro.
'''),
('たい', '''
私 は 水 を 飲みたい です|Quero beber água.
明日 映画 を 見たい です|Quero assistir a um filme amanhã.
日本 に 行きたい です|Quero ir ao Japão.
この 本 を 読みたい です|Quero ler este livro.
お茶 を 買いたい です|Quero comprar chá.
'''),
('たり～たり', '''
日曜日 は 本 を 読んだり 映画 を 見たり します|Aos domingos, leio livros e assisto a filmes, entre outras coisas.
公園 で 歩いたり 走ったり します|No parque, caminho e corro, entre outras coisas.
夜 は お茶 を 飲んだり 音楽 を 聞いたり します|À noite, tomo chá e ouço música, entre outras coisas.
学校 で 勉強したり 友達 と 話したり します|Na escola, estudo e converso com amigos, entre outras coisas.
日曜日 は 料理したり 本 を 読んだり します|Aos domingos, cozinho e leio, entre outras coisas.
'''),
('てある', '''
机 の 上 に 本 が 置いてあります|Há um livro colocado sobre a mesa.
ドア が 開けてあります|A porta foi deixada aberta.
部屋 に 写真 が 飾ってあります|Há uma foto exposta no quarto.
紙 に 名前 が 書いてあります|Há um nome escrito no papel.
店 の 前 に 車 が 止めてあります|Há um carro estacionado em frente à loja.
'''),
('ている', '''
私 は 今 本 を 読んでいます|Estou lendo um livro agora.
母 は 料理しています|Minha mãe está cozinhando.
子供 は 公園 で 遊んでいます|A criança está brincando no parque.
彼 は 日本語 を 勉強しています|Ele está estudando japonês.
先生 は 教室 で 話しています|O professor está falando na sala de aula.
'''),
('てから', '''
ご飯 を 食べてから 学校 に 行きます|Depois de comer, vou à escola.
本 を 読んでから 寝ます|Depois de ler um livro, durmo.
水 を 飲んでから 働きます|Depois de beber água, trabalho.
映画 を 見てから 友達 と 話します|Depois de assistir ao filme, converso com um amigo.
手紙 を 書いてから 店 に 行きます|Depois de escrever a carta, vou à loja.
'''),
('てください', '''
この 本 を 読んでください|Por favor, leia este livro.
ここ で 待ってください|Por favor, espere aqui.
日本語 で 話してください|Por favor, fale em japonês.
水 を 飲んでください|Por favor, beba água.
名前 を 書いてください|Por favor, escreva o nome.
'''),
('てはいけない', '''
ここ で 食べてはいけない|Não se pode comer aqui.
図書館 で 話してはいけない|Não se pode falar na biblioteca.
この 水 を 飲んではいけない|Não se pode beber esta água.
学校 で 走ってはいけない|Não se pode correr na escola.
ここ に 入ってはいけない|Não se pode entrar aqui.
'''),
('てもいいです', '''
ここ で 食べてもいいです|Pode comer aqui.
この 本 を 読んでもいいです|Pode ler este livro.
水 を 飲んでもいいです|Pode beber água.
部屋 に 入ってもいいです|Pode entrar no quarto.
ここ で 写真 を 撮ってもいいです|Pode tirar fotos aqui.
'''),
('と', '''
友達 と 映画 を 見ます|Assisto a um filme com um amigo.
母 と 店 に 行きます|Vou à loja com minha mãe.
猫 と 犬 が います|Há um gato e um cachorro.
父 と 話します|Converso com meu pai.
本 と 新聞 を 買います|Compro um livro e um jornal.
'''),
('とき', '''
朝 起きた とき 水 を 飲みます|Quando acordo de manhã, bebo água.
子供 の とき 日本 に いました|Quando era criança, eu estava no Japão.
暇 な とき 本 を 読みます|Quando tenho tempo livre, leio um livro.
寝る とき 電気 を 消します|Quando vou dormir, apago a luz.
学校 に 行く とき 電車 に 乗ります|Quando vou à escola, pego o trem.
'''),
('とても', '''
この 映画 は とても 楽しい です|Este filme é muito divertido.
今日 は とても 暑い です|Hoje está muito quente.
この 本 は とても おもしろい です|Este livro é muito interessante.
私 の 母 は とても 元気 です|Minha mãe está muito bem.
あの 山 は とても 高い です|Aquela montanha é muito alta.
'''),
('つもり', '''
明日 日本語 を 勉強する つもり です|Pretendo estudar japonês amanhã.
日曜日 に 映画 を 見る つもり です|Pretendo assistir a um filme no domingo.
この 本 を 買う つもり です|Pretendo comprar este livro.
今日 は 早く 寝る つもり です|Pretendo dormir cedo hoje.
来週 東京 に 行く つもり です|Pretendo ir a Tóquio na próxima semana.
'''),
('は', '''
私 は 毎日 働きます|Eu trabalho todos os dias.
この 映画 は 長い です|Este filme é longo.
猫 は 部屋 に います|O gato está no quarto.
母 は 日本語 を 話します|Minha mãe fala japonês.
明日 は 日曜日 です|Amanhã é domingo.
'''),
('は〜より・・・です', '''
東京 は ここ より 大きい です|Tóquio é maior que aqui.
この 本 は あの 本 より おもしろい です|Este livro é mais interessante que aquele.
電車 は 車 より 速い です|O trem é mais rápido que o carro.
この 店 は あの 店 より 安い です|Esta loja é mais barata que aquela.
今日 は 昨日 より 寒い です|Hoje está mais frio que ontem.
'''),
('はどうですか', '''
この お茶 は どうですか|Que tal este chá?
日本 の 映画 は どうですか|Que tal um filme japonês?
この 本 は どうですか|Que tal este livro?
新しい かばん は どうですか|Que tal uma bolsa nova?
明日 は どうですか|Que tal amanhã?
'''),
('や', '''
机 の 上 に 本 や 新聞 が あります|Há livros e jornais, entre outras coisas, sobre a mesa.
店 で パン や 野菜 を 買います|Compro pão e vegetais, entre outras coisas, na loja.
公園 に 猫 や 犬 が います|Há gatos e cachorros, entre outros animais, no parque.
私 は 映画 や 音楽 が 好き です|Gosto de filmes e música, entre outras coisas.
かばん に 本 や 時計 が あります|Há livros e um relógio, entre outras coisas, na bolsa.
'''),
('よ', '''
この 本 は おもしろい です よ|Este livro é interessante, viu.
明日 は 日曜日 です よ|Amanhã é domingo, viu.
水 は ここ に あります よ|A água está aqui, viu.
母 は 元気 です よ|Minha mãe está bem, viu.
駅 は あそこ です よ|A estação fica ali, viu.
'''),
('より～ほうが', '''
車 より 電車 の ほうが 速い です|O trem é mais rápido que o carro.
お茶 より 水 の ほうが 好き です|Gosto mais de água do que de chá.
この 本 より あの 本 の ほうが おもしろい です|Aquele livro é mais interessante que este.
今日 より 明日 の ほうが 暑い でしょう|Amanhã provavelmente será mais quente que hoje.
魚 より 肉 の ほうが 好き です|Gosto mais de carne do que de peixe.
'''),
]

# reading, class, possible PT meanings, usage/grammar note
EXTRA = {
"だ":("だ","cópula",["é","sou","está"],"Cópula informal; segue substantivos e adjetivos な."),
"だけ":("だけ","partícula",["somente","apenas"],"Limita a quantidade ou o elemento referido."),
"だろう":("だろう","estrutura gramatical",["provavelmente","deve ser"],"Expressa suposição em registro informal."),
"でも":("でも","partícula",["até","também","por exemplo"],"Depois de substantivo, pode incluir um caso inesperado ou sugerir uma opção."),
"でしょう":("でしょう","estrutura gramatical",["provavelmente","não é?"],"Suposição ou pedido de confirmação em registro polido."),
"どんな":("どんな","determinante",["que tipo de","como"],"Vem antes de substantivo para perguntar sua natureza."),
"どうして":("どうして","advérbio interrogativo",["por que","como assim"],"Pergunta pelo motivo."),
"どうやって":("どうやって","advérbio interrogativo",["como","de que maneira"],"Pergunta pelo método."),
"ほしい":("ほしい","adjetivo い",["querer","desejar"],"O objeto desejado geralmente é marcado por が."),
"ほうがいい":("ほうがいい","estrutura gramatical",["é melhor","seria aconselhável"],"Depois de verbo no passado informal, dá conselho."),
"一番":("いちばん","advérbio",["o mais","o melhor","em primeiro lugar"],"Marca grau superlativo no grupo comparado."),
"いつも":("いつも","advérbio",["sempre","habitualmente"],"Expressa frequência constante."),
"じゃない":("じゃない","estrutura gramatical",["não é","não sou"],"Negação informal de substantivos e adjetivos な."),
"ではない":("ではない","estrutura gramatical",["não é","não sou"],"Negação informal em registro mais escrito que じゃない."),
"けど":("けど","conjunção",["mas","embora"],"Liga orações em contraste; registro coloquial."),
"けれども":("けれども","conjunção",["mas","embora"],"Liga orações em contraste; registro neutro ou polido."),
"前に":("まえに","estrutura gramatical",["antes de"],"Depois de verbo de dicionário ou expressão de tempo, marca anterioridade."),
"なあ":("なあ","partícula final",["como...!","puxa"],"Expressa admiração ou sentimento do falante."),
"んです":("んです","estrutura gramatical",["é que","o fato é que"],"Acrescenta explicação; após substantivo/adjetivo な, usa な antes."),
"のです":("のです","estrutura gramatical",["é que","o fato é que"],"Forma plena de んです para explicar contexto ou motivo."),
"のが下手":("のがへた","estrutura gramatical",["ser ruim em","não ter habilidade em"],"Nominaliza uma ação com の e avalia habilidade com 下手."),
"のが上手":("のがじょうず","estrutura gramatical",["ser bom em","ter habilidade em"],"Nominaliza uma ação com の e avalia habilidade com 上手."),
"のが好き":("のがすき","estrutura gramatical",["gostar de fazer","ter prazer em"],"Nominaliza uma ação com の para expressar gosto."),
"の中で":("のなかで","estrutura gramatical",["entre","dentro de"],"Define o grupo para uma comparação superlativa."),
"ので":("ので","conjunção",["porque","como","já que"],"Indica motivo com tom explicativo."),
"お":("お","prefixo de cortesia",["prefixo honorífico","forma polida"],"Prefixo de cortesia em palavras de origem japonesa."),
"ご":("ご","prefixo de cortesia",["prefixo honorífico","forma polida"],"Prefixo de cortesia comum em palavras sino-japonesas."),
"しかし":("しかし","conjunção",["entretanto","porém"],"Introduz contraste entre duas frases."),
"それから":("それから","conjunção",["depois disso","e então"],"Introduz o próximo evento numa sequência."),
"そして":("そして","conjunção",["e então","além disso"],"Liga eventos ou fatos que se somam."),
"とき":("とき","substantivo gramatical",["quando","momento em que"],"Segue verbo, adjetivo ou substantivo + の; indica ocasião."),
"つもり":("つもり","substantivo gramatical",["intenção","plano"],"Após verbo de dicionário + つもりです expressa intenção."),
"どうですか":("どうですか","estrutura gramatical",["que tal?","como é?"],"Pede opinião ou oferece uma sugestão."),
"や":("や","partícula",["e","entre outros"],"Enumera exemplos, sem afirmar que a lista está completa."),
"ほうが":("ほうが","estrutura gramatical",["a opção de","o lado de"],"Com より, marca a alternativa preferida ou superior."),
"より":("より","partícula",["do que","a partir de"],"Marca o padrão de comparação."),
"な":("な","conector gramatical",["conexão de adjetivo な","que é"],"Liga adjetivo な ou substantivo a のです/ので/とき."),
"します":("します","verbo",["faço","faz","fazer"],"Forma polida de する; com にする indica escolha."),
"人":("ひと","substantivo",["pessoa","gente"],"Pessoa não especificada."),
"雨":("あめ","substantivo",["chuva"],"Fenômeno climático."),
"料理":("りょうり","substantivo",["comida","culinária","cozinha"],"Pode significar prato ou ato de cozinhar conforme o contexto."),
"山":("やま","substantivo",["montanha","monte"],"Elevação natural."),
"天気":("てんき","substantivo",["tempo","clima"],"Condição meteorológica."),
"空":("そら","substantivo",["céu"],"Espaço visível acima de nós."),
"赤い":("あかい","adjetivo い",["vermelho","vermelha"],"Adjetivo de cor."),
"青い":("あおい","adjetivo い",["azul"],"Adjetivo de cor."),
"冷たい":("つめたい","adjetivo い",["frio","gelado"],"Frio ao toque; difere de 寒い para clima."),
"おもしろい":("おもしろい","adjetivo い",["interessante","divertido"],"O contexto define o tom."),
"長い":("ながい","adjetivo い",["longo","comprido"],"Extensão no espaço ou no tempo."),
"速い":("はやい","adjetivo い",["rápido","veloz"],"Velocidade."),
"若い":("わかい","adjetivo い",["jovem"],"Idade pequena."),
"親切":("しんせつ","adjetivo な",["gentil","prestativo"],"Bondade no trato com outros."),
"有名":("ゆうめい","adjetivo な",["famoso","conhecido"],"Notoriedade."),
"暇":("ひま","adjetivo な",["livre","sem ocupação"],"Disponibilidade de tempo."),
"果物":("くだもの","substantivo",["fruta","frutas"],"Categoria de alimento."),
"家族":("かぞく","substantivo",["família"],"Pessoas da família."),
"飲み物":("のみもの","substantivo",["bebida"],"Algo para beber."),
"絵":("え","substantivo",["desenho","pintura"],"Imagem feita à mão."),
"紙":("かみ","substantivo",["papel"],"Material para escrever."),
"ドア":("ドア","substantivo",["porta"],"Entrada ou saída de um cômodo."),
"電気":("でんき","substantivo",["luz","eletricidade"],"Nesta frase, luz elétrica."),
"あそこ":("あそこ","advérbio",["ali","aquele lugar"],"Lugar distante de falante e ouvinte."),
"来週":("らいしゅう","substantivo",["próxima semana"],"Semana seguinte à atual."),
"五時":("ごじ","expressão de tempo",["cinco horas"],"Hora do relógio."),
"早く":("はやく","advérbio",["cedo","rapidamente"],"Forma adverbial de 早い."),
"いる":("いる","verbo",["estar","existir"],"Existência de ser animado; forma informal."),
"ある":("ある","verbo",["haver","existir","ter"],"Existência de objeto ou evento; forma informal."),
"来る":("くる","verbo",["vir","chegar"],"Forma de dicionário de 来ます."),
"行く":("いく","verbo",["ir"],"Forma de dicionário de 行きます."),
"見る":("みる","verbo",["ver","assistir"],"Forma de dicionário de 見ます."),
"寝る":("ねる","verbo",["dormir","deitar"],"Forma de dicionário de 寝ます."),
"読む":("よむ","verbo",["ler"],"Forma de dicionário de 読みます."),
"買う":("かう","verbo",["comprar"],"Forma de dicionário de 買います."),
"話す":("はなす","verbo",["falar","conversar"],"Forma de dicionário de 話します."),
"歌う":("うたう","verbo",["cantar"],"Forma de dicionário."),
"泳ぐ":("およぐ","verbo",["nadar"],"Forma de dicionário."),
"描く":("かく","verbo",["desenhar","pintar"],"Forma de dicionário."),
"料理する":("りょうりする","verbo",["cozinhar","preparar comida"],"Substantivo 料理 + する."),
"勉強する":("べんきょうする","verbo",["estudar"],"Substantivo 勉強 + する."),
"読み方":("よみかた","substantivo gramatical",["modo de ler","leitura"],"Base verbal + 方 forma 'modo de fazer'."),
"書き方":("かきかた","substantivo gramatical",["modo de escrever","grafia"],"Base verbal + 方 forma 'modo de fazer'."),
"行き方":("いきかた","substantivo gramatical",["modo de ir","caminho"],"Base verbal + 方 forma 'modo de fazer'."),
"作り方":("つくりかた","substantivo gramatical",["modo de preparar","receita"],"Base verbal + 方 forma 'modo de fazer'."),
"教えてください":("おしえてください","estrutura gramatical",["por favor, diga","por favor, ensine"],"Forma て + ください do verbo 教える."),
"選んでください":("えらんでください","estrutura gramatical",["por favor, escolha"],"Forma て + ください do verbo 選ぶ."),
"もらいました":("もらいました","verbo",["recebi","ganhei"],"Passado polido de もらう."),
"暑く":("あつく","forma adverbial",["quente","de modo quente"],"Adjetivo 暑い sem い + く; com なる significa 'ficar quente'."),
"なります":("なります","verbo",["torna-se","fica"],"Forma polida de なる; mudança de estado."),
"なりました":("なりました","verbo",["tornou-se","ficou"],"Passado polido de なる."),
"いました":("いました","verbo",["estava","havia"],"Passado polido de いる, para seres animados."),
"茶":("ちゃ","substantivo",["chá"],"Em お茶, お é prefixo de cortesia."),
"飯":("はん","substantivo",["arroz cozido","refeição"],"Em ご飯, ご é prefixo de cortesia."),
"見":("み","base verbal",["ver","assistir"],"Base de 見る, usada antes de に行く."),
"高すぎます":("たかすぎます","estrutura gramatical",["é caro demais","é alto demais"],"Adjetivo 高い sem い + すぎる; aqui, preço excessivo."),
"大きすぎます":("おおきすぎます","estrutura gramatical",["é grande demais"],"Adjetivo 大きい sem い + すぎる; tamanho excessivo."),
"置いてあります":("おいてあります","estrutura gramatical",["está colocado","foi deixado colocado"],"Colocar + てある: resultado de uma ação intencional."),
"開けてあります":("あけてあります","estrutura gramatical",["foi deixado aberto","está aberto de propósito"],"Abrir + てある: estado preparado intencionalmente."),
"飾ってあります":("かざってあります","estrutura gramatical",["está exposto","foi colocado em exposição"],"Expor + てある: resultado intencional."),
"書いてあります":("かいてあります","estrutura gramatical",["está escrito","foi deixado escrito"],"Escrever + てある: texto presente como resultado."),
"止めてあります":("とめてあります","estrutura gramatical",["está estacionado","foi deixado estacionado"],"Estacionar + てある: estado resultante."),
}

# Written verb stems, their pronunciation, and the Portuguese infinitive.
ROOTS = {
"勉強し":("べんきょうし","estudar"),"料理し":("りょうりし","cozinhar"),
"電話し":("でんわし","telefonar"),"勉強":("べんきょう","estudar"),
"料理":("りょうり","cozinhar"),"食べ":("たべ","comer"),
"飲":("の","beber"),"話":("はな","falar"),"遊":("あそ","brincar"),
"入":("はい","entrar"),"作":("つく","preparar"),"寝":("ね","dormir"),
"読":("よ","ler"),"行":("い","ir"),"見":("み","ver"),
"書":("か","escrever"),"歩":("ある","caminhar"),"来":("き","vir"),
"帰":("かえ","voltar"),"持":("も","levar"),"出":("で","sair"),
"乗":("の","pegar transporte"),"働":("はたら","trabalhar"),
"起":("お","acordar"),"待":("ま","esperar"),"買":("か","comprar"),
"会":("あ","encontrar"),"迎":("むか","buscar"),"休":("やす","descansar"),
"歌":("うた","cantar"),"泳":("およ","nadar"),"描":("か","desenhar"),
"置":("お","colocar"),"開":("あ","abrir"),"飾":("かざ","expor"),
"止":("と","estacionar"),"聞":("き","ouvir"),"走":("はし","correr"),
"撮":("と","tirar foto"),"消":("け","apagar"),
}

PT_PAST = {"comer":"comi","beber":"bebi","falar":"falei","brincar":"brinquei",
"entrar":"entrei","preparar":"preparei","dormir":"dormi","ler":"li","ir":"fui",
"ver":"vi","escrever":"escrevi","caminhar":"caminhei","vir":"vim","voltar":"voltei",
"levar":"levei","sair":"saí","pegar transporte":"peguei transporte","trabalhar":"trabalhei",
"acordar":"acordei","esperar":"esperei","comprar":"comprei","encontrar":"encontrei",
"buscar":"busquei","descansar":"descansei","estudar":"estudei","cozinhar":"cozinhei",
"telefonar":"telefonei","cantar":"cantei","nadar":"nadei","desenhar":"desenhei",
"colocar":"coloquei","abrir":"abri","expor":"expus","estacionar":"estacionei",
"ouvir":"ouvi","correr":"corri","tirar foto":"tirei foto","apagar":"apaguei"}
PT_GERUND = {"ver":"vendo","vir":"vindo","ir":"indo","ler":"lendo","pôr":"pondo"}
def gerund(action):
    if action in PT_GERUND: return PT_GERUND[action]
    if action.endswith('ar'): return action[:-2]+'ando'
    if action.endswith('er'): return action[:-2]+'endo'
    if action.endswith('ir'): return action[:-2]+'indo'
    return 'fazendo a ação de '+action
def past(action):
    return PT_PAST.get(action,f'já realizou a ação de {action}')

FORM_ENDINGS = [
 ("ちゃいけない",lambda v:[f"não pode {v}",f"é proibido {v}"],"contração coloquial de てはいけない"),
 ("じゃいけない",lambda v:[f"não pode {v}",f"é proibido {v}"],"contração coloquial de ではいけない"),
 ("なくてはならない",lambda v:[f"tem que {v}",f"é obrigatório {v}"],"obrigação forte com forma negativa"),
 ("なくてはいけない",lambda v:[f"precisa {v}",f"deve {v}"],"obrigação com forma negativa"),
 ("ないといけない",lambda v:[f"precisa {v}",f"deve {v}"],"obrigação em registro cotidiano"),
 ("なくてもいい",lambda v:[f"não precisa {v}",f"pode deixar de {v}"],"dispensa de obrigação"),
 ("ないでください",lambda v:[f"por favor, não {v}"],"pedido negativo polido"),
 ("たことがある",lambda v:[f"já {past(v)}",f"ter experiência de {v}"],"experiência passada"),
 ("だことがある",lambda v:[f"já {past(v)}",f"ter experiência de {v}"],"experiência passada"),
 ("てはいけない",lambda v:[f"não pode {v}",f"é proibido {v}"],"proibição"),
 ("ではいけない",lambda v:[f"não pode {v}",f"é proibido {v}"],"proibição"),
 ("てもいいです",lambda v:[f"pode {v}",f"tem permissão para {v}"],"permissão polida"),
 ("でもいいです",lambda v:[f"pode {v}",f"tem permissão para {v}"],"permissão polida"),
 ("ていません",lambda v:[f"ainda não {past(v)}",f"não está {gerund(v)}"],"forma ている negativa"),
 ("でいません",lambda v:[f"ainda não {past(v)}",f"não está {gerund(v)}"],"forma ている negativa"),
 ("てあります",lambda v:[f"resultado de {v}",f"foi deixado após {v}"],"resultado de ação intencional"),
 ("であります",lambda v:[f"resultado de {v}",f"foi deixado após {v}"],"resultado de ação intencional"),
 ("てください",lambda v:[f"por favor, {v}"],"pedido polido com forma て"),
 ("でください",lambda v:[f"por favor, {v}"],"pedido polido com forma て"),
 ("てから",lambda v:[f"depois de {v}"],"sequência após forma て"),
 ("でから",lambda v:[f"depois de {v}"],"sequência após forma て"),
 ("なくちゃ",lambda v:[f"precisa {v}",f"tem que {v}"],"obrigação coloquial abreviada"),
 ("ないで",lambda v:[f"sem {v}"],"ação não realizada antes da seguinte"),
 ("ませんか",lambda v:[f"vamos {v}?",f"quer {v}?"],"convite polido"),
 ("ましょうか",lambda v:[f"vamos {v}?",f"quer que eu {v}?"],"convite ou oferta polida"),
 ("ましょう",lambda v:[f"vamos {v}"],"convite polido"),
 ("すぎました",lambda v:[f"{past(v)} demais"],"excesso no passado"),
 ("すぎます",lambda v:[f"{v} demais"],"excesso"),
 ("ていました",lambda v:[f"estava {gerund(v)}"],"ação em andamento no passado"),
 ("でいました",lambda v:[f"estava {gerund(v)}"],"ação em andamento no passado"),
 ("ています",lambda v:[f"está {gerund(v)}"],"ação em andamento ou estado resultante"),
 ("でいます",lambda v:[f"está {gerund(v)}"],"ação em andamento ou estado resultante"),
 ("ている",lambda v:[f"está {gerund(v)}"],"forma ている informal"),
 ("でいる",lambda v:[f"está {gerund(v)}"],"forma ている informal"),
 ("たり",lambda v:[f"{v}, entre outras ações"],"exemplo de ação, normalmente repetido antes de する"),
 ("だり",lambda v:[f"{v}, entre outras ações"],"exemplo de ação, normalmente repetido antes de する"),
 ("たい",lambda v:[f"quer {v}",f"deseja {v}"],"desejo de realizar ação"),
 ("ません",lambda v:[f"não {v}"],"negativa polida"),
 ("ました",lambda v:[past(v),f"{v} (passado)"],"passado polido"),
 ("ます",lambda v:[v,f"{v} (forma polida)"],"presente/futuro polido"),
 ("た",lambda v:[past(v),f"{v} (passado)"],"passado informal"),
 ("だ",lambda v:[past(v),f"{v} (passado)"],"passado informal"),
]

TOPIC_NOTES = {
"ちゃいけない・じゃいけない":"Proibição coloquial: forma て/で contraída em ちゃ/じゃ + いけない.",
"だ / です":"Cópula informal だ e polida です ligam tema e predicado nominal.",
"だけ":"だけ restringe a referência a 'somente' o elemento anterior.",
"だろう":"だろう expressa uma suposição informal.",
"で":"で marca local da ação, meio de transporte ou idioma utilizado.",
"でも":"でも apresenta opção, inclusão ou exemplo, conforme o contexto.",
"でしょう":"でしょう expressa probabilidade ou pede concordância educadamente.",
"どんな":"どんな pergunta 'que tipo de' antes de um substantivo.",
"どうして":"どうして pergunta o motivo de uma situação.",
"どうやって":"どうやって pergunta o método ou o caminho para fazer algo.",
"が":"が marca o sujeito ou uma informação apresentada como nova.",
"があります":"が + あります apresenta a existência de um objeto ou evento.",
"がほしい":"が marca o objeto desejado com o adjetivo ほしい.",
"がいます":"が + います apresenta a existência de pessoas ou animais.",
"ほうがいい":"Verbo no passado informal + ほうがいい dá um conselho.",
"い-adjectives":"Adjetivos い terminam em い e modificam substantivos diretamente.",
"一番（いちばん）":"一番 marca o grau mais alto dentro do grupo comparado.",
"一緒に（いっしょに）":"一緒に indica uma ação realizada junto com alguém.",
"いつも":"いつも indica hábito constante: 'sempre'.",
"じゃない・ではない":"じゃない e ではない negam substantivos e adjetivos な informalmente.",
"か":"か no fim da frase forma uma pergunta; entre termos pode indicar escolha.",
"か～か":"A repetição de か apresenta alternativas a escolher ou identificar.",
"から":"から indica ponto de partida no tempo/lugar ou motivo.",
"方（かた）":"Base verbal + 方 transforma uma ação em 'modo de fazer'.",
"けど":"けど liga duas ideias em contraste no registro coloquial.",
"けれども":"けれども liga ideias contrastantes com tom mais formal.",
"まだ":"まだ indica que um estado continua ou uma ação ainda não ocorreu.",
"まだ～ていません":"まだ + forma ていません indica que algo ainda não foi feito.",
"まで":"まで indica limite final de tempo ou lugar.",
"前に（まえに）":"Verbo de dicionário + 前に indica ação feita antes de outra.",
"ませんか":"Forma ませんか faz um convite polido.",
"ましょう":"Forma ましょう propõe uma ação em conjunto.",
"ましょうか":"Forma ましょうか oferece ajuda ou sugere uma ação conjunta.",
"も":"も acrescenta 'também' ou inclui um caso adicional.",
"もう":"もう indica 'já' antes de uma ação concluída ou estado alcançado.",
"な-adjectives":"Adjetivos な usam な antes de substantivo e です ao fim de predicado polido.",
"なあ":"なあ expressa surpresa, emoção ou admiração do falante.",
"ないで":"Forma negativa + で indica fazer outra ação sem realizar a primeira.",
"ないでください":"Forma negativa + でください pede educadamente que não se faça algo.",
"ないといけない":"Forma negativa + といけない expressa obrigação cotidiana.",
"なくてもいい":"Forma negativa + なくてもいい dispensa uma obrigação.",
"なくちゃ":"なくちゃ é uma abreviação coloquial de obrigação.",
"なくてはいけない":"Forma negativa + なくてはいけない indica necessidade ou dever.",
"なくてはならない":"Forma negativa + なくてはならない indica obrigação forte.",
"なる":"なる indica mudança de estado: substantivo/adjetivo な + に ou adjetivo い + く.",
"んです":"んです acrescenta uma explicação em registro conversacional.",
"ね":"ね no fim pede concordância ou compartilha uma impressão.",
"に":"に marca destino, horário, receptor ou local de existência.",
"に行く（にいく）":"Base verbal + に行く indica ir para realizar aquela ação.",
"にする":"Substantivo + にする indica escolher uma opção.",
"に/へ":"に aponta o destino; へ destaca a direção do movimento.",
"の":"の liga substantivos em relação de posse, origem ou especificação.",
"のです":"のです apresenta explicação com tom mais pleno que んです.",
"のが下手（のがへた）":"Verbo + のが下手 avalia pouca habilidade numa ação.",
"のが上手（のがじょうず）":"Verbo + のが上手 avalia boa habilidade numa ação.",
"のが好き（のがすき）":"Verbo + のが好き expressa gosto por realizar uma ação.",
"の中で[A]が一番（のなかで[A]がいちばん）":"の中で define o grupo; 一番 aponta o grau máximo nele.",
"ので":"ので introduz uma razão com tom explicativo.",
"お / ご":"お e ご são prefixos de cortesia, conforme a palavra.",
"を":"を marca o objeto direto da ação.",
"をください":"Objeto + をください é um pedido polido para receber algo.",
"しかし":"しかし inicia uma frase em contraste com a anterior.",
"それから":"それから indica o evento que vem depois.",
"そして":"そして liga ou acrescenta eventos e fatos.",
"すぎる":"Base verbal ou adjetival + すぎる indica excesso.",
"たことがある":"Passado informal + ことがある indica experiência anterior.",
"たい":"Base verbal + たい expressa desejo do falante.",
"たり～たり":"Formas たり listam exemplos de ações, seguidas de する.",
"てある":"Verbo transitivo em てある descreve o resultado preparado de uma ação.",
"ている":"Forma ている indica ação em andamento ou estado resultante.",
"てから":"Forma てから coloca uma ação antes da seguinte.",
"てください":"Forma てください faz um pedido polido de ação.",
"てはいけない":"Forma てはいけない proíbe uma ação.",
"てもいいです":"Forma てもいいです permite uma ação.",
"と":"と une substantivos ou indica companhia.",
"とき":"とき marca a ocasião em que algo acontece.",
"とても":"とても intensifica um adjetivo: 'muito'.",
"つもり":"Verbo de dicionário + つもりです expressa intenção futura.",
"は":"は marca o tópico sobre o qual se fala.",
"は〜より・・・です":"より marca o padrão de comparação; o tópico fica com は.",
"はどうですか":"Tópico + はどうですか pede opinião ou sugere uma opção.",
"や":"や enumera exemplos sem esgotar a lista.",
"よ":"よ no fim reforça a informação dada ao ouvinte.",
"より～ほうが":"A estrutura より ... のほうが indica a alternativa superior ou preferida.",
}

FOCUS_ALIASES = {
"ちゃいけない・じゃいけない":("ちゃいけない","じゃいけない"),
"だ / です":("だ","です"),"がほしい":("ほしい",),"がいます":("が","います"),
"があります":("が","あります"),"ほうがいい":("ほうがいい",),
"い-adjectives":(),"な-adjectives":(),"一番（いちばん）":("一番",),
"一緒に（いっしょに）":("一緒に",),"じゃない・ではない":("じゃない","ではない"),
"か～か":("か",),"方（かた）":("方",),"まだ～ていません":("ていません","でいません"),
"前に（まえに）":("前に",),"に行く（にいく）":("に","行く"),
"にする":("に","します"),"に/へ":("に","へ"),
"のが下手（のがへた）":("のが下手",),"のが上手（のがじょうず）":("のが上手",),
"のが好き（のがすき）":("のが好き",),
"の中で[A]が一番（のなかで[A]がいちばん）":("の中で","一番"),
"お / ご":("お","ご"),"をください":("を","ください"),
"すぎる":("すぎ",),"たことがある":("ことがある",),"たい":("たい",),
"たり～たり":("たり","だり"),"てある":("てあります","であります"),
"ている":("ています","でいます"),"てから":("てから","でから"),
"てください":("てください","でください"),
"てはいけない":("てはいけない","ではいけない"),
"てもいいです":("てもいいです","でもいいです"),
"は〜より・・・です":("より",),"はどうですか":("どうですか",),
"より～ほうが":("ほうが","より"),
"なる":("なります","なりました"),
}

def auto_entry(word):
    for stem,(reading,action) in sorted(ROOTS.items(),key=lambda kv:-len(kv[0])):
        if not word.startswith(stem): continue
        ending=word[len(stem):]
        if not ending or any(ch not in 'ぁあぃいうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよりらりるれろゎわをんー' for ch in ending):
            continue
        pronunciation=reading+ending
        for suffix,meanings,note in FORM_ENDINGS:
            if word.endswith(suffix):
                kind='verbo' if suffix in ('ます','ました','ません','た','だ') else 'estrutura gramatical'
                return (pronunciation,kind,meanings(action),f"{action.capitalize()}: {note}.")
        if len(word)<=len(stem)+2:
            return (pronunciation,'base verbal',[action,f"para {action}"],"Base verbal; liga-se a outra estrutura da frase.")
    raise ValueError(f"Trecho sem anotação: {word}")

def extend(phrases, base_lexicon):
    if set(TOPIC_NOTES)!={topic for topic,_ in GROUPS}:
        raise ValueError('As explicações dos tópicos estão incompletas.')
    lexicon={**base_lexicon,**{word:(word,*entry) for word,entry in EXTRA.items()}}
    existing={phrase['text'] for phrase in phrases}
    for topic,raw in GROUPS:
        lines=raw.strip().splitlines()
        if len(lines)!=5: raise ValueError(f"{topic}: esperado 5 frases, recebeu {len(lines)}")
        for raw_line in lines:
            keys_pt=raw_line.split('|')
            if len(keys_pt)!=2: raise ValueError(raw_line)
            keys,translation=keys_pt
            keys=keys.split()
            tokens=[]
            for position,key in enumerate(keys):
                surface,reading,kind,meanings,note=lexicon.get(key) or (key,*auto_entry(key))
                if key=='何' and position+1<len(keys) and keys[position+1]=='です': reading='なん'
                tokens.append({'surface':surface,'reading':reading,'kind':kind,
                    'meanings_pt':meanings,'note_pt':note})
            if topic=='い-adjectives':
                focus=[i for i,t in enumerate(tokens) if t['kind']=='adjetivo い']
            elif topic=='な-adjectives':
                focus=[i for i,t in enumerate(tokens) if t['kind']=='adjetivo な']
            else:
                aliases=FOCUS_ALIASES.get(topic,(topic,))
                focus=[i for i,t in enumerate(tokens) if any(
                    (alias==t['surface'] if len(alias)==1 and alias!='方' else alias in t['surface']) for alias in aliases)]
            if not focus:
                raise ValueError(f'Sem trecho-alvo para {topic}: {keys}')
            text=''.join(token['surface'] for token in tokens)
            text=text.replace('ですしかし','です。しかし').replace('ますそれから','ます。それから').replace('ますそして','ます。そして').replace('ますしかし','ます。しかし').replace('ですそして','です。そして')
            text+= '？' if translation.endswith('?') else '。'
            if text in existing: raise ValueError(f"Frase repetida ({topic}): {text}")
            existing.add(text)
            phrases.append({'id':len(phrases)+1,'level':'N5','category':'gramática',
                'grammar_point':topic,'grammar_explanation_pt':TOPIC_NOTES[topic],
                'focus_token_indices':focus,'text':text,'translation_pt':translation,'tokens':tokens})
    return phrases

