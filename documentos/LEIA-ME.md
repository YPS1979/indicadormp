# Documentos institucionais do IndicadorMP

Geradores dos cinco documentos que acompanham o pedido de institucionalização do painel.
Cada script monta o corpo em HTML e chama `doc(titulo, subtitulo, corpo, nome_do_arquivo)`
do módulo `_base`, que aplica o modelo visual e grava o HTML final.

| Script | Documento gerado |
|---|---|
| g1.py | 01_manual_do_usuario.html — Manual do Usuário |
| g2.py | 02_manual_tecnico.html — Manual Técnico de Implementação |
| g3.py | 03_justificativa.html — Justificativa de Implementação |
| g4.py | 04_requerimento_pgj.html — Requerimento ao Procurador-Geral de Justiça |
| g5.py | 05_apresentacao.html — Apresentação do Trabalho |

Pendente: `_base.py` ainda não está no repositório (só no Mac). Sem ele, os scripts não rodam.
Os HTML gerados, se existirem, também podem ser guardados aqui.

Observação: os textos citam o painel com "aproximadamente 14 MB" e a rotina de atualização
com o `gerar_visual.py`. O arquivo atual tem cerca de 8,3 MB e o gerador foi aposentado em
14/08/2026; convém rever esses trechos antes de reemitir os documentos.
