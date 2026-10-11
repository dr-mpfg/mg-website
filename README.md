# Matteo Giordano — personal website

Static site: plain HTML + CSS + a little vanilla JS. No framework, no build step, no backend, no third-party requests. Live at https://mg-macro.vercel.app.

```
index.html                 Home: hero, statement, bio, four lines of work, academic roots, affiliations
advisory.html              Advisory: areas, delivered work, ways to engage
research.html              One page, four sections, project anchors (#eurozone, #subordination, ...)
publications.html          Published, in preparation, selected talks (#talks)
research/<slug>.html      Six project pages (balance-sheet-modelling, eurozone, subordination, gegi-study, macro-structures-dmo, defence-economics)
cargo-and-collateral.html  The newsletter: description + recent entries from data/writing.json
about.html                 Positions, education, methods, recognition, CV links
disclaimer.html  404.html
css/site.css   js/site.js   js/config.js   data/writing.json   fonts/   img/
tools/chrome.py            rewrites the shared nav + footer in every page from tools/chrome/*.html
tools/check.py             links, anchors, metadata, DRAFT markers (--strict), sitemap
tools/indexing.py          search-engine indexing switch (on|off)
tools/make_assets.py       regenerates favicon.ico, apple-touch-icon.png, img/og-share.png (needs Pillow)
serve.py                   local server mirroring vercel.json
```

## Run locally

```bash
python3 serve.py
```
Then http://localhost:8765 (clean URLs and the production security headers).

## Edit

- Copy lives in the HTML files. After touching the nav or footer, edit `tools/chrome/nav.html` or `footer.html` and run `python3 tools/chrome.py`. The nav partial carries the Research sub-menu: to add a project, add a link there (and a page under `research/`), then run `tools/chrome.py`.
- Addresses and links used in several places: `js/config.js` (the HTML carries the same values as fallbacks; update both).
- Add a newsletter entry: prepend to `data/writing.json` (`title`, `date`, `href`); keep the five most recent.
- Add an advisory engagement: append an `<li>` under Delivered work in `advisory.html` following the comment there.
- Before committing: `python3 tools/check.py --strict` and `python3 -m unittest discover -s tools/tests`.

## Indexing

`python3 tools/indexing.py off` hides the site from search engines (noindex meta, robots Disallow); `on` reverses it. Deploy afterwards.

## Deploy

Pushes to `main` on GitHub (`dr-mpfg/mg-website`) deploy to Vercel automatically. Framework preset Other, no build command, output directory `.`.
