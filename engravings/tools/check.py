"""Проверка базы перед коммитом: все картинки на месте, поля в порядке, сводка по каталогам.
    python3 engravings/tools/check.py
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from cropkit import load, R
D = load(); bad = []; by = collections.defaultdict(lambda: [0, 0, 0, 0])
for i, r in enumerate(D):
    for f in ("brand", "kind", "mark_code", "mark_visual", "model", "where", "source", "page", "image"):
        if f not in r: bad.append((i, "нет поля " + f))
    paths = [r.get("image"), r.get("crop")] + [p for _, p in r.get("prod", [])] + [p for _, p in r.get("card", [])]
    for p in filter(None, paths):
        if not os.path.exists(f"{R}/engravings/{p}"): bad.append((i, "нет файла " + p))
    s = by[r["source"]]; s[0] += 1; s[1] += bool(r.get("prod")); s[2] += bool(r.get("card")); s[3] += bool(r.get("crop"))
print(f"{'записей':>7} {'продукт':>7} {'карта':>6} {'вырезка':>7}  каталог")
for k, (n, a, b, c) in sorted(by.items(), key=lambda x: -x[1][0]): print(f"{n:7} {a:7} {b:6} {c:7}  {k}")
print("всего", len(D), "| ошибок", len(bad)); [print(" ", x) for x in bad[:30]]
sys.exit(1 if bad else 0)
