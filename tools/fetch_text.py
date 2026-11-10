import json, re, urllib.request, io, os, html
from html.parser import HTMLParser

URL = "https://iching.sjlyedu.com/quanwen.html"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

def strip(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

blocks = re.split(r'<article class="hex"', raw)[1:]
clean = []
for b in blocks:
    t = re.search(r"<h2[^>]*>(.*?)</h2>", b, re.S)
    if not t:
        continue
    title = strip(t.group(1))
    name = re.split(r"[（(]", title)[0].strip()
    name = re.sub(r"^\d+\.\s*", "", name)
    g = re.search(r'class="gua"[^>]*>(.*?)</p>', b, re.S)
    x = strip(g.group(1)) if g else ""
    x = re.sub(r"^卦辞[:：]\s*", "", x)
    ys = re.findall(r'class="yao-tag"[^>]*>(.*?)</span>\s*<span class="yao-text"[^>]*>(.*?)</span>', b, re.S)
    y = [strip(a) + "：" + strip(c) for a, c in ys]
    if not name or not x or len(y) < 6:
        continue
    clean.append({"n": len(clean) + 1, "f": name, "x": x, "y": y})

out = os.path.join(ROOT, "data")
os.makedirs(out, exist_ok=True)
with io.open(os.path.join(out, "64gua.json"), "w", encoding="utf-8") as f:
    json.dump(clean, f, ensure_ascii=False, indent=1)
print("count", len(clean))
for h in clean[:2]:
    print(h["n"], h["f"], "|", h["x"], "|", h["y"][0], "|", len(h["y"]))
if clean:
    print("last", clean[-1]["n"], clean[-1]["f"], len(clean[-1]["y"]))
