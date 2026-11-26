# -*- coding: utf-8 -*-
"""Atualiza a aba 'Acervo Judicial - DataJud' do IndicadorMP com dados frescos da API do CNJ.

Uso:  python3 atualizar_datajud.py
Faz tudo sozinho: consulta a API pública do DataJud (TJAP) e reconstrói a seção do painel
diretamente em indicadormp.html.

Em 14/08/2026 o alvo passou de dashboard_la_psc_amapa_32.html para indicadormp.html, que
virou a fonte de verdade; a etapa de regeneração pelo gerar_visual.py foi removida, porque
reescreveria o painel a partir da base antiga e apagaria as alterações feitas desde então.
A chave pública abaixo é a divulgada pelo CNJ em datajud-wiki.cnj.jus.br; se o CNJ trocá-la,
substitua o valor de KEY pela nova chave da wiki.
"""
import urllib.request, json, re, time, os, datetime, subprocess, sys

PASTA = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(PASTA, 'indicadormp.html')
KEY = 'cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=='
URL = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjap/_search'
HOJE = datetime.date.today()
HOJE_BR = HOJE.strftime('%d/%m/%Y')
PROX = (HOJE + datetime.timedelta(days=92)).isoformat()

def q(body):
    for tent in range(6):
        try:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                headers={'Authorization': 'APIKey ' + KEY, 'Content-Type': 'application/json'})
            return json.loads(urllib.request.urlopen(req, timeout=120).read())
        except Exception:
            if tent == 5: raise
            time.sleep(6 * (tent + 1))

def count(query):
    return q({"size": 0, "track_total_hits": True, "query": query})['hits']['total']['value']

COMARCAS = ['Macapá', 'Santana', 'Laranjal do Jari', 'Oiapoque', 'Mazagão', 'Porto Grande',
            'Tartarugalzinho', 'Pedra Branca do Amapari', 'Calçoene', 'Comarca de Amapá',
            'Ferreira Gomes', 'Vitória do Jari']

print('Consultando a API do DataJud (CNJ)...')
DJ = {'comarcas': {}}
for c in COMARCAS:
    base = {"match_phrase": {"orgaoJulgador.nome": c}}
    nome = c.replace('Comarca de ', '')
    DJ['comarcas'][nome] = {
        'total': count(base),
        'acp': count({"bool": {"must": [base, {"term": {"classe.nome.keyword": "Ação Civil Pública"}}]}}),
        'improbidade': count({"bool": {"must": [base, {"term": {"classe.nome.keyword": "Ação Civil de Improbidade Administrativa"}}]}}),
        'viol_dom': count({"bool": {"must": [base, {"match_phrase": {"assuntos.nome": "Violência Doméstica"}}]}}),
        'trafico': count({"bool": {"must": [base, {"match_phrase": {"assuntos.nome": "Tráfico de Drogas"}}]}}),
        'penal': count({"bool": {"must": [base, {"term": {"classe.nome.keyword": "Ação Penal - Procedimento Ordinário"}}]}}),
    }
    print(' ', nome, DJ['comarcas'][nome]['total'], 'processos')
    time.sleep(0.2)
DJ['tjap_total'] = count({"match_all": {}})
DJ['tjap_acp'] = count({"term": {"classe.nome.keyword": "Ação Civil Pública"}})
DJ['tjap_improb'] = count({"term": {"classe.nome.keyword": "Ação Civil de Improbidade Administrativa"}})
DJ['tjap_infancia'] = count({"match_phrase": {"orgaoJulgador.nome": "Infância e da Juventude"}})
_SEM_BAIXA = [{"match_phrase": {"movimentos.nome": "Definitivo"}}, {"match_phrase": {"movimentos.nome": "Baixa Definitiva"}}]
def _tram(graus):
    return count({"bool": {"must": [{"terms": {"grau.keyword": graus}}], "must_not": _SEM_BAIXA}})
DJ['tram_g1'] = _tram(['G1', 'JE'])
DJ['tram_g2'] = _tram(['G2', 'TR'])
print('em tramitação 1º grau:', DJ['tram_g1'], '· 2º grau:', DJ['tram_g2'])
_agg = q({"size": 0, "aggs": {"ult": {"max": {"field": "dataHoraUltimaAtualizacao"}}}})
_ms = _agg['aggregations']['ult']['value']
DJ['tjap_ult_atualizacao'] = datetime.datetime.utcfromtimestamp(_ms / 1000).strftime('%d/%m/%Y') if _ms else '-'
json.dump(DJ, open('/tmp/datajud_ap.json', 'w'), ensure_ascii=False)
print('TJAP total:', DJ['tjap_total'])

# ---------- reconstruir a seção do painel ----------
def fi(n): return f'{int(n):,}'.replace(',', '.')

TH = 'style="text-align:left; padding:8px 10px; border-bottom:2px solid rgba(13,36,54,0.18); font-size:10px; text-transform:uppercase; letter-spacing:0.5px; color:#5a7080;"'
THR = TH[:-1] + ' text-align:right;"'
TD = 'style="padding:8px 10px; border-bottom:1px solid rgba(13,36,54,0.08); font-size:12px; color:#33475b;"'
TDN = TD[:-1] + ' text-align:right; font-weight:700; color:#0d2436;"'

def tabela(rows):
    h = '<table class="man-table" style="table-layout:fixed; margin-top:8px;"><thead><tr>'
    for i, c in enumerate(rows[0]):
        h += f'<th{"" if i == 0 else " class=\"num\""}>{c}</th>'
    h += '</tr></thead><tbody>'
    for r in rows[1:]:
        h += '<tr>' + ''.join(f'<td{"" if i==0 else " class=\"num\""}>{c}</td>' for i, c in enumerate(r)) + '</tr>'
    return h + '</tbody></table>'

ICONES = ['<path d="M12 3v18"/><path d="M5 7h14"/><path d="M5 7l-2 5a3 3 0 0 0 6 0l-2-5"/><path d="M19 7l-2 5a3 3 0 0 0 6 0l-2-5"/><path d="M8 21h8"/>',
          '<path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/>',
          '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>']
_ic = {'n': -1}
def card(titulo, sub, corpo, aberto=False):
    _ic['n'] += 1
    ico = ICONES[_ic['n'] % len(ICONES)]
    return (f'<div class="ibge-card{" ibge-aberto" if aberto else ""}">'
            f'<div class="ibge-head" role="button" tabindex="0">'
            f'<span class="ibge-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">{ico}</svg></span>'
            f'<div class="ibge-tit">{titulo}</div><span class="ibge-chev">&#9662;</span></div>'
            f'<div class="ibge-body">'
            + (f'<div class="card-sub" style="margin-top:2px;">{sub}</div>' if sub else '') + corpo + '</div></div>')

def _cor_kpi(rotulo):
    rl = rotulo.lower()
    if re.search(r'há 5\+|revogad|improbidade|vencid', rl): return '#b8323b'
    if re.search(r'cumprid|homolog|em dia', rl): return '#2e7d4f'
    if re.search(r'em tramitação', rl): return '#a97600'
    return '#0d47a1'
def kpis(pares):
    h = '<div class="stat-grid">'
    for v, r in pares:
        h += (f'<div class="stat-card"><div class="eyebrow">{r}</div>'
              f'<div class="big" style="color:{_cor_kpi(r)};">{v}</div></div>')
    return h + '</div>'

CARDS = card('Vis&atilde;o geral do TJAP', f'Base p&uacute;blica DataJud (CNJ) &middot; metadados de todos os processos do TJAP &middot; consulta em {HOJE_BR}',
    kpis([(fi(DJ['tjap_total']), 'processos na base do TJAP'),
          (fi(DJ['tjap_acp']), 'Ações Civis Públicas'),
          (fi(DJ['tjap_improb']), 'ações de improbidade administrativa'),
          (fi(DJ['tjap_infancia']), 'processos na Justiça da Infância e Juventude'),
          (fi(DJ['tram_g1']), 'em tramitação no 1º grau (varas e juizados)'),
          (fi(DJ['tram_g2']), 'em tramitação no 2º grau (Tribunal e Turmas)'),
          ('12', 'comarcas com recorte no painel'),
          ('mensal', 'atualização da base pelo tribunal'),
          (DJ['tjap_ult_atualizacao'], 'última carga do TJAP na base'),
          (HOJE_BR, 'data desta consulta')]), aberto=True)

rows = [['Comarca', 'Processos', 'ACP', 'Improbidade', 'Ação penal', 'Violência doméstica', 'Tráfico']]
tot = {'total': 0, 'acp': 0, 'improbidade': 0, 'penal': 0, 'viol_dom': 0, 'trafico': 0}
for nome, e in sorted(DJ['comarcas'].items(), key=lambda x: -x[1]['total']):
    for k in tot: tot[k] += e[k]
    rows.append([nome, fi(e['total']), fi(e['acp']), fi(e['improbidade']), fi(e['penal']), fi(e['viol_dom']), fi(e['trafico'])])
rows.append(['<b>Total (12 comarcas)</b>'] + [f"<b>{fi(tot[k])}</b>" for k in ['total', 'acp', 'improbidade', 'penal', 'viol_dom', 'trafico']])

CARDS += card('Acervo por comarca', 'Processos cujo &oacute;rg&atilde;o julgador cont&eacute;m o nome da comarca &middot; ACP e improbidade pela classe processual CNJ &middot; viol&ecirc;ncia dom&eacute;stica e tr&aacute;fico pelo assunto declarado', tabela(rows))

# ---------- acervo por classe processual ----------
print('Agregando classes processuais...')
_agg_tot = q({"size": 0, "aggs": {"cls": {"terms": {"field": "classe.nome.keyword", "size": 22}}}})
_SEM_BAIXA2 = [{"match_phrase": {"movimentos.nome": "Definitivo"}}, {"match_phrase": {"movimentos.nome": "Baixa Definitiva"}}]
_agg_trm = q({"size": 0, "query": {"bool": {"must_not": _SEM_BAIXA2}},
              "aggs": {"cls": {"terms": {"field": "classe.nome.keyword", "size": 60}}}})
_trm = {b['key']: b['doc_count'] for b in _agg_trm['aggregations']['cls']['buckets']}
rows_c = [['Classe processual', 'Total na base', 'Em tramitação', '% do acervo vivo']]
for b in _agg_tot['aggregations']['cls']['buckets']:
    t = b['doc_count']; v = _trm.get(b['key'], 0)
    rows_c.append([b['key'], fi(t), fi(v), f"{(v / t * 100):.0f}%" if t else '-'])
CARDS += card('Acervo por classe processual (TJAP)',
    'As 22 classes mais numerosas da base, com o recorte do acervo vivo (sem baixa ou arquivamento definitivo) &middot; taxonomia processual unificada do CNJ',
    '<div style="overflow-x:auto;">' + tabela(rows_c) + '</div>'
    + '<div class="card-sub" style="margin-top:10px;">Leitura: % alto de acervo vivo indica classe de tramita&ccedil;&atilde;o longa (execu&ccedil;&otilde;es, precat&oacute;rios) ou de entrada recente; % baixo, classe de resolu&ccedil;&atilde;o r&aacute;pida ou registro hist&oacute;rico.</div>')


# ---------- consultas por categoria: coleta integral com paginação ----------
def _fmt_num(n):
    n = str(n).zfill(20)
    return f"{n[:7]}-{n[7:9]}.{n[9:13]}.{n[13]}.{n[14:16]}.{n[16:]}"
def _fmt_dt(a):
    a = str(a)
    return f"{a[6:8]}/{a[4:6]}/{a[:4]}" if len(a) >= 8 else '-'
_COM_MAP = ['Macapá', 'Santana', 'Laranjal do Jari', 'Oiapoque', 'Mazagão', 'Porto Grande',
            'Tartarugalzinho', 'Amapari', 'Calçoene', 'Ferreira Gomes', 'Vitória do Jari', 'Amapá']
def _comarca(vara, grau):
    if grau != 'G1': return '2º grau / Tribunal'
    vu = vara.upper()
    for c in _COM_MAP:
        if c.upper() in vu: return 'Pedra Branca do Amapari' if c == 'Amapari' else c
    return 'Outras/estadual'
def _desfecho(movs):
    txt = ' | '.join(m.get('nome', '') or '' for m in movs)
    if 'Procedência em Parte' in txt or 'Parcial Procedência' in txt or 'Procedente em Parte' in txt: return 'Parcialmente procedente'
    if 'Improcedência' in txt or 'Improcedente' in txt: return 'Improcedente'
    if 'Procedência' in txt or 'Procedente' in txt: return 'Procedente'
    if 'Condena' in txt: return 'Condenação'
    if 'Absolvi' in txt: return 'Absolvição'
    if 'Homologa' in txt: return 'Acordo/homologação'
    if 'Extinção da Punibilidade' in txt: return 'Extinção da punibilidade'
    if 'Extinção' in txt: return 'Extinção sem mérito'
    return '-'

def _sit(movs):
    nomes = [m.get('nome', '') or '' for m in movs]
    txt = ' | '.join(nomes)
    if 'Baixa Definitiva' in txt or 'Arquivamento Definitivo' in txt or any(n.strip() == 'Definitivo' for n in nomes): return 'Baixado/Arquivado'
    for kw in ['Procedência', 'Improcedência', 'Extinção', 'Homologa', 'Julgamento', 'Procedente', 'Improcedente', 'Condena', 'Absolvi']:
        if kw in txt: return 'Julgado'
    return 'Em tramitação'

def colher(query, rotulo, des_fn=None):
    print(f'Coletando {rotulo} (paginação)...')
    body = {"size": 1000, "query": query, "sort": [{"@timestamp": "asc"}],
            "_source": ["numeroProcesso", "dataAjuizamento", "grau", "nivelSigilo",
                        "orgaoJulgador.nome", "assuntos.nome", "movimentos.nome", "movimentos.dataHora"]}
    docs = []; after = None
    while True:
        b = dict(body)
        if after: b['search_after'] = after
        h = q(b)['hits']['hits']
        if not h: break
        docs += h; after = h[-1]['sort']
        print(f'  {rotulo}: {len(docs)}...', flush=True)
        if len(h) < 1000: break
        time.sleep(0.2)
    regs = []
    for dcc in docs:
        src = dcc['_source']
        movs = src.get('movimentos', []) or []
        movs_dt = [m for m in movs if m.get('dataHora')]
        ult = max(movs_dt, key=lambda m: m['dataHora']) if movs_dt else {}
        aju = str(src.get('dataAjuizamento', ''))
        try:
            idade = round((HOJE - datetime.date(int(aju[:4]), int(aju[4:6]), int(aju[6:8]))).days / 365.25, 1)
        except Exception:
            idade = None
        vara = (src.get('orgaoJulgador') or {}).get('nome', '-')
        regs.append({'n': _fmt_num(src.get('numeroProcesso', '')), 'vara': vara,
                     'com': _comarca(vara, src.get('grau', 'G1')),
                     'dt': _fmt_dt(aju), 'ano': aju[:4] if len(aju) >= 4 else '-', 'idade': idade,
                     'sig': (src.get('nivelSigilo') or 0) > 0,
                     'ass': '; '.join(a.get('nome', '') for a in (src.get('assuntos') or []) if a.get('nome')) or '-',
                     'sit': _sit(movs), 'des': (des_fn or _desfecho)(movs), 'um': (ult.get('nome') or '-'), 'umd': (ult.get('dataHora') or '')[:10]})
    regs.sort(key=lambda x: (x['com'], -(x['idade'] or 0)))
    return regs

LIMITE_EMBED = 6000
def card_consulta(pfx, titulo, regs):
    total = len(regs)
    n_tram = sum(1 for x in regs if x['sit'] == 'Em tramitação')
    n_julg = sum(1 for x in regs if x['sit'] == 'Julgado')
    n_baix = sum(1 for x in regs if x['sit'] == 'Baixado/Arquivado')
    idosas = sum(1 for x in regs if x['sit'] == 'Em tramitação' and (x['idade'] or 0) >= 5)
    idades = [x['idade'] for x in regs if x['idade'] is not None]
    id_med = round(sum(idades) / len(idades), 1) if idades else 0
    nota = ''
    if total > LIMITE_EMBED:
        tram = [x for x in regs if x['sit'] == 'Em tramitação']
        resto = [x for x in regs if x['sit'] != 'Em tramitação'][:max(0, LIMITE_EMBED - len(tram))]
        regs = sorted(tram + resto, key=lambda x: (x['com'], -(x['idade'] or 0)))[:LIMITE_EMBED]
        nota = (f' Pelo volume, a listagem embutida prioriza o acervo <b>em tramita&ccedil;&atilde;o</b> '
                f'({len(regs)} de {total} processos); os KPIs consideram o total.')
    dados_json = json.dumps(regs, ensure_ascii=False)
    return card(titulo + ' - consulta', '', f"""
<div class="card-sub" style="margin-top:2px;">Situa&ccedil;&atilde;o inferida dos movimentos (Baixado = baixa/arquivamento definitivo; Julgado = julgamento/extin&ccedil;&atilde;o/condena&ccedil;&atilde;o; demais = em tramita&ccedil;&atilde;o). Consulta de {HOJE_BR}.{nota}</div>
{kpis([(fi(total), 'processos na base'), (fi(n_tram), 'em tramitação'), (fi(n_julg), 'julgados'), (fi(n_baix), 'baixados/arquivados'), (fi(idosas), 'em tramitação há 5+ anos'), (str(id_med).replace('.', ','), 'anos de idade média')])}
<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:10px; margin-top:14px;">
  <div><label style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:#5a7080; display:block; margin-bottom:4px;">Comarca</label><select id="{pfx}-com" style="width:100%; padding:8px 10px; border-radius:9px; border:1px solid rgba(0,40,80,0.15); font:inherit; font-size:12px; background:#fff;"><option value="">Todas</option></select></div>
  <div><label style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:#5a7080; display:block; margin-bottom:4px;">Situa&ccedil;&atilde;o</label><select id="{pfx}-sit" style="width:100%; padding:8px 10px; border-radius:9px; border:1px solid rgba(0,40,80,0.15); font:inherit; font-size:12px; background:#fff;"><option value="">Todas</option><option>Em tramitação</option><option>Julgado</option><option>Baixado/Arquivado</option></select></div>
  <div><label style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:#5a7080; display:block; margin-bottom:4px;">Desfecho</label><select id="{pfx}-des" style="width:100%; padding:8px 10px; border-radius:9px; border:1px solid rgba(0,40,80,0.15); font:inherit; font-size:12px; background:#fff;"><option value="">Todos</option></select></div>
  <div><label style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:#5a7080; display:block; margin-bottom:4px;">Ano de ajuizamento</label><select id="{pfx}-ano" style="width:100%; padding:8px 10px; border-radius:9px; border:1px solid rgba(0,40,80,0.15); font:inherit; font-size:12px; background:#fff;"><option value="">Todos</option></select></div>
  <div><label style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:#5a7080; display:block; margin-bottom:4px;">Buscar (n&uacute;mero, vara ou assunto)</label><input id="{pfx}-busca" type="text" placeholder="digite para filtrar" style="width:100%; padding:8px 10px; border-radius:9px; border:1px solid rgba(0,40,80,0.15); font:inherit; font-size:12px; background:#fff;"></div>
</div>
<div id="{pfx}-resumo" style="margin-top:10px; font-size:11.5px; color:#5a7080;"></div>
<div style="overflow-x:auto;"><table class="man-table" style="margin-top:6px; min-width:1060px;"><thead><tr>
<th>Processo</th><th>Comarca</th><th>Vara</th><th class="num">Ajuizamento</th><th class="num">Idade (anos)</th><th>Assunto</th><th>Situa&ccedil;&atilde;o</th><th>Desfecho</th><th>&Uacute;ltimo movimento</th><th class="num">Data &uacute;lt. mov.</th></tr></thead>
<tbody id="{pfx}-corpo"></tbody></table></div>
<script type="application/json" id="{pfx}-dados">{dados_json}</script>
<script>
(function(){{
  var TD='{TD}'.replace('style="','').replace('"','');
  var dados=JSON.parse(document.getElementById('{pfx}-dados').textContent);
  var selCom=document.getElementById('{pfx}-com'), selSit=document.getElementById('{pfx}-sit'),
      selAno=document.getElementById('{pfx}-ano'), selDes=document.getElementById('{pfx}-des'), busca=document.getElementById('{pfx}-busca'),
      corpo=document.getElementById('{pfx}-corpo'), resumo=document.getElementById('{pfx}-resumo');
  Array.from(new Set(dados.map(function(x){{return x.com;}})).values()).sort().forEach(function(c){{ var o=document.createElement('option'); o.textContent=c; selCom.appendChild(o); }});
  Array.from(new Set(dados.map(function(x){{return x.ano;}})).values()).sort().reverse().forEach(function(a){{ var o=document.createElement('option'); o.textContent=a; selAno.appendChild(o); }});
  Array.from(new Set(dados.map(function(x){{return x.des;}})).values()).sort().forEach(function(a){{ if(a!=='-'){{ var o=document.createElement('option'); o.textContent=a; selDes.appendChild(o); }} }});
  var CORES={{'Em tramitação':'#a97600','Julgado':'#2e7d4f','Baixado/Arquivado':'#5a7080'}};
  function render(){{
    var qq=(busca.value||'').toLowerCase();
    var f=dados.filter(function(x){{
      return (!selCom.value||x.com===selCom.value)&&(!selSit.value||x.sit===selSit.value)&&(!selAno.value||x.ano===selAno.value)&&(!selDes.value||x.des===selDes.value)
        &&(!qq||(x.n+' '+x.vara+' '+x.ass).toLowerCase().indexOf(qq)>=0);
    }});
    var LIM=300, mostrar=f.slice(0,LIM);
    corpo.innerHTML=mostrar.map(function(x){{
      var c=CORES[x.sit]||'#333';
      return '<tr><td style="font-family:monospace; font-size:11px;">'+x.n+(x.sig?' &#128274;':'')+'</td>'
        +'<td>'+x.com+'</td><td>'+x.vara+'</td>'
        +'<td class="num">'+x.dt+'</td>'
        +'<td class="num">'+(x.idade==null?'-':String(x.idade).replace('.',','))+'</td>'
        +'<td>'+x.ass+'</td>'
        +'<td><span style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.4px; border-radius:6px; padding:3px 8px; background:'+c+'1e; color:'+c+'; white-space:nowrap;">'+x.sit+'</span></td>'
        +'<td>'+(x.des||'-')+'</td>'
        +'<td>'+x.um+'</td><td class="num">'+x.umd+'</td></tr>';
    }}).join('');
    resumo.textContent=f.length+' processo(s) no filtro'+(f.length>LIM?' - exibindo os '+LIM+' mais antigos':'')+' · idade média: '+(f.length?(f.reduce(function(a,x){{return a+(x.idade||0);}},0)/f.length).toFixed(1).replace('.',','):'-')+' anos';
  }}
  [selCom,selSit,selAno,selDes].forEach(function(e){{e.addEventListener('change',render);}});
  busca.addEventListener('input',render);
  render();
}})();
</script>
""")

CATEGORIAS = [
    ('djimp', 'Improbidade administrativa', {"term": {"classe.nome.keyword": "Ação Civil de Improbidade Administrativa"}}),
    ('djacp', 'A&ccedil;&atilde;o Civil P&uacute;blica', {"term": {"classe.nome.keyword": "Ação Civil Pública"}}),
    ('djvd', 'Viol&ecirc;ncia dom&eacute;stica (assunto)', {"match_phrase": {"assuntos.nome": "Violência Doméstica"}}),
    ('djtraf', 'Tr&aacute;fico de drogas (assunto)', {"match_phrase": {"assuntos.nome": "Tráfico de Drogas"}}),
    ('djpen', 'A&ccedil;&atilde;o penal', {"term": {"classe.nome.keyword": "Ação Penal - Procedimento Ordinário"}}),
]
for _pfx, _tit, _qq in CATEGORIAS:
    CARDS += card_consulta(_pfx, _tit, colher(_qq, _tit))

# ---------- ANPP: card autônomo ----------
def _estagio_anpp(movs):
    txt = ' | '.join(m.get('nome', '') or '' for m in movs)
    if 'Cumprimento de Acordo de Não Persecução Penal' in txt: return 'Cumprido (punibilidade extinta)'
    if 'Revogação do Acordo de Não Persecução Penal' in txt: return 'Revogado'
    if 'Homologação do Acordo de Não Persecução Penal' in txt: return 'Homologado (em cumprimento)'
    return 'Sem homologação registrada'

ANPP_Q = {"match_phrase": {"movimentos.nome": "Acordo de Não Persecução Penal"}}
ANPP = colher(ANPP_Q, 'ANPP', des_fn=_estagio_anpp)
_n_classe = count({"term": {"classe.nome.keyword": "Acordo de Não Persecução Penal"}})
_n_hom = count({"match_phrase": {"movimentos.nome": "Homologação do Acordo de Não Persecução Penal"}})
_n_cum = sum(1 for x in ANPP if x['des'] == 'Cumprido (punibilidade extinta)')
_n_rev = sum(1 for x in ANPP if x['des'] == 'Revogado')
_tx = f"{(_n_cum / _n_hom * 100):.0f}%" if _n_hom else '-'

_agg_com = {}
for x in ANPP:
    e = _agg_com.setdefault(x['com'], {'tot': 0, 'hom': 0, 'cum': 0, 'rev': 0})
    e['tot'] += 1
    if x['des'] != 'Sem homologação registrada': e['hom'] += 1  # acordo firmado (hom., cumpr. ou revog.)
    if x['des'] == 'Cumprido (punibilidade extinta)': e['cum'] += 1
    if x['des'] == 'Revogado': e['rev'] += 1
_rows = [['Comarca', 'Processos c/ ANPP', 'Com acordo firmado', 'Cumpridos', 'Taxa de cumprimento', 'Revogados']]
for nome, e in sorted(_agg_com.items(), key=lambda kv: -kv[1]['tot']):
    tx = f"{(e['cum'] / e['hom'] * 100):.0f}%" if e['hom'] else '-'
    _rows.append([nome, fi(e['tot']), fi(e['hom']), fi(e['cum']), tx, fi(e['rev'])])
_rows.append(['<b>Total</b>', f'<b>{fi(len(ANPP))}</b>', f'<b>{fi(_n_hom)}</b>', f'<b>{fi(_n_cum)}</b>', f'<b>{_tx}</b>', f'<b>{fi(_n_rev)}</b>'])

CARDS += card('ANPP - Acordo de N&atilde;o Persecu&ccedil;&atilde;o Penal (vis&atilde;o por comarca)',
    f'Art. 28-A do CPP &middot; processos com movimento de ANPP na base &middot; est&aacute;gio inferido dos movimentos (homologa&ccedil;&atilde;o, cumprimento com extin&ccedil;&atilde;o da punibilidade, revoga&ccedil;&atilde;o) &middot; consulta de {HOJE_BR}',
    kpis([(fi(len(ANPP)), 'processos com movimento de ANPP'), (fi(_n_classe), 'autuados na classe própria ANPP'),
          (fi(_n_hom), 'acordos homologados'), (fi(_n_cum), 'cumpridos (punibilidade extinta)'),
          (_tx, 'taxa de cumprimento dos homologados'), (fi(_n_rev), 'revogados por descumprimento')])
    + '<div style="overflow-x:auto;">' + tabela(_rows) + '</div>')

CARDS += card_consulta('djanpp', 'ANPP - processos', ANPP)

# ---------- Justiça penal negociada: ANPP x transação x sursis, por comarca ----------
print('Contando instrumentos despenalizadores por comarca...')
INSTR = [
    ('ANPP', {'hom': [{"match_phrase": {"movimentos.nome": "Homologação do Acordo de Não Persecução Penal"}}],
              'cum': [{"match_phrase": {"movimentos.nome": "Cumprimento de Acordo de Não Persecução Penal"}}],
              'rev': [{"match_phrase": {"movimentos.nome": "Revogação do Acordo de Não Persecução Penal"}}]}),
    ('Transação penal', {'hom': [{"match_phrase": {"movimentos.nome": "Homologação de Transação"}}],
              'cum': [{"match_phrase": {"movimentos.nome": "Cumprimento de transação penal"}}],
              'rev': [{"match_phrase": {"movimentos.nome": "Revogação da Transação Penal"}}]}),
    ('Suspensão condicional do processo', {'hom': [{"match_phrase": {"movimentos.nome": "Suspensão Condicional do Processo"}}],
              'cum': [{"match_phrase": {"movimentos.nome": "Cumprimento da suspensão condicional do processo"}}],
              'rev': [{"match_phrase": {"movimentos.nome": "Revogação da Suspensão Condicional do Processo"}}]}),
]
def _cnt(shoulds, extra=None):
    time.sleep(0.4)
    must = [{"bool": {"should": shoulds, "minimum_should_match": 1}}]
    if extra: must.append(extra)
    return count({"bool": {"must": must}})
NEG = {}
for _nome, _mv in INSTR:
    NEG[_nome] = {'estado': {k: _cnt(v) for k, v in _mv.items()}, 'com': {}}
    for _c in COMARCAS:
        _e = {"match_phrase": {"orgaoJulgador.nome": _c}}
        NEG[_nome]['com'][_c.replace('Comarca de ', '')] = {k: _cnt(v, _e) for k, v in _mv.items()}
    print(' ', _nome, NEG[_nome]['estado'])

def _txp(cum, hom): return f"{(cum / hom * 100):.0f}%" if hom else '-'
_kp = []
for _nome, _ in INSTR:
    _e = NEG[_nome]['estado']
    _kp += [(fi(_e['hom']), f"{_nome.lower()}: homologações"), (_txp(_e['cum'], _e['hom']), f"{_nome.lower()}: taxa de cumprimento registrada")]
_rows = [['Comarca', 'ANPP hom.', 'ANPP cumpr.', 'ANPP taxa', 'Transação hom.', 'Transação cumpr.', 'Sursis proc. hom.', 'Sursis cumpr.', 'Sursis taxa']]
_coms = sorted(NEG['ANPP']['com'].keys(), key=lambda c: -NEG['Transação penal']['com'][c]['hom'])
for _c in _coms:
    a = NEG['ANPP']['com'][_c]; t = NEG['Transação penal']['com'][_c]; sp = NEG['Suspensão condicional do processo']['com'][_c]
    _rows.append([_c, fi(a['hom']), fi(a['cum']), _txp(a['cum'], a['hom']),
                  fi(t['hom']), fi(t['cum']), fi(sp['hom']), fi(sp['cum']), _txp(sp['cum'], sp['hom'])])
_ea = NEG['ANPP']['estado']; _et = NEG['Transação penal']['estado']; _es = NEG['Suspensão condicional do processo']['estado']
_rows.append(['<b>Estado (base toda)</b>', f"<b>{fi(_ea['hom'])}</b>", f"<b>{fi(_ea['cum'])}</b>", f"<b>{_txp(_ea['cum'], _ea['hom'])}</b>",
              f"<b>{fi(_et['hom'])}</b>", f"<b>{fi(_et['cum'])}</b>", f"<b>{fi(_es['hom'])}</b>", f"<b>{fi(_es['cum'])}</b>", f"<b>{_txp(_es['cum'], _es['hom'])}</b>"])
CARDS += card('Justi&ccedil;a penal negociada - ANPP, transa&ccedil;&atilde;o penal e suspens&atilde;o condicional (por comarca)',
    f'Os tr&ecirc;s instrumentos despenalizadores lado a lado, pelos movimentos de homologa&ccedil;&atilde;o, cumprimento e revoga&ccedil;&atilde;o &middot; taxas baixas de cumprimento podem refletir falta de registro do movimento pelo TJAP, n&atilde;o descumprimento real &middot; consulta de {HOJE_BR}',
    kpis(_kp) + '<div style="overflow-x:auto;">' + tabela(_rows) + '</div>')

CARDS += card('Sobre a fonte e limita&ccedil;&otilde;es', '',
    '<p style="font-size:12.5px; color:#33475b; line-height:1.7; margin-top:8px;">O <b>DataJud</b> &eacute; a base nacional de metadados processuais do CNJ (Resolu&ccedil;&atilde;o CNJ 331/2020), alimentada mensalmente pelos tribunais. Cada processo traz classe, assuntos, &oacute;rg&atilde;o julgador, datas e movimentos - mas <b>n&atilde;o o conte&uacute;do das pe&ccedil;as</b>. Os n&uacute;meros dependem da qualidade do registro do TJAP: assuntos mal classificados subestimam contagens tem&aacute;ticas; processos sigilosos aparecem com dados reduzidos; e n&atilde;o h&aacute; campo "autor = Minist&eacute;rio P&uacute;blico" - ACP e improbidade s&atilde;o identificadas pela classe processual. Uso recomendado no IndicadorMP: <b>medir o esfor&ccedil;o resolutivo judicializado</b> (quantas ACPs existem onde o diagn&oacute;stico aponta desconformidade) e o perfil criminal de cada comarca.</p>')

MIOLO = f'''
      <div class="eyebrow">CNJ &middot; DataJud &middot; consulta de {HOJE_BR}</div>
      <h1 class="page-title">Acervo Judicial<br><span style="font-size:0.6em; font-weight:600; color:var(--text-dim,#5a7080); letter-spacing:-0.2px;">Metadados processuais do TJAP na base nacional do CNJ (DataJud)</span></h1>
      {CARDS}
    '''

d = open(BASE, encoding='utf-8').read()
ini = d.index('<section class="view" id="view-datajud-dados">') + len('<section class="view" id="view-datajud-dados">')
fim = d.index('</section>', ini)
d = d[:ini] + MIOLO + d[fim:]

# Painel de Alerta: atualizar referência e próxima coleta da linha do DataJud
d = re.sub(r"\{fonte:'Acervo Judicial - DataJud \(CNJ\)'[^}]*\}",
           "{fonte:'Acervo Judicial - DataJud (CNJ)', norma:'Res. CNJ 331/2020 - API pública', rec:'Mensal (alimentação pelos tribunais)', ref:'Consulta de " + HOJE_BR + "', prox:'" + PROX + "'}", d, count=1)
open(BASE, 'w', encoding='utf-8').write(d)
print('Pronto: indicadormp.html atualizado com dados de', HOJE_BR)
