# -*- coding: utf-8 -*-
from _base import doc
corpo = """
<p style="text-align:right">Macapá/AP, ____ de ______________ de 2026.</p>
<p><strong>Excelentíssimo Senhor Procurador-Geral de Justiça do Estado do Amapá,</strong></p>

<p>ANDERSON BATISTA DE SOUZA, Promotor de Justiça, no exercício das atribuições junto à Corregedoria-Geral do Ministério Público do Estado do Amapá, vem, respeitosamente, à presença de Vossa Excelência expor e requerer o que segue.</p>

<h2>I — Do objeto</h2>
<p>Trata-se de requerimento de <strong>institucionalização e publicação, em sítio institucional do Ministério Público do Estado do Amapá, do painel IndicadorMP</strong>, ferramenta de inteligência de dados desenvolvida no âmbito da Corregedoria-Geral, destinada a consolidar os resultados das inspeções e visitas técnicas realizadas com base nas Resoluções e Recomendações do Conselho Nacional do Ministério Público e a cruzá-los com indicadores sociais oficiais dos 16 municípios do Estado.</p>

<h2>II — Da situação atual</h2>
<p>O painel encontra-se concluído e operacional, consolidando <strong>97 unidades inspecionadas</strong> no ciclo 2026, com <strong>729 não conformidades</strong> classificadas por severidade e fundamento legal, distribuídas em <strong>12 comarcas</strong> e <strong>16 municípios</strong>, além da rede socioassistencial do Censo SUAS 2024 e de <strong>786 escolas</strong> da educação básica apuradas nos microdados do Censo Escolar 2025.</p>
<p>A ferramenta gera, de forma automatizada, três documentos institucionais: o Relatório de Diagnóstico por Promotoria de Justiça, o Relatório de Não Conformidades por Município e o Relatório de Diagnóstico por Centro de Apoio Operacional.</p>

<h2>III — Do fundamento</h2>
<p>A medida encontra amparo no art. 130-A, § 2º, da Constituição da República e no art. 155, parágrafo único, da Lei Complementar Estadual nº 0079/2013 (LOMPAP), que atribuem à Corregedoria-Geral a competência para avaliar, orientar e fiscalizar a resolutividade da atuação ministerial, bem como na Carta de Brasília (2016), na Resolução CNMP nº 147/2016, na Recomendação CNMP-CN nº 02/2018 — que exige do membro o conhecimento dos indicadores sociais de sua área e afere a resolutividade material pela melhoria desses indicadores ao longo do tempo — e na Resolução CNMP nº 276/2023, que determina o uso de dados na tomada de decisões, com transparência de origem, data e método.</p>

<h2>IV — Da viabilidade técnica</h2>
<p>O IndicadorMP é uma aplicação estática de arquivo único, com aproximadamente 14 MB, que funciona integralmente no navegador, sem servidor de aplicação, banco de dados, licenças ou dependências externas. Sua publicação não demanda contratação, investimento em infraestrutura ou desenvolvimento adicional, conforme detalhado no Manual Técnico de Implementação que acompanha este requerimento.</p>
<p>Quanto à proteção de dados, o painel utiliza exclusivamente informações públicas ou agregadas, não tratando dados pessoais sensíveis de usuários dos serviços fiscalizados.</p>

<h2>V — Do pedido</h2>
<p>Ante o exposto, requer a Vossa Excelência:</p>
<ol>
<li>o <strong>reconhecimento institucional do IndicadorMP</strong> como ferramenta oficial de apoio à atividade fiscalizatória e à atuação resolutiva no âmbito do Ministério Público do Estado do Amapá;</li>
<li>a <strong>autorização para publicação</strong> do painel em sítio institucional, na modalidade que Vossa Excelência entender adequada — área restrita, para uso interno de membros e servidores, ou área pública, como medida de transparência ativa;</li>
<li>a <strong>designação da Secretaria de Tecnologia da Informação</strong> para a hospedagem, o backup e o monitoramento do serviço, nos termos do manual técnico anexo;</li>
<li>a <strong>comunicação às Promotorias de Justiça e aos Centros de Apoio Operacional</strong> acerca da disponibilização da ferramenta e dos relatórios por ela produzidos;</li>
<li>a fixação de <strong>ciclo periódico de atualização</strong> dos dados, sob responsabilidade da Corregedoria-Geral, de modo a permitir a aferição comparada entre ciclos e a medição da resolutividade material.</li>
</ol>

<p>Nestes termos, pede deferimento.</p>

<p style="margin-top:46px;text-align:center">_____________________________________________<br>
<strong>Anderson Batista de Souza</strong><br>Promotor de Justiça</p>

<h2>Anexos</h2>
<ol>
<li>Apresentação do IndicadorMP;</li>
<li>Justificativa de Implementação;</li>
<li>Manual Técnico de Implementação;</li>
<li>Manual do Usuário;</li>
<li>Relatório-modelo gerado pela ferramenta.</li>
</ol>
"""
print(doc("Requerimento ao Procurador-Geral de Justiça","Institucionalização e publicação do painel IndicadorMP em sítio institucional", corpo, "04_requerimento_pgj.html"))
