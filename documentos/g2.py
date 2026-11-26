# -*- coding: utf-8 -*-
from _base import doc
corpo = """
<h2>1. Objeto</h2>
<p>Este manual descreve os requisitos e o procedimento para publicação do IndicadorMP em sítio institucional do Ministério Público do Estado do Amapá, bem como as rotinas de atualização, versionamento e segurança.</p>

<h2>2. Natureza técnica do produto</h2>
<table><tr><th style="width:32%">Característica</th><th>Descrição</th></tr>
<tr><td>Tipo</td><td>Aplicação estática de página única (<em>single-file HTML</em>). Não há back-end, banco de dados nem processamento no servidor.</td></tr>
<tr><td>Arquivo</td><td><code>indicadormp.html</code> — aproximadamente 14 MB, com HTML, CSS, JavaScript e dados embarcados.</td></tr>
<tr><td>Dependências externas</td><td>Nenhuma. Sem CDN, sem fontes remotas, sem chamadas de rede. Os gráficos são desenhados em CSS puro.</td></tr>
<tr><td>Execução</td><td>Integralmente no navegador do usuário. Nenhum dado é transmitido a terceiros.</td></tr>
<tr><td>Compatibilidade</td><td>Navegadores baseados em Chromium (Chrome, Edge), Firefox e Safari, em versões dos últimos três anos. Responsivo para tablet; a leitura em celular é possível, mas os quadros extensos exigem rolagem horizontal.</td></tr>
<tr><td>Impressão</td><td>Geração de PDF pelo próprio navegador, com folha A4, cabeçalho e rodapé corridos e nome de arquivo sugerido.</td></tr>
</table>

<h2>3. Requisitos de hospedagem</h2>
<ul>
<li>Servidor web capaz de servir arquivos estáticos (Apache, Nginx, IIS) ou serviço de hospedagem estática já contratado pela instituição.</li>
<li>Espaço em disco: 20 MB por versão publicada.</li>
<li>Transferência: cada acesso baixa o arquivo integral (~14 MB). Recomenda-se compressão <code>gzip</code> ou <code>brotli</code>, que reduz a transferência para cerca de 2 a 3 MB.</li>
<li>Não são necessários PHP, Node.js, banco de dados, agendadores ou certificados adicionais além do TLS já usado pelo portal.</li>
</ul>

<h3>3.1 Configuração recomendada (Nginx)</h3>
<p>Exemplo de bloco de configuração, a ser adaptado pela equipe de TI:</p>
<table><tr><th>Diretiva</th><th>Valor sugerido</th></tr>
<tr><td>gzip / brotli</td><td>habilitado para <code>text/html</code></td></tr>
<tr><td>Cache-Control</td><td><code>public, max-age=3600</code> — permite atualização no mesmo dia</td></tr>
<tr><td>Content-Security-Policy</td><td><code>default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'</code></td></tr>
<tr><td>X-Content-Type-Options</td><td><code>nosniff</code></td></tr>
</table>
<div class="nota">O painel usa estilos e scripts embutidos no próprio arquivo; por isso a política de segurança precisa admitir <code>'unsafe-inline'</code> para <em>style</em> e <em>script</em>, restrita à própria origem. Não há carregamento de recurso externo, o que mantém a superfície de exposição mínima.</div>

<h2>4. Formas de publicação</h2>
<table><tr><th style="width:26%">Modalidade</th><th>Quando usar</th><th>Observações</th></tr>
<tr><td>Área pública do portal</td><td>Transparência ativa e acesso do cidadão</td><td>Exige revisão prévia do conteúdo publicado; recomenda-se publicar a versão sem dados de identificação de membros.</td></tr>
<tr><td>Área restrita (intranet)</td><td>Uso interno por membros e servidores</td><td>Modalidade recomendada para a fase inicial, com autenticação pelo diretório institucional.</td></tr>
<tr><td>Distribuição por arquivo</td><td>Contingência e trabalho em campo</td><td>O mesmo arquivo funciona offline, sem qualquer perda de função.</td></tr>
</table>

<h2>5. Rotina de atualização</h2>
<ol>
<li>Exportação dos dados de inspeção do sistema do CNMP e das bases oficiais (IBGE, INEP, MDS, DataSUS, DataJud, PNTP), conforme calendário da aba Documentação.</li>
<li>Atualização do arquivo-fonte e execução do gerador de estilo (<code>gerar_visual.py</code>), que produz a versão final publicável.</li>
<li>Validação: conferência de sintaxe dos scripts, verificação da integridade dos painéis e geração de um relatório-teste por comarca.</li>
<li>Publicação com nome versionado (por exemplo <code>indicadormp_2026-1.html</code>) e atualização do apontador estável (<code>indicadormp.html</code>).</li>
<li>Registro da versão no histórico, com data-base de cada fonte.</li>
</ol>

<h2>6. Governança de dados e LGPD</h2>
<ul>
<li>O painel utiliza <strong>dados públicos ou agregados</strong>: resultados de inspeções institucionais, microdados públicos do INEP e do Censo SUAS, estatísticas do IBGE, DataSUS e MDS e índices do Radar da Transparência.</li>
<li>Não há dados pessoais de usuários dos serviços, prontuários, nomes de crianças, adolescentes ou pessoas atendidas.</li>
<li>Constam nomes de agentes públicos apenas quando a base de origem os registra na condição de responsáveis institucionais, hipótese de tratamento amparada no cumprimento de obrigação legal e no exercício regular de competência (art. 7º, II e III, da Lei nº 13.709/2018).</li>
<li>Cada indicador exibe fonte e ano-base, atendendo à exigência de transparência de origem, data e método da Resolução CNMP nº 276/2023.</li>
</ul>

<h2>7. Acessibilidade e preservação</h2>
<ul>
<li>Estrutura semântica de títulos, contraste adequado entre texto e fundo e navegação por teclado nos controles.</li>
<li>Todo o conteúdo é texto — não há imagem com informação exclusiva —, o que favorece leitores de tela e a indexação.</li>
<li>Por ser arquivo único e autônomo, o painel é naturalmente arquivável: cada versão publicada permanece legível no futuro sem dependência de infraestrutura.</li>
</ul>

<h2>8. Suporte e responsabilidades</h2>
<table><tr><th style="width:34%">Atribuição</th><th>Responsável sugerido</th></tr>
<tr><td>Conteúdo, metodologia e atualização dos dados</td><td>Corregedoria-Geral</td></tr>
<tr><td>Publicação, backup e monitoramento do serviço</td><td>Secretaria de Tecnologia da Informação</td></tr>
<tr><td>Revisão de transparência ativa e acessibilidade</td><td>Assessoria de Comunicação e Ouvidoria</td></tr>
</table>
"""
print(doc("Manual Técnico de Implementação","Requisitos, publicação em sítio institucional, atualização e governança", corpo, "02_manual_tecnico.html"))
