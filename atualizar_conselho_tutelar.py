#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza o painel de Conselhos Tutelares (Rec. CNMP 119/2025) a partir da exportacao
nacional do sistema do CNMP (CSV ';', latin-1, "relatorio.csv").

Uso:
    python3 atualizar_conselho_tutelar.py /caminho/relatorio.csv            # aplica
    python3 atualizar_conselho_tutelar.py /caminho/relatorio.csv --dry-run  # so mostra

O que faz, em indicadormp.html:
  1. template tplRec119Anual: ALL_RESULTS (todas as unidades do pais), objetos E (panorama
     nacional) e D (comparativo Amapa x Brasil) e os textos com contagens;
  2. REL_DATA: substitui os registros de tipo "Conselho Tutelar" (fonte dos relatorios por
     Comarca e por CAO);
  3. Inicio: contador "unidades inspecionadas";
  4. copia o CSV para fontes/conselho tutelar.2026.csv.
Faz backup do painel e da fonte anterior em backups/ antes de gravar.

As 24 regras abaixo foram ajustadas contra o painel original (reproduzem 199 de 201
unidades; as 2 restantes tinham resposta em branco contada como nao conformidade).
Criado em 19/10/2026.
"""
import re, json, csv, io, sys, os, shutil, collections, datetime

BASE=os.path.dirname(os.path.abspath(__file__))
PAINEL=os.path.join(BASE,'indicadormp.html')
FONTE=os.path.join(BASE,'fontes','conselho tutelar.2026.csv')
W={'Alta':3,'Média':2,'Atenção':1}

# id -> (label, severidade, fundamento) - mesma tabela usada pelo painel
IDS={
 "5": [
  "Legislação municipal desatualizada frente aos parâmetros vigentes",
  "Alta",
  "Art. 134, ECA c/c Res. CONANDA 231/2022"
 ],
 "10": [
  "Sem sala reservada para atendimento e recepção ao público",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "14": [
  "Equipamentos/mobiliários insuficientes para o trabalho",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "18": [
  "Relatório trimestral não atende o art. 23, §1º, da Res. 231/2022",
  "Média",
  "Art. 23, §1º, Res. CONANDA 231/2022"
 ],
 "20": [
  "Sem estudo de caso prévio à aplicação de medida de proteção",
  "Média",
  "Art. 100, ECA"
 ],
 "23": [
  "Sem cronograma/plano de formação continuada",
  "Atenção",
  "Res. CONANDA 231/2022"
 ],
 "24": [
  "Não utiliza o SIPIA de forma obrigatória e rotineira",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "4": [
  "Conselheiro(a) reside fora do município de atribuição",
  "Média",
  "Art. 133, III, ECA"
 ],
 "6": [
  "Sem regimento interno",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "8": [
  "Sede em local de difícil acesso à comunidade",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "9": [
  "Sem placa indicativa/identificação externa",
  "Atenção",
  "Res. CONANDA 231/2022"
 ],
 "11": [
  "Condições do imóvel percebidas como inadequadas",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "16": [
  "Escala de plantão/sobreaviso não afixada em local de fácil acesso",
  "Atenção",
  "Res. CONANDA 231/2022"
 ],
 "19": [
  "Sem plano anual de fiscalização das entidades de atendimento",
  "Média",
  "Art. 95, ECA"
 ],
 "21": [
  "Sem reuniões periódicas com a rede de atendimento",
  "Atenção",
  "Res. CONANDA 231/2022"
 ],
 "22": [
  "Conselheiros sem capacitação inicial ao assumir a função",
  "Alta",
  "Res. CONANDA 231/2022"
 ],
 "17": [
  "Sem relatório trimestral ao Ministério Público",
  "Alta",
  "Art. 23, Res. CONANDA 231/2022"
 ],
 "2": [
  "Sem suplentes habilitados a assumir o cargo",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "7": [
  "Regimento interno não publicado ou afixado",
  "Atenção",
  "Res. CONANDA 231/2022"
 ],
 "13": [
  "Sem controle de frequência dos Conselheiros",
  "Atenção",
  "Res. CONANDA 231/2022"
 ],
 "15": [
  "Sem equipe de apoio administrativo",
  "Média",
  "Res. CONANDA 231/2022"
 ],
 "12": [
  "Imóvel sem acessibilidade para pessoas com deficiência",
  "Alta",
  "Lei 13.146/2015 e Res. CONANDA 231/2022"
 ],
 "1": [
  "Menos de 5 Conselheiros Tutelares titulares em exercício",
  "Alta",
  "Art. 132, ECA"
 ],
 "3": [
  "Conselheiros não exercem as funções com exclusividade",
  "Alta",
  "Res. CONANDA 231/2022"
 ]
}

IDS={int(k):v for k,v in IDS.items()}   # chaves numericas

def n_lt5(v):
    try: return int(v)<5
    except Exception: return False
NAO=lambda v: v=='Não'
# id -> (prefixo do titulo da coluna no CSV, condicao que gera o apontamento)
RULES={
 1:('1.13 ', n_lt5), 2:('1.15 ', lambda v: v=='0'), 3:('1.16 ', NAO), 4:('1.17 ', lambda v: v=='Sim'),
 5:('1.21 ', lambda v: v.lower()=='não'), 6:('2.1 ', NAO), 7:('2.4 ', NAO), 8:('3.1 ', NAO), 9:('3.2.1 ', NAO),
 10:('3.2.2 ', NAO), 11:('3.3 ', lambda v: v=='Inadequada'), 12:('3.4 ', NAO), 13:('3.7 ', NAO), 14:('3.9 ', NAO),
 15:('4.1 ', NAO), 16:('5.5 ', NAO), 17:('5.18.2 ', NAO), 18:('5.19 ', NAO), 19:('6.1 ', NAO), 20:('6.4 ', NAO),
 21:('6.5 ', NAO), 22:('7.1 ', NAO), 23:('7.4 ', NAO), 24:('8.1 ', NAO),
}

def parse(p):
    txt=open(p,'rb').read().decode('latin-1').replace('\r\n','\n').replace('\r','\n'); lines=txt.split('\n')
    h=next(csv.reader([lines[0]], delimiter=';')); recs=[]; cur=[]
    for ln in lines[1:]:
        if re.match(r'^\d+;', ln) and cur: recs.append('\n'.join(cur)); cur=[]
        cur.append(ln)
    if cur and cur[0].strip(): recs.append('\n'.join(cur))
    rows=[]
    for r in recs:
        try: f=next(csv.reader(io.StringIO(r, newline=''), delimiter=';'))
        except Exception: f=r.split(';')
        rows.append([x.strip() for x in f]+['']*(len(h)-len(f)))
    return h, rows
def col(h, prefix):
    for k,c in enumerate(h):
        if c.strip().startswith(prefix): return k
    raise KeyError('coluna nao encontrada: '+prefix)

def nome_fix(r):
    n=r[1].strip().rstrip('/').strip()
    if r[0]=='96585': n='Conselho Tutelar do Município de Mazagão'   # exportacao traz so "MUNICÍPIO DE MAZAGÃO"
    return n
def mun_fix(r):
    m=r[3].strip()
    if r[4].strip()=='Amapá' and m=='Amapá' and 'MACAP' in r[1].upper(): m='Macapá'   # 3 conselhos de Macapa cadastrados com municipio "Amapa"
    return m

def main():
    if len(sys.argv)<2: print(__doc__); sys.exit(1)
    csvp=sys.argv[1]; dry='--dry-run' in sys.argv
    d=open(PAINEL,encoding='utf-8').read()
    COMARCAS=json.loads(re.search(r'COMARCAS = (\{.*?\})', d).group(1)); MUN2COM={m:c for c,ms in COMARCAS.items() for m in ms}
    h,R=parse(csvp)
    R=[r for r in R if r[2].strip()=='Conselhos Tutelares' and re.match(r'\d\d/\d\d/\d{4}', r[6])]
    R.sort(key=lambda r:int(r[0]))
    cols={k:col(h,p) for k,(p,_) in RULES.items()}
    ALL=[]
    for r in R:
        flags=[k for k,(p,fn) in sorted(RULES.items()) if fn(r[cols[k]])]
        desc=[{'id':k,'label':IDS[k][0],'base':IDS[k][2],'sev':IDS[k][1]} for k in flags]
        ALL.append({'ciclo':'2026','id':r[0],'nome':nome_fix(r),'municipio':mun_fix(r),'uf':r[4].strip(),'regiao':r[5].strip(),'data_visita':r[6].strip(),'visitado_por':r[7].strip(),'score':sum(W[x['sev']] for x in desc),'n_desconf':len(desc),'desconformidades':desc})
    AP=[e for e in ALL if e['uf']=='Amapá']
    for e in AP:
        if e['municipio'] not in MUN2COM: raise SystemExit('municipio sem comarca: '+e['municipio'])
    L=sorted({v[0] for v in IDS.values()}); Lsev={v[0]:v[1] for v in IDS.values()}; LI={l:i for i,l in enumerate(L)}
    U=[{'n':e['nome'],'m':e['municipio'],'uf':e['uf'],'r':e['regiao'],'s':e['score'],'d':e['n_desconf'],'a':sum(1 for x in e['desconformidades'] if x['sev']=='Alta'),'me':sum(1 for x in e['desconformidades'] if x['sev']=='Média'),'at':sum(1 for x in e['desconformidades'] if x['sev']=='Atenção'),'i':[LI[x['label']] for x in e['desconformidades']]} for e in ALL]
    cnt=collections.Counter(x['label'] for e in ALL for x in e['desconformidades']); ufc=collections.Counter(e['uf'] for e in ALL)
    nac={'tot':str(len(ALL)),'alta':str(sum(1 for e in ALL for x in e['desconformidades'] if x['sev']=='Alta')),'score':'%.1f'%(sum(e['score'] for e in ALL)/len(ALL)),'top':None,'apsc':'%.1f'%(sum(e['score'] for e in AP)/max(1,len(AP))),
         'uf':{'labels':[u for u,_ in ufc.most_common(15)],'data':[c for _,c in ufc.most_common(15)]},'nc':{'labels':[l[:38] for l,_ in cnt.most_common(10)],'data':[c for _,c in cnt.most_common(10)]}}
    i=d.find('<template id="tplRec119Anual">'); j=d.find('</template>',i); t=d[i:j]
    E_old=json.loads(re.search(r'var E=(\{.*?\});\s*\n', t, re.S).group(1))
    E={'tid':E_old['tid'],'suf':E_old['suf'],'modo':E_old['modo'],'rot':E_old['rot'],'U':U,'L':L,'S':[Lsev[l] for l in L],'nac':nac}
    apc=collections.Counter(x['label'] for e in AP for x in e['desconformidades'])
    comp=sorted([{'l':l,'sev':Lsev[l],'ap':apc[l],'apP':round(100*apc[l]/len(AP)),'br':cnt[l],'brP':round(100*cnt[l]/len(ALL))} for l in apc], key=lambda x:(-x['ap'],-x['br']))
    D={'un':[{'n':e['nome'],'m':e['municipio'],'s':e['score'],'nc':[{'l':x['label'],'sev':x['sev']} for x in e['desconformidades']]} for e in AP],'comp':comp,'nac':len(ALL)}
    def sub1(pat, repl, s, flags=0):
        s2,n=re.subn(pat, repl, s, count=1, flags=flags)
        if n!=1: raise SystemExit('padrao nao encontrado: '+pat[:60])
        return s2
    t=sub1(r'ALL_RESULTS\s*=\s*\[.*?\];', lambda m:'ALL_RESULTS='+json.dumps(ALL,ensure_ascii=False)+';', t, re.S)
    t=sub1(r'var E=\{.*?\};\s*\n', lambda m:'var E='+json.dumps(E,ensure_ascii=False)+';\n', t, re.S)
    t=sub1(r'var D=\{.*?\};', lambda m:'var D='+json.dumps(D,ensure_ascii=False)+';', t, re.S)
    NT=len(ALL); NUF=len(ufc); topl,topc=cnt.most_common(1)[0]; muns=sorted({e['municipio'] for e in AP}); ncAP=sum(e['n_desconf'] for e in AP); itens=len(AP)*len(IDS)
    t=sub1(r'Cobertura e distribuição dos \d+ Conselhos Tutelares inspecionados', 'Cobertura e distribuição dos %d Conselhos Tutelares inspecionados'%NT, t)
    t=sub1(r'(TOTAL DE CONSELHOS</div><div class="big">)\d+', lambda m:m.group(1)+str(NT), t)
    t=sub1(r'(ITENS DE SEVERIDADE ALTA</div><div class="big">)\d+(</div><div class="sub">somados entre os )\d+', lambda m:m.group(1)+nac['alta']+m.group(2)+str(NT), t)
    t=sub1(r'(DESCONFORMIDADE MAIS FREQUENTE</div><div class="big" style="font-size:15px;">)[^<]*(</div><div class="sub">)\d+ Conselhos \(\d+%\)', lambda m:m.group(1)+topl[:48]+m.group(2)+'%d Conselhos (%d%%)'%(topc,round(100*topc/NT)), t)
    t=sub1(r'(CONSELHOS INSPECIONADOS</div><div class="big">)\d+ <span[^>]*>[^<]*</span></div><div class="sub">[^<]*</div>', lambda m:m.group(1)+'%d <span style="font-size:0.55em; font-weight:700; color:#5a7080;">em %d municípios</span></div><div class="sub">%s · Macapá com três conselhos (zonas Sul, Norte e Oeste)</div>'%(len(AP),len(muns),', '.join(muns)), t)
    t=sub1(r'(NÃO CONFORMIDADES</div><div class="big" style="color:#c03030;">)\d+(</div><div class="sub">de )\d+( itens verificados em )\d+( unidades</div></div><div class="stat-card"><div class="eyebrow">CONFORMIDADES</div><div class="big">)\d+(</div><div class="sub">)[\d,]+(% dos itens verificados)', lambda m:m.group(1)+str(ncAP)+m.group(2)+str(itens)+m.group(3)+str(len(AP))+m.group(4)+str(itens-ncAP)+m.group(5)+('%.1f'%(100*(itens-ncAP)/itens)).replace('.',',')+m.group(6), t)
    t=sub1(r'\d+ unidades inspecionadas em \d+ UFs', '%d unidades inspecionadas em %d UFs'%(NT,NUF), t)
    d=d[:i]+t+d[j:]
    s=d.find('const REL_DATA = window.REL_DATA = '); e=d.find('];', s)+1; REL=json.loads(d[s+len('const REL_DATA = window.REL_DATA = '):e])
    REL_CT=[{'comarca':MUN2COM[x['municipio']],'municipio':x['municipio'],'tipo':'Conselho Tutelar','res':'Rec. CNMP 119/2025','id':x['id'],'painel':'119','nome':x['nome'],'data':x['data_visita'],'orgao':x['visitado_por'],'metric':'—','score':x['score'],'n_desconf':x['n_desconf'],'desconf':[{'label':y['label'],'sev':y['sev'],'base':y['base']} for y in x['desconformidades']]} for x in sorted(AP, key=lambda x:(MUN2COM[x['municipio']], x['municipio'], x['nome']))]
    pos=[k for k,r in enumerate(REL) if r['tipo']=='Conselho Tutelar']; first=pos[0] if pos else len(REL)
    REL=[r for r in REL if r['tipo']!='Conselho Tutelar']; REL[first:first]=REL_CT
    d=d[:s]+'const REL_DATA = window.REL_DATA = '+json.dumps(REL,ensure_ascii=False)+d[e:]
    nun=len({(r['tipo'],r['id']) for r in REL})
    d=sub1(r'(<div class="ini-num"><b>)\d+(</b><span>unidades inspecionadas</span></div>)', lambda m:m.group(1)+str(nun)+m.group(2), d)
    print('unidades no pais: %d | Amapa: %d | UFs: %d | REL_DATA: %d unidades (%d conselhos)'%(NT,len(AP),NUF,nun,len(REL_CT)))
    for x in REL_CT: print('  %-24s %-24s %-50s %s  NC %2d  score %2d'%(x['comarca'],x['municipio'],x['nome'][:50],x['data'],x['n_desconf'],x['score']))
    if dry: print('(dry-run: nada gravado)'); return
    ts=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'); os.makedirs(os.path.join(BASE,'backups'), exist_ok=True)
    shutil.copy(PAINEL, os.path.join(BASE,'backups','dashboard_pre_ct_%s.html'%ts))
    if os.path.exists(FONTE) and os.path.abspath(csvp)!=os.path.abspath(FONTE): shutil.copy(FONTE, os.path.join(BASE,'backups','fonte_conselho_tutelar_2026_anterior_%s.csv'%ts)); shutil.copy(csvp, FONTE)
    open(PAINEL,'w',encoding='utf-8').write(d); print('gravado:', PAINEL)
if __name__=='__main__': main()

