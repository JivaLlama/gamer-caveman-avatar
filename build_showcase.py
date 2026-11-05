#!/usr/bin/env python3
"""Regenerate showcase.md from _data/styles.yml. Pure stdlib; no network.
Per style id, expects assets/styles/<id>/<id>_anim.gif and <state>_<frames>.png
unless the entry sets gif/sheet explicitly."""
import pathlib
R = pathlib.Path(__file__).parent
STATES = ["idle", "blink", "talk", "talk_blink", "grin"]
def load():
    out, cur = [], None
    for l in (R/"_data/styles.yml").read_text().splitlines():
        if l.lstrip().startswith("#") or not l.strip(): continue
        if l.startswith("- "): cur = {}; out.append(cur); l = l[2:]
        k, v = l.strip().split(":", 1); cur[k.strip()] = v.strip().strip('"')
    return out
def card(s):
    gif = s.get("gif") or f"assets/styles/{s['id']}/{s['id']}_anim.gif"
    o = ['<div class="card">']
    if s.get("badge"): o.append(f'<span class="badge">{s["badge"]}</span>')
    o += [f'<img src="{gif}" alt="{s["id"]} animation">', f'<h3>{s["style"]} <code>{s["id"]}</code></h3>',
          f'<p><b>Resolution:</b> {s["resolution"]}<br><b>Headphones:</b> {s["headphones"]}</p>',
          f'<p class="note">{s.get("note","")}</p>']
    if s.get("frames"):
        o.append('<div class="frames">' + "".join(
            f'<img src="assets/styles/{s["id"]}/{st}_{s["frames"]}.png" alt="{st}" title="{st}">' for st in STATES) + "</div>")
    if s.get("sheet"): o.append(f'<img src="{s["sheet"]}" alt="{s["id"]} contact sheet">')
    o.append("</div>")
    return o
def render(st):
    o = ["---", "layout: default", "title: Style showcase", "---",
         '<p class="banner">⚠️ CONCEPT / PROTOTYPE: style exploration, nothing final.</p>', "",
         "# Style showcase", "", "[← Back](index.md)", "",
         "All 14 style variants, animating in sync, then the labelled overview sheet.", "",
         '<img class="wide" src="assets/styles/styles_preview_all.gif" alt="All 14 styles animating">', "",
         '<img class="wide" src="assets/styles/styles_overview_contact_sheet.png" alt="Overview contact sheet">', ""]
    tiers = []
    for s in st:
        if s["tier"] not in tiers: tiers.append(s["tier"])
    for t in tiers:
        o += [f"## {t}", "", '<div class="grid">']
        for s in st:
            if s["tier"] == t: o += card(s)
        o += ["</div>", ""]
    o.append("Per-state frames shown: idle, blink, talk, talk_blink, grin.")
    (R/"showcase.md").write_text("\n".join(o) + "\n")
render(load())
