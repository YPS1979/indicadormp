# -*- coding: utf-8 -*-
from _base import doc

corpo = """
<h2>1. O que é o IndicadorMP</h2>
<p>O IndicadorMP é o painel de inteligência de dados da Corregedoria-Geral do Ministério Público do Estado do Amapá. Reúne, em um único arquivo que abre no navegador e funciona sem conexão com a internet, duas camadas de informação: as inspeções e visitas técnicas realizadas pelo MP-AP com base nas Resoluções e Recomendações do CNMP e o retrato social, econômico e institucional dos 16 municípios do Estado, extraído de mais de trinta fontes oficiais.</p>
<p>Na versão atual, o painel consolida <strong>97 unidades inspecionadas</strong> no ciclo 2026, distribuídas em <strong>12 comarcas</strong> e <strong>16 municípios</strong>, com <strong>729 não conformidades</strong> apuradas, além de <strong>786 escolas</strong> da educação básica e da rede socioassistencial do Censo SUAS.</p>

<h2>2. Como navegar</h2>
<h3>Coluna da esquerda</h3>
<table><tr><th style="width:26%">Aba</th><th>O que traz</th></tr>
<tr><td>Início</td><td>Apresentação do painel: o que é, para que serve e o fundamento normativo.</td></tr>
<tr><td>Indicadores</td><td>Reúne dois grupos: <em>Indicadores CNMP</em>, com os dez eixos de inspeção, e <em>Outros Indicadores</em>, com as bases que descrevem a rede local (Censo SUAS, Censo Escolar, Radar da Transparência).</td></tr>
<tr><td>Dados de apoio</td><td>Bases de contexto: Censo 2022 (IBGE), Saúde (DataSUS), Bolsa Família e CadÚnico (MDS) e acervo judicial (DataJud).</td></tr>
<tr><td>Relatórios</td><td>Geração dos três relatórios institucionais.</td></tr>
<tr><td>Documentação</td><td>Apresentação do painel, governança de dados (calendário de coleta das fontes) e este manual.</td></tr>
</table>

<h3>Dentro de cada painel</h3>
<p>Os painéis de inspeção seguem sempre a mesma sequência de páginas: <strong>Sobre</strong> (o que a norma exige), <strong>Indicadores</strong> (o quadro completo de itens verificados, com severidade e fundamento legal), <strong>Amapá</strong> (o retrato estadual, unidade por unidade), <strong>Padrão Nacional</strong> (a comparação com o Brasil) e <strong>Evolução</strong> (a comparação entre ciclos, quando há dois ciclos coletados).</p>

<h2>3. Como ler os números</h2>
<table><tr><th style="width:24%">Conceito</th><th>Definição</th></tr>
<tr><td>Indicador</td><td>Pergunta objetiva do roteiro oficial de inspeção. A resposta pode ser conforme, não conforme ou não informado.</td></tr>
<tr><td>Não conformidade</td><td>Cada resposta “não conforme”. É o achado que enseja atuação.</td></tr>
<tr><td>Severidade</td><td><strong>Alta</strong>: violação direta de direito ou risco imediato. <strong>Média</strong>: obrigação legal expressa descumprida. <strong>Atenção</strong>: parâmetro de qualidade ou sinal de alerta.</td></tr>
<tr><td>Escore de penalidade</td><td>Soma ponderada das não conformidades (Alta ×3, Média ×2, Atenção ×1). Quanto menor, mais conforme.</td></tr>
<tr><td>Trilha resolutiva</td><td>Sugestão de encaminhamento para cada não conformidade, com parâmetro normativo e o registro taxonômico (classe e assunto) a adotar na instauração.</td></tr>
</table>
<div class="nota">A severidade não é adjetivo: ela separa o que exige resposta imediata, por atingir direito indisponível, do que comporta prazo, plano e monitoramento.</div>

<h2>4. Os relatórios</h2>
<h3>4.1 Relatório de Diagnóstico por Promotoria de Justiça</h3>
<p>Documento completo da comarca. Estrutura: <em>Parte 1</em> — apresentação e metodologia; <em>Parte 2</em> — resumo, análise por unidade ou serviço, contexto municipal em fontes integradas, evolução da reinspeção, plano de atuação sugerido, orientações para o monitoramento do resultado e conclusão. Traz ainda o anexo com a relação das escolas da rede local.</p>
<h3>4.2 Relatório de Não Conformidades por Município</h3>
<p>Recorte objetivo por município ou comarca, com o quadro das unidades, o detalhamento das não conformidades e o complemento das demais bases.</p>
<h3>4.3 Relatório de Diagnóstico por CAO</h3>
<p>Leitura temática para os Centros de Apoio Operacional, inclusive para áreas sem inspeção própria — como a Educação, cujo diagnóstico é construído sobre os microdados do INEP.</p>

<h3>Como gerar</h3>
<ol>
<li>Abra a aba <strong>Relatórios</strong> e escolha a subaba desejada.</li>
<li>Selecione o filtro (Promotoria, Município ou CAO).</li>
<li>Clique em <strong>Pesquisar</strong> — o relatório é montado na tela.</li>
<li>Clique em <strong>Salvar/Imprimir</strong> e escolha “Salvar como PDF”. O nome do arquivo já vem sugerido no padrão <code>Relatório por Promotoria_IndicadorMP_Município</code>.</li>
</ol>
<div class="nota">Marque a opção “Gráficos de plano de fundo” do navegador apenas se quiser conferir; o painel já força a impressão fiel das cores, independentemente dessa caixa.</div>

<h2>5. Limites de uso</h2>
<ul>
<li>Os dados das inspeções são verificados pelo Ministério Público; os das demais bases são <strong>autodeclarados</strong> pelos gestores aos órgãos de origem e não passaram por conferência in loco.</li>
<li>Os indicadores sociais são <strong>médias municipais</strong> e escondem desigualdades internas entre bairros, zona rural e comunidades tradicionais.</li>
<li>Os relatórios são <strong>diagnósticos</strong>: prioridades e prazos têm natureza de proposta técnica, cabendo ao membro titular, com independência funcional, definir instrumentos e estratégia.</li>
</ul>

<h2>6. Perguntas frequentes</h2>
<table><tr><th style="width:34%">Pergunta</th><th>Resposta</th></tr>
<tr><td>Preciso de internet?</td><td>Não. O painel é um arquivo único e funciona offline, inclusive para gerar e salvar relatórios.</td></tr>
<tr><td>Posso enviar o arquivo a terceiros?</td><td>Sim. Não há dados pessoais sensíveis: as bases são públicas ou agregadas.</td></tr>
<tr><td>Como sei se um dado está desatualizado?</td><td>A aba Documentação traz o calendário de coleta de cada fonte, com referência carregada, recorrência e situação.</td></tr>
<tr><td>Encontrei um erro. O que faço?</td><td>Use a aba Sugestões, que abre uma mensagem endereçada à Corregedoria-Geral.</td></tr>
</table>
"""
print(doc("Manual do Usuário","IndicadorMP · orientações de navegação, leitura dos indicadores e geração de relatórios", corpo, "01_manual_do_usuario.html"))
