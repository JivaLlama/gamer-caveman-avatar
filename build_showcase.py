#!/usr/bin/env python3
"""Regenerate showcase.md from _data/styles.yml.
Optional: --scan DIR copies <style>_<hs|bare>[_big].{gif,png} + *_sheet.png from DIR
into assets/styles/ and appends missing entries (hs = headphones, _big = high-res).
Pure stdlib; no network."""
import sys, shutil, re, pathlib
R = pathlib.Path(__file__).parent
Y = R/"_data/styles.yml"
def load():
    out, cur = [], None
    for l in Y.read_text().splitlines():
        if l.startswith("#") or not l.strip(): continue
        if l.startswith("- "): cur = {}; out.append(cur); l = l[2:]
        k, v = l.strip().split(":", 1); cur[k.strip()] = v.strip().strip('"')
    return out
def save(st):
    lines = ["# One entry per style. build_showcase.py regenerates showcase.md from this list."]
    for s in st:
        for i, (k, v) in enumerate(s.items()):
            lines.append(("- " if i == 0 else "  ") + f'{k}: "{v}"')
    Y.write_text("\n".join(lines) + "\n")
def scan(d, st):
    d = pathlib.Path(d); have = {s["id"] for s in st}; dst = R/"assets/styles"; dst.mkdir(parents=True, exist_ok=True)
    for g in sorted(d.rglob("*.gif")):
        m = re.match(r"(.+?)_(hs|bare)(_big)?$", g.stem)
        sid = g.stem
        if sid in have: continue
        shutil.copy(g, dst/g.name)
        sheet = next((p for p in g.parent.glob(sid + "*sheet*.png")), None)
        if sheet: shutil.copy(sheet, dst/sheet.name)
        st.append({"id": sid, "style": m.group(1) if m else sid,
                   "resolution": ("high-res" if m and m.group(3) else "low-res") if m else "wildcard",
                   "headphones": ("yes" if m.group(2) == "hs" else "no") if m else "?",
                   "gif": f"assets/styles/{g.name}", "sheet": f"assets/styles/{sheet.name}" if sheet else ""})
def render(st):
    o = ["---", "layout: default", "title: Style showcase", "---",
         '<p class="banner">⚠️ CONCEPT / PROTOTYPE</p>', "", "# Style showcase", "", "[← Back](index.md)", ""]
    for s in st:
        o += [f"## {s['style']}", "", f"- **Style:** {s['style']}", f"- **Resolution:** {s['resolution']}",
              f"- **Headphones:** {s['headphones']}", "", f"![{s['id']} loop]({s['gif']})", ""]
        if s.get("sheet"): o += [f"![{s['id']} contact sheet]({s['sheet']})", ""]
    (R/"showcase.md").write_text("\n".join(o))
st = load()
if "--scan" in sys.argv: scan(sys.argv[sys.argv.index("--scan")+1], st); save(st)
render(st)
