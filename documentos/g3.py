# -*- coding: utf-8 -*-
from _base import doc
corpo = """
<h2>1. O problema que a ferramenta enfrenta</h2>
<p>A atividade fiscalizatória do Ministério Público produz, a cada ciclo, um volume expressivo de informação: roteiros de inspeção preenchidos, relatórios individuais, ofícios e respostas. Essa informação, contudo, costuma permanecer dispersa — cada unidade em seu procedimento, cada eixo em seu formulário, cada base social em seu portal. A consequência prática é conhecida: decide-se o que priorizar por percepção, e não por evidência; e, um ano depois, não há como afirmar objetivamente se a atuação mudou alguma coisa.</p>
<p>O IndicadorMP foi construído para enfrentar exatamente esses dois pontos: <strong>reunir o que está disperso</strong> e <strong>tornar mensurável o efeito da atuação</strong>.</p>

<h2>2. O que já existe, hoje, pronto para uso</h2>
<table><tr><th style="width:38%">Camada</th><th>Conteúdo consolidado</th></tr>
<tr><td>Inspeções do CNMP</td><td>97 unidades inspecionadas no ciclo 2026, em 10 eixos temáticos, 12 comarcas e 16 municípios, com 729 não conformidades classificadas por severidade e fundamento legal.</td></tr>
<tr><td>Rede socioassistencial</td><td>Unidades do Censo SUAS 2024: CRAS, CREAS, Centro POP, acolhimento, centros de convivência e centros-dia, gestões, fundos e conselhos.</td></tr>
<tr><td>Rede escolar</td><td>786 escolas da educação básica, a partir dos microdados do Censo Escolar 2025 (INEP).</td></tr>
<tr><td>Contexto municipal</td><td>Mais de trinta fontes oficiais: IBGE, DataSUS, MDS (Censo SUAS, CadÚnico, Bolsa Família), DataJud e Radar da Transparência Pública.</td></tr>
<tr><td>Produtos</td><td>Três relatórios institucionais prontos para uso — por Promotoria de Justiça, por Município e por CAO —, com plano de atuação por prioridade e orientações de monitoramento.</td></tr>
</table>

<h2>3. Fundamento normativo</h2>
<ul>
<li><strong>Carta de Brasília (2016)</strong> — firma a atuação resolutiva pautada em diagnóstico prévio das carências da sociedade.</li>
<li><strong>Resolução CNMP nº 147/2016</strong> — fixa as diretrizes do Planejamento Estratégico e padroniza a definição de indicadores e metas.</li>
<li><strong>Recomendação CNMP-CN nº 02/2018</strong> — exige do membro o conhecimento dos indicadores sociais de sua área de atribuição (art. 6º, VI) e afere a resolutividade material pela melhoria desses indicadores ao longo do tempo (art. 12, parágrafo único).</li>
<li><strong>Resolução CNMP nº 276/2023</strong> — Política Nacional do MP Digital: determina o uso de dados na tomada de decisões, com transparência de origem, data e método (art. 2º, V).</li>
<li><strong>Art. 130-A, § 2º, da CR/1988 e art. 155, parágrafo único, da LC Estadual nº 0079/2013 (LOMPAP)</strong> — competência da Corregedoria-Geral para avaliar, orientar e fiscalizar a resolutividade da atuação.</li>
</ul>

<h2>4. Benefícios esperados</h2>
<h3>4.1 Para os órgãos de execução</h3>
<p>Cada Promotoria recebe, pronto, o diagnóstico da sua comarca: o que foi apurado, em quais unidades, com que gravidade, sob qual fundamento legal e com sugestão de encaminhamento. O tempo hoje gasto para reunir e organizar informação é convertido em tempo de atuação.</p>
<h3>4.2 Para os Centros de Apoio</h3>
<p>A leitura temática revela padrões de rede — falhas que se repetem em dezenas de unidades — e permite substituir dezenas de procedimentos individuais por uma atuação coletiva junto ao gestor responsável.</p>
<h3>4.3 Para a Corregedoria-Geral e a Administração Superior</h3>
<p>O painel oferece base objetiva para orientar, priorizar inspeções e medir resultado, na exata função que a Recomendação CNMP-CN nº 02/2018 atribui ao órgão correicional.</p>
<h3>4.4 Para a sociedade</h3>
<p>Publicado em sítio institucional, o painel materializa transparência ativa qualificada: não apenas dados brutos, mas diagnóstico compreensível, com fonte, data e método declarados.</p>

<h2>5. Custo e risco</h2>
<table><tr><th style="width:30%">Aspecto</th><th>Situação</th></tr>
<tr><td>Custo de desenvolvimento</td><td>Já realizado, sem contratação externa.</td></tr>
<tr><td>Custo de infraestrutura</td><td>Praticamente nulo: arquivo estático de 14 MB, sem servidor de aplicação, banco de dados ou licenças.</td></tr>
<tr><td>Custo de manutenção</td><td>Atualização periódica dos dados, conforme calendário de coleta já documentado no próprio painel.</td></tr>
<tr><td>Risco tecnológico</td><td>Baixo. Sem dependência de serviços externos; o arquivo permanece funcional mesmo sem internet e é naturalmente arquivável.</td></tr>
<tr><td>Risco de dados</td><td>Baixo. Utiliza dados públicos ou agregados; não trata dados pessoais sensíveis de usuários dos serviços.</td></tr>
</table>

<h2>6. Por que institucionalizar agora</h2>
<p>A ferramenta está pronta e testada, e o ciclo de inspeções 2026 já produziu a primeira base completa. Institucionalizar o painel neste momento permite que a próxima coleta funcione como <strong>reinspeção com linha de base</strong> — isto é, que seja possível medir a variação e atribuir sentido à atuação do primeiro ciclo. Sem publicação e uso oficial, os dados envelhecem e a oportunidade de medição comparada se perde.</p>
<div class="nota">O ganho decisivo não é ter os dados: é ter os dados no momento certo, no formato em que o membro consegue usá-los, e com a possibilidade de aferir depois o que mudou.</div>
"""
print(doc("Justificativa de Implementação","Fundamento, benefícios e oportunidade da institucionalização do IndicadorMP", corpo, "03_justificativa.html"))
