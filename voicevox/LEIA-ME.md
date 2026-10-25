# Voz japonesa local

VOICEVOX Engine 0.26.0, versao CUDA para Windows. A GTX 1660 de 6 GB foi detectada e o motor confirmou suporte a CUDA. Ha varias vozes e estilos.

## Usar

Abra o PowerShell nesta pasta e execute:

```powershell
.\iniciar.ps1
python .\speak.py --list-voices
python .\speak.py 'こんにちは。今日はいい天気ですね。' --speaker 2 --output .\minha-voz.wav
```

O numero em `--speaker` vem da lista de vozes. A saida e um arquivo WAV. Para desligar o motor, encerre `run.exe` no Gerenciador de Tarefas.

## Verificacao nesta maquina

- GTX 1660, 6 GB; suporte CUDA confirmado em `/supported_devices`.
- Frase japonesa de exatamente 256 caracteres: 6,01 segundos para analise e sintese, gerando 47,9 segundos de audio.
- Duas vozes testadas: IDs 2 e 3, com arquivos `voz-2.wav` e `voz-3.wav`.
- O tempo foi medido com o motor ja iniciado; a primeira inicializacao pode demorar mais.

As vozes do VOICEVOX podem ter regras proprias de atribuicao e uso. Consulte os termos correspondentes antes de publicar audio gerado.
