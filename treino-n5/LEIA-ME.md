# Prática N5 e N4: escuta e escrita

Execute `iniciar.ps1` no PowerShell. A interface abrirá em <http://127.0.0.1:8765>.

O arquivo **Lista e Frases N5.json** contém 520 frases: as 100 originais mais cinco exemplos para cada um dos 84 tópicos gramaticais solicitados. Cada frase tem tradução integral; cada trecho registra escrita, leitura, classe, significados em português e nota de uso. As frases novas também incluem tópico, explicação gramatical e os trechos que exercitam o tópico. `gerar_frases.py` e `gramatica_extra.py` são as fontes editáveis do banco.

O seletor de nível inclui **900 entradas N4** em `Lista e Frases N4.json`. As 400 primeiras cobrem 132 tópicos gramaticais; outras 500 combinam temas de vocabulário com situações de conversa, aula, pesquisa, família e deslocamento. As novas entradas têm de 41 a 50 caracteres japoneses. A lista inclui tradução da frase inteira e leitura, classe e significados de cada trecho. `gerar_frases_n4.py` e `cenarios_n4.py` permitem regenerá-la com o motor VOICEVOX em execução. O nível selecionado é lembrado no navegador.

O áudio é gerado pelo VOICEVOX CUDA instalado na pasta irmã `voicevox`. O seletor oferece as vozes de fala disponíveis no motor, e cada combinação de frase e voz fica em `audio-cache/` após a primeira reprodução. O player permite pausar e retomar do mesmo ponto, além de escolher velocidades de 0,5× a 2×. O checkbox de pausa após partículas cria uma versão da frase com 0,5 segundo de silêncio depois de cada partícula identificada. Velocidade e checkbox ficam salvos no navegador. O motor pode demorar alguns segundos para iniciar na primeira vez.

O resultado da correção também inclui um player da frase japonesa. Ao selecionar texto japonês no exercício ou no resultado, a voz japonesa do navegador lê o trecho e o repete dois segundos após terminar, até a seleção ser desfeita. Se o navegador não tiver essa voz, o aplicativo usa um clipe local curto em cache. Um pequeno painel mostra os significados cadastrados para os trechos correspondentes da frase atual.

No modo **Escuta**, ouça a frase e transcreva o que ouviu. A correção aceita a escrita da frase ou a leitura em kana de cada trecho. Espaços e pontuação não contam. A associação entre o texto digitado e os trechos é aproximada quando há vários erros juntos; confira a análise exibida no resultado.

No modo **Complete a frase**, a tradução em português aparece como objetivo e de duas a quatro partes da frase japonesa viram campos vazios. Nas entradas N4, as lacunas ficam no exemplo do tópico. O áudio da frase pode ser ouvido antes de responder, com a voz e a velocidade escolhidas. Só as lacunas são avaliadas. Para cada lacuna, a escrita original ou sua leitura em kana é aceita. Gramática recebe peso 1,5 e vocabulário, 1,25. Escuta recebe peso 1. Os resultados são guardados separadamente por nível e modo em `desempenho.sqlite3`, preservando o histórico anterior.
