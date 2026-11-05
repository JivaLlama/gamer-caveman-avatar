#!/usr/bin/env python3
"""Regenerate index.md (site) and README.md (GitHub) from _data/gallery.yml. Stdlib only."""
import json, os, sys, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))

def load(path):
    items, cur = [], None
    for line in open(path, encoding="utf-8"):
        s = line.rstrip("\n")
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        if s.startswith("- "):
            cur = {}; items.append(cur); s = s[2:]
        k, v = s.strip().split(":", 1)
        cur[k.strip()] = json.loads(v.strip()) if v.strip() else ""
    return items

def img(src, alt, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{src}" alt="{html.escape(alt)}" loading="lazy"{c}>'

def card(e, big=False):
    smooth = e["round"] == "nonpixel"
    cls = "card" + (" big" if big else "") + (" smooth" if smooth else " pixel")
    main = e.get("gif") or e["image"]
    out = [f'<div class="{cls}" id="{e["id"]}">']
    if e.get("badge"):
        out.append(f'<span class="badge">{html.escape(e["badge"])}</span>')
    out.append(img(main, e["name"]))
    out.append(f'<h3>{html.escape(e["name"])} <code>{e["id"]}</code></h3>')
    out.append(f'<p class="note">{html.escape(e["note"])}</p>')
    if e.get("stills"):
        out.append('<div class="frames">' + "".join(
            img(s, os.path.basename(s).rsplit(".", 1)[0]) for s in e["stills"]) + "</div>")
    links = []
    if e.get("gif") and e["image"] != e["gif"]:
        links.append(f'<a href="{e["image"]}">full image</a>')
    if e.get("cutout"):
        links.append(f'<a href="{e["cutout"]}">transparent cutout</a>')
    if links:
        out.append('<p class="links">' + " · ".join(links) + "</p>")
    out.append("</div>")
    return "\n".join(out)

def grid(entries, big=False):
    return '<div class="grid' + (" big" if big else "") + '">\n' + "\n".join(card(e, big) for e in entries) + "\n</div>"

V1 = ["idle", "idle_blink", "talk_open", "talk_open_blink", "talk_wide", "grin", "angry", "surprised"]

def body(items, today):
    t = lambda x: [e for e in items if e["tier"] == x]
    picks = t("jims_pick")
    names = ", ".join(e["name"] for e in picks)
    v1 = "".join(f'<figure>{img(f"assets/v1/pngtuber/{s}.png", s)}<figcaption>{s}</figcaption></figure>' for s in V1)
    return f"""<p class="banner">⚠️ CONCEPT / PROTOTYPE: style exploration, nothing final.</p>

<h1>Gamer Caveman</h1>

<p>Gamer Caveman is a stream avatar concept for Jim's buddy Ant: a caveman gamer, shown here in a bunch of art styles while Jim narrows down the look. It's built as a <strong>PNGtuber</strong>: instead of a rigged 3D or Live2D model, the app swaps flat images based on your mic (idle when quiet, talk when speaking, each with a blink). Free apps: <a href="https://olmewe.itch.io/veadotube-mini">Veadotube mini</a> (one image per state, set the mic threshold, add to OBS) and <a href="https://kaiakairos.itch.io/pngtuber-plus">PNGTuber Plus</a> (import the PNGs as sprites, choose speaking/silent/blink, hotkey expressions). Map <code>idle</code> → silent, <code>blink</code> → silent + blink, <code>talk</code> → talking; extra expressions go on hotkeys.</p>

<p class="updated">Last updated {today}. Refresh this page to see the latest picks.</p>

<h2 id="picks">Jim's picks</h2>
<p>Current primary picks: {html.escape(names)}.</p>
{grid(picks, big=True)}

<h2 id="running">Still in the running</h2>
{grid(t("contender"))}

<details id="earlier">
<summary><strong>Earlier rounds</strong> (archived styles, v1 original, overview sheets)</summary>

<h3>Archived styles</h3>
{grid(t("archived"))}

<h3>v1 original: 8 PNGtuber states</h3>
<p>312×320 transparent PNGs in <a href="assets/v1/pngtuber/">assets/v1/pngtuber/</a>. idle/idle_blink = silent, talk_open/talk_open_blink = talking, talk_wide = loud, grin/angry/surprised = hotkeys.</p>
<div class="states pixel">{v1}</div>
<p>{img("assets/v1/caveman_loop.gif", "v1 idle loop", "wide pixel")}</p>
<p>{img("assets/v1/caveman_contact_sheet.png", "v1 contact sheet", "wide pixel")}</p>
<p>Also: <a href="assets/v1/caveman_loop.webm">WebM with alpha</a>, <a href="assets/v1/caveman_loop.png">APNG</a>, <a href="assets/v1/caveman_native_39x40.png">native 39×40</a>.</p>

<h3>Overview sheets</h3>
<p>Pixel round, all 14 animating:</p>
<p>{img("assets/styles/styles_preview_all.gif", "All 14 pixel styles", "wide pixel")}</p>
<p>{img("assets/styles/styles_overview_contact_sheet.png", "Pixel round overview", "wide pixel")}</p>
<p>Non-pixel round:</p>
<p>{img("assets/nonpixel/overview.jpg", "Non-pixel round overview", "wide")}</p>
<p>{img("assets/nonpixel/pngtuber/trios_sheet.jpg", "Non-pixel idle/blink/talk trios", "wide")}</p>
</details>
"""

def main():
    items = load(os.path.join(ROOT, "_data", "gallery.yml"))
    missing = [p for e in items for p in [e["image"], e.get("gif"), e.get("cutout"), *e.get("stills", [])]
               if p and not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        sys.exit("Missing assets:\n" + "\n".join(missing))
    today = datetime.date.today().strftime("%B %-d, %Y")
    b = body(items, today)
    open(os.path.join(ROOT, "index.md"), "w", encoding="utf-8").write(
        "---\nlayout: default\ntitle: Gamer Caveman\n---\n<!-- GENERATED by build_site.py from _data/gallery.yml. Do not edit by hand. -->\n" + b)
    site = "https://jivallama.github.io/gamer-caveman-avatar/"
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(
        f"<!-- GENERATED by build_site.py from _data/gallery.yml. Do not edit by hand. -->\n**Live site:** {site}\n\n" + b)
    print(f"Built index.md and README.md from {len(items)} entries.")

if __name__ == "__main__":
    main()
