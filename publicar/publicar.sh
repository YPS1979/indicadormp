#!/bin/bash
# Publica a versão atual do painel no Cloudflare Pages (https://indicadormp.pages.dev)
# Uso: ./publicar.sh
set -e
BASE="$(cd "$(dirname "$0")/.." && pwd)"
PUB="$BASE/publicar/public"

# O passo de geração (gerar_visual.py) foi aposentado em 14/08/2026: o indicadormp.html
# passou a ser a fonte de verdade, editado diretamente. Regenerá-lo a partir da base
# apagaria as alterações feitas desde 07/08/2026. Ver gerar_visual.py.

echo "→ copiando para a pasta de publicação…"
cp "$BASE/indicadormp.html" "$PUB/index.html"

echo "→ preparando o PWA (manifesto + service worker)…"
VERSAO=$(date +%Y%m%d%H%M%S)
python3 - "$PUB" "$VERSAO" <<'PYEOF'
import sys, re
pub, versao = sys.argv[1], sys.argv[2]

# 1) injeta manifesto/ícones/registro do SW no index publicado (o arquivo local fica intacto)
p = pub + '/index.html'
d = open(p, encoding='utf-8').read()
TAGS = ('<link rel="manifest" href="/manifest.json">'
        '<meta name="theme-color" content="#005B96">'
        '<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">'
        '<meta name="apple-mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-title" content="IndicadorMP">')
SW = ('<script>if("serviceWorker" in navigator && location.protocol==="https:"){'
      'addEventListener("load",function(){navigator.serviceWorker.register("/sw.js");});}</script>')
i = d.find('</head>')          # primeiro head = documento principal
d = d[:i] + TAGS + SW + d[i:]
open(p, 'w', encoding='utf-8').write(d)

# 2) versiona o cache do service worker para forçar atualização nos apps instalados
q = pub + '/sw.js'
s = open(q, encoding='utf-8').read()
s = re.sub(r"indicadormp-[A-Za-z0-9_]+", "indicadormp-" + versao, s)
open(q, 'w', encoding='utf-8').write(s)
print("   PWA ok · cache indicadormp-" + versao)
PYEOF
ls -la "$PUB/index.html" | awk '{printf "   %.1f MB\n", $5/1048576}'

echo "→ enviando ao Cloudflare Pages…"
cd "$BASE/publicar"
npx --yes wrangler pages deploy public --project-name indicadormp --branch main --commit-dirty=true

echo "✓ pronto: https://indicadormp.pages.dev"
