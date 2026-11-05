#!/bin/zsh
# Выгрузка страниц каталога для ссылок «показать страницу»: 200 dpi, WebP q70.
#   OC_CATALOGS=~/каталоги engravings/tools/render_pages.sh "Nikon 18.pdf" nikon 11 20 118 130
# -> engravings/pages/nikon/p011.webp и т.д. (номер = номер страницы PDF)
set -e
pdf="$1"; slug="$2"; shift 2
root="${0:A:h}/../.."; out="$root/engravings/pages/$slug"; mkdir -p "$out"
for p in "$@"; do
  f=$(printf "%s/p%03d" "$out" "$p")
  pdftoppm -f "$p" -l "$p" -r 200 -png -singlefile "${OC_CATALOGS:-.}/$pdf" "$f" 2>/dev/null
  python3 -c "from PIL import Image;import sys;Image.open(sys.argv[1]).convert('RGB').save(sys.argv[2],'WEBP',quality=70,method=6)" "$f.png" "$f.webp"
  rm -f "$f.png"; echo "$f.webp"
done
