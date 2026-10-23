"""Mete en index.html una copia de los partidos del torneo (por si la web no puede leer Sportelia en directo).

Uso: python3 actualizar_copia.py
"""
import json
import pathlib
import re
import time
import urllib.request

TID = "-P0c-Ek5aDiamycFMz6H"
BASE = "https://sportelia-torneos.firebaseio.com/tournaments/"
CATS = {"-P0c0KCVA9HLmbtUu-LS", "-P0c0KCWF3GxfJfqdRVI", "-P0c0KCWF3GxfJfqdRVJ", "-P0c0KCWF3GxfJfqdRVK"}
PAGE = pathlib.Path(__file__).with_name("index.html")


def get(path):
    with urllib.request.urlopen(f"{BASE}{path}/{TID}.json", timeout=30) as r:
        return json.load(r)


matches = {k: v for k, v in get("matches").items() if v.get("categoryId") in CATS}
pub = get("public")
snap = {"at": int(time.time() * 1000), "matches": matches, "pub": {"name": pub.get("name")}}
js = "/*SNAPSHOT*/const SNAPSHOT = " + json.dumps(snap, ensure_ascii=False, separators=(",", ":")) + ";/*/SNAPSHOT*/"
html = PAGE.read_text(encoding="utf-8")
html = re.sub(r"/\*SNAPSHOT\*/.*?/\*/SNAPSHOT\*/", lambda _: js, html, count=1, flags=re.S)
PAGE.write_text(html, encoding="utf-8")
print(f"{len(matches)} partidos guardados")
