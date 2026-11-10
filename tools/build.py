import json, io, os, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
GUA = os.path.join(ROOT, "data", "64gua.json")

gua = json.load(io.open(GUA, encoding="utf-8"))

notes = {}
for f in sorted(glob.glob(os.path.join(ROOT, "data", "notes*.json"))):
    txt = io.open(f, encoding="utf-8").read()
    txt = re.sub(r",\s*(?=[}\]])", "", txt)
    notes.update(json.loads(txt))

def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

parts = []
filled = 0
for h in gua:
    nt = notes.get(str(h["n"]), {})
    r, z, c = nt.get("r", ""), nt.get("z", ""), nt.get("c", "")
    if r and z and c:
        filled += 1
    parts.append('{n:%d,f:%s,\n x:%s,\n y:[%s],\n r:%s,\n z:%s,\n c:%s},'
                 % (h["n"], q(h["f"]), q(h["x"]),
                    ",".join(q(t) for t in h["y"]), q(r), q(z), q(c)))
data = "\n".join(parts)

src = io.open(HTML, encoding="utf-8").read()
start = src.index("const YI = [")
end = src.index("];", start)
new = src[:start] + "const YI = [/* 由 tools/build.py 生成，勿手改 */\n" + data + "\n" + src[end:]
io.open(HTML, "w", encoding="utf-8", newline="\n").write(new)
print("卦数", len(gua), "三栏已录", filled, "注入字节", len(new))

