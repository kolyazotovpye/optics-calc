"""Инструменты для пополнения базы гравировок (engravings/data.js).

Каталоги (PDF) в репозиторий не кладём: путь к папке с ними задаётся переменной
окружения OC_CATALOGS. Корень репозитория определяется по расположению файла.

Пример:
    OC_CATALOGS=~/путь/к/каталогам python3 -i engravings/tools/cropkit.py
    >>> L = lines("Nikon 18.pdf", 118)          # строки текста с координатами (pt)
    >>> crop("Nikon 18.pdf", 118, (280,170,300,180), "pages/nikon/marks/x@2x.png")
"""
import json, os, re, subprocess
from PIL import Image

CAT = os.path.expanduser(os.environ.get("OC_CATALOGS", "."))
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
K = 600 / 72          # пикселей на pt при рендере 600 dpi
PRE = "window.ENGRAVINGS="
CACHE = os.environ.get("OC_CACHE", "/tmp/oc-cache")
_cache = {}

# ---------- данные ----------
def load():
    raw = open(f"{R}/engravings/data.js", encoding="utf-8").read()
    assert raw.startswith(PRE)
    return json.loads(raw[len(PRE):].rstrip().rstrip(";"))

def save(D):
    open(f"{R}/engravings/data.js", "w", encoding="utf-8").write(
        PRE + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";")

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]

# ---------- текст страницы ----------
def lines(pdf, page):
    """Строки текста страницы: dict(x0,y0,x1,y1,t,w=[(x0,y0,x1,y1,слово)]), координаты в pt.
    Пустой список = страница картинкой (текста нет), тогда ищем ячейки по растру."""
    key = (pdf, page, "l")
    if key in _cache: return _cache[key]
    out = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-bbox-layout",
                          f"{CAT}/{pdf}", "-"], capture_output=True, text=True).stdout
    L = []
    for x0, y0, x1, y1, inner in re.findall(
            r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', out, re.S):
        w = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in re.findall(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', inner)]
        L.append(dict(x0=float(x0), y0=float(y0), x1=float(x1), y1=float(y1), t=" ".join(x[4] for x in w), w=w))
    _cache[key] = L
    return L

# ---------- растр ----------
def raster(pdf, page, dpi=600):
    key = (pdf, page, dpi)
    if key in _cache: return _cache[key]
    os.makedirs(CACHE, exist_ok=True)
    f = f"{CACHE}/{re.sub(r'[^A-Za-z0-9]+', '_', pdf)}-{page}-{dpi}"
    if not os.path.exists(f + ".png"):
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi), "-png",
                        "-singlefile", f"{CAT}/{pdf}", f], check=True, stderr=subprocess.DEVNULL)
    im = Image.open(f + ".png").convert("RGB")
    _cache[key] = im
    return im

def _ink(px, mode):
    r, g, b = px
    if mode == "dark": return min(r, g, b) < 120 and max(r, g, b) - min(r, g, b) < 90
    if mode == "blue": return b - r > 40 and b > 90
    if mode == "any":  return min(r, g, b) < 150
    raise ValueError(mode)

def _save(out, name, scale):
    out = out.resize((max(1, round(out.width * scale)), max(1, round(out.height * scale))), Image.LANCZOS)
    os.makedirs(os.path.dirname(f"{R}/engravings/{name}"), exist_ok=True)
    out.save(f"{R}/engravings/{name}", optimize=True)
    return out.size

def crop(pdf, page, box, name, mode="dark", pad=2.0, scale=0.72):
    """Вырезка: box (x0,y0,x1,y1) в pt, обрезка по «чернилам» внутри box, сохранение в engravings/<name>.
    Имя на @2x.png — карточка покажет картинку в половинном размере (чётко на ретине)."""
    im = raster(pdf, page); x0, y0, x1, y1 = [int(v * K) for v in box]
    c = im.crop((x0, y0, x1, y1)); px = c.load(); w, h = c.size
    pts = [(x, y) for y in range(0, h, 2) for x in range(0, w, 2) if _ink(px[x, y], mode)]
    if not pts: return None
    p = int(pad * K); xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    return _save(c.crop((max(0, min(xs) - p), max(0, min(ys) - p), min(w, max(xs) + p + 2), min(h, max(ys) + p + 2))), name, scale)

def crop_clean(pdf, page, box, name, keep=lambda r, g, b: (b - r > 40 and b > 90) or max(r, g, b) < 95,
               pad=2.0, scale=0.72):
    """Как crop, но всё, что не проходит keep (серые подписи, цветной фон, жёлтая разметка), закрашивается белым."""
    im = raster(pdf, page); x0, y0, x1, y1 = [int(v * K) for v in box]
    c = im.crop((x0, y0, x1, y1)).copy(); px = c.load(); w, h = c.size; xs = []; ys = []
    for y in range(h):
        for x in range(w):
            if keep(*px[x, y]):
                if x % 2 == 0 and y % 2 == 0: xs.append(x); ys.append(y)
            else:
                px[x, y] = (255, 255, 255)
    if not xs: return None
    p = int(pad * K)
    return _save(c.crop((max(0, min(xs) - p), max(0, min(ys) - p), min(w, max(xs) + p + 2), min(h, max(ys) + p + 2))), name, scale)

def compose(parts, name, gap_pt=7, scale=0.72):
    """Склеить несколько вырезок (PIL.Image) в ряд: метка продукта + код, височная + назальная и т.п."""
    parts = [p for p in parts if p]
    h = max(p.height for p in parts); gap = int(gap_pt * K)
    o = Image.new("RGB", (sum(p.width for p in parts) + gap * (len(parts) - 1), h), "white"); x = 0
    for p in parts: o.paste(p, (x, (h - p.height) // 2)); x += p.width + gap
    return _save(o, name, scale)

# ---------- проверка ----------
def sheet(records, out, cols=4, cw=330, ch=64):
    """Сводная картинка «модель | код | вырезка» — смотреть глазами перед коммитом."""
    from PIL import ImageDraw
    rows = (len(records) + cols - 1) // cols
    o = Image.new("RGB", (cw * cols, ch * rows), "#ccc"); d = ImageDraw.Draw(o)
    for i, r in enumerate(records):
        x, y = (i % cols) * cw, (i // cols) * ch
        d.text((x + 2, y), (r["model"] + " | " + r.get("mark_code", ""))[:54], fill="red")
        if r.get("crop"):
            a = Image.open(f"{R}/engravings/{r['crop']}"); a.thumbnail((cw - 6, ch - 14)); o.paste(a, (x + 3, y + 12))
    o.save(out)
    return out
