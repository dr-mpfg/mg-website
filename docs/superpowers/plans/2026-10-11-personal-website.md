# Personal Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and launch Dr Matteo Giordano's personal website, a seven-page static business card, replacing the Obsidian digital garden at mg-macro.vercel.app.

**Architecture:** Plain HTML, CSS and vanilla JS, no build step, one file per page. Shared nav and footer are duplicated in every page and kept identical by `tools/chrome.py`. `tools/check.py` validates links, metadata, DRAFT markers and the sitemap. `serve.py` mirrors `vercel.json` locally.

**Tech Stack:** HTML5, CSS custom properties, ES5-style vanilla JS, Python 3.13 stdlib (tools, tests via `unittest`), Pillow 11 (asset generation only, not a runtime dependency), Vercel static hosting, `gh` CLI.

Spec: `docs/superpowers/specs/2026-10-11-personal-website-design.md`. Vault (content source): `/Users/matteo/Library/Mobile Documents/iCloud~md~obsidian/Documents/MG Macro/` (call it `$VAULT`). Pattern source: `/Users/matteo/work_codes_offline/GS/gs-website` (call it `$GS`). Repo root: `/Users/matteo/work_codes_offline/MG_macro_offline` (call it `$ROOT`; all paths below are relative to it).

## Global Constraints

- Static site: no framework, no bundler, no npm, no backend. Ask before adding any dependency.
- No third-party requests at runtime: fonts and images self-hosted, no analytics, no embeds. CSP `default-src 'self'` must hold (no inline scripts; inline `style` attributes are allowed only on `<svg>` sizing, prefer classes).
- Vault text is final copy. Only new lines are wrapped `<!-- DRAFT --> ... <!-- /DRAFT -->`; `check.py --strict` must pass (zero DRAFT markers) before launch.
- Page map is exactly: `/`, `/research`, `/publications`, `/cargo-and-collateral`, `/about`, `/advisory`, `/disclaimer`, plus `404.html`. Nav: `Research · Publications · Cargo & Collateral · About` + button `Advisory`. The newsletter tab is labelled exactly `Cargo & Collateral`.
- Tokens: `--paper #F6F2EA`, `--paper-2 #EDE7DB`, `--ink #1B1D22`, `--muted #6B6F76`, `--rule rgba(27,29,34,0.12)`, `--accent #1F6FB5`.
- Type: Source Serif 4 (400, 400 italic, 600) for headlines and prose; IBM Plex Sans (400, 500, 600) for nav, eyebrows, buttons, metadata, captions.
- Motion: 300 ms fade-in on scroll only; everything visible under `prefers-reduced-motion`.
- Every page: `<title>`, `meta description`, `<link rel="canonical">`, OpenGraph + Twitter tags, `lang="en-GB"`, skip link, `<main id="main">`.
- Email `mg.macroeconomics@gmail.com`. External links: Substack `https://cargoandcollateral.substack.com/`, subscribe `.../subscribe`, archive `.../archive`; LinkedIn `https://www.linkedin.com/in/matteogiordano-economist/`; ORCID `https://orcid.org/0000-0002-1588-6735`; CV `https://app.box.com/s/18pq9r7919gcxvu23hk5v4wda4hq6dq4`; academic CV `https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt`; Garrison Sterling `https://garrisonsterling.com`; GCF `https://globalclimateforum.org/portfolio-item/matteo-giordano/`; OBFA `https://obfa-transform.eu`; MA tool `https://monetary-architecture.com/`; UKDSC `https://www.ukdsc.org`; MoD `https://www.gov.uk/government/organisations/ministry-of-defence`; SOAS profile `https://www.soas.ac.uk/about/matteo-giordano-0`; SPARC `https://wearesparc.org/`.
- Live site today: `https://mg-macro.vercel.app` (mgmacro.vercel.app 307-redirects to it). Confirmed old slugs (all 200 today): `/about`, `/advisory`, `/cargo-and-collateral`, `/research-projects/research-projects`, `/research-projects/eurozone`, `/research-projects/gegi-study`, `/research-projects/balance-sheet-modelling`, `/research-projects/subordination`, `/research-projects/defence-and-security-economics`, `/research-projects/macro-structures-and-dmo`, `/publications/publications`, `/publications/the-state-of-capitalism`, `/talks-and-conferences/talk-and-conferences`.
- Commit after every task with `git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit` unless a global identity is configured. Commit messages end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Run Python that reads downloaded archives with `python3 -I`, from `$ROOT`, never from inside the download directory.

---

## File structure

| File | Responsibility |
|---|---|
| `index.html`, `research.html`, `publications.html`, `cargo-and-collateral.html`, `about.html`, `advisory.html`, `disclaimer.html`, `404.html` | one page each, complete without JS |
| `css/site.css` | tokens, fonts, base, nav, hero, blocks, figures, lists, footer, reveal |
| `js/site.js` | mobile nav toggle, reveal-on-scroll, config wiring, writing list |
| `js/config.js` | `window.MG_CONFIG`: addresses and the `INDEXING` mirror |
| `data/writing.json` | recent Cargo & Collateral entries |
| `tools/chrome/nav.html`, `tools/chrome/footer.html` | the single source of nav and footer markup |
| `tools/chrome.py` | writes nav/footer into every page between markers, sets `aria-current` |
| `tools/check.py` | link, image, anchor, metadata, DRAFT and sitemap checks |
| `tools/indexing.py` | indexing switch (from GS) |
| `tools/make_assets.py` | one-off Pillow script: favicon.ico, apple-touch-icon.png, og-share.png from the T mark |
| `tools/tests/test_chrome.py`, `tools/tests/test_check.py` | unittest suites, run with `python3 -m unittest discover -s tools/tests` |
| `serve.py` | local server mirroring vercel.json |
| `vercel.json`, `robots.txt`, `sitemap.xml` | hosting config |
| `.claude/launch.json` | browser-pane dev server entry |
| `README.md` | run, edit, add entry, indexing, deploy |

---

### Task 1: Scaffold, fonts, hosting config, local server

**Files:**
- Create: `.gitignore`, `js/config.js`, `vercel.json`, `robots.txt`, `serve.py`, `.claude/launch.json`, `fonts/*`, `README.md` (stub)
- Copy from `$GS`: `serve.py`, `fonts/IBMPlexSans-*.woff2`, `fonts/SourceSerif4-Regular.woff2`, `fonts/SourceSerif4-Semibold.woff2`, `fonts/LICENSE-*`

**Interfaces:**
- Produces: `window.MG_CONFIG` keys `CONTACT_EMAIL, SUBSTACK_URL, SUBSTACK_SUBSCRIBE_URL, SUBSTACK_ARCHIVE_URL, LINKEDIN_URL, ORCID_URL, CV_URL, CV_ACADEMIC_URL, INDEXING`; `serve.py` on port 8765 with clean URLs.

- [ ] **Step 1: .gitignore and directories**

```bash
cd "$ROOT"
mkdir -p css js data fonts img/figures/full tools/chrome tools/tests .claude
printf '.DS_Store\n.vercel\n.env*\n.claude/settings.local.json\n_dl/\n' > .gitignore
```

- [ ] **Step 2: Copy fonts and server from GS**

```bash
cp "$GS"/fonts/IBMPlexSans-Regular.woff2 "$GS"/fonts/IBMPlexSans-Medium.woff2 "$GS"/fonts/IBMPlexSans-SemiBold.woff2 "$GS"/fonts/SourceSerif4-Regular.woff2 "$GS"/fonts/SourceSerif4-Semibold.woff2 "$GS"/fonts/LICENSE-IBMPlexSans.txt "$GS"/fonts/LICENSE-SourceSerif4.md fonts/
cp "$GS"/serve.py serve.py
```

- [ ] **Step 3: Download Source Serif 4 Italic (OFL) from the Adobe release into an isolated directory**

```bash
mkdir -p _dl/source-serif && cd _dl/source-serif
gh release download 4.005R --repo adobe-fonts/source-serif --pattern 'source-serif-4.005_WOFF2.zip'
unzip -q source-serif-4.005_WOFF2.zip
find . -iname 'SourceSerif4-It.*woff2' -print
cd "$ROOT"
```
Expected: one path such as `./source-serif-4.005_WOFF2/WOFF2/OTF/SourceSerif4-It.otf.woff2`. Copy it:
```bash
cp "$(find _dl/source-serif -iname 'SourceSerif4-It.*woff2' | head -1)" fonts/SourceSerif4-Italic.woff2
ls -l fonts/SourceSerif4-Italic.woff2
```
Expected: a file around 80 KB. `_dl/` is gitignored.

- [ ] **Step 4: vercel.json**

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    { "source": "/(.*)", "headers": [
      { "key": "Content-Security-Policy", "value": "default-src 'self'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; object-src 'none'" },
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "X-Frame-Options", "value": "DENY" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
      { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), interest-cohort=()" },
      { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains" }
    ] },
    { "source": "/fonts/(.*)", "headers": [ { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" } ] },
    { "source": "/img/(.*)", "headers": [ { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" } ] }
  ],
  "redirects": [
    { "source": "/research-projects/research-projects", "destination": "/research", "permanent": true },
    { "source": "/research-projects/eurozone", "destination": "/research#eurozone", "permanent": true },
    { "source": "/research-projects/gegi-study", "destination": "/research#gegi-study", "permanent": true },
    { "source": "/research-projects/balance-sheet-modelling", "destination": "/research#balance-sheet-modelling", "permanent": true },
    { "source": "/research-projects/subordination", "destination": "/research#subordination", "permanent": true },
    { "source": "/research-projects/defence-and-security-economics", "destination": "/research#defence", "permanent": true },
    { "source": "/research-projects/macro-structures-and-dmo", "destination": "/research#macro-structures-dmo", "permanent": true },
    { "source": "/research-projects/(.*)", "destination": "/research", "permanent": true },
    { "source": "/publications/publications", "destination": "/publications", "permanent": true },
    { "source": "/publications/the-state-of-capitalism", "destination": "/publications#state-of-capitalism", "permanent": true },
    { "source": "/publications/(.*)", "destination": "/publications", "permanent": true },
    { "source": "/talks-and-conferences/(.*)", "destination": "/publications#talks", "permanent": true },
    { "source": "/dr-matteo-giordano", "destination": "/", "permanent": true }
  ]
}
```

- [ ] **Step 5: robots.txt (indexing on) and js/config.js**

`robots.txt`:
```
# Managed by tools/indexing.py
User-agent: *
Allow: /
Sitemap: https://mg-macro.vercel.app/sitemap.xml
```

`js/config.js`:
```js
/* Matteo Giordano site constants. Edit here only; the HTML carries the same values as fallbacks. */
window.MG_CONFIG = Object.freeze({
  CONTACT_EMAIL: 'mg.macroeconomics@gmail.com',
  SUBSTACK_URL: 'https://cargoandcollateral.substack.com/',
  SUBSTACK_SUBSCRIBE_URL: 'https://cargoandcollateral.substack.com/subscribe',
  SUBSTACK_ARCHIVE_URL: 'https://cargoandcollateral.substack.com/archive',
  LINKEDIN_URL: 'https://www.linkedin.com/in/matteogiordano-economist/',
  ORCID_URL: 'https://orcid.org/0000-0002-1588-6735',
  CV_URL: 'https://app.box.com/s/18pq9r7919gcxvu23hk5v4wda4hq6dq4',
  CV_ACADEMIC_URL: 'https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt',
  // Mirrors tools/indexing.py state. Flip with the script, not here.
  INDEXING: true
});
```

- [ ] **Step 6: launch.json and README stub**

`.claude/launch.json`:
```json
{ "version": "0.0.1", "configurations": [ { "name": "mg-website", "runtimeExecutable": "python3", "runtimeArgs": ["serve.py", "8765"], "port": 8765 } ] }
```
`README.md`: a title line `# Matteo Giordano — personal website` and `Static site. See docs/superpowers/specs for the design.` (completed in Task 11).

- [ ] **Step 7: Verify the server serves a clean URL with headers**

```bash
printf '<!DOCTYPE html><title>t</title>' > _probe.html
python3 serve.py 8765 & SP=$!; sleep 1
curl -s -D - -o /dev/null http://localhost:8765/_probe | grep -E "HTTP/|Content-Security-Policy"
kill $SP; rm _probe.html
```
Expected: `HTTP/1.0 200 OK` and the CSP header line.

- [ ] **Step 8: Commit**

```bash
git add -A && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Scaffold: fonts, hosting config, local server

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Stylesheet

**Files:**
- Create: `css/site.css`

**Interfaces:**
- Produces the class vocabulary every page uses: `.wrap .skip-link .nav .nav__bar .nav__links .nav__link .nav__cta .nav__toggle .nav__toggle-label .nav__toggle-icon .logo .logo__mark .logo__text .btn .btn--sm .link .eyebrow .muted .hero .hero__title .hero__roles .hero__links .statement .statement__text .block .block__grid .block__title .block__body .lines .line .line__title .papers .affil .page-head .page-title .lede .section .section__title .project .project__title .figure .figure__caption .figure__link .areas .area__title .delivered .engage .pubs .pubs--talks .writing .writing__item .writing__date .writing__title .cv-links .prose .footer .footer__row .footer__links .footer__tag .reveal .is-visible`.

- [ ] **Step 1: Write css/site.css**

```css
/* Matteo Giordano — site.css. Warm paper, ink, one accent. Plain CSS, no build. */

/* Fonts (self-hosted, OFL) */
@font-face { font-family: 'Source Serif 4'; font-style: normal; font-weight: 400; font-display: swap; src: url('../fonts/SourceSerif4-Regular.woff2') format('woff2'); }
@font-face { font-family: 'Source Serif 4'; font-style: italic; font-weight: 400; font-display: swap; src: url('../fonts/SourceSerif4-Italic.woff2') format('woff2'); }
@font-face { font-family: 'Source Serif 4'; font-style: normal; font-weight: 600; font-display: swap; src: url('../fonts/SourceSerif4-Semibold.woff2') format('woff2'); }
@font-face { font-family: 'IBM Plex Sans'; font-style: normal; font-weight: 400; font-display: swap; src: url('../fonts/IBMPlexSans-Regular.woff2') format('woff2'); }
@font-face { font-family: 'IBM Plex Sans'; font-style: normal; font-weight: 500; font-display: swap; src: url('../fonts/IBMPlexSans-Medium.woff2') format('woff2'); }
@font-face { font-family: 'IBM Plex Sans'; font-style: normal; font-weight: 600; font-display: swap; src: url('../fonts/IBMPlexSans-SemiBold.woff2') format('woff2'); }

/* Tokens */
:root {
  --paper: #F6F2EA; --paper-2: #EDE7DB; --ink: #1B1D22; --muted: #6B6F76;
  --rule: rgba(27, 29, 34, 0.12); --accent: #1F6FB5; --accent-soft: rgba(31, 111, 181, 0.35);
  --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
  --sans: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
  --max: 1120px; --gutter: 20px; --nav-h: 72px; --ease: cubic-bezier(0.2, 0.7, 0.2, 1);
}
@media (min-width: 768px) { :root { --gutter: 40px; --nav-h: 84px; } }

/* Base */
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--serif); font-size: 1.0625rem; line-height: 1.6; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; overflow-x: hidden; min-height: 100vh; display: flex; flex-direction: column; }
@media (min-width: 768px) { body { font-size: 1.125rem; } }
main { flex: 1 0 auto; }
h1, h2, h3 { margin: 0; font-family: var(--serif); font-weight: 600; letter-spacing: -0.015em; line-height: 1.15; text-wrap: balance; }
p { margin: 0 0 1em; max-width: 62ch; text-wrap: pretty; }
p:last-child { margin-bottom: 0; }
a { color: inherit; text-decoration: none; }
ul, ol { margin: 0; padding: 0; list-style: none; }
button { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; }
img, svg { display: block; max-width: 100%; }
img { height: auto; }
em, i { font-style: italic; }
[hidden] { display: none !important; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; }
:target { scroll-margin-top: calc(var(--nav-h) + 16px); }
.skip-link { position: absolute; left: var(--gutter); top: -100px; z-index: 100; background: var(--ink); color: var(--paper); padding: 8px 14px; font-family: var(--sans); font-weight: 500; }
.skip-link:focus { top: 12px; }
.wrap { width: 100%; max-width: calc(var(--max) + 2 * var(--gutter)); margin: 0 auto; padding-left: var(--gutter); padding-right: var(--gutter); }
.muted { color: var(--muted); }
.eyebrow { font-family: var(--sans); font-size: 0.8125rem; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); }

/* Links and buttons */
.link { color: var(--ink); border-bottom: 1px solid var(--accent-soft); padding-bottom: 1px; transition: border-color 200ms var(--ease), color 200ms var(--ease); }
.link:hover { color: var(--accent); border-color: var(--accent); }
.prose a, .block__body a, .project a, .pubs a, .areas a, .delivered a, .engage a, .line a, .papers a, .affil a, .statement a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); transition: border-color 200ms var(--ease), color 200ms var(--ease); }
.prose a:hover, .block__body a:hover, .project a:hover, .pubs a:hover, .areas a:hover, .delivered a:hover, .engage a:hover, .line a:hover, .papers a:hover, .affil a:hover, .statement a:hover { color: var(--accent); border-color: var(--accent); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 46px; padding: 11px 24px; border: 1px solid var(--accent); border-radius: 2px; font-family: var(--sans); font-weight: 500; font-size: 0.9375rem; line-height: 1.2; white-space: nowrap; color: var(--ink); background: transparent; transition: background-color 200ms var(--ease), color 200ms var(--ease); }
.btn:hover { background: var(--accent); color: var(--paper); }
.btn--sm { min-height: 38px; padding: 7px 16px; font-size: 0.875rem; }

/* Logo: T-account mark + wordmark */
.logo { display: inline-flex; align-items: center; gap: 10px; flex-shrink: 0; color: var(--ink); }
.logo__mark { width: 22px; height: 22px; stroke: currentColor; stroke-width: 2; stroke-linecap: square; fill: none; }
.logo__text { font-family: var(--sans); font-weight: 600; font-size: 0.9375rem; letter-spacing: 0.08em; text-transform: uppercase; white-space: nowrap; }
.logo:hover { color: var(--accent); }

/* Nav */
.nav { position: relative; z-index: 30; min-height: var(--nav-h); display: flex; align-items: center; border-bottom: 1px solid var(--rule); }
.nav__bar { display: flex; align-items: center; justify-content: space-between; gap: 32px; min-height: var(--nav-h); }
.nav__links { display: flex; align-items: center; gap: 32px; }
.nav__link { font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; color: var(--muted); transition: color 200ms var(--ease); }
.nav__link:hover, .nav__link[aria-current="page"] { color: var(--ink); }
.nav__cta { margin-left: 8px; }
.nav__cta[aria-current="page"] { background: var(--accent); color: var(--paper); }
.nav__toggle { display: none; align-items: center; gap: 10px; min-height: 44px; padding: 0 4px; z-index: 41; position: relative; font-family: var(--sans); font-size: 0.875rem; font-weight: 500; color: var(--ink); }
.nav__toggle-icon { position: relative; width: 20px; height: 12px; }
.nav__toggle-icon::before, .nav__toggle-icon::after { content: ''; position: absolute; left: 0; right: 0; height: 1.5px; background: currentColor; transition: transform 200ms var(--ease), top 200ms var(--ease), bottom 200ms var(--ease); }
.nav__toggle-icon::before { top: 0; }
.nav__toggle-icon::after { bottom: 0; }
.nav__toggle[aria-expanded="true"] .nav__toggle-icon::before { top: 5px; transform: rotate(45deg); }
.nav__toggle[aria-expanded="true"] .nav__toggle-icon::after { bottom: 5px; transform: rotate(-45deg); }
@media (max-width: 899px) {
  .nav__toggle { display: inline-flex; }
  .nav__links { display: none; position: fixed; inset: 0; z-index: 40; flex-direction: column; align-items: flex-start; justify-content: center; gap: 8px; padding: var(--nav-h) var(--gutter) 40px; background: var(--paper); }
  .nav__links.is-open { display: flex; }
  .nav .logo { position: relative; z-index: 41; }
  .nav__link { font-family: var(--serif); font-size: 2rem; font-weight: 600; letter-spacing: -0.015em; color: var(--ink); padding: 8px 0; }
  .nav__cta { margin: 32px 0 0; }
  body.nav-open { overflow: hidden; }
}

/* Home hero (typographic) */
.hero { padding: 56px 0 48px; }
@media (min-width: 768px) { .hero { padding: 104px 0 80px; } }
.hero .eyebrow { margin-bottom: 20px; }
.hero__title { font-size: clamp(2.25rem, 5vw, 4rem); line-height: 1.08; letter-spacing: -0.025em; max-width: 20ch; }
.hero__roles { margin-top: 28px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; letter-spacing: 0.02em; color: var(--muted); max-width: 70ch; line-height: 1.7; }
.hero__roles span { white-space: nowrap; }
.hero__roles .sep { color: var(--accent); padding: 0 6px; }
.hero__links { display: flex; flex-wrap: wrap; gap: 12px 24px; margin-top: 32px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; }
.hero__links a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); padding-bottom: 2px; transition: color 200ms var(--ease), border-color 200ms var(--ease); }
.hero__links a:hover { color: var(--accent); border-color: var(--accent); }

/* Statement (large paragraph) */
.statement { padding: 48px 0; border-top: 1px solid var(--rule); }
@media (min-width: 768px) { .statement { padding: 72px 0; } }
.statement__text { font-size: clamp(1.375rem, 2.4vw, 1.875rem); line-height: 1.4; letter-spacing: -0.01em; max-width: 34ch; }

/* Generic block with title/body grid */
.block { padding: 40px 0; border-top: 1px solid var(--rule); }
@media (min-width: 768px) { .block { padding: 64px 0; } }
.block__grid { display: grid; gap: 16px; }
@media (min-width: 768px) { .block__grid { grid-template-columns: minmax(0, 3fr) minmax(0, 8fr); column-gap: 64px; align-items: start; } }
.block__title { font-family: var(--sans); font-size: 0.8125rem; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); line-height: 1.5; padding-top: 6px; }
.block__body { font-size: 1.0625rem; line-height: 1.6; }
@media (min-width: 768px) { .block__body { font-size: 1.1875rem; } }
.block__body p { max-width: 60ch; }
.block__body ul { display: grid; gap: 10px; }
.block__body li { max-width: 60ch; }

/* Four lines of work */
.lines { display: grid; gap: 28px; }
@media (min-width: 768px) { .lines { grid-template-columns: 1fr 1fr; gap: 40px 64px; } }
.line { padding-top: 20px; border-top: 1px solid var(--rule); }
.line__n { font-family: var(--sans); font-size: 0.8125rem; font-weight: 500; letter-spacing: 0.1em; color: var(--accent); margin-bottom: 8px; display: block; }
.line__title { font-size: 1.375rem; margin-bottom: 10px; }
@media (min-width: 768px) { .line__title { font-size: 1.5rem; } }
.line p { color: var(--ink); font-size: 1.0625rem; max-width: 44ch; }
.line__more { display: inline-block; margin-top: 8px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; }

/* Selected papers (home) and publications */
.papers { display: grid; gap: 14px; }
.papers li { font-size: 1.0625rem; line-height: 1.5; max-width: 60ch; }
.pubs { display: grid; gap: 18px; counter-reset: pub; }
.pubs li { position: relative; padding-left: 2.5rem; max-width: 66ch; line-height: 1.55; }
.pubs li::before { counter-increment: pub; content: counter(pub); position: absolute; left: 0; top: 0.2em; font-family: var(--sans); font-size: 0.8125rem; font-weight: 500; color: var(--muted); }
.pubs--talks li { padding-left: 0; }
.pubs--talks li::before { content: none; }
.pubs .where { color: var(--muted); }

/* Affiliations row */
.affil { display: flex; flex-wrap: wrap; gap: 8px 0; font-family: var(--sans); font-size: 0.9375rem; color: var(--muted); }
.affil li + li::before { content: '·'; color: var(--accent); padding: 0 12px; }
.affil a { color: var(--ink); border-bottom: 1px solid transparent; }
.affil a:hover { color: var(--accent); border-color: var(--accent); }

/* Inner pages */
.page-head { padding: 48px 0 32px; }
@media (min-width: 768px) { .page-head { padding: 88px 0 56px; } }
.page-head .eyebrow { margin-bottom: 18px; }
.page-title { font-size: clamp(2rem, 4.5vw, 3.25rem); line-height: 1.1; letter-spacing: -0.02em; max-width: 20ch; }
.lede { margin-top: 24px; font-size: clamp(1.125rem, 1.8vw, 1.375rem); line-height: 1.5; color: var(--muted); max-width: 56ch; }
.lede--ink { color: var(--ink); }
.page-head .btn { margin-top: 28px; }

/* Research sections and projects */
.section { padding: 40px 0; border-top: 1px solid var(--rule); }
@media (min-width: 768px) { .section { padding: 64px 0; } }
.section__title { font-size: clamp(1.625rem, 3vw, 2.25rem); letter-spacing: -0.02em; margin-bottom: 8px; }
.section__intro { color: var(--muted); max-width: 60ch; margin-bottom: 8px; }
.project { padding-top: 32px; margin-top: 32px; border-top: 1px solid var(--rule); display: grid; gap: 16px; }
@media (min-width: 768px) { .project { grid-template-columns: minmax(0, 3fr) minmax(0, 8fr); column-gap: 64px; } .project { padding-top: 40px; margin-top: 40px; } }
.project__title { font-size: 1.375rem; line-height: 1.25; }
@media (min-width: 768px) { .project__title { font-size: 1.5rem; } }
.project__meta { display: block; margin-top: 8px; font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); letter-spacing: 0.02em; }
.project__body h3 { font-size: 1.0625rem; font-family: var(--sans); font-weight: 600; letter-spacing: 0; margin: 20px 0 6px; }
.project__body h3:first-child { margin-top: 0; }
.project__body p { max-width: 60ch; }
.project__links { margin-top: 16px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; display: flex; flex-wrap: wrap; gap: 8px 20px; }
.project__links a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); }
.project__links a:hover { color: var(--accent); border-color: var(--accent); }

/* Figures */
.figure { margin: 20px 0 8px; }
.figure img { width: 100%; height: auto; background: var(--paper-2); border: 1px solid var(--rule); }
.figure--cover { max-width: 240px; }
.figure--cover img { border: 1px solid var(--rule); }
.figure__caption { margin-top: 8px; font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); line-height: 1.5; max-width: 60ch; }
.figure__link { white-space: nowrap; }
.figure__link::before { content: '·'; color: var(--accent); padding: 0 6px; }

/* Advisory: areas, delivered, ways to engage */
.areas { display: grid; gap: 28px; }
.area { padding-top: 20px; border-top: 1px solid var(--rule); }
.area__title { font-size: 1.375rem; margin-bottom: 8px; }
.area p { max-width: 56ch; }
.delivered { display: grid; gap: 20px; }
.delivered li { padding-top: 18px; border-top: 1px solid var(--rule); max-width: 60ch; }
.delivered strong { font-weight: 600; }
.engage { display: grid; gap: 14px; }
.engage li { max-width: 60ch; }
.engage strong { font-weight: 600; }
.closing { padding: 48px 0 80px; border-top: 1px solid var(--rule); }
@media (min-width: 768px) { .closing { padding: 72px 0 112px; } }
.closing__line { font-size: clamp(1.375rem, 2.4vw, 1.875rem); line-height: 1.4; max-width: 34ch; }
.closing .btn { margin-top: 28px; }
.note { margin-top: 28px; font-family: var(--sans); font-size: 0.875rem; color: var(--muted); max-width: 70ch; }

/* Cargo & Collateral */
.wordmark { width: 100%; max-width: 420px; margin: 0 0 28px; }
.writing { display: grid; }
.writing__item { padding: 20px 0; border-top: 1px solid var(--rule); display: grid; gap: 4px; }
.writing__item:last-child { border-bottom: 1px solid var(--rule); }
.writing__date { font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); }
.writing__title { font-size: 1.1875rem; font-weight: 600; letter-spacing: -0.01em; }
.writing__title:hover { color: var(--accent); }
.actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px; }

/* About: CV links */
.cv-links { display: flex; flex-wrap: wrap; gap: 10px 24px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; }
.cv-links a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); }
.cv-links a:hover { color: var(--accent); border-color: var(--accent); }

/* Prose pages (disclaimer, 404) */
.prose { padding: 24px 0 96px; }
.prose .wrap { max-width: calc(68ch + 2 * var(--gutter)); margin-left: 0; }
@media (min-width: 1000px) { .prose .wrap { margin-left: max(var(--gutter), calc((100% - var(--max) - 2 * var(--gutter)) / 2 + var(--gutter))); padding-left: 0; } }
.prose p { max-width: 68ch; }
.prose h2 { font-size: 1.25rem; margin: 32px 0 10px; }
.page-head--tall { min-height: 60vh; display: flex; align-items: center; }

/* Footer */
.footer { padding: 40px 0 32px; border-top: 1px solid var(--rule); }
.footer__row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 20px 40px; font-family: var(--sans); font-size: 0.875rem; color: var(--muted); }
.footer__links { display: flex; align-items: center; flex-wrap: wrap; gap: 8px 24px; }
.footer__links a { color: var(--muted); border-bottom: 1px solid transparent; }
.footer__links a:hover { color: var(--accent); border-color: var(--accent); }
.footer__tag { margin-top: 12px; font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); }

/* Reveal on scroll */
.reveal { opacity: 0; transition: opacity 300ms var(--ease); }
.reveal.is-visible { opacity: 1; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .reveal { opacity: 1; transition: none; }
  *, *::before, *::after { transition: none !important; animation: none !important; }
}
```

- [ ] **Step 2: Sanity check the file parses (brace balance)**

```bash
python3 -c "s=open('css/site.css').read(); assert s.count('{')==s.count('}'), (s.count('{'), s.count('}')); print('braces ok', s.count('{'))"
```
Expected: `braces ok` and a count.

- [ ] **Step 3: Commit**

```bash
git add css/site.css && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Stylesheet: tokens, type, nav, blocks, figures, footer

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: Shared chrome (nav + footer), chrome.py, site.js

**Files:**
- Create: `tools/chrome/nav.html`, `tools/chrome/footer.html`, `tools/chrome.py`, `tools/tests/test_chrome.py`, `tools/tests/__init__.py` (empty), `js/site.js`

**Interfaces:**
- Produces: every page must contain the two marker pairs `<!-- CHROME:nav -->...<!-- /CHROME:nav -->` and `<!-- CHROME:footer -->...<!-- /CHROME:footer -->`; `python3 tools/chrome.py` rewrites their contents and sets `aria-current="page"` on the nav link whose `href` equals the page path (`index.html` → `/`, `about.html` → `/about`; `404.html` gets none). `site.js` reads `window.MG_CONFIG`, wires `[data-mailto]`, `[data-link="KEY"]`, the nav toggle, `.reveal`, and `#writing-list`/`#writing-empty`.

- [ ] **Step 1: Write the nav and footer partials**

`tools/chrome/nav.html`:
```html
<nav class="nav" aria-label="Primary">
  <div class="wrap nav__bar">
    <a class="logo" href="/" aria-label="Matteo Giordano, home">
      <svg class="logo__mark" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 5h20M12 5v17"/></svg>
      <span class="logo__text">Matteo Giordano</span>
    </a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-links">
      <span class="nav__toggle-label">Menu</span>
      <span class="nav__toggle-icon" aria-hidden="true"></span>
    </button>
    <div class="nav__links" id="nav-links">
      <a class="nav__link" href="/research">Research</a>
      <a class="nav__link" href="/publications">Publications</a>
      <a class="nav__link" href="/cargo-and-collateral">Cargo &amp; Collateral</a>
      <a class="nav__link" href="/about">About</a>
      <a class="btn btn--sm nav__cta" href="/advisory">Advisory</a>
    </div>
  </div>
</nav>
```

`tools/chrome/footer.html`:
```html
<footer class="footer" id="site-footer">
  <div class="wrap">
    <div class="footer__row">
      <div>
        <a class="logo" href="/" aria-label="Matteo Giordano, home">
          <svg class="logo__mark" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 5h20M12 5v17"/></svg>
          <span class="logo__text">Matteo Giordano</span>
        </a>
        <p class="footer__tag">Macro-financial strategy · Shipping, monetary structures, off-balance-sheet finance</p>
      </div>
      <div class="footer__links">
        <span>© 2026 Matteo Giordano</span>
        <a href="mailto:mg.macroeconomics@gmail.com" data-mailto>Email</a>
        <a href="https://www.linkedin.com/in/matteogiordano-economist/" data-link="LINKEDIN_URL" rel="noopener" target="_blank">LinkedIn</a>
        <a href="https://orcid.org/0000-0002-1588-6735" data-link="ORCID_URL" rel="noopener" target="_blank">ORCID</a>
        <a href="/disclaimer">Disclaimer</a>
      </div>
    </div>
  </div>
</footer>
```

- [ ] **Step 2: Write the failing test for chrome.py**

`tools/tests/test_chrome.py`:
```python
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import chrome

NAV = '<nav><a class="nav__link" href="/research">Research</a><a class="btn nav__cta" href="/advisory">Advisory</a></nav>'
FOOT = '<footer>f</footer>'
PAGE = ('<html><body>\n<!-- CHROME:nav -->\nOLD NAV\n<!-- /CHROME:nav -->\n<main>x</main>\n'
        '<!-- CHROME:footer -->OLD FOOT<!-- /CHROME:footer -->\n</body></html>')

class ChromeTest(unittest.TestCase):
    def test_page_path(self):
        self.assertEqual(chrome.page_path('index.html'), '/')
        self.assertEqual(chrome.page_path('about.html'), '/about')
        self.assertIsNone(chrome.page_path('404.html'))

    def test_mark_current_sets_aria_current_on_matching_link_only(self):
        out = chrome.mark_current(NAV, '/research')
        self.assertIn('href="/research" aria-current="page"', out)
        self.assertNotIn('href="/advisory" aria-current', out)

    def test_mark_current_handles_cta_and_none(self):
        self.assertIn('href="/advisory" aria-current="page"', chrome.mark_current(NAV, '/advisory'))
        self.assertEqual(chrome.mark_current(NAV, None), NAV)

    def test_render_replaces_both_blocks(self):
        out = chrome.render(PAGE, NAV, FOOT, '/research')
        self.assertNotIn('OLD NAV', out); self.assertNotIn('OLD FOOT', out)
        self.assertIn('<!-- CHROME:nav -->\n<nav>', out)
        self.assertIn('<footer>f</footer>\n<!-- /CHROME:footer -->', out)
        self.assertIn('aria-current="page"', out)

    def test_render_raises_when_markers_missing(self):
        with self.assertRaises(chrome.MissingMarker):
            chrome.render('<html></html>', NAV, FOOT, '/')

    def test_run_rewrites_files_in_root(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, 'tools', 'chrome'))
            open(os.path.join(d, 'tools', 'chrome', 'nav.html'), 'w').write(NAV)
            open(os.path.join(d, 'tools', 'chrome', 'footer.html'), 'w').write(FOOT)
            open(os.path.join(d, 'research.html'), 'w').write(PAGE)
            changed = chrome.run(d)
            self.assertEqual(changed, ['research.html'])
            self.assertIn('aria-current="page"', open(os.path.join(d, 'research.html')).read())
            self.assertEqual(chrome.run(d), [])  # idempotent

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 3: Run it to see it fail**

```bash
touch tools/tests/__init__.py && python3 -m unittest tools/tests/test_chrome.py 2>&1 | tail -3
```
Expected: `ModuleNotFoundError: No module named 'chrome'`.

- [ ] **Step 4: Write tools/chrome.py**

```python
#!/usr/bin/env python3
"""Write the shared nav and footer into every page. Stdlib only.

    python3 tools/chrome.py          # rewrites *.html in the repo root, prints the files changed

Pages carry two marker pairs:  <!-- CHROME:nav --> ... <!-- /CHROME:nav -->
and                            <!-- CHROME:footer --> ... <!-- /CHROME:footer -->
Sources: tools/chrome/nav.html and tools/chrome/footer.html. The nav link whose
href equals the page's clean URL gets aria-current="page".
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MissingMarker(Exception):
    pass

def page_path(filename):
    """index.html -> '/', about.html -> '/about', 404.html -> None."""
    name = os.path.basename(filename)[:-5]
    if name == 'index':
        return '/'
    if name == '404':
        return None
    return '/' + name

def mark_current(nav_html, path):
    if path is None:
        return nav_html
    return re.sub(r'href="%s"(?! aria-current)' % re.escape(path), 'href="%s" aria-current="page"' % path, nav_html)

def _block(name):
    return re.compile(r'(<!-- CHROME:%s -->)(.*?)(<!-- /CHROME:%s -->)' % (name, name), re.S)

def render(page_html, nav_html, footer_html, path):
    out = page_html
    for name, body in (('nav', mark_current(nav_html, path)), ('footer', footer_html)):
        pat = _block(name)
        if not pat.search(out):
            raise MissingMarker('missing CHROME:%s markers' % name)
        out = pat.sub(lambda m, b=body: m.group(1) + '\n' + b.strip() + '\n' + m.group(3), out, count=1)
    return out

def run(root=ROOT):
    nav = open(os.path.join(root, 'tools', 'chrome', 'nav.html'), encoding='utf-8').read()
    foot = open(os.path.join(root, 'tools', 'chrome', 'footer.html'), encoding='utf-8').read()
    changed = []
    for p in sorted(glob.glob(os.path.join(root, '*.html'))):
        src = open(p, encoding='utf-8').read()
        out = render(src, nav, foot, page_path(p))
        if out != src:
            open(p, 'w', encoding='utf-8').write(out)
            changed.append(os.path.basename(p))
    return changed

if __name__ == '__main__':
    for f in run():
        print('updated', f)
    sys.exit(0)
```

- [ ] **Step 5: Run the tests**

```bash
python3 -m unittest tools/tests/test_chrome.py -v 2>&1 | tail -4
```
Expected: `OK` with 6 tests.

- [ ] **Step 6: Write js/site.js**

```js
/* Matteo Giordano — site.js. Nav toggle, reveal-on-scroll, config wiring, writing list. No network requests except data/writing.json. */
(function () {
  'use strict';
  var cfg = window.MG_CONFIG || {};
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function applyConfig() {
    var email = cfg.CONTACT_EMAIL || '';
    if (/\S+@\S+\.\S+/.test(email)) {
      var m = document.querySelectorAll('[data-mailto]');
      for (var i = 0; i < m.length; i++) {
        var subject = m[i].getAttribute('data-subject');
        m[i].setAttribute('href', 'mailto:' + email + (subject ? '?subject=' + encodeURIComponent(subject) : ''));
        if (m[i].hasAttribute('data-show-email')) m[i].textContent = email;
      }
    }
    var links = document.querySelectorAll('[data-link]');
    for (var j = 0; j < links.length; j++) {
      var key = links[j].getAttribute('data-link');
      if (typeof cfg[key] === 'string' && /^https:\/\//.test(cfg[key])) links[j].setAttribute('href', cfg[key]);
    }
  }

  function initNav() {
    var toggle = document.querySelector('.nav__toggle');
    var links = document.querySelector('.nav__links');
    if (!toggle || !links) return;
    function setOpen(open) {
      links.classList.toggle('is-open', open);
      document.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.querySelector('.nav__toggle-label').textContent = open ? 'Close' : 'Menu';
    }
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      for (var i = 0; i < els.length; i++) els[i].classList.add('is-visible');
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
    for (var j = 0; j < els.length; j++) io.observe(els[j]);
  }

  function initWriting() {
    var list = document.getElementById('writing-list');
    var empty = document.getElementById('writing-empty');
    if (!list || !empty || !window.fetch) return;
    fetch('data/writing.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (items) {
      if (!Array.isArray(items) || !items.length) return;
      items.forEach(function (it) {
        if (!it || !it.title) return;
        var li = document.createElement('li'); li.className = 'writing__item';
        var d = document.createElement('span'); d.className = 'writing__date'; d.textContent = it.date || '';
        var t = document.createElement(it.href ? 'a' : 'span'); t.className = 'writing__title'; t.textContent = it.title;
        if (it.href) { t.setAttribute('href', it.href); t.setAttribute('rel', 'noopener'); t.setAttribute('target', '_blank'); }
        li.appendChild(d); li.appendChild(t); list.appendChild(li);
      });
      if (list.children.length) { list.removeAttribute('hidden'); empty.setAttribute('hidden', ''); }
    }).catch(function () { /* keep the empty state */ });
  }

  function init() { applyConfig(); initNav(); initReveal(); initWriting(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
```

- [ ] **Step 7: Syntax-check site.js with the system JavaScriptCore**

```bash
/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc -e "load('js/site.js')" 2>&1 | head -3 || node --check js/site.js
```
Expected: no `SyntaxError` line (a `ReferenceError: window` is fine: it means the file parsed). If neither `jsc` nor `node` exists, skip; the browser check in Task 11 covers it.

- [ ] **Step 8: Commit**

```bash
git add tools js && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Shared chrome: nav and footer partials, chrome.py, site.js

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: check.py (links, anchors, metadata, DRAFT, sitemap)

**Files:**
- Create: `tools/check.py`, `tools/tests/test_check.py`

**Interfaces:**
- Produces: `python3 tools/check.py [--strict]` exits 0 when clean, 1 with a line per problem. `--strict` also fails on any `<!-- DRAFT -->`. Checks: internal `href`/`src` resolve (`/x` → `x.html` or `x/index.html` or a file; `#id` targets exist in the target page; relative paths exist); every page has `<title>`, `meta name="description"`, `link rel="canonical"`; `sitemap.xml` lists every page except `404.html` and nothing else.

- [ ] **Step 1: Write the failing tests**

`tools/tests/test_check.py`:
```python
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import check

GOOD = ('<!DOCTYPE html><html><head><title>A</title><meta name="description" content="d">'
        '<link rel="canonical" href="https://x/a"></head><body>'
        '<a href="/b#sec">b</a><a href="https://ext/">e</a><img src="img/p.png"><h2 id="here">h</h2></body></html>')
B = ('<!DOCTYPE html><html><head><title>B</title><meta name="description" content="d">'
     '<link rel="canonical" href="https://x/b"></head><body><h2 id="sec">s</h2><a href="/a#here">a</a><!-- DRAFT -->new<!-- /DRAFT --></body></html>')

def site(d, sitemap=True):
    os.makedirs(os.path.join(d, 'img'))
    open(os.path.join(d, 'img', 'p.png'), 'wb').write(b'x')
    open(os.path.join(d, 'a.html'), 'w').write(GOOD)
    open(os.path.join(d, 'b.html'), 'w').write(B)
    if sitemap:
        open(os.path.join(d, 'sitemap.xml'), 'w').write('<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url></urlset>')

class CheckTest(unittest.TestCase):
    def test_clean_site_has_no_problems(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            self.assertEqual(check.problems(d), [])

    def test_strict_reports_draft_markers(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            p = check.problems(d, strict=True)
            self.assertEqual(len(p), 1); self.assertIn('b.html: DRAFT', p[0])

    def test_broken_link_image_anchor_and_meta(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            open(os.path.join(d, 'c.html'), 'w').write('<html><head></head><body><a href="/nope">x</a><a href="/a#missing">y</a><img src="img/no.png"></body></html>')
            open(os.path.join(d, 'sitemap.xml'), 'w').write('<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url><url><loc>https://x/c</loc></url></urlset>')
            p = '\n'.join(check.problems(d))
            for needle in ('c.html: missing <title>', 'c.html: missing meta description', 'c.html: missing canonical',
                           'c.html: broken link /nope', 'c.html: missing anchor /a#missing', 'c.html: missing file img/no.png'):
                self.assertIn(needle, p)

    def test_sitemap_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            open(os.path.join(d, 'sitemap.xml'), 'w').write('<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/zzz</loc></url></urlset>')
            p = '\n'.join(check.problems(d))
            self.assertIn('sitemap.xml: missing page /b', p)
            self.assertIn('sitemap.xml: unknown page /zzz', p)

    def test_404_is_not_required_in_sitemap(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            open(os.path.join(d, '404.html'), 'w').write(GOOD.replace('/b#sec', '/a#here'))
            self.assertEqual(check.problems(d), [])

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run to see it fail**

```bash
python3 -m unittest tools/tests/test_check.py 2>&1 | tail -3
```
Expected: `ModuleNotFoundError: No module named 'check'`.

- [ ] **Step 3: Write tools/check.py**

```python
#!/usr/bin/env python3
"""Static checks for the site. Stdlib only.

    python3 tools/check.py            # links, images, anchors, metadata, sitemap
    python3 tools/check.py --strict   # also fail on any <!-- DRAFT --> marker
Exit 1 and one line per problem when anything is wrong.
"""
import glob, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.srcs, self.ids = [], [], set()
        self.title = self.description = self.canonical = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'a' and a.get('href'): self.hrefs.append(a['href'])
        if tag in ('img', 'script', 'source') and a.get('src'): self.srcs.append(a['src'])
        if tag == 'link':
            if a.get('rel') == 'stylesheet' and a.get('href'): self.srcs.append(a['href'])
            if a.get('rel') == 'canonical' and a.get('href'): self.canonical = True
        if tag == 'meta' and a.get('name') == 'description' and a.get('content'): self.description = True
        if tag == 'title': self.title = True

def scan(path):
    s = Scan(); s.feed(open(path, encoding='utf-8').read()); return s

def page_for(root, url_path):
    """'/about' -> about.html, '/' -> index.html, '/x/' -> x/index.html; None if absent."""
    p = url_path.strip('/')
    cands = [os.path.join(root, 'index.html')] if p == '' else [os.path.join(root, p + '.html'), os.path.join(root, p, 'index.html'), os.path.join(root, p)]
    for c in cands:
        if os.path.isfile(c): return c
    return None

def problems(root=ROOT, strict=False):
    out = []
    pages = sorted(glob.glob(os.path.join(root, '*.html')))
    scans = {p: scan(p) for p in pages}
    for p in pages:
        name = os.path.basename(p); s = scans[p]
        if not s.title: out.append('%s: missing <title>' % name)
        if not s.description: out.append('%s: missing meta description' % name)
        if not s.canonical: out.append('%s: missing canonical' % name)
        if strict and '<!-- DRAFT -->' in open(p, encoding='utf-8').read(): out.append('%s: DRAFT marker present' % name)
        for h in s.hrefs:
            if re.match(r'^(https?:|mailto:|tel:)', h): continue
            if h.startswith('#'):
                if h[1:] and h[1:] not in s.ids: out.append('%s: missing anchor %s' % (name, h))
                continue
            if h.startswith('/'):
                path, _, frag = h.partition('#')
                target = page_for(root, path)
                if not target: out.append('%s: broken link %s' % (name, h)); continue
                if frag and target.endswith('.html') and frag not in (scans.get(target) or scan(target)).ids:
                    out.append('%s: missing anchor %s' % (name, h))
                continue
            if not os.path.isfile(os.path.join(root, h.partition('#')[0])): out.append('%s: missing file %s' % (name, h))
        for src in s.srcs:
            if re.match(r'^https?:', src): out.append('%s: external resource %s' % (name, src)); continue
            rel = src.lstrip('/')
            if not os.path.isfile(os.path.join(root, rel)): out.append('%s: missing file %s' % (name, src))
    sm = os.path.join(root, 'sitemap.xml')
    if os.path.isfile(sm):
        locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', open(sm, encoding='utf-8').read())
        listed = set(re.sub(r'^https?://[^/]+', '', l) or '/' for l in locs)
        expected = set('/' if os.path.basename(p) == 'index.html' else '/' + os.path.basename(p)[:-5] for p in pages if os.path.basename(p) != '404.html')
        for miss in sorted(expected - listed): out.append('sitemap.xml: missing page %s' % miss)
        for extra in sorted(listed - expected): out.append('sitemap.xml: unknown page %s' % extra)
    return out

if __name__ == '__main__':
    probs = problems(strict='--strict' in sys.argv)
    for line in probs: print(line)
    print('check: %d problem(s)' % len(probs))
    sys.exit(1 if probs else 0)
```

- [ ] **Step 4: Run all tests**

```bash
python3 -m unittest discover -s tools/tests -v 2>&1 | tail -4
```
Expected: `OK` with 11 tests.

- [ ] **Step 5: Commit**

```bash
git add tools && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "check.py: links, anchors, metadata, DRAFT and sitemap checks

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## Page shell (used verbatim by Tasks 5 to 10)

Every page is this file with `{{TITLE}}`, `{{DESCRIPTION}}`, `{{PATH}}` (`/`, `/about`, ...) and `{{MAIN}}` filled in. `{{MAIN}}` is the `<main>` element given in each task. The chrome blocks are left as the placeholder shown and filled by `python3 tools/chrome.py`.

```html
<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{TITLE}}</title>
  <meta name="description" content="{{DESCRIPTION}}">
  <!-- ROBOTS:on --><!-- /ROBOTS -->
  <link rel="canonical" href="https://mg-macro.vercel.app{{PATH}}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Matteo Giordano">
  <meta property="og:title" content="{{TITLE}}">
  <meta property="og:description" content="{{DESCRIPTION}}">
  <meta property="og:url" content="https://mg-macro.vercel.app{{PATH}}">
  <meta property="og:image" content="https://mg-macro.vercel.app/img/og-share.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#F6F2EA">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/fonts/SourceSerif4-Semibold.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/SourceSerif4-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/css/site.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <!-- CHROME:nav -->
  <!-- /CHROME:nav -->

  {{MAIN}}

  <!-- CHROME:footer -->
  <!-- /CHROME:footer -->

  <script src="/js/config.js"></script>
  <script src="/js/site.js"></script>
</body>
</html>
```

Rules for `{{MAIN}}`: paragraphs are vault text, edited only for web punctuation (`--` becomes a proper dash or a full stop; `~` separators dropped). Wiki links become site links or external links as the task says. Anything not in the vault is wrapped `<!-- DRAFT --> ... <!-- /DRAFT -->`. After writing each page run `python3 tools/chrome.py && python3 tools/check.py`; the sitemap check will report missing pages until Task 10 creates `sitemap.xml`, which is expected, and the check must otherwise be clean.

---

### Task 5: Home page

**Files:**
- Create: `index.html`

Head values: TITLE `Dr Matteo Giordano — Macro-financial strategist`; DESCRIPTION `Macro-financial strategist: shipping, monetary structures, and off-balance-sheet finance. Co-founder of Garrison Sterling, Associate Researcher at the Global Climate Forum, PhD SOAS.`; PATH `/`.

- [ ] **Step 1: Write index.html from the shell with this `<main>`**

```html
  <main id="main">
    <header class="hero" aria-labelledby="hero-title">
      <div class="wrap">
        <p class="eyebrow">Dr Matteo Giordano</p>
        <!-- DRAFT -->
        <h1 class="hero__title" id="hero-title">Macro-financial strategist. Shipping, monetary structures, and off-balance-sheet finance.</h1>
        <p class="hero__roles"><span>Macro strategist, shipping industry</span><span class="sep" aria-hidden="true">·</span><span>Co-founder and Director, <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a></span><span class="sep" aria-hidden="true">·</span><span>Associate Researcher, <a href="https://globalclimateforum.org/portfolio-item/matteo-giordano/" rel="noopener">Global Climate Forum</a></span></p>
        <!-- /DRAFT -->
        <nav class="hero__links" aria-label="Contact and profiles">
          <a href="mailto:mg.macroeconomics@gmail.com" data-mailto>Email</a>
          <a href="https://cargoandcollateral.substack.com/" data-link="SUBSTACK_URL" rel="noopener" target="_blank">Cargo &amp; Collateral</a>
          <a href="https://app.box.com/s/18pq9r7919gcxvu23hk5v4wda4hq6dq4" data-link="CV_URL" rel="noopener" target="_blank">CV</a>
          <a href="https://www.linkedin.com/in/matteogiordano-economist/" data-link="LINKEDIN_URL" rel="noopener" target="_blank">LinkedIn</a>
          <a href="https://orcid.org/0000-0002-1588-6735" data-link="ORCID_URL" rel="noopener" target="_blank">ORCID</a>
        </nav>
      </div>
    </header>

    <section class="statement" aria-label="The method">
      <div class="wrap">
        <p class="statement__text reveal">Financial systems are claims and obligations: who owes what to whom, on whose balance sheet, funded how. Read that way, a rearmament programme is a working-capital cycle before it is a capability, and freight is a credit business wearing logistics clothes, where the credit is what breaks first. The method came out of the euro area: repo, collateral, TARGET, sovereign debt. It does not stay there.</p>
      </div>
    </section>

    <section class="block" aria-labelledby="bio-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="bio-title">In brief</h2>
        <div class="block__body reveal">
          <p>Macro strategist and financial analyst in the shipping industry, based in Greece. Co-founder and Director of <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a>, an independent defence economics firm. Associate Researcher at the <a href="https://globalclimateforum.org/portfolio-item/matteo-giordano/" rel="noopener">Global Climate Forum</a>, Berlin, behind the balance-sheet models of the <a href="https://obfa-transform.eu" rel="noopener">OBFA-TRANSFORM Project</a> and the <a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a>.</p>
          <p>PhD in economics, SOAS University of London: monetary subordination in the euro area, under Prof. Costas Lapavitsas; lecturer there to 2025. To September 2026, defence economist at the <a href="https://www.ukdsc.org" rel="noopener">UKDSC</a>, inside the <a href="https://www.gov.uk/government/organisations/ministry-of-defence" rel="noopener">Ministry of Defence</a> ecosystem. Dual Italian-British national.</p>
          <p><a href="/about">The full record</a></p>
        </div>
      </div>
    </section>

    <section class="block" aria-labelledby="lines-title">
      <div class="wrap">
        <h2 class="block__title reveal" id="lines-title">Four lines of work</h2>
        <ol class="lines" style="margin-top:24px">
          <li class="line reveal">
            <span class="line__n" aria-hidden="true">1</span>
            <h3 class="line__title">Shipping and trade finance</h3>
            <p>The freight rate is the output; the credit chain is the mechanism. Chartering and freight rates, port throughput and tonne-mile demand, forwarder and carrier working capital, and the financing behind a single shipment, read from inside the industry rather than off a screen.</p>
            <a class="line__more" href="/cargo-and-collateral">Cargo &amp; Collateral, the newsletter</a>
          </li>
          <li class="line reveal">
            <span class="line__n" aria-hidden="true">2</span>
            <h3 class="line__title">Macro-financial strategy and research</h3>
            <p>Where the pressure sits in a system, and what it takes to move it. Commissioned structural reads for ship finance and freight, and for allocators and credit funds, on a sovereign, a sector or a market structure.</p>
            <a class="line__more" href="/advisory">Scope and terms</a>
          </li>
          <li class="line reveal">
            <span class="line__n" aria-hidden="true">3</span>
            <h3 class="line__title">Defence and security economics</h3>
            <p>Capability is downstream of industrial structure and financing. The defence-industrial base read as an economy: where supply-chain and strategic dependencies concentrate, what industrial resilience actually requires, and whether sustained rearmament can be financed at all. The commercial side runs through Garrison Sterling.</p>
            <a class="line__more" href="/research#defence">The research</a>
          </li>
          <li class="line reveal">
            <span class="line__n" aria-hidden="true">4</span>
            <h3 class="line__title">Monetary architecture and hierarchy</h3>
            <p>Money is a hierarchy of interlocking balance sheets; a crisis is the moment they stop clearing. Collateral, repo, TARGET and subordination in the euro area, mapped that way, with the Global Climate Forum's OBFA-TRANSFORM project and its public Monetary Architecture tool.</p>
            <a class="line__more" href="/research#monetary-architecture">The projects</a>
          </li>
        </ol>
      </div>
    </section>

    <section class="block" aria-labelledby="papers-title">
      <div class="wrap block__grid">
        <div>
          <h2 class="block__title reveal" id="papers-title">Academic roots</h2>
        </div>
        <div class="block__body reveal">
          <p>Peer-reviewed work on the euro area: monetary hierarchy, repo markets, TARGET balances, subordination. Not a line of work in itself; it is why the reads hold up.</p>
          <ul class="papers" style="margin-top:20px">
            <li>Lapavitsas, C. &amp; Giordano, M. (2026). <a href="https://doi.org/10.1017/elo.2025.10043" rel="noopener">ECB monetary policy in a quandary</a>, <em>European Law Open</em>.</li>
            <li>Giordano, M. (2025). <a href="https://doi.org/10.1177/10245294251400025" rel="noopener">Monetary Subordination in the Eurozone: Pillars and Asymmetries</a>, <em>Competition &amp; Change</em>.</li>
            <li>Murau, S., Goghie, A. &amp; Giordano, M. (2025). <a href="https://doi.org/10.1093/jfr/fjaf003" rel="noopener">Encumbered Security? Vertical and Horizontal Repos in the Euro Area</a>, <em>Journal of Financial Regulation</em>.</li>
            <li>Murau, S. &amp; Giordano, M. (2024). <a href="https://doi.org/10.1093/ser/mwad067" rel="noopener">Forging monetary unification through novation: the TARGET system</a>, <em>Socio-Economic Review</em>.</li>
          </ul>
          <p style="margin-top:20px"><a href="/publications">All publications and talks</a></p>
        </div>
      </div>
    </section>

    <section class="block" aria-labelledby="affil-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="affil-title">Affiliations</h2>
        <ul class="affil reveal">
          <li><a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a></li>
          <li><a href="https://globalclimateforum.org/portfolio-item/matteo-giordano/" rel="noopener">Global Climate Forum</a></li>
          <li><a href="https://www.soas.ac.uk/about/matteo-giordano-0" rel="noopener">SOAS University of London</a></li>
          <li><a href="https://www.ukdsc.org" rel="noopener">UKDSC</a> (to September 2026)</li>
          <li><a href="https://wearesparc.org/" rel="noopener">SPARCollective</a></li>
          <li>EReNSEP</li>
          <li>YSI, Institute for New Economic Thinking</li>
        </ul>
      </div>
    </section>
  </main>
```

Note on the three `style="margin-top:..."` attributes: inline *style attributes* do not violate the CSP (`style-src` is not restricted by `default-src 'self'` for attributes in the way inline `<style>` elements are; Vercel + Chrome accept them). If the browser console in Task 11 reports a CSP style violation, move them into `css/site.css` as `.lines { margin-top: 24px } .papers { margin-top: 20px } .papers + p { margin-top: 20px }` and delete the attributes.

- [ ] **Step 2: Run chrome and check, then count words**

```bash
python3 tools/chrome.py && python3 tools/check.py; python3 - <<'PY'
import re,html
s=open('index.html',encoding='utf-8').read()
m=re.search(r'<main.*?</main>',s,re.S).group(0)
t=html.unescape(re.sub(r'<[^>]+>',' ',m))
print('home words:',len(t.split()))
PY
```
Expected: `updated index.html`; the only problems are `broken link` lines for pages not yet built (`/about`, `/advisory`, `/research`, `/publications`, `/cargo-and-collateral`); nothing else. Home words under 500.

- [ ] **Step 3: Commit**

```bash
git add index.html && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Home page

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: Advisory page

**Files:**
- Create: `advisory.html`

Head values: TITLE `Advisory — Matteo Giordano`; DESCRIPTION `Macro-financial strategy for institutions that need to know how a system clears before they need to know where it trades. Shipping and trade finance, sovereign credit and monetary structure, balance-sheet modelling.`; PATH `/advisory`.

- [ ] **Step 1: Write advisory.html from the shell with this `<main>`**

```html
  <main id="main">
    <header class="page-head">
      <div class="wrap">
        <p class="eyebrow reveal">Advisory</p>
        <h1 class="page-title reveal">Macro-financial strategy for institutions that need to know how a system clears before they need to know where it trades.</h1>
        <p class="lede lede--ink reveal">I take commissioned work from two directions. Ship finance and freight: lenders, lessors, owners, marine insurers and platforms. Allocators and credit funds: where the question is euro-area sovereign and monetary risk read structurally rather than off the spread. The brief is usually a version of the same one: below the headline, what is the actual structure of claims here, where does the pressure sit, and what breaks first.</p>
        <a class="btn reveal" href="mailto:mg.macroeconomics@gmail.com?subject=Advisory%20brief" data-mailto data-subject="Advisory brief">Discuss a brief</a>
      </div>
    </header>

    <section class="block" aria-labelledby="areas-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="areas-title">Areas</h2>
        <ul class="areas">
          <li class="area reveal">
            <h3 class="area__title">Shipping and trade finance</h3>
            <p>Freight exposure is working-capital exposure. Chartering and freight-rate risk, tonne-mile and throughput demand, forwarder and carrier working capital, trade finance structures, and the capital stack behind a fleet, including Greek and Mediterranean maritime economics. From inside the industry, and written up in <a href="/cargo-and-collateral">Cargo &amp; Collateral</a>.</p>
          </li>
          <li class="area reveal">
            <h3 class="area__title">Sovereign credit and monetary structure</h3>
            <p>Read at the level of the mechanism, not the spread. Sovereign risk and debt management, monetary transmission, collateral and repo, fragmentation and the euro-area settlement plumbing beneath it. Where the structural view comes from: <a href="/research#eurozone">the eurozone</a>, <a href="/research#subordination">subordination</a>, <a href="/research#macro-structures-dmo">macro-structure and debt management</a>.</p>
          </li>
          <li class="area reveal">
            <h3 class="area__title">Balance-sheet modelling</h3>
            <p>For questions that need a structure rather than a forecast. Bespoke modelling of a monetary architecture, a sector or a firm as interlocking balance sheets, built to be interrogated rather than believed. Method: <a href="/research#balance-sheet-modelling">balance-sheet modelling</a>.</p>
          </li>
        </ul>
      </div>
    </section>

    <section class="block" aria-labelledby="delivered-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="delivered-title">Delivered work</h2>
        <!-- Append anonymised engagements below in the same pattern:
             <li><strong>[Who, by type and geography].</strong> [The question they brought.] [What was delivered.]</li> -->
        <ul class="delivered">
          <li class="reveal"><strong>A public analytical tool.</strong> The <a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a>, built with the Global Climate Forum: the euro area's monetary architecture rendered as navigable, practitioner-facing balance-sheet analysis, open to anyone.</li>
          <li class="reveal"><strong>Models built to be interrogated.</strong> Balance-sheet and stock-flow-consistent models of monetary architectures; Input-Output and scenario models of the defence-industrial base; long-run financial-flow analysis.</li>
          <li class="reveal"><strong>Briefings to government and industry.</strong> Strategic briefings and decision-relevant economic assessments delivered at the UKDSC, inside the Ministry of Defence ecosystem. Reports that contributed to shaping MoD policy on measuring defence-industrial productivity, evaluating programme viability, assessing supply-chain resilience and vulnerability, and defining industrial readiness.</li>
        </ul>
      </div>
    </section>

    <section class="block" aria-labelledby="engage-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="engage-title">Ways to engage</h2>
        <div class="block__body reveal">
          <ul class="engage">
            <li><strong>Expert calls.</strong> A single conversation on a specific question.</li>
            <li><strong>Commissioned notes and models.</strong> A defined question, a defined deliverable, a fixed deadline.</li>
            <li><strong>Speaking and workshops.</strong> Talks, seminars and closed-door briefings.</li>
          </ul>
          <p style="margin-top:24px">Anything where the exposure is defence, whether defence-industrial, rearmament, or macro-financial work on the defence economy, goes through <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a>, the defence economics firm I co-founded and direct. Shipping, sovereign and monetary work is taken here, in a personal capacity.</p>
        </div>
      </div>
    </section>

    <section class="closing" aria-label="Get in touch">
      <div class="wrap">
        <p class="closing__line reveal">To discuss a brief, write to me. Background: <a href="/about">About</a> and <a href="/publications">Publications</a>.</p>
        <a class="btn reveal" href="mailto:mg.macroeconomics@gmail.com?subject=Advisory%20brief" data-mailto data-subject="Advisory brief">mg.macroeconomics@gmail.com</a>
        <p class="note reveal">All engagements are undertaken in a personal capacity and are independent of any employer, past or present, and of Garrison Sterling. Nothing produced under them is investment advice. See the <a href="/disclaimer">disclaimer</a>.</p>
      </div>
    </section>
  </main>
```

- [ ] **Step 2: Run chrome and check**

```bash
python3 tools/chrome.py && python3 tools/check.py
```
Expected: `updated advisory.html`; the only problems are `broken link` lines for pages not yet built and nothing else (no missing file, no missing metadata).

- [ ] **Step 3: Commit**

```bash
git add advisory.html && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Advisory page

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: Research page and figures

**Files:**
- Create: `research.html`, `img/figures/*.png|jpg`, `img/figures/full/*`

Head values: TITLE `Research — Matteo Giordano`; DESCRIPTION `Research behind the four lines of work: shipping and trade finance, macro-financial strategy, defence and security economics, monetary architecture and hierarchy in the euro area.`; PATH `/research`.

- [ ] **Step 1: Copy originals and make web versions**

```bash
A="$VAULT/Attachments"
for f in Macro_Structure T2_EoP_plot Liabilities_nonEA_Euro_Plot Origin_Collateral_plot Italy_T2_Fdec_BoP_Cumulative_Plot Subordination_EMU GEGIStudy; do cp "$A/$f.png" img/figures/full/; done
for f in T2_EoP_plot Liabilities_nonEA_Euro_Plot Origin_Collateral_plot Italy_T2_Fdec_BoP_Cumulative_Plot; do sips -Z 1600 "img/figures/full/$f.png" --out "img/figures/$f.png" >/dev/null; done
cp img/figures/full/Macro_Structure.png img/figures/Macro_Structure.png
cp img/figures/full/Subordination_EMU.png img/figures/Subordination_EMU.png
sips -s format jpeg -s formatOptions 85 img/figures/full/GEGIStudy.png --out img/figures/GEGIStudy.jpg >/dev/null
for f in img/figures/*.png img/figures/*.jpg; do printf "%-45s" "$f"; sips -g pixelWidth -g pixelHeight "$f" | awk '/pixel/{printf "%s ",$2}'; ls -l "$f" | awk '{print $5}'; done
```
Expected: the four plots at 1600×889, Macro_Structure 1178×1020, Subordination_EMU 841×595, GEGIStudy.jpg 209×297. Record the dimensions: they go into `width`/`height` attributes below (already filled in with these expected values).

- [ ] **Step 2: Write research.html from the shell with this `<main>`**

```html
  <main id="main">
    <header class="page-head">
      <div class="wrap">
        <p class="eyebrow reveal">Research</p>
        <!-- DRAFT -->
        <h1 class="page-title reveal">The projects behind the four lines of work.</h1>
        <!-- /DRAFT -->
        <p class="lede reveal">Each project carries its own argument, data and outputs. The published record is on <a class="link" href="/publications">Publications</a>; commissioned work in these areas runs through <a class="link" href="/advisory">Advisory</a>.</p>
      </div>
    </header>

    <section class="section" id="shipping" aria-labelledby="shipping-title">
      <div class="wrap">
        <h2 class="section__title reveal" id="shipping-title">Shipping and trade finance</h2>
        <div class="project reveal" id="cargo-and-collateral">
          <div><h3 class="project__title">Cargo &amp; Collateral</h3><span class="project__meta">Newsletter, ongoing</span></div>
          <div class="project__body">
            <p>Chartering, freight rates, port throughput, forwarder and carrier working capital and trade finance, read as claims and obligations. One original chart an entry, with its source named.</p>
            <div class="project__links"><a href="/cargo-and-collateral">About the newsletter</a><a href="https://cargoandcollateral.substack.com/" data-link="SUBSTACK_URL" rel="noopener" target="_blank">Read it on Substack</a></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="macro-strategy" aria-labelledby="macro-title">
      <div class="wrap">
        <h2 class="section__title reveal" id="macro-title">Macro-financial strategy and research</h2>
        <div class="project reveal" id="macro-structures-dmo">
          <div><h3 class="project__title">Macro-Structure, DMOs and Monetary Regimes</h3><span class="project__meta">With Enrico Pulieri, in preparation</span></div>
          <div class="project__body">
            <p>Central bank independence is half the story. Sovereign debt is managed by a separate institution with its own claim to independence, and the two postures interact. This project reads monetary policy and debt management as one architecture rather than two literatures, and situates both inside the systemic structure of financialised capitalism.</p>
            <figure class="figure">
              <img src="/img/figures/Macro_Structure.png" alt="Diagram of the macro-structure: the systemic relations between monetary policy, debt management and the financial architecture." width="1178" height="1020" loading="lazy" decoding="async">
              <figcaption class="figure__caption">The macro-structure of financialised capitalism.<a class="figure__link" href="/img/figures/full/Macro_Structure.png">Full size</a></figcaption>
            </figure>
            <h3>Macro-structure</h3>
            <p>A conceptualisation of the systemic relations, architectures and tendencies running through financialised capitalism.</p>
            <h3>Debt management operations</h3>
            <p>The political economy of debt management: whether DMO "independence" holds, and where debt management offices work with the central bank or against it.</p>
            <h3>Monetary regime</h3>
            <p>Central-bank posture is not readable from policy decisions alone. Placing those decisions inside the financial architecture and the instruments available is what makes the regime visible.</p>
            <div class="project__links"><a href="/publications#in-preparation">Giordano and Pulieri, forthcoming</a><a href="https://doi.org/10.31235/osf.io/rw3ms" rel="noopener">Giordano and Goghie (2023)</a></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="defence" aria-labelledby="defence-title">
      <div class="wrap">
        <h2 class="section__title reveal" id="defence-title">Defence and security economics</h2>
        <p class="section__intro reveal">Modelling the economics of the defence-industrial base: industrial linkages, supply-chain resilience, and the fiscal sustainability of security spending.</p>
        <div class="project reveal" id="defence-industrial-base">
          <div><h3 class="project__title">Modelling the defence-industrial base</h3><span class="project__meta">Applied work, 2025 to 2026</span></div>
          <div class="project__body">
            <p>Capability is downstream of industrial structure and financing. This strand applies macro-financial and structural economics to defence, asking the questions that run through the rest of my research, how a system absorbs shocks, where dependencies concentrate, what it costs to hold capability over time, of the defence-industrial base rather than the monetary system.</p>
            <p>It was the substance of my work as a defence economist at the UKDSC to September 2026. It continues commercially at <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a>, the defence economics firm I co-founded and direct, and as research here: applied, quantitative, and aimed at decision-relevant intelligence for policy and industry.</p>
            <h3>Defence-industrial structure and resilience</h3>
            <p>Where supply-chain and strategic dependencies concentrate, and what industrial resilience actually requires. Input-Output modelling traces inter-sectoral linkages and spillovers across strategic sectors, alongside sector-level industrial assessment.</p>
            <h3>Alliances, trade and burden-sharing</h3>
            <p>The economics of security cooperation and defence trade. Gravity models of bilateral defence and industrial flows, including NATO and allied contexts, and the structural forces shaping them.</p>
            <h3>Fiscal sustainability of defence</h3>
            <p>Whether elevated defence commitments can be financed over the long run. This connects defence spending to sovereign debt dynamics, fiscal-monetary interaction, and the macroeconomic constraints studied elsewhere on this site.</p>
            <h3>Capability, productivity and measurement</h3>
            <p>Frameworks for measuring defence-industrial productivity and performance, and scenario-based assessment of investment gaps and capability shortfalls. Stock-flow-consistent accounting, VAR models and scenario analysis.</p>
            <h3>Method</h3>
            <p>The toolkit mirrors the macro-financial work: Input-Output and gravity modelling, stock-flow-consistent and VAR frameworks, time-series and panel methods, and scenario analysis, combined with qualitative industrial assessment and stakeholder engagement.</p>
            <p class="note">This section describes research themes and methods only. It does not represent, and should not be read as, the views, positions, or outputs of the UK Defence Solutions Centre, the Ministry of Defence, Garrison Sterling, or any defence industry partner. See the <a href="/disclaimer">disclaimer</a>.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="monetary-architecture" aria-labelledby="monetary-title">
      <div class="wrap">
        <h2 class="section__title reveal" id="monetary-title">Monetary architecture and hierarchy</h2>
        <p class="section__intro reveal">Money as a hierarchy of interlocking balance sheets, crises as the moment they stop clearing. The methodological core of everything else here.</p>

        <div class="project reveal" id="balance-sheet-modelling">
          <div><h3 class="project__title">Balance-Sheet Modelling and Monetary Architecture</h3><span class="project__meta">Ongoing, with the Global Climate Forum</span></div>
          <div class="project__body">
            <p>Balance-sheet modelling makes the structure visible, traces how elasticity and stress propagate through it, and carries both historical analysis and forward scenarios.</p>
            <h3>The Monetary Architecture framework</h3>
            <p>As Associate Researcher at the Global Climate Forum I contribute to the <a href="https://obfa-transform.eu" rel="noopener">OBFA-TRANSFORM Project</a> and helped build the <a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a>: the euro area's architecture rendered as navigable, practitioner-facing balance-sheet analysis.</p>
            <h3>Long-run financial-flow dynamics</h3>
            <p>Trade, capital and financial flows from 1870 to the present, read for structural breaks and regime shifts in globalisation and financial integration, and linked to scenarios for financing large-scale transformation.</p>
            <h3>Crisis dynamics through balance sheets</h3>
            <p>Structured process-tracing combined with balance-sheet visualisation, used to explain crisis-driven institutional change, applied to the transformation of the euro-area architecture from the Global Financial Crisis onward.</p>
            <h3>Method</h3>
            <p>Balance-sheet mapping and visualisation, stock-flow-consistent accounting, long-run time-series analysis, and scenario frameworks, on primary and secondary data across private and public sectors.</p>
            <div class="project__links"><a href="https://monetary-architecture.com/" rel="noopener">Try the tool</a></div>
          </div>
        </div>

        <div class="project reveal" id="eurozone">
          <div><h3 class="project__title">Asymmetries, Imbalances and Fragmentation in the Eurozone</h3><span class="project__meta">Ongoing</span></div>
          <div class="project__body">
            <p>The euro area's imbalances are built into its infrastructure. This project traces them to the plumbing, CCPs, CSDs, the ECB and the national central banks, and to the link between monetary integration and the financialisation of the member economies. Three empirical pillars, built on official datasets that are largely unused.</p>
            <figure class="figure">
              <img src="/img/figures/T2_EoP_plot.png" alt="Chart of TARGET2 end-of-period balances by national central bank over time." width="1600" height="889" loading="lazy" decoding="async">
              <figcaption class="figure__caption">TARGET2 balances, end of period.<a class="figure__link" href="/img/figures/full/T2_EoP_plot.png">Full size</a></figcaption>
            </figure>
            <h3>Monetary hierarchies in the EMU</h3>
            <p>Jurisdictions are tiered and legacy euros persist. TARGET is the backstop that holds the tiering together.</p>
            <figure class="figure">
              <img src="/img/figures/Liabilities_nonEA_Euro_Plot.png" alt="Chart of euro-denominated liabilities held outside the euro area." width="1600" height="889" loading="lazy" decoding="async">
              <figcaption class="figure__caption">Euro liabilities outside the euro area.<a class="figure__link" href="/img/figures/full/Liabilities_nonEA_Euro_Plot.png">Full size</a></figcaption>
            </figure>
            <h3>Fragmentation and selective integration</h3>
            <p>Money markets fragment even with liquidity in excess. The shortage that binds is collateral.</p>
            <figure class="figure">
              <img src="/img/figures/Origin_Collateral_plot.png" alt="Chart of the origin of collateral used in euro-area refinancing operations." width="1600" height="889" loading="lazy" decoding="async">
              <figcaption class="figure__caption">Origin of collateral in Eurosystem refinancing.<a class="figure__link" href="/img/figures/full/Origin_Collateral_plot.png">Full size</a></figcaption>
            </figure>
            <h3>Capital and liquidity in hybrid refinancing</h3>
            <p>Where TARGET balances actually come from, and how the hybrid working of the mechanism produces them.</p>
            <figure class="figure">
              <img src="/img/figures/Italy_T2_Fdec_BoP_Cumulative_Plot.png" alt="Chart decomposing Italy's cumulative TARGET2 balance by balance-of-payments component." width="1600" height="889" loading="lazy" decoding="async">
              <figcaption class="figure__caption">Italy: TARGET2 balance decomposed through the balance of payments, cumulative.<a class="figure__link" href="/img/figures/full/Italy_T2_Fdec_BoP_Cumulative_Plot.png">Full size</a></figcaption>
            </figure>
          </div>
        </div>

        <div class="project reveal" id="subordination">
          <div><h3 class="project__title">Monetary Subordination in the Eurozone</h3><span class="project__meta">PhD thesis, SOAS University of London, 2025. Supervisor: Prof. Costas Lapavitsas</span></div>
          <div class="project__body">
            <p>Subordination inside a monetary union is obvious in aggregate, persistent yield spreads, divergent productivity, and elusive in its specific forms. This thesis identifies the forms.</p>
            <p>The argument starts from monetary subordination as the vertex of subordination, and from the peculiarity of a monetary union: it is the most extreme form of monetary integration, which makes subordination more visible in appearance and more subtle in mechanism at the same time. Shared money formalises it.</p>
            <figure class="figure">
              <img src="/img/figures/Subordination_EMU.png" alt="Diagram of the three pillars of monetary subordination in the EMU: monetary hierarchies, hybrid money, and selective fragmentation." width="841" height="595" loading="lazy" decoding="async">
              <figcaption class="figure__caption">The three pillars of monetary subordination in the EMU.<a class="figure__link" href="/img/figures/full/Subordination_EMU.png">Full size</a></figcaption>
            </figure>
            <h3>Three pillars</h3>
            <p>Monetary subordination in the EMU rests on monetary hierarchies, hybrid money, and the selective fragmentation and integration of euro-area markets and institutions. Each is taken twice: as it appears, and through the mechanisms that sustain it, with empirical support from official datasets that are largely unused, balance-sheet analysis and graphical representation.</p>
            <h3>Consequences</h3>
            <p><strong>Italy.</strong> The single currency did not remove subordination; it reframed it. The centre shifted from the USD-based international system to a euro-centric form, with direct consequences for domestic economic development. Italy's financial and economic fragility cannot be fully read without that lens.</p>
            <p><strong>Six member states.</strong> A comparative analysis of financialisation shows subordinated EMU members behaving like subordinated emerging markets: their financialisation is shaped by their position in the hierarchy.</p>
            <div class="project__links"><a href="https://soas-repository.worktribe.com/output/461747" rel="noopener">The thesis</a><a href="https://doi.org/10.1177/10245294251400025" rel="noopener">Giordano (2025), Competition &amp; Change</a><a href="https://doi.org/10.1093/ser/mwad067" rel="noopener">Murau and Giordano (2024), Socio-Economic Review</a></div>
          </div>
        </div>

        <div class="project reveal" id="gegi-study">
          <div><h3 class="project__title">Transformation of the Eurozone Architecture</h3><span class="project__meta">S. Murau, A. S. Goghie, M. Giordano and F. Reimer. GEGI Study, Global Development Policy Center, Boston University, 2025</span></div>
          <div class="project__body">
            <figure class="figure figure--cover">
              <img src="/img/figures/GEGIStudy.jpg" alt="Cover of the GEGI Study: Transformation of the Eurozone Architecture." width="209" height="297" loading="lazy" decoding="async">
            </figure>
            <p>The Eurocrisis is usually explained by excessive sovereign issuance, a weak Stability and Growth Pact, or missing supranational supervision. None of those explains how a US-centric run on shadow money reached some EMU treasuries and not others.</p>
            <p>Our answer: it travelled through euro-area repo markets and the Eurosystem's collateral framework. Contagion across the private and public balance sheets of the eurozone and US monetary architectures was the endogenous force that determined the EMU's transformation into its contemporary shape, from the Global Financial Crisis to the 2014 asset purchase programmes.</p>
            <h3>Method</h3>
            <p>Structured process-tracing combined with balance-sheet visualisation of crisis dynamics, built on the macro-financial model developed in Murau (2020) and on primary and secondary sources with private and public sector data. The analytical scheme runs in three steps: on-balance-sheet contraction; activation of inbuilt elasticity-provision mechanisms; and, where those fail, innovation: enhanced elasticity space, new instruments, or new institutions.</p>
            <div class="project__links"><a href="https://doi.org/10.2139/ssrn.5648890" rel="noopener">Read the study on SSRN</a><a href="https://obfa-transform.eu/key-concepts/monetary-architecture" rel="noopener">The framework</a><a href="https://monetary-architecture.com/" rel="noopener">The tool</a></div>
          </div>
        </div>
      </div>
    </section>
  </main>
```

- [ ] **Step 3: Run chrome and check**

```bash
python3 tools/chrome.py && python3 tools/check.py
```
Expected: `updated research.html`; the advisory `/research#...` anchors now resolve; the only problems are `broken link` lines for `/publications`, `/cargo-and-collateral`, `/about`, `/disclaimer`.

- [ ] **Step 4: Commit**

```bash
git add research.html img && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Research page with figures

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8: Publications page

**Files:**
- Create: `publications.html`, `img/state-of-capitalism.jpg`

Head values: TITLE `Publications — Matteo Giordano`; DESCRIPTION `Peer-reviewed articles, working papers and books on monetary economics, financial regulation and European political economy, with selected talks.`; PATH `/publications`.

- [ ] **Step 1: Cover image**

```bash
sips -s format jpeg -s formatOptions 85 "$VAULT/Attachments/StateofCapitalism.png" --out img/state-of-capitalism.jpg >/dev/null && sips -g pixelWidth -g pixelHeight img/state-of-capitalism.jpg
```
Expected: 286 × 437.

- [ ] **Step 2: Write publications.html from the shell with this `<main>`**

```html
  <main id="main">
    <header class="page-head">
      <div class="wrap">
        <p class="eyebrow reveal">Publications</p>
        <!-- DRAFT -->
        <h1 class="page-title reveal">Peer-reviewed articles, working papers, and books.</h1>
        <!-- /DRAFT -->
        <p class="lede reveal">Across monetary economics, financial regulation, and European political economy. Full list also on <a class="link" href="https://orcid.org/0000-0002-1588-6735" data-link="ORCID_URL" rel="noopener" target="_blank">ORCID</a>.</p>
      </div>
    </header>

    <section class="block" id="published" aria-labelledby="published-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="published-title">Published</h2>
        <ol class="pubs reveal">
          <li>Lapavitsas, C. and Giordano, M. 2026. "ECB monetary policy in a quandary", <em>European Law Open</em>. <a href="https://doi.org/10.1017/elo.2025.10043" rel="noopener">DOI</a></li>
          <li>Murau, S., Goghie, A., Giordano, M. and Reimer, F. 2025. "Transformation of the Eurozone Architecture. Crises and Institutional Change in the Offshore US-Dollar System", <em>GEGI Study</em>, Global Development Policy Center, Boston University. <a href="https://doi.org/10.2139/ssrn.5648890" rel="noopener">DOI</a></li>
          <li>Giordano, M. 2025. "Monetary Subordination in the Eurozone: Pillars and Asymmetries", <em>Competition &amp; Change</em>. <a href="https://doi.org/10.1177/10245294251400025" rel="noopener">DOI</a></li>
          <li>Giordano, M. 2025. "Displacement and Complementarity between Cryptocurrencies and Legacy Money", <em>The Japanese Political Economy</em>. <a href="https://doi.org/10.1080/2329194X.2025.2547035" rel="noopener">DOI</a></li>
          <li>Giordano, M. 2025. "Tiered Euro-Monies: Perpetrating Monetary Hierarchies from the ECU to the Euro", <em>Review of Evolutionary Political Economy</em>, 6: 565–587. <a href="https://doi.org/10.1007/s43253-025-00154-4" rel="noopener">DOI</a></li>
          <li>Giordano, M. 2025. <em>Monetary Subordination in the Eurozone: Fragmentation and tiering of markets and institutions</em>. PhD thesis, SOAS University of London. <a href="https://soas-repository.worktribe.com/output/461747" rel="noopener">Repository</a></li>
          <li>Murau, S., Goghie, A. and Giordano, M. 2025. "Encumbered Security? Vertical and Horizontal Repos in the Euro Area and Their Inherent Ambiguity", <em>Journal of Financial Regulation</em>, 11(2). <a href="https://doi.org/10.1093/jfr/fjaf003" rel="noopener">DOI</a></li>
          <li>Giordano, M. 2024. "Monetary Subordination in the Eurozone: Pillars and Asymmetries", <em>SSRN Working Paper</em>. <a href="https://ssrn.com/abstract=4911906" rel="noopener">SSRN</a></li>
          <li>Murau, S., Goghie, A. and Giordano, M. 2024. "Encumbered Security? Conceptualising Vertical and Horizontal Repos in the Euro Area", <em>SOAS Working Paper 262</em>. <a href="https://www.soas.ac.uk/sites/default/files/2024-04/economics-wp262.pdf" rel="noopener">PDF</a></li>
          <li>Murau, S. and Giordano, M. 2024. "Forging Monetary Unification through Novation. The TARGET System and the Politics of Central Banking in Europe", <em>Socio-Economic Review</em>, 22(3): 1283–1312. <a href="https://doi.org/10.1093/ser/mwad067" rel="noopener">DOI</a></li>
          <li>Giordano, M. and Lapavitsas, C. 2023. "Persistent institutional malfunctioning in the Eurozone", <em>The Japanese Political Economy</em>, 49(4): 295–307. <a href="https://doi.org/10.1080/2329194X.2023.2289883" rel="noopener">DOI</a></li>
          <li id="state-of-capitalism">Lapavitsas, C. and the EReNSEP Writing Collective. 2023. <em>The State of Capitalism: Economy, Society, and Hegemony after the Pandemic</em>. London: Verso. <a href="https://www.versobooks.com/en-gb/products/2727-the-state-of-capitalism" rel="noopener">Verso</a></li>
          <li>Giordano, M. and Goghie, A. 2023. "From Policy to Regime: the changing posture of the ECB between liquidity and collateral through the lens of Monetary Regime", <em>SocArXiv Working Paper</em>. <a href="https://doi.org/10.31235/osf.io/rw3ms" rel="noopener">DOI</a></li>
          <li>Murau, S. and Giordano, M. 2022. "European Monetary Unification through Novation: The Political Economy of the TARGET System", <em>SocArXiv Working Paper</em>. <a href="https://osf.io/preprints/socarxiv/k3nbh" rel="noopener">Preprint</a></li>
          <li>Lapavitsas, C., Meadway, J., Nicholls, D. and Giordano, M. 2022. "The True Causes of Inflation: Weak Production and High Profits", PEF and GFTU. <a href="https://www.nautilusint.org/globalassets/public-resources/pdfs/the_real_causes_of_inflation_gftu.pdf" rel="noopener">PDF</a></li>
          <li>Giordano, M. 2020. <em>It Seems as Though We Live to Wait</em>. Independently published.</li>
        </ol>
      </div>
    </section>

    <section class="block" id="in-preparation" aria-labelledby="prep-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="prep-title">In preparation and review</h2>
        <ol class="pubs reveal">
          <li>Giordano, M. and Pulieri, E. Forthcoming. "From International to 'Regional' Financial Subordination: Italian Monetary Integration in the Eurozone", <em>Cambridge Journal of Economics</em>.</li>
          <li>Giordano, M. and Pulieri, E. Forthcoming. "Debt Management (in-)Dependence: The missing side of Central Banks and the Legacy of CBI".</li>
          <li>Murau, S., Goghie, A., Giordano, M. and Reimer, F. Forthcoming. "The Monetary Architecture Framework", <em>GEGI Study</em>, Boston University.</li>
        </ol>
      </div>
    </section>

    <section class="block" id="talks" aria-labelledby="talks-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="talks-title">Selected talks</h2>
        <div class="block__body reveal">
          <ul class="pubs pubs--talks">
            <li>"Tiered Euro-Monies: Perpetrating Monetary Hierarchies from the ECU to the Euro". <span class="where">Euromemo Group 30th Annual Conference, Vienna, September 2024.</span></li>
            <li>"Encumbered Security? Vertical and Horizontal Repos in the Euro Area and Their Inherent Ambiguity". <span class="where">Association for Heterodox Economics, UWE Bristol, July 2024.</span></li>
            <li>"Forging Monetary Unification through Novation: The TARGET System and the Politics of Central Banking in Europe" (with S. Murau). <span class="where">Money View Symposium, Institute for New Economic Thinking, February 2024.</span></li>
            <li>"The State of Capitalism: Imperialism, Subordination, and Beyond". <span class="where">Rethinking Economics, SOAS University of London, February 2024.</span></li>
            <li>"Off-Balance-Sheet Fiscal Agencies and the Role of the State in Financing the Green Transition". <span class="where">Money in Open Economies, University of Leeds, September 2023.</span></li>
            <li>"Hegemony in Europe: Allowing the EMU to tick over" (with Prof. C. Lapavitsas). <span class="where">Musashi University International Symposium, Tokyo, May 2023.</span></li>
          </ul>
          <p style="margin-top:24px">Full list of presentations and workshops in the <a href="https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt" data-link="CV_ACADEMIC_URL" rel="noopener" target="_blank">academic CV</a>.</p>
        </div>
      </div>
    </section>
  </main>
```

- [ ] **Step 3: Run chrome and check**

```bash
python3 tools/chrome.py && python3 tools/check.py
```
Expected: `updated publications.html`; the only problems are `broken link` lines for `/cargo-and-collateral`, `/about`, `/disclaimer`.

- [ ] **Step 4: Commit**

```bash
git add publications.html img/state-of-capitalism.jpg && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Publications page

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9: Cargo & Collateral and About pages

**Files:**
- Create: `cargo-and-collateral.html`, `data/writing.json`, `img/cargo-and-collateral-wordmark.png`, `about.html`

- [ ] **Step 1: Wordmark and writing data**

```bash
sips -Z 1000 "$VAULT/Attachments/wordmark-transparent.png" --out img/cargo-and-collateral-wordmark.png >/dev/null && sips -g pixelWidth -g pixelHeight img/cargo-and-collateral-wordmark.png
```
Expected: 1000 × 190 (record the exact height for the `height` attribute; 190 is 256 × 1000 / 1344 rounded).

`data/writing.json` (newest first, five most recent, maintained by hand):
```json
[
  { "title": "Paying for delivery is not the same as funding capacity", "date": "23 September 2026", "href": "https://cargoandcollateral.substack.com/p/state-pays-for-delivery-not-capacity" }
]
```

- [ ] **Step 2: Write cargo-and-collateral.html**

Head values: TITLE `Cargo & Collateral — Matteo Giordano`; DESCRIPTION `Cargo & Collateral: macro-finance and shipping, read through balance sheets and monetary architecture. A newsletter by Matteo Giordano on Substack.`; PATH `/cargo-and-collateral`.

```html
  <main id="main">
    <header class="page-head">
      <div class="wrap">
        <p class="eyebrow reveal">Cargo &amp; Collateral</p>
        <img class="wordmark reveal" src="/img/cargo-and-collateral-wordmark.png" alt="Cargo & Collateral" width="1000" height="190">
        <h1 class="page-title reveal">Macro-finance and shipping, read through balance sheets and monetary architecture.</h1>
        <div class="actions reveal">
          <a class="btn" href="https://cargoandcollateral.substack.com/" data-link="SUBSTACK_URL" rel="noopener" target="_blank">Read it on Substack</a>
          <a class="btn" href="https://cargoandcollateral.substack.com/subscribe" data-link="SUBSTACK_SUBSCRIBE_URL" rel="noopener" target="_blank">Subscribe</a>
        </div>
      </div>
    </header>

    <section class="block" aria-labelledby="cc-what">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="cc-what">What it covers</h2>
        <div class="block__body reveal">
          <p>Seaborne trade and monetary systems can be read the same way: as claims and obligations. Who owes what to whom, on whose balance sheet, and funded how.</p>
          <p>Forwarder and carrier working capital, chartering and freight rates, chokepoint transits and tonne-mile demand, ship finance and the capital stack behind a fleet, marine insurance pricing, trade finance. Monetary side: repo markets, debt management offices, central-bank balance sheets, and the euro-area settlement plumbing where it touches trade. Defence appears occasionally and on the same terms: rearmament as a working-capital problem before a capability one.</p>
        </div>
      </div>
    </section>

    <section class="block" aria-labelledby="cc-recent">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="cc-recent">Recent entries</h2>
        <div class="block__body reveal">
          <ol class="writing" id="writing-list" hidden></ol>
          <p id="writing-empty">Latest entries on <a href="https://cargoandcollateral.substack.com/archive" data-link="SUBSTACK_ARCHIVE_URL" rel="noopener" target="_blank">Substack</a>.</p>
          <p style="margin-top:20px"><a href="https://cargoandcollateral.substack.com/archive" data-link="SUBSTACK_ARCHIVE_URL" rel="noopener" target="_blank">Full archive on Substack</a></p>
        </div>
      </div>
    </section>
  </main>
```

- [ ] **Step 3: Write about.html**

Head values: TITLE `About — Matteo Giordano`; DESCRIPTION `Positions, education, methods and recognition. Macro strategist in the shipping industry; co-founder of Garrison Sterling; Associate Researcher, Global Climate Forum; PhD, SOAS University of London.`; PATH `/about`.

```html
  <main id="main">
    <header class="page-head">
      <div class="wrap">
        <p class="eyebrow reveal">About</p>
        <h1 class="page-title reveal">The record: positions, training, published output, and where the full paper trail sits.</h1>
        <nav class="cv-links reveal" aria-label="CV and profiles" style="margin-top:28px">
          <a href="https://app.box.com/s/18pq9r7919gcxvu23hk5v4wda4hq6dq4" data-link="CV_URL" rel="noopener" target="_blank">Download CV</a>
          <a href="https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt" data-link="CV_ACADEMIC_URL" rel="noopener" target="_blank">Academic CV</a>
          <a href="https://orcid.org/0000-0002-1588-6735" data-link="ORCID_URL" rel="noopener" target="_blank">ORCID</a>
          <a href="https://www.linkedin.com/in/matteogiordano-economist/" data-link="LINKEDIN_URL" rel="noopener" target="_blank">LinkedIn</a>
          <a href="mailto:mg.macroeconomics@gmail.com" data-mailto>Email</a>
        </nav>
      </div>
    </header>

    <section class="block" aria-labelledby="positions-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="positions-title">Positions</h2>
        <ul class="block__body reveal">
          <!-- DRAFT -->
          <li><strong>Macro strategist and financial analyst</strong>, shipping industry, Greece (2026–).</li>
          <!-- /DRAFT -->
          <li><strong>Co-founder and Director</strong>, <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a> (2026–). Independent defence economics firm: a company-level data platform on the defence economy, with input-output and economic-impact models on top. Leads the modelling: economic-impact models and the supplier-level metrics built on public spend and company records.</li>
          <li><strong>Associate Researcher</strong>, Global Climate Forum, Berlin (2023–). OBFA-TRANSFORM: balance-sheet modelling of the euro-area monetary architecture, and delivery of the public <a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a>.</li>
          <li><strong>Senior Defence Economist</strong>, <a href="https://www.ukdsc.org" rel="noopener">UKDSC</a>, within the <a href="https://www.gov.uk/government/organisations/ministry-of-defence" rel="noopener">Ministry of Defence</a> ecosystem (2025–2026). Input-Output and scenario models of the defence-industrial base; strategic briefings to government and industry. Reports I authored contributed to shaping MoD policy on measuring defence-industrial productivity, evaluating programme viability, assessing supply-chain resilience and vulnerability, and defining industrial readiness.</li>
          <li><strong>Lecturer in Economics</strong>, SOAS University of London (2023–2025).</li>
        </ul>
      </div>
    </section>

    <section class="block" aria-labelledby="education-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="education-title">Education</h2>
        <ul class="block__body reveal">
          <li><strong>PhD, Economics</strong>, SOAS University of London (2020–2025). Thesis: <em>Monetary Subordination in the Eurozone: Fragmentation and tiering of markets and institutions</em>. Advisor: Prof. Costas Lapavitsas.</li>
          <li><strong>MSc, International Political Economy</strong>, LSE (2019–2020). Advisor: Prof. Jeffrey Chwieroth.</li>
          <li><strong>BSc, Economics (Hons)</strong>, SOAS University of London (2016–2019). Winner of the Undergraduate Prize in Economics.</li>
        </ul>
      </div>
    </section>

    <section class="block" aria-labelledby="methods-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="methods-title">Methods</h2>
        <div class="block__body reveal">
          <p><strong>Modelling:</strong> balance-sheet mapping, stock-flow-consistent accounting, Input-Output, gravity models, VAR/SVAR, panel and time-series methods, scenario analysis.</p>
          <p><strong>Applied to:</strong> euro-area monetary policy and transmission, sovereign debt dynamics, fiscal-monetary interaction, financial fragmentation, shipping and trade finance, defence and war finance, trade and capital-flow regimes.</p>
          <p><strong>Tools:</strong> R and Python for macro-financial modelling and data work; Excel; LaTeX.</p>
        </div>
      </div>
    </section>

    <section class="block" aria-labelledby="recognition-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="recognition-title">Recognition</h2>
        <div class="block__body reveal">
          <p>Research Associate funding, OBFA-Transformation project (Deutsche Forschungsgemeinschaft and GCF Berlin). Scholarship, Minsky Summer Seminar, Levy Economics Institute of Bard College (2018).</p>
          <p>Teaching at SOAS: Outstanding Teaching Award (2024–25), Best Use of Technology Enhanced Learning (2023–24), and a nomination for Postgraduate Research Supervisor of the Year (2024–25).</p>
        </div>
      </div>
    </section>

    <section class="block" aria-labelledby="personal-title">
      <div class="wrap block__grid">
        <h2 class="block__title reveal" id="personal-title">Personal</h2>
        <div class="block__body reveal">
          <p>Dual Italian-British national, based in Greece. Italian (native) · English (bilingual) · French (advanced) · Greek and Spanish (beginner).</p>
          <p style="margin-top:20px">The published record: <a href="/publications">Publications</a>. Where the work lives: <a href="/cargo-and-collateral">Cargo &amp; Collateral</a> · <a href="/advisory">Advisory</a> · <a href="/research">Research</a>.</p>
        </div>
      </div>
    </section>
  </main>
```

- [ ] **Step 4: Run chrome and check, then commit**

```bash
python3 tools/chrome.py && python3 tools/check.py
git add cargo-and-collateral.html about.html data img && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Cargo & Collateral and About pages

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```
Expected before commit: the only problem is `broken link /disclaimer` (built in Task 10).

---

### Task 10: Disclaimer, 404, icons, share image, sitemap, indexing switch, README

**Files:**
- Create: `disclaimer.html`, `404.html`, `favicon.svg`, `tools/make_assets.py`, `favicon.ico`, `apple-touch-icon.png`, `img/og-share.png`, `sitemap.xml`, `tools/indexing.py`
- Modify: `README.md`

- [ ] **Step 1: disclaimer.html**

Head values: TITLE `Disclaimer — Matteo Giordano`; DESCRIPTION `The content on this site represents Matteo Giordano's personal work and views, not those of any employer or of Garrison Sterling. Nothing on it is investment advice.`; PATH `/disclaimer`.

```html
  <main id="main">
    <header class="page-head">
      <div class="wrap">
        <p class="eyebrow reveal">Disclaimer</p>
        <h1 class="page-title reveal">Personal work and views.</h1>
      </div>
    </header>
    <section class="prose">
      <div class="wrap">
        <p>The content on this website, including research, publications, opinions, and other materials, represents my personal work and views. Nothing on this site should be interpreted as representing the views, positions, or policies of any past or present employer, including the UK Defence Solutions Centre (UKDSC), the Ministry of Defence, or any defence industry primes, nor those of Garrison Sterling, whose research and analysis are published under its own name.</p>
        <p>All content is provided for informational and educational purposes only, and nothing on this site is investment advice.</p>
        <h2>Advisory engagements</h2>
        <p>All engagements are undertaken in a personal capacity and are independent of any employer, past or present, and of Garrison Sterling. Nothing produced under them is investment advice.</p>
        <h2>Privacy</h2>
        <p>This site sets no cookies, runs no analytics, and makes no request to any third party. An email you send is used only to reply.</p>
      </div>
    </section>
  </main>
```
The Privacy paragraph is new copy: wrap it in `<!-- DRAFT -->`/`<!-- /DRAFT -->` for approval.

- [ ] **Step 2: 404.html**

Head values: TITLE `Page not found — Matteo Giordano`; DESCRIPTION `That page is not here.`; PATH `/404`.

```html
  <main id="main">
    <header class="page-head page-head--tall">
      <div class="wrap">
        <p class="eyebrow">Not found</p>
        <h1 class="page-title">That page is not here.</h1>
        <p class="lede"><a class="link" href="/">Back to the start</a> · <a class="link" href="/research">Research</a> · <a class="link" href="/publications">Publications</a></p>
      </div>
    </header>
  </main>
```

- [ ] **Step 3: favicon.svg (the T-account mark)**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="4" fill="#F6F2EA"/><path d="M5 8h22M16 8v19" stroke="#1B1D22" stroke-width="2.6" stroke-linecap="square" fill="none"/></svg>
```

- [ ] **Step 4: tools/make_assets.py (Pillow, run once; not a runtime dependency)**

```python
#!/usr/bin/env python3
"""One-off asset generation with Pillow: favicon.ico, apple-touch-icon.png, img/og-share.png.
    python3 tools/make_assets.py
Re-run after changing the palette or the positioning line."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER, INK, ACCENT = (246, 242, 234), (27, 29, 34), (31, 111, 181)
SERIF_BOLD = os.path.join(ROOT, 'fonts', 'SourceSerif4-Semibold.woff2')
SANS = os.path.join(ROOT, 'fonts', 'IBMPlexSans-Medium.woff2')

def font(path, size):
    for p in (path, path.replace('.woff2', '.ttf')):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default(size)

def t_mark(draw, x, y, size, width, colour=INK):
    draw.line([(x, y), (x + size, y)], fill=colour, width=width)
    draw.line([(x + size / 2, y), (x + size / 2, y + size * 0.95)], fill=colour, width=width)

def icon(px):
    im = Image.new('RGB', (px, px), PAPER)
    d = ImageDraw.Draw(im)
    t_mark(d, px * 0.16, px * 0.25, px * 0.68, max(2, round(px * 0.085)))
    return im

def main():
    icon(32).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32)])
    icon(180).save(os.path.join(ROOT, 'apple-touch-icon.png'))
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    t_mark(d, 80, 80, 56, 5)
    d.text((80, 170), 'Dr Matteo Giordano', font=font(SANS, 28), fill=(107, 111, 118))
    f = font(SERIF_BOLD, 60)
    y = 225
    for line in ('Macro-financial strategist.', 'Shipping, monetary structures,', 'and off-balance-sheet finance.'):
        d.text((80, y), line, font=f, fill=INK); y += 74
    d.line([(80, 500), (1120, 500)], fill=ACCENT, width=2)
    d.text((80, 525), 'mg-macro.vercel.app', font=font(SANS, 26), fill=(107, 111, 118))
    im.save(os.path.join(ROOT, 'img', 'og-share.png'), optimize=True)
    print('wrote favicon.ico, apple-touch-icon.png, img/og-share.png')

if __name__ == '__main__':
    main()
```
Pillow's FreeType loader reads woff2 only when built with that support; if `font()` falls back to the default face, the share image will look wrong. In that case extract TTFs from the already-downloaded `_dl/source-serif` zip (`source-serif-4.005_Desktop.zip` has `TTF/SourceSerif4-Semibold.ttf`) and the IBM Plex release (`gh release download --repo IBM/plex --pattern 'TrueType.zip'`) into `_dl/`, and point `SERIF_BOLD`/`SANS` at those `.ttf` paths (they are build inputs only, not shipped). Run:

```bash
python3 tools/make_assets.py && sips -g pixelWidth -g pixelHeight img/og-share.png favicon.ico apple-touch-icon.png
```
Expected: 1200×630, 32×32, 180×180. Open `img/og-share.png` with the Read tool and confirm the text rendered in the serif, not a bitmap default.

- [ ] **Step 5: sitemap.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://mg-macro.vercel.app/</loc></url>
  <url><loc>https://mg-macro.vercel.app/research</loc></url>
  <url><loc>https://mg-macro.vercel.app/publications</loc></url>
  <url><loc>https://mg-macro.vercel.app/cargo-and-collateral</loc></url>
  <url><loc>https://mg-macro.vercel.app/about</loc></url>
  <url><loc>https://mg-macro.vercel.app/advisory</loc></url>
  <url><loc>https://mg-macro.vercel.app/disclaimer</loc></url>
</urlset>
```

- [ ] **Step 6: tools/indexing.py**

Copy `$GS/tools/indexing.py` unchanged except the `set_state` robots writer, which must keep the Sitemap line:

```python
    open(rp, 'w', encoding='utf-8').write(
        '# Managed by tools/indexing.py\nUser-agent: *\n' + ('Allow: /\n' if on else 'Disallow: /\n')
        + 'Sitemap: https://mg-macro.vercel.app/sitemap.xml\n')
```
Then verify the state reads `on` everywhere:
```bash
cp "$GS/tools/indexing.py" tools/indexing.py   # then apply the edit above
python3 tools/indexing.py
```
Expected: every `*.html` line and `robots.txt` and `config.js` report `on`.

- [ ] **Step 7: README.md** (write exactly this content)

````markdown
# Matteo Giordano — personal website

Static site: plain HTML + CSS + a little vanilla JS. No framework, no build step, no backend, no third-party requests. Live at https://mg-macro.vercel.app.

```
index.html                 Home: hero, statement, bio, four lines of work, academic roots, affiliations
advisory.html              Advisory: areas, delivered work, ways to engage
research.html              One page, four sections, project anchors (#eurozone, #subordination, ...)
publications.html          Published, in preparation, selected talks (#talks)
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

- Copy lives in the HTML files. After touching the nav or footer, edit `tools/chrome/nav.html` or `footer.html` and run `python3 tools/chrome.py`.
- Addresses and links used in several places: `js/config.js` (the HTML carries the same values as fallbacks; update both).
- Add a newsletter entry: prepend to `data/writing.json` (`title`, `date`, `href`); keep the five most recent.
- Add an advisory engagement: append an `<li>` under Delivered work in `advisory.html` following the comment there.
- Before committing: `python3 tools/check.py --strict` and `python3 -m unittest discover -s tools/tests`.

## Indexing

`python3 tools/indexing.py off` hides the site from search engines (noindex meta, robots Disallow); `on` reverses it. Deploy afterwards.

## Deploy

Pushes to `main` on GitHub (`dr-mpfg/mg-website`) deploy to Vercel automatically. Framework preset Other, no build command, output directory `.`.
````

- [ ] **Step 8: Run everything**

```bash
python3 tools/chrome.py && python3 tools/check.py && python3 -m unittest discover -s tools/tests 2>&1 | tail -2
```
Expected: `check: 0 problem(s)` (DRAFT markers are reported only with `--strict`) and `OK`.

- [ ] **Step 9: Commit**

```bash
git add -A && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Disclaimer, 404, icons, share image, sitemap, indexing switch, README

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 11: Visual verification in the browser pane

**Files:**
- Modify: any page or `css/site.css` as fixes require

- [ ] **Step 1: Start the server and open the home page**

Use `mcp__Claude_Browser__preview_start` with `name: "mg-website"` (from `.claude/launch.json`). Then for each of `/`, `/advisory`, `/research`, `/publications`, `/cargo-and-collateral`, `/about`, `/disclaimer`, `/nonexistent`:
  1. `navigate` to `http://localhost:8765<path>`.
  2. `resize_window` preset `desktop`, screenshot; preset `tablet`, screenshot; preset `mobile`, screenshot. On mobile, click the Menu button and screenshot the overlay once (home page only).
  3. `read_console_messages` with `onlyErrors: true`: expected empty. A CSP violation for `style` attributes means moving the inline `style="margin-top:..."` attributes into `css/site.css` (see Task 5 note) across all pages.
  4. `read_network_requests`: every URL starts with `http://localhost:8765`.
  5. Reset with `resize_window` preset `desktop`.

- [ ] **Step 2: Check behaviours**

- On `/cargo-and-collateral` the Recent entries list shows the one entry from `data/writing.json` and the empty line is hidden.
- On `/research`, navigate to `http://localhost:8765/research#subordination` and confirm the heading lands below the nav (the `:target` scroll margin).
- Nav shows `aria-current` on the right link on every page (use `find` for `aria-current`).
- `resize_window` with `colorScheme: "dark"`: the page stays paper (no dark mode is defined; confirm nothing inverts), then set it back to `light`.

- [ ] **Step 3: Review and fix**

Look at every screenshot for: clipped headlines at 360px, the roles line wrapping sensibly, figures not overflowing, the T mark aligned with the wordmark, the CTA button legible. Fix in CSS or markup, re-run `python3 tools/check.py`, re-screenshot the affected page.

- [ ] **Step 4: Send the screenshots to the user and commit**

Save screenshots under the scratchpad directory, send the 1440 and 360 home and research shots with `SendUserFile`, then:
```bash
git add -A && git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "Visual fixes after browser review

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```
Stop here for the user's review of the screenshots and the DRAFT lines (`grep -rn "DRAFT" *.html` lists them). Apply their edits, remove the markers, and only then continue.

---

### Task 12: Launch

**Files:**
- Modify: none in the repo except removing DRAFT markers after approval

- [ ] **Step 1: Strict check**

```bash
python3 tools/check.py --strict && python3 -m unittest discover -s tools/tests 2>&1 | tail -1
```
Expected: `check: 0 problem(s)` and `OK`. If DRAFT markers remain, the user has not approved them yet: stop.

- [ ] **Step 2: Create the GitHub repo and push**

```bash
gh repo create dr-mpfg/mg-website --public --description "Personal website of Dr Matteo Giordano" --source . --remote origin --push
gh repo view dr-mpfg/mg-website --json url -q .url
```
Expected: the repo URL printed; `git log origin/main --oneline -1` matches local.

- [ ] **Step 3: Repoint the Vercel project**

The live project is the one serving `mg-macro.vercel.app` (mgmacro.vercel.app is a redirect to it). In the Vercel dashboard, with the user logged in (drive it in the browser pane if the user asks, otherwise give these steps):
  1. Open the project → Settings → Git → Disconnect `dr-mpfg/mg_macro` → Connect `dr-mpfg/mg-website`, production branch `main`.
  2. Settings → General → Framework Preset `Other`, Build Command empty (override on, blank), Output Directory `.` (override on), Install Command empty.
  3. Deployments → Redeploy the latest, or push an empty commit: `git commit --allow-empty -m "Trigger deploy" && git push`.

Changing Git settings and redeploying are account-setting changes: confirm with the user before each click if driving the browser.

- [ ] **Step 4: Verify the live site**

```bash
for p in / /research /publications /cargo-and-collateral /about /advisory /disclaimer /sitemap.xml /robots.txt /img/og-share.png; do printf "%-28s" "$p"; curl -s -o /dev/null -w "%{http_code}\n" "https://mg-macro.vercel.app$p"; done
for p in /research-projects/eurozone /research-projects/defence-and-security-economics /talks-and-conferences/talk-and-conferences /publications/the-state-of-capitalism /nope; do printf "%-55s" "$p"; curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "https://mg-macro.vercel.app$p"; done
curl -s -D - -o /dev/null https://mg-macro.vercel.app/ | grep -iE "content-security-policy|strict-transport"
```
Expected: 200 for every page and asset; 308 with the new destination for each old slug; 404 for `/nope`; both headers present. Then open `https://mg-macro.vercel.app` in the browser pane and screenshot once.

- [ ] **Step 5: Archive the old source**

Only after the user confirms the live site: `gh repo archive dr-mpfg/mg_macro --yes` (asks the user first; it is reversible but outward-facing). Tell the user to leave the Obsidian digital-garden plugin disconnected so it cannot republish over the new site.
