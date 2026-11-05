# Maintaining the site

Everything on the main page comes from `_data/gallery.yml`.

1. Edit `_data/gallery.yml`: add entries, or move styles between tiers by changing `tier:` (`jims_pick`, `contender`, `archived`). Set `badge:` as needed. File order is display order.
2. Run `python3 build_site.py` (regenerates `index.md` and `README.md`; fails if an asset path is missing).
3. Commit and push to `main`. GitHub Pages rebuilds in a minute or two.

Don't edit `index.md` or `README.md` by hand. `showcase.html` and `nonpixel.html` are redirects to the main page for old links.
