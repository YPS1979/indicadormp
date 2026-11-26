# IndicadorMP

Repositório: https://github.com/YPS1979/indicadormpap

Painel de indicadores do MP-AP.
Artefato publicado: https://claude.ai/artifact/Sps523SJDUoPkKmaFLXiwn

- indicadormp.html: o painel completo (página única, dados embutidos).
- atualizar_datajud.py: consulta a API pública do DataJud (CNJ) e reconstrói a aba Acervo Judicial no HTML.
- atualizar_conselho_tutelar.py: atualiza o painel de Conselhos Tutelares (Rec. CNMP 119/2025) a partir do CSV do CNMP; lê fontes/ e grava cópia em backups/.
- publicar/publicar.sh: publica o painel no Cloudflare Pages (https://indicadormp.pages.dev) como PWA; depende de publicar/public (sw.js, manifest.json, icons/), ainda só no Mac.
- gerar_visual.py: gerador aposentado em 14/08/2026 (a enviar do Mac, só como registro).
- fontes/: 29 arquivos de origem: exportações do sistema de inspeções do CNMP por eixo e ciclo (2S/2025 e 1S/2026), IDEB 2025, taxonomia CNJ (classes, assuntos, movimentos), matriz de atribuições das PJs, anuário 2025, logo.
- documentos/: geradores dos cinco documentos institucionais (manuais, justificativa, requerimento, apresentação); falta _base.py.

Os scripts calculam caminhos a partir da própria pasta: devem ficar onde estão nesta árvore.
- backups/: base histórica arquivada (8 versões anteriores do painel, de 25/07 a 19/10/2026).
- conclusao_cao_educacao.md: registro do texto da seção Conclusão do CAO Educação (versão didática, aplicada em 26/11/2026).
