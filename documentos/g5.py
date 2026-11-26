# -*- coding: utf-8 -*-
from _base import doc
corpo = """
<h2>1. Em uma frase</h2>
<p style="font-size:18px;line-height:1.5">O IndicadorMP transforma o resultado das inspeções do Ministério Público em diagnóstico municipal utilizável — e mensurável no ciclo seguinte.</p>

<h2>2. O caminho percorrido</h2>
<table><tr><th style="width:22%">Etapa</th><th>Entrega</th></tr>
<tr><td>Consolidação</td><td>Importação e padronização dos resultados de inspeção dos dez eixos regulados por Resoluções e Recomendações do CNMP.</td></tr>
<tr><td>Classificação</td><td>Cada não conformidade recebeu severidade (Alta, Média, Atenção), fundamento legal e trilha resolutiva, com registro taxonômico correspondente.</td></tr>
<tr><td>Contextualização</td><td>Integração de mais de trinta fontes oficiais — IBGE, INEP, MDS, DataSUS, DataJud e Radar da Transparência — com recorte municipal.</td></tr>
<tr><td>Ampliação</td><td>Incorporação da rede socioassistencial do Censo SUAS e da rede escolar do Censo Escolar, que não passam por inspeção direta mas compõem a mesma rede de proteção.</td></tr>
<tr><td>Produção</td><td>Geração automatizada de três relatórios institucionais, com plano de atuação por prioridade e orientações de monitoramento.</td></tr>
</table>

<h2>3. O que o painel entrega hoje</h2>
<table><tr><th style="width:30%">Número</th><th>Significado</th></tr>
<tr><td>97 unidades</td><td>inspecionadas no ciclo 2026, em 12 comarcas e 16 municípios</td></tr>
<tr><td>729 não conformidades</td><td>classificadas por severidade e fundamento legal</td></tr>
<tr><td>10 eixos</td><td>de conselhos tutelares a delegacias, perícia e sistema prisional</td></tr>
<tr><td>786 escolas</td><td>avaliadas nos microdados do Censo Escolar 2025</td></tr>
<tr><td>3 relatórios</td><td>por Promotoria, por Município e por CAO — este último inclusive para a Educação</td></tr>
</table>

<h2>4. Como o membro usa</h2>
<ol>
<li>Abre a aba Relatórios, escolhe a sua Promotoria e clica em Pesquisar.</li>
<li>Lê, na mesma página: o que foi apurado em cada unidade, o contexto social do município, o que mudou desde o ciclo anterior e o plano de atuação sugerido por prioridade.</li>
<li>Salva em PDF, com nome padronizado, e instaura os procedimentos na classe e no assunto indicados.</li>
<li>No ciclo seguinte, compara — e é essa comparação que permite afirmar se houve resolutividade material.</li>
</ol>

<h2>5. Diferenciais</h2>
<ul>
<li><strong>Funciona offline</strong>: arquivo único, sem servidor, sem internet, sem licença.</li>
<li><strong>Diz de onde veio cada número</strong>: fonte e ano-base declarados item a item, como exige a Resolução CNMP nº 276/2023.</li>
<li><strong>Assume os próprios limites</strong>: separa o que foi verificado pelo MP do que é autodeclarado pelos gestores, e trata prioridades como proposta técnica, preservando a independência funcional.</li>
<li><strong>Fecha o ciclo</strong>: da inspeção ao diagnóstico, do diagnóstico ao plano, do plano à medição do impacto.</li>
</ul>

<h2>6. O que se pede</h2>
<p>Reconhecimento institucional da ferramenta, autorização para publicação em sítio do Ministério Público, designação da área de tecnologia para hospedagem e definição de ciclo periódico de atualização sob responsabilidade da Corregedoria-Geral.</p>

<h2>7. Próximos passos previstos</h2>
<ol>
<li>Publicação da versão 1.0 e comunicação às Promotorias e Centros de Apoio.</li>
<li>Coleta do segundo ciclo de inspeções, com a base atual servindo de linha de base.</li>
<li>Ativação da página de Evolução em todos os eixos, com medição comparada por unidade.</li>
<li>Extensão dos relatórios temáticos aos demais Centros de Apoio.</li>
</ol>
<div class="nota">Documentos que acompanham esta apresentação: Justificativa de Implementação, Manual Técnico de Implementação, Manual do Usuário e Requerimento ao Procurador-Geral de Justiça.</div>
"""
print(doc("Apresentação do Trabalho","IndicadorMP · síntese executiva para a Administração Superior", corpo, "05_apresentacao.html"))
