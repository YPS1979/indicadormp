# Documentos institucionais do IndicadorMP

## Geradores (g1 a g5 + _base.py)
Cada `gN.py` monta o corpo em HTML e chama `doc()` de `_base.py`, que aplica o modelo visual
e grava o arquivo final. Rodar, nesta pasta: `python3 g1.py` (e assim por diante).

| Script | Documento gerado |
|---|---|
| g1.py | 01_manual_do_usuario.html — Manual do Usuário |
| g2.py | 02_manual_tecnico.html — Manual Técnico de Implementação |
| g3.py | 03_justificativa.html — Justificativa de Implementação |
| g4.py | 04_requerimento_pgj.html — Requerimento ao Procurador-Geral de Justiça |
| g5.py | 05_apresentacao.html — Apresentação do Trabalho |

## Demais arquivos
- 06_painel_de_metricas.md, 07_fonte_notebooklm.md, 07_roteiro_video.md, 07_instrucoes_video.txt: material de apoio (métricas, fonte para o NotebookLM, roteiro de vídeo).
- IndicadorMP-Apresentacao.html / .pdf e apresentação.indicadorMP.gamma.rtf: apresentação do painel.
- arquitetura-indicadormp.html, governanca-dados.html, padroes-nacionais.html, trilha-resolutiva-fluxograma.html: páginas de documentação técnica.

Observação: os textos de g2 e g4 citam o painel com "aproximadamente 14 MB" e a rotina de
atualização com o `gerar_visual.py`. O arquivo atual tem cerca de 8,3 MB e o gerador foi
aposentado em 14/08/2026; convém rever esses trechos antes de reemitir os documentos.
