# -*- coding: utf-8 -*-
CSS = """
<style>
:root{--tinta:#0d2436;--sub:#44586a;--verde:#1f5c46;--azul:#005B96;--linha:#dfe6ec;--bg:#fff;}
*{box-sizing:border-box}
body{margin:0;background:#f5f8fc;color:var(--tinta);font-family:'IBM Plex Serif',Georgia,serif;line-height:1.62;font-size:16px;}
.folha{max-width:900px;margin:24px auto;background:#fff;padding:56px 64px;border:1px solid var(--linha);}
.tri{display:flex;height:7px;margin-bottom:26px}
.tri span{flex:1}.tri span:nth-child(1){background:#2f6690}.tri span:nth-child(2){background:var(--verde)}.tri span:nth-child(3){background:#e8b33a}
.marca{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:12px;color:var(--verde)}
.marca small{display:block;font-weight:600;letter-spacing:.1em;color:#6b7a86;font-size:10px;margin-top:2px}
h1{font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:30px;line-height:1.18;letter-spacing:-.02em;margin:26px 0 6px}
h2{font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:18px;margin:30px 0 8px;color:var(--tinta);border-bottom:1px solid var(--linha);padding-bottom:6px}
h3{font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:14.5px;margin:20px 0 4px;color:var(--verde)}
p,li{text-align:justify}
.sub{color:var(--sub);font-size:15px;margin:0 0 18px}
table{width:100%;border-collapse:collapse;font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:13.5px;margin:12px 0 18px}
th{background:#eef3f7;text-align:left;padding:8px 10px;border:1px solid #ccd6df;font-weight:700}
td{padding:7px 10px;border:1px solid #dde4ea;vertical-align:top}
.nota{border-left:3px solid var(--azul);background:#f2f7fb;padding:10px 14px;margin:14px 0;font-size:14.5px}
code{background:#f2f5f8;padding:1px 5px;border:1px solid #e0e7ee;font-family:ui-monospace,Menlo,monospace;font-size:13px}
.rod{margin-top:36px;border-top:1px solid var(--linha);padding-top:10px;font-family:'IBM Plex Sans',sans-serif;font-size:11px;color:#7a8791;display:flex;justify-content:space-between}
ol,ul{padding-left:22px}
@media print{body{background:#fff}.folha{border:0;margin:0;padding:0;max-width:none}@page{size:A4;margin:2cm}}
</style>
"""
def doc(titulo, subtitulo, corpo, arquivo):
    html = ("<!doctype html><html lang=\"pt-BR\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>"+titulo+" · IndicadorMP</title>"+CSS+"</head><body><div class=\"folha\">"
            "<div class=\"tri\"><span></span><span></span><span></span></div>"
            "<div class=\"marca\">IndicadorMP<small>Corregedoria-Geral do Ministério Público do Estado do Amapá</small></div>"
            "<h1>"+titulo+"</h1><p class=\"sub\">"+subtitulo+"</p>"+corpo+
            "<div class=\"rod\"><span>IndicadorMP · Corregedoria-Geral do MP-AP</span><span>Documento de trabalho · 2026</span></div>"
            "</div></body></html>")
    open(arquivo,'w',encoding='utf-8').write(html)
    return arquivo
