# Personal Website v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the built v1 site into a hub-and-spoke index: one-screen pages, six project pages under `/research/`, a Research sub-menu, single-column layout.

**Architecture:** Same static stack (HTML, CSS, vanilla JS, Python stdlib tools). Pages in the repo root plus `research/<slug>.html`. Shared chrome written by `tools/chrome.py`; checks by `tools/check.py`. The stylesheet is rewritten for the single-column, card-based layout; the nav partial gains a CSS-only dropdown.

**Tech Stack:** HTML5, CSS custom properties, ES5 vanilla JS, Python 3.13 stdlib + unittest, Vercel static hosting.

Spec: `docs/superpowers/specs/2026-10-11-personal-website-v2-structure.md` (structure) and `docs/superpowers/specs/2026-10-11-personal-website-design.md` (palette, type, plumbing). Repo root `$ROOT` = `/Users/matteo/work_codes_offline/MG_macro_offline`. Vault `$VAULT` = `/Users/matteo/Library/Mobile Documents/iCloud~md~obsidian/Documents/MG Macro`. The v1 pages exist and carry the full vault text; v2 page tasks REWRITE them (replace the whole file) using the copy given in each task.

## Global Constraints

- Static site: no framework, no npm, no backend, no third-party requests at runtime. CSP `default-src 'self'`: no inline scripts, no inline `style` attributes (use classes).
- Page map and word budgets exactly as in the v2 spec table. Nav: About · Research ▾ · Publications · Cargo & Collateral · `Advisory` button. The newsletter tab is labelled exactly `Cargo & Collateral`.
- Tokens: `--paper #F6F2EA`, `--paper-2 #EDE7DB`, `--ink #1B1D22`, `--muted #6B6F76`, `--rule rgba(27,29,34,0.12)`, `--accent #1F6FB5`. Type: Source Serif 4 (400, 400i, 600) prose and headlines; IBM Plex Sans (400, 500, 600) nav, eyebrows, buttons, meta, captions. Motion: 300 ms fade-in on scroll only; everything visible under `prefers-reduced-motion`. No `scroll-behavior: smooth`.
- Every page: `<title>`, `meta description`, `<link rel="canonical" href="https://mg-macro.vercel.app<path>">`, OG + Twitter tags, `lang="en-GB"`, skip link, `<main id="main">`, chrome marker blocks, scripts `/js/config.js` then `/js/site.js`. All asset and page hrefs absolute (`/css/site.css`, `/img/...`, `/research/eurozone`).
- Copy: the text in each task is final (it is the user's vault text, trimmed). Lines that are new are wrapped `<!-- DRAFT --> ... <!-- /DRAFT -->`; `check.py --strict` passes only after the user approves them.
- Links: email `mg.macroeconomics@gmail.com`; Substack `https://cargoandcollateral.substack.com/` (+`subscribe`, +`archive`); LinkedIn `https://www.linkedin.com/in/matteogiordano-economist/`; ORCID `https://orcid.org/0000-0002-1588-6735`; CV `https://app.box.com/s/18pq9r7919gcxvu23hk5v4wda4hq6dq4`; academic CV `https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt`; Garrison Sterling `https://garrisonsterling.com`; GCF `https://globalclimateforum.org/portfolio-item/matteo-giordano/`; OBFA `https://obfa-transform.eu`; MA tool `https://monetary-architecture.com/`; UKDSC `https://www.ukdsc.org`; MoD `https://www.gov.uk/government/organisations/ministry-of-defence`; SOAS `https://www.soas.ac.uk/about/matteo-giordano-0`; SPARC `https://wearesparc.org/`. External links carry `rel="noopener"`; profile/CV/Substack links also `target="_blank"` and `data-link="<CONFIG_KEY>"`.
- After every page task: `python3 tools/chrome.py && python3 tools/check.py`. Expected problems are only `broken link` lines for pages the plan has not yet built; anything else is a defect.
- Commit per task: `git -c user.name="Matteo Giordano" -c user.email="mattegiordano@me.com" commit -m "<subject>

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"`.

---

### Task 1: Tools for sub-directory pages (chrome.py, check.py)

**Files:**
- Modify: `tools/chrome.py`, `tools/check.py`, `tools/tests/test_chrome.py`, `tools/tests/test_check.py`

**Interfaces:**
- `chrome.pages(root)` returns sorted paths of `*.html` in root and in `root/research/`.
- `chrome.page_path(filename, root)` → `'/'` for `index.html`, `None` for `404.html`, `'/about'` for `about.html`, `'/research/eurozone'` for `research/eurozone.html`.
- `chrome.mark_current(nav_html, path)` marks `href="<path>"`; when `path` starts with `/research/` it also marks `href="/research"`.
- `check.problems(root, strict)` scans the same page set; sitemap expectation = all pages except `404.html`, mapped to clean URLs.

- [ ] **Step 1: Add failing tests to `tools/tests/test_chrome.py`**

Append inside `class ChromeTest`:
```python
    def test_page_path_subdirectory(self):
        self.assertEqual(chrome.page_path('/x/research/eurozone.html', '/x'), '/research/eurozone')
        self.assertEqual(chrome.page_path('/x/about.html', '/x'), '/about')

    def test_mark_current_marks_parent_for_project_pages(self):
        nav = '<a class="nav__link" href="/research">Research</a><a href="/research/eurozone">Eurozone</a><a href="/research/gegi-study">GEGI</a>'
        out = chrome.mark_current(nav, '/research/eurozone')
        self.assertIn('href="/research" aria-current="page"', out)
        self.assertIn('href="/research/eurozone" aria-current="page"', out)
        self.assertNotIn('href="/research/gegi-study" aria-current', out)

    def test_run_includes_research_directory(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, 'tools', 'chrome')); os.makedirs(os.path.join(d, 'research'))
            open(os.path.join(d, 'tools', 'chrome', 'nav.html'), 'w').write('<a class="nav__link" href="/research">R</a>')
            open(os.path.join(d, 'tools', 'chrome', 'footer.html'), 'w').write(FOOT)
            open(os.path.join(d, 'research', 'eurozone.html'), 'w').write(PAGE)
            self.assertEqual(chrome.run(d), ['research/eurozone.html'])
            self.assertIn('href="/research" aria-current="page"', open(os.path.join(d, 'research', 'eurozone.html')).read())
```
Change the existing `test_page_path` to pass the root: `chrome.page_path('/r/index.html', '/r')`, `chrome.page_path('/r/about.html', '/r')`, `chrome.page_path('/r/404.html', '/r')`.

Append to `tools/tests/test_check.py` inside `class CheckTest`:
```python
    def test_research_subpages_are_scanned_and_expected_in_sitemap(self):
        with tempfile.TemporaryDirectory() as d:
            site(d)
            os.makedirs(os.path.join(d, 'research'))
            write(os.path.join(d, 'research', 'eurozone.html'), GOOD.replace('/b#sec', '/a#here').replace('https://x/a', 'https://x/research/eurozone'))
            p = '\n'.join(check.problems(d))
            self.assertIn('sitemap.xml: missing page /research/eurozone', p)
            write(os.path.join(d, 'sitemap.xml'), '<urlset><url><loc>https://x/a</loc></url><url><loc>https://x/b</loc></url><url><loc>https://x/research/eurozone</loc></url></urlset>')
            self.assertEqual(check.problems(d), [])
            write(os.path.join(d, 'research', 'bad.html'), '<html><head></head><body><a href="/nope">x</a></body></html>')
            self.assertIn('research/bad.html: broken link /nope', '\n'.join(check.problems(d)))
```
(`write` is the helper already in that test file; if it is named differently, use the existing helper.)

- [ ] **Step 2: Run tests, expect failures**

`python3 -m unittest discover -s tools/tests 2>&1 | tail -3` → FAIL/ERROR on the new tests.

- [ ] **Step 3: Implement in `tools/chrome.py`**

Replace `page_path` and `run`, add `pages`, extend `mark_current`:
```python
def pages(root=ROOT):
    """Root *.html plus research/*.html, sorted."""
    return sorted(glob.glob(os.path.join(root, '*.html')) + glob.glob(os.path.join(root, 'research', '*.html')))

def page_path(filename, root=ROOT):
    """index.html -> '/', about.html -> '/about', research/eurozone.html -> '/research/eurozone', 404.html -> None."""
    rel = os.path.relpath(filename, root)[:-5].replace(os.sep, '/')
    if rel == 'index':
        return '/'
    if rel == '404':
        return None
    return '/' + rel

def mark_current(nav_html, path):
    if path is None:
        return nav_html
    targets = [path]
    if path.startswith('/research/'):
        targets.append('/research')
    out = nav_html
    for t in targets:
        out = re.sub(r'href="%s"(?! aria-current)' % re.escape(t), 'href="%s" aria-current="page"' % t, out)
    return out

def run(root=ROOT):
    nav = open(os.path.join(root, 'tools', 'chrome', 'nav.html'), encoding='utf-8').read()
    foot = open(os.path.join(root, 'tools', 'chrome', 'footer.html'), encoding='utf-8').read()
    changed = []
    for p in pages(root):
        src = open(p, encoding='utf-8').read()
        out = render(src, nav, foot, page_path(p, root))
        if out != src:
            open(p, 'w', encoding='utf-8').write(out)
            changed.append(os.path.relpath(p, root).replace(os.sep, '/'))
    return changed
```
Use `with open(...)` for every file read/write in this module while you are there (removes the ResourceWarnings noted in review).

- [ ] **Step 4: Implement in `tools/check.py`**

In `problems()`: build `pages` as `sorted(glob.glob(os.path.join(root, '*.html')) + glob.glob(os.path.join(root, 'research', '*.html')))`; report names as `os.path.relpath(p, root).replace(os.sep, '/')`; compute the sitemap expectation as
```python
        def clean(p):
            rel = os.path.relpath(p, root)[:-5].replace(os.sep, '/')
            return '/' if rel == 'index' else '/' + rel
        expected = set(clean(p) for p in pages if os.path.basename(p) != '404.html')
```

- [ ] **Step 5: Run tests, expect all green**

`python3 -m unittest discover -s tools/tests 2>&1 | tail -3` → `OK` (21 tests). Then `python3 tools/chrome.py && python3 tools/check.py` on the real repo → `check: 0 problem(s)` (no research/ pages exist yet).

- [ ] **Step 6: Commit** — subject `Tools: handle research/ sub-pages`.

---

### Task 2: Stylesheet v2, nav with Research sub-menu, latest-note hook

**Files:**
- Rewrite: `css/site.css`
- Modify: `tools/chrome/nav.html`, `js/site.js`

- [ ] **Step 1: Rewrite `css/site.css` with exactly this content**

```css
/* Matteo Giordano — site.css v2. Warm paper, ink, one accent. Single column, cards. Plain CSS. */

@font-face { font-family: 'Source Serif 4'; font-style: normal; font-weight: 400; font-display: swap; src: url('../fonts/SourceSerif4-Regular.woff2') format('woff2'); }
@font-face { font-family: 'Source Serif 4'; font-style: italic; font-weight: 400; font-display: swap; src: url('../fonts/SourceSerif4-Italic.woff2') format('woff2'); }
@font-face { font-family: 'Source Serif 4'; font-style: normal; font-weight: 600; font-display: swap; src: url('../fonts/SourceSerif4-Semibold.woff2') format('woff2'); }
@font-face { font-family: 'IBM Plex Sans'; font-style: normal; font-weight: 400; font-display: swap; src: url('../fonts/IBMPlexSans-Regular.woff2') format('woff2'); }
@font-face { font-family: 'IBM Plex Sans'; font-style: normal; font-weight: 500; font-display: swap; src: url('../fonts/IBMPlexSans-Medium.woff2') format('woff2'); }
@font-face { font-family: 'IBM Plex Sans'; font-style: normal; font-weight: 600; font-display: swap; src: url('../fonts/IBMPlexSans-SemiBold.woff2') format('woff2'); }

:root {
  --paper: #F6F2EA; --paper-2: #EDE7DB; --ink: #1B1D22; --muted: #6B6F76;
  --rule: rgba(27, 29, 34, 0.12); --accent: #1F6FB5; --accent-soft: rgba(31, 111, 181, 0.35);
  --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
  --sans: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
  --wide: 1040px; --prose: 720px; --gutter: 20px; --nav-h: 68px; --ease: cubic-bezier(0.2, 0.7, 0.2, 1);
}
@media (min-width: 768px) { :root { --gutter: 32px; --nav-h: 76px; } }

/* Base */
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--serif); font-size: 1.0625rem; line-height: 1.6; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; min-height: 100vh; display: flex; flex-direction: column; }
@media (min-width: 768px) { body { font-size: 1.125rem; } }
main { flex: 1 0 auto; }
h1, h2, h3 { margin: 0; font-family: var(--serif); font-weight: 600; letter-spacing: -0.015em; line-height: 1.15; text-wrap: balance; }
p { margin: 0 0 1em; text-wrap: pretty; }
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
.col { width: 100%; max-width: calc(var(--prose) + 2 * var(--gutter)); margin: 0 auto; padding: 0 var(--gutter); }
.col--wide { max-width: calc(var(--wide) + 2 * var(--gutter)); }
.muted { color: var(--muted); }
.eyebrow { font-family: var(--sans); font-size: 0.8125rem; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); }
.eyebrow a { color: var(--muted); }
.eyebrow a:hover { color: var(--accent); }
.mt-20 { margin-top: 20px; } .mt-24 { margin-top: 24px; } .mt-28 { margin-top: 28px; }

/* Inline links in prose */
.prose a, .abstract a, .area__text a, .bio a, .lines a, .note a, .engage a, .delivered a, .pubs a, .papers a, .positions a, .background a {
  color: var(--ink); border-bottom: 1px solid var(--accent-soft); transition: color 200ms var(--ease), border-color 200ms var(--ease);
}
.prose a:hover, .abstract a:hover, .area__text a:hover, .bio a:hover, .lines a:hover, .note a:hover, .engage a:hover, .delivered a:hover, .pubs a:hover, .papers a:hover, .positions a:hover, .background a:hover { color: var(--accent); border-color: var(--accent); }
.link { color: var(--ink); border-bottom: 1px solid var(--accent-soft); padding-bottom: 1px; transition: color 200ms var(--ease), border-color 200ms var(--ease); }
.link:hover { color: var(--accent); border-color: var(--accent); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 44px; padding: 10px 22px; border: 1px solid var(--accent); border-radius: 2px; font-family: var(--sans); font-weight: 500; font-size: 0.9375rem; line-height: 1.2; white-space: nowrap; color: var(--ink); background: transparent; transition: background-color 200ms var(--ease), color 200ms var(--ease); }
.btn:hover { background: var(--accent); color: var(--paper); }
.btn--sm { min-height: 36px; padding: 6px 14px; font-size: 0.875rem; }
.actions { display: flex; flex-wrap: wrap; gap: 12px; }

/* Logo */
.logo { display: inline-flex; align-items: center; gap: 10px; flex-shrink: 0; color: var(--ink); }
.logo__mark { width: 22px; height: 22px; stroke: currentColor; stroke-width: 2; stroke-linecap: square; fill: none; }
.logo__text { font-family: var(--sans); font-weight: 600; font-size: 0.9375rem; letter-spacing: 0.08em; text-transform: uppercase; white-space: nowrap; }
.logo:hover { color: var(--accent); }

/* Nav */
.nav { position: relative; z-index: 30; min-height: var(--nav-h); display: flex; align-items: center; border-bottom: 1px solid var(--rule); }
.nav__bar { display: flex; align-items: center; justify-content: space-between; gap: 32px; min-height: var(--nav-h); }
.nav__links { display: flex; align-items: center; gap: 28px; }
.nav__item { position: relative; }
.nav__link { font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; color: var(--muted); transition: color 200ms var(--ease); display: inline-flex; align-items: center; gap: 6px; }
.nav__link:hover, .nav__link[aria-current="page"] { color: var(--ink); }
.nav__caret { width: 10px; height: 10px; stroke: currentColor; stroke-width: 1.6; fill: none; }
.nav__cta { margin-left: 4px; }
.nav__cta[aria-current="page"] { background: var(--accent); color: var(--paper); }
/* dropdown panel (desktop) */
.nav__menu { display: none; position: absolute; top: calc(100% + 14px); left: -16px; min-width: 300px; padding: 14px 16px 16px; background: var(--paper); border: 1px solid var(--rule); box-shadow: 0 12px 32px rgba(27, 29, 34, 0.08); }
.nav__menu::before { content: ''; position: absolute; left: 0; right: 0; top: -15px; height: 15px; } /* hover bridge */
.nav__item--menu:hover .nav__menu, .nav__item--menu:focus-within .nav__menu { display: block; }
.nav__menu-all { display: block; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; color: var(--ink); padding: 4px 0 10px; border-bottom: 1px solid var(--rule); margin-bottom: 8px; }
.nav__menu-group { font-family: var(--sans); font-size: 0.75rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin: 12px 0 4px; }
.nav__menu a:not(.nav__menu-all) { display: block; font-family: var(--sans); font-size: 0.9375rem; color: var(--ink); padding: 5px 0; }
.nav__menu a:hover, .nav__menu-all:hover, .nav__menu a[aria-current="page"] { color: var(--accent); }
.nav__toggle { display: none; align-items: center; gap: 10px; min-height: 44px; padding: 0 4px; z-index: 41; position: relative; font-family: var(--sans); font-size: 0.875rem; font-weight: 500; color: var(--ink); }
.nav__toggle-icon { position: relative; width: 20px; height: 12px; }
.nav__toggle-icon::before, .nav__toggle-icon::after { content: ''; position: absolute; left: 0; right: 0; height: 1.5px; background: currentColor; transition: transform 200ms var(--ease), top 200ms var(--ease), bottom 200ms var(--ease); }
.nav__toggle-icon::before { top: 0; }
.nav__toggle-icon::after { bottom: 0; }
.nav__toggle[aria-expanded="true"] .nav__toggle-icon::before { top: 5px; transform: rotate(45deg); }
.nav__toggle[aria-expanded="true"] .nav__toggle-icon::after { bottom: 5px; transform: rotate(-45deg); }
@media (max-width: 899px) {
  .nav__toggle { display: inline-flex; }
  .nav__links { display: none; position: fixed; inset: 0; z-index: 40; flex-direction: column; align-items: stretch; justify-content: flex-start; gap: 0; padding: calc(var(--nav-h) + 16px) var(--gutter) 40px; background: var(--paper); overflow-y: auto; }
  .nav__links.is-open { display: flex; }
  .nav .logo { position: relative; z-index: 41; }
  .nav__link { font-family: var(--serif); font-size: 1.75rem; font-weight: 600; letter-spacing: -0.015em; color: var(--ink); padding: 10px 0; }
  .nav__caret { display: none; }
  .nav__menu { display: block; position: static; min-width: 0; padding: 0 0 8px 0; border: 0; box-shadow: none; background: transparent; }
  .nav__menu::before { content: none; }
  .nav__menu-all { display: none; }
  .nav__menu-group { margin: 8px 0 2px; }
  .nav__menu a:not(.nav__menu-all) { font-size: 1.0625rem; padding: 6px 0; }
  .nav__cta { margin: 28px 0 0; align-self: flex-start; }
  body.nav-open { overflow: hidden; }
}

/* Hero (home) */
.hero { padding: 56px 0 44px; }
@media (min-width: 768px) { .hero { padding: 88px 0 64px; } }
.hero .eyebrow { margin-bottom: 18px; }
.hero__title { font-size: clamp(2.125rem, 4.6vw, 3.5rem); line-height: 1.1; letter-spacing: -0.02em; max-width: 22ch; }
.hero__roles { margin-top: 24px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; letter-spacing: 0.02em; color: var(--muted); line-height: 1.7; }
.hero__roles .sep { color: var(--accent); padding: 0 6px; }
@media (max-width: 599px) { .hero__roles > span:not(.sep) { display: block; } .hero__roles .sep { display: none; } }
.hero__links { display: flex; flex-wrap: wrap; gap: 10px 22px; margin-top: 26px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; }
.hero__links a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); padding-bottom: 2px; transition: color 200ms var(--ease), border-color 200ms var(--ease); }
.hero__links a:hover { color: var(--accent); border-color: var(--accent); }

/* Sections and headers */
.section { padding: 40px 0; border-top: 1px solid var(--rule); }
@media (min-width: 768px) { .section { padding: 56px 0; } }
.section__head { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin-bottom: 20px; }
.section__title { font-size: 1.5rem; letter-spacing: -0.015em; }
@media (min-width: 768px) { .section__title { font-size: 1.75rem; } }
.section__more { font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; color: var(--muted); white-space: nowrap; }
.section__more:hover { color: var(--accent); }
.section__intro { color: var(--muted); max-width: 60ch; margin: -8px 0 20px; }
.page-head { padding: 44px 0 28px; }
@media (min-width: 768px) { .page-head { padding: 72px 0 40px; } }
.page-head .eyebrow { margin-bottom: 16px; }
.page-title { font-size: clamp(1.875rem, 4vw, 2.75rem); line-height: 1.12; letter-spacing: -0.02em; max-width: 24ch; }
.lede { margin-top: 18px; font-size: clamp(1.0625rem, 1.6vw, 1.25rem); line-height: 1.5; color: var(--muted); max-width: 58ch; }
.lede--ink { color: var(--ink); }
.page-head .actions { margin-top: 24px; }
.meta { margin-top: 14px; font-family: var(--sans); font-size: 0.875rem; color: var(--muted); letter-spacing: 0.01em; }

/* Cards */
.cards { display: grid; gap: 14px; }
@media (min-width: 640px) { .cards { grid-template-columns: 1fr 1fr; gap: 16px; } }
.cards--3 { }
@media (min-width: 900px) { .cards--3 { grid-template-columns: 1fr 1fr 1fr; } }
.card { display: flex; flex-direction: column; gap: 6px; padding: 18px 20px 20px; border: 1px solid var(--rule); border-radius: 3px; background: transparent; transition: border-color 200ms var(--ease), background-color 200ms var(--ease); min-height: 100%; }
a.card:hover { border-color: var(--accent); }
.card__n { font-family: var(--sans); font-size: 0.75rem; font-weight: 500; letter-spacing: 0.12em; color: var(--accent); }
.card__title { font-size: 1.1875rem; line-height: 1.25; }
.card__meta { font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); }
.card__text { font-size: 0.9375rem; line-height: 1.5; color: var(--ink); }
.card__more { margin-top: auto; padding-top: 8px; font-family: var(--sans); font-size: 0.875rem; font-weight: 500; color: var(--muted); }
a.card:hover .card__more { color: var(--accent); }

/* Latest strip (home) */
.latest { display: grid; gap: 14px; }
@media (min-width: 640px) { .latest { grid-template-columns: 1fr 1fr; gap: 16px; } }
.latest__item { padding: 16px 0 0; border-top: 1px solid var(--rule); }
.latest__label { font-family: var(--sans); font-size: 0.75rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
.latest__title { font-size: 1.0625rem; font-weight: 600; line-height: 1.35; }
.latest__title a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); }
.latest__title a:hover { color: var(--accent); border-color: var(--accent); }
.latest__meta { margin-top: 6px; font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); }

/* Theme groups (research hub) */
.theme { padding: 32px 0; border-top: 1px solid var(--rule); }
.theme:first-of-type { border-top: 0; padding-top: 8px; }
.theme__title { font-size: 1.375rem; margin-bottom: 6px; }
.theme__text { color: var(--muted); max-width: 60ch; margin-bottom: 18px; }

/* Project pages */
.abstract { font-size: clamp(1.125rem, 1.7vw, 1.3125rem); line-height: 1.5; margin-bottom: 28px; }
.prose h2 { font-family: var(--sans); font-size: 0.8125rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin: 32px 0 10px; }
.prose h2:first-child { margin-top: 0; }
.prose p, .prose li { max-width: 62ch; }
.prose ul { display: grid; gap: 8px; }
.prose ul li { padding-left: 18px; position: relative; }
.prose ul li::before { content: ''; position: absolute; left: 0; top: 0.75em; width: 8px; height: 1px; background: var(--accent); }
.figure { margin: 24px 0; }
.figure img { width: 100%; height: auto; background: var(--paper-2); border: 1px solid var(--rule); }
.figure--cover { max-width: 220px; }
.figure__caption { margin-top: 8px; font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); line-height: 1.5; }
.figure__link { white-space: nowrap; }
.figure__link::before { content: '·'; color: var(--accent); padding: 0 6px; }
.links { display: flex; flex-wrap: wrap; gap: 8px 20px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; }
.links a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); }
.links a:hover { color: var(--accent); border-color: var(--accent); }
.prose ul.links li { padding-left: 0; }
.prose ul.links li::before { content: none; }
.papers { display: grid; gap: 10px; }
.papers li { font-size: 1rem; line-height: 1.5; }
.prose ul.papers li { padding-left: 0; }
.prose ul.papers li::before { content: none; }
.pager { margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--rule); display: flex; justify-content: space-between; gap: 16px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; }
.pager a { color: var(--muted); }
.pager a:hover { color: var(--accent); }

/* About */
.bio { font-size: clamp(1.0625rem, 1.6vw, 1.25rem); line-height: 1.55; }
.positions { display: grid; gap: 10px; }
.positions li { display: grid; grid-template-columns: 1fr; gap: 2px; padding: 10px 0; border-top: 1px solid var(--rule); }
@media (min-width: 640px) { .positions li { grid-template-columns: minmax(0, 1fr) auto; column-gap: 24px; align-items: baseline; } }
.positions li:last-child { border-bottom: 1px solid var(--rule); }
.positions strong { font-weight: 600; }
.positions .where { color: var(--muted); }
.positions .when { font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); white-space: nowrap; }
.background { color: var(--ink); max-width: 62ch; }
.cv-links { display: flex; flex-wrap: wrap; gap: 10px 22px; font-family: var(--sans); font-size: 0.9375rem; font-weight: 500; }
.cv-links a { color: var(--ink); border-bottom: 1px solid var(--accent-soft); }
.cv-links a:hover { color: var(--accent); border-color: var(--accent); }

/* Publications */
.pubs { display: grid; gap: 12px; counter-reset: pub; }
.pubs li { position: relative; padding-left: 2.25rem; line-height: 1.5; font-size: 1rem; }
.pubs li::before { counter-increment: pub; content: counter(pub); position: absolute; left: 0; top: 0.15em; font-family: var(--sans); font-size: 0.75rem; font-weight: 500; color: var(--muted); }
.pubs--plain li { padding-left: 0; }
.pubs--plain li::before { content: none; }
.pubs .where { color: var(--muted); }

/* Advisory */
.area__title { font-size: 1.125rem; margin-bottom: 6px; }
.area__text { font-size: 0.9375rem; line-height: 1.5; }
.engage { display: grid; gap: 8px; }
.engage li, .delivered li { max-width: 62ch; }
.engage strong, .delivered strong { font-weight: 600; }
.delivered { display: grid; gap: 12px; }
.note { margin-top: 24px; font-family: var(--sans); font-size: 0.875rem; color: var(--muted); max-width: 70ch; }
.closing { padding: 40px 0 72px; border-top: 1px solid var(--rule); }
.closing__line { font-size: clamp(1.25rem, 2.2vw, 1.625rem); line-height: 1.4; max-width: 34ch; margin-bottom: 20px; }

/* Cargo & Collateral */
.wordmark { width: 100%; max-width: 380px; margin: 0 0 24px; }
.writing { display: grid; }
.writing__item { padding: 16px 0; border-top: 1px solid var(--rule); display: grid; gap: 4px; }
.writing__item:last-child { border-bottom: 1px solid var(--rule); }
.writing__date { font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); }
.writing__title { font-size: 1.125rem; font-weight: 600; letter-spacing: -0.01em; }
.writing__title:hover { color: var(--accent); }

/* Prose pages: disclaimer, 404 */
.page-head--tall { min-height: 60vh; display: flex; align-items: center; }
.prose-page { padding: 8px 0 80px; }
.prose-page h2 { font-size: 1.25rem; margin: 28px 0 8px; font-family: var(--serif); letter-spacing: -0.01em; text-transform: none; color: var(--ink); }

/* Footer */
.footer { padding: 36px 0 28px; border-top: 1px solid var(--rule); }
.footer__row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px 40px; font-family: var(--sans); font-size: 0.875rem; color: var(--muted); }
.footer__links { display: flex; align-items: center; flex-wrap: wrap; gap: 8px 22px; }
.footer__links a { color: var(--muted); border-bottom: 1px solid transparent; }
.footer__links a:hover { color: var(--accent); border-color: var(--accent); }
.footer__tag { margin-top: 10px; font-family: var(--sans); font-size: 0.8125rem; color: var(--muted); }

/* Reveal */
.reveal { opacity: 0; transition: opacity 300ms var(--ease); }
.reveal.is-visible { opacity: 1; }
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transition: none; }
  *, *::before, *::after { transition: none !important; animation: none !important; }
}
```

- [ ] **Step 2: Rewrite `tools/chrome/nav.html`**

```html
<nav class="nav" aria-label="Primary">
  <div class="col col--wide nav__bar">
    <a class="logo" href="/" aria-label="Matteo Giordano, home">
      <svg class="logo__mark" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 5h20M12 5v17"/></svg>
      <span class="logo__text">Matteo Giordano</span>
    </a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-links">
      <span class="nav__toggle-label">Menu</span>
      <span class="nav__toggle-icon" aria-hidden="true"></span>
    </button>
    <div class="nav__links" id="nav-links">
      <div class="nav__item"><a class="nav__link" href="/about">About</a></div>
      <div class="nav__item nav__item--menu">
        <a class="nav__link" href="/research">Research <svg class="nav__caret" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5l3 3 3-3"/></svg></a>
        <div class="nav__menu" aria-label="Research projects">
          <a class="nav__menu-all" href="/research">All research</a>
          <p class="nav__menu-group">Monetary architecture</p>
          <a href="/research/balance-sheet-modelling">Balance-sheet modelling</a>
          <a href="/research/eurozone">Eurozone asymmetries and fragmentation</a>
          <a href="/research/subordination">Monetary subordination</a>
          <a href="/research/gegi-study">Transformation of the eurozone architecture</a>
          <p class="nav__menu-group">Macro-financial strategy</p>
          <a href="/research/macro-structures-dmo">Macro-structure, DMOs and monetary regimes</a>
          <p class="nav__menu-group">Defence economics</p>
          <a href="/research/defence-economics">Modelling the defence-industrial base</a>
        </div>
      </div>
      <div class="nav__item"><a class="nav__link" href="/publications">Publications</a></div>
      <div class="nav__item"><a class="nav__link" href="/cargo-and-collateral">Cargo &amp; Collateral</a></div>
      <a class="btn btn--sm nav__cta" href="/advisory">Advisory</a>
    </div>
  </div>
</nav>
```
And in `tools/chrome/footer.html` change `<div class="wrap">` to `<div class="col col--wide">` (nothing else).

- [ ] **Step 3: `js/site.js`: render the newest writing entry on the home page**

Replace `initWriting` with a version that also fills `#latest-note` when present:
```js
  function renderLatest(items) {
    var slot = document.getElementById('latest-note');
    if (!slot || !items.length || !items[0].title) return;
    var it = items[0];
    var t = slot.querySelector('.latest__title'), m = slot.querySelector('.latest__meta');
    if (!t) return;
    var a = document.createElement('a'); a.textContent = it.title;
    if (it.href && /^https:\/\//.test(it.href)) { a.setAttribute('href', it.href); a.setAttribute('rel', 'noopener'); a.setAttribute('target', '_blank'); }
    t.textContent = ''; t.appendChild(a);
    if (m && it.date) m.textContent = it.date + ' · Cargo & Collateral';
  }

  function initWriting() {
    var list = document.getElementById('writing-list');
    var empty = document.getElementById('writing-empty');
    var latest = document.getElementById('latest-note');
    if ((!list || !empty) && !latest) return;
    if (!window.fetch) return;
    fetch('/data/writing.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (items) {
      if (!Array.isArray(items) || !items.length) return;
      renderLatest(items);
      if (!list || !empty) return;
      items.forEach(function (it) {
        if (!it || !it.title) return;
        var li = document.createElement('li'); li.className = 'writing__item';
        var d = document.createElement('span'); d.className = 'writing__date'; d.textContent = it.date || '';
        var t = document.createElement(it.href && /^https:\/\//.test(it.href) ? 'a' : 'span'); t.className = 'writing__title'; t.textContent = it.title;
        if (t.tagName === 'A') { t.setAttribute('href', it.href); t.setAttribute('rel', 'noopener'); t.setAttribute('target', '_blank'); }
        li.appendChild(d); li.appendChild(t); list.appendChild(li);
      });
      if (list.children.length) { list.removeAttribute('hidden'); empty.setAttribute('hidden', ''); }
    }).catch(function () { /* keep the static fallback */ });
  }
```
Note the fetch path is now absolute (`/data/writing.json`).

- [ ] **Step 4: Checks** — brace balance on the CSS (`python3 -c "s=open('css/site.css').read(); assert s.count('{')==s.count('}')"`), `node --check js/site.js` or `jsc`, `python3 tools/chrome.py` (rewrites the nav into all existing pages; they will look wrong until rewritten in later tasks, which is expected), `python3 tools/check.py` → the dropdown links report `broken link /research/...` for the six project pages (expected until Task 4 and 5).

- [ ] **Step 5: Commit** — subject `Stylesheet v2, Research sub-menu, latest-note hook`.

---

## Page shell (all page tasks)

Every page is this file with `{{TITLE}}`, `{{DESCRIPTION}}`, `{{PATH}}` and `{{MAIN}}` filled. Project pages live at `research/<slug>.html` and use the same shell (all hrefs are absolute so depth does not matter).

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

Project-page `<main>` template (used by Tasks 4 and 5; `{{THEME}}`, `{{H1}}`, `{{META}}`, `{{BODY}}`, `{{PREV}}`, `{{NEXT}}` filled per page):
```html
  <main id="main">
    <article>
      <header class="page-head">
        <div class="col">
          <p class="eyebrow reveal"><a href="/research">Research</a> · {{THEME}}</p>
          <h1 class="page-title reveal">{{H1}}</h1>
          <p class="meta reveal">{{META}}</p>
        </div>
      </header>
      <div class="col prose reveal">
        {{BODY}}
        <nav class="pager" aria-label="Other projects">{{PREV}}{{NEXT}}</nav>
      </div>
    </article>
  </main>
```
`{{PREV}}`/`{{NEXT}}` are `<a href="/research/<slug>">← <short title></a>` and `<a href="/research/<slug>"><short title> →</a>` following the dropdown order (balance-sheet-modelling → eurozone → subordination → gegi-study → macro-structures-dmo → defence-economics); the first page has an empty `{{PREV}}` replaced by `<span></span>`, the last an empty `{{NEXT}}` replaced by `<span></span>`.

---

### Task 3: Home and About (rewrite)

**Files:**
- Rewrite: `index.html`, `about.html`

- [ ] **Step 1: `index.html`** — TITLE `Dr Matteo Giordano — Macro-financial strategist`; DESCRIPTION `Macro-financial strategist: shipping, monetary structures, and off-balance-sheet finance. Co-founder of Garrison Sterling; Associate Researcher, Global Climate Forum; PhD, SOAS.`; PATH `/`.

```html
  <main id="main">
    <header class="hero" aria-labelledby="hero-title">
      <div class="col col--wide">
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

    <section class="section" aria-labelledby="lines-title">
      <div class="col col--wide">
        <div class="section__head reveal"><h2 class="section__title" id="lines-title">Four lines of work</h2><a class="section__more" href="/research">All research</a></div>
        <div class="cards">
          <a class="card reveal" href="/cargo-and-collateral"><span class="card__n" aria-hidden="true">1</span><h3 class="card__title">Shipping and trade finance</h3><p class="card__text">The freight rate is the output; the credit chain is the mechanism. Read from inside the industry rather than off a screen.</p><span class="card__more">Cargo &amp; Collateral</span></a>
          <a class="card reveal" href="/research/macro-structures-dmo"><span class="card__n" aria-hidden="true">2</span><h3 class="card__title">Macro-financial strategy and research</h3><p class="card__text">Where the pressure sits in a system, and what it takes to move it. Sovereign, monetary and market structure, read at the level of the mechanism.</p><span class="card__more">Macro-structure, DMOs and monetary regimes</span></a>
          <a class="card reveal" href="/research/defence-economics"><span class="card__n" aria-hidden="true">3</span><h3 class="card__title">Defence and security economics</h3><p class="card__text">Capability is downstream of industrial structure and financing. The defence-industrial base read as an economy; the commercial side runs through Garrison Sterling.</p><span class="card__more">Modelling the defence-industrial base</span></a>
          <a class="card reveal" href="/research#monetary-architecture"><span class="card__n" aria-hidden="true">4</span><h3 class="card__title">Monetary architecture and hierarchy</h3><p class="card__text">Money is a hierarchy of interlocking balance sheets; a crisis is the moment they stop clearing. Collateral, repo, TARGET and subordination in the euro area.</p><span class="card__more">Four projects</span></a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="latest-title">
      <div class="col col--wide">
        <div class="section__head reveal"><h2 class="section__title" id="latest-title">Latest</h2></div>
        <div class="latest">
          <div class="latest__item reveal" id="latest-note">
            <p class="latest__label">Newsletter</p>
            <p class="latest__title"><a href="https://cargoandcollateral.substack.com/" data-link="SUBSTACK_URL" rel="noopener" target="_blank">Cargo &amp; Collateral on Substack</a></p>
            <p class="latest__meta">Macro-finance and shipping, read through balance sheets</p>
          </div>
          <div class="latest__item reveal">
            <p class="latest__label">Paper</p>
            <p class="latest__title"><a href="https://doi.org/10.1017/elo.2025.10043" rel="noopener">ECB monetary policy in a quandary</a></p>
            <p class="latest__meta">Lapavitsas and Giordano, 2026 · <em>European Law Open</em></p>
          </div>
        </div>
      </div>
    </section>
  </main>
```

- [ ] **Step 2: `about.html`** — TITLE `About — Matteo Giordano`; DESCRIPTION `Macro strategist in the shipping industry; co-founder of Garrison Sterling; Associate Researcher, Global Climate Forum; PhD in economics, SOAS University of London.`; PATH `/about`.

```html
  <main id="main">
    <header class="page-head">
      <div class="col">
        <p class="eyebrow reveal">About</p>
        <!-- DRAFT -->
        <h1 class="page-title reveal">Economist by training, strategist by trade.</h1>
        <!-- /DRAFT -->
        <p class="bio mt-24 reveal">Macro strategist and financial analyst in the shipping industry, based in Greece. Co-founder and Director of <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a>, an independent defence economics firm, and Associate Researcher at the <a href="https://globalclimateforum.org/portfolio-item/matteo-giordano/" rel="noopener">Global Climate Forum</a>, Berlin, behind the balance-sheet models of the <a href="https://obfa-transform.eu" rel="noopener">OBFA-TRANSFORM Project</a> and the <a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a>. PhD in economics, SOAS University of London, on monetary subordination in the euro area, under Prof. Costas Lapavitsas; lecturer there to 2025; defence economist at the <a href="https://www.ukdsc.org" rel="noopener">UKDSC</a>, inside the <a href="https://www.gov.uk/government/organisations/ministry-of-defence" rel="noopener">Ministry of Defence</a> ecosystem, to September 2026.</p>
        <nav class="cv-links mt-24 reveal" aria-label="CV and profiles">
          <a href="https://app.box.com/s/18pq9r7919gcxvu23hk5v4wda4hq6dq4" data-link="CV_URL" rel="noopener" target="_blank">Download CV</a>
          <a href="https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt" data-link="CV_ACADEMIC_URL" rel="noopener" target="_blank">Academic CV</a>
          <a href="https://orcid.org/0000-0002-1588-6735" data-link="ORCID_URL" rel="noopener" target="_blank">ORCID</a>
          <a href="https://www.linkedin.com/in/matteogiordano-economist/" data-link="LINKEDIN_URL" rel="noopener" target="_blank">LinkedIn</a>
          <a href="mailto:mg.macroeconomics@gmail.com" data-mailto>Email</a>
        </nav>
      </div>
    </header>

    <section class="section" aria-labelledby="positions-title">
      <div class="col">
        <div class="section__head reveal"><h2 class="section__title" id="positions-title">Positions</h2></div>
        <ul class="positions reveal">
          <!-- DRAFT -->
          <li><span><strong>Macro strategist and financial analyst</strong>, <span class="where">shipping industry, Greece</span></span><span class="when">2026–</span></li>
          <!-- /DRAFT -->
          <li><span><strong>Co-founder and Director</strong>, <span class="where"><a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a>. Leads the modelling: economic-impact models and supplier-level metrics on the defence economy</span></span><span class="when">2026–</span></li>
          <li><span><strong>Associate Researcher</strong>, <span class="where">Global Climate Forum, Berlin. OBFA-TRANSFORM: balance-sheet modelling of the euro-area monetary architecture</span></span><span class="when">2023–</span></li>
          <li><span><strong>Senior Defence Economist</strong>, <span class="where">UKDSC, within the Ministry of Defence ecosystem. Input-Output and scenario models of the defence-industrial base; briefings to government and industry</span></span><span class="when">2025–2026</span></li>
          <li><span><strong>Lecturer in Economics</strong>, <span class="where">SOAS University of London</span></span><span class="when">2023–2025</span></li>
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="education-title">
      <div class="col">
        <div class="section__head reveal"><h2 class="section__title" id="education-title">Education</h2></div>
        <ul class="positions reveal">
          <li><span><strong>PhD, Economics</strong>, <span class="where">SOAS University of London. <em>Monetary Subordination in the Eurozone</em>, supervised by Prof. Costas Lapavitsas</span></span><span class="when">2020–2025</span></li>
          <li><span><strong>MSc, International Political Economy</strong>, <span class="where">LSE. Advisor: Prof. Jeffrey Chwieroth</span></span><span class="when">2019–2020</span></li>
          <li><span><strong>BSc, Economics (Hons)</strong>, <span class="where">SOAS University of London. Undergraduate Prize in Economics</span></span><span class="when">2016–2019</span></li>
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="background-title">
      <div class="col">
        <div class="section__head reveal"><h2 class="section__title" id="background-title">Background</h2></div>
        <div class="background reveal">
          <p><strong>Methods.</strong> Balance-sheet mapping, stock-flow-consistent accounting, Input-Output, gravity models, VAR/SVAR, panel and time-series methods, scenario analysis. Applied to euro-area monetary policy and transmission, sovereign debt dynamics, fiscal-monetary interaction, financial fragmentation, shipping and trade finance, defence and war finance, trade and capital-flow regimes. R and Python; Excel; LaTeX.</p>
          <p><strong>Recognition.</strong> Research Associate funding, OBFA-Transformation project (Deutsche Forschungsgemeinschaft and GCF Berlin). Scholarship, Minsky Summer Seminar, Levy Economics Institute (2018). At SOAS: Outstanding Teaching Award (2024–25), Best Use of Technology Enhanced Learning (2023–24), nomination for Postgraduate Research Supervisor of the Year (2024–25).</p>
          <p><strong>Affiliations.</strong> <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a> · <a href="https://globalclimateforum.org/portfolio-item/matteo-giordano/" rel="noopener">Global Climate Forum</a> · <a href="https://www.soas.ac.uk/about/matteo-giordano-0" rel="noopener">SOAS University of London</a> · <a href="https://www.ukdsc.org" rel="noopener">UKDSC</a> (to September 2026) · <a href="https://wearesparc.org/" rel="noopener">SPARCollective</a>, founding member · EReNSEP · Young Scholars Initiative, INET.</p>
          <p><strong>Personal.</strong> Dual Italian-British national, based in Greece. Italian (native) · English (bilingual) · French (advanced) · Greek and Spanish (beginner).</p>
        </div>
      </div>
    </section>
  </main>
```

- [ ] **Step 3: Run chrome + check; word counts** — the snippet from v1 Task 5 Step 2 adapted (`re.search(r'<main.*?</main>')`) on both files: home ≤150 words outside the Latest strip is the target, whole main ≤200; about ≤300. Report the numbers.
- [ ] **Step 4: Commit** — subject `Home and About v2`.

---

### Task 4: Research hub and the four monetary-architecture project pages

**Files:**
- Rewrite: `research.html`
- Create: `research/balance-sheet-modelling.html`, `research/eurozone.html`, `research/subordination.html`, `research/gegi-study.html`

- [ ] **Step 1: `research.html`** — TITLE `Research — Matteo Giordano`; DESCRIPTION `Research projects behind four lines of work: shipping and trade finance, macro-financial strategy, defence economics, and monetary architecture in the euro area.`; PATH `/research`.

```html
  <main id="main">
    <header class="page-head">
      <div class="col col--wide">
        <p class="eyebrow reveal">Research</p>
        <!-- DRAFT -->
        <h1 class="page-title reveal">Six projects, four lines of work.</h1>
        <p class="lede reveal">Each project carries its own argument, data and outputs. The published record is on <a class="link" href="/publications">Publications</a>; commissioned work runs through <a class="link" href="/advisory">Advisory</a>.</p>
        <!-- /DRAFT -->
      </div>
    </header>

    <div class="col col--wide">
      <section class="theme" id="monetary-architecture" aria-labelledby="t-monetary">
        <h2 class="theme__title reveal" id="t-monetary">Monetary architecture and hierarchy</h2>
        <p class="theme__text reveal">Money as a hierarchy of interlocking balance sheets, crises as the moment they stop clearing. The methodological core of everything else here.</p>
        <div class="cards">
          <a class="card reveal" href="/research/balance-sheet-modelling"><h3 class="card__title">Balance-sheet modelling and monetary architecture</h3><p class="card__meta">Ongoing · Global Climate Forum</p><p class="card__text">The framework behind the public Monetary Architecture Online Tool; long-run financial flows from 1870; crisis dynamics through balance sheets.</p></a>
          <a class="card reveal" href="/research/eurozone"><h3 class="card__title">Asymmetries, imbalances and fragmentation in the eurozone</h3><p class="card__meta">Ongoing</p><p class="card__text">The euro area's imbalances traced to its plumbing: CCPs, CSDs, the ECB and the national central banks. Three empirical pillars.</p></a>
          <a class="card reveal" href="/research/subordination"><h3 class="card__title">Monetary subordination in the eurozone</h3><p class="card__meta">PhD thesis · SOAS, 2025</p><p class="card__text">Monetary hierarchy, hybrid money and selective fragmentation as the three pillars of subordination inside a monetary union.</p></a>
          <a class="card reveal" href="/research/gegi-study"><h3 class="card__title">Transformation of the eurozone architecture</h3><p class="card__meta">GEGI Study · Boston University, 2025</p><p class="card__text">Contagion across euro-area and US balance sheets as the endogenous force that reshaped the EMU, from the financial crisis to 2014.</p></a>
        </div>
      </section>

      <section class="theme" id="macro-strategy" aria-labelledby="t-macro">
        <h2 class="theme__title reveal" id="t-macro">Macro-financial strategy and research</h2>
        <p class="theme__text reveal">Where the pressure sits in a system, and what it takes to move it.</p>
        <div class="cards">
          <a class="card reveal" href="/research/macro-structures-dmo"><h3 class="card__title">Macro-structure, DMOs and monetary regimes</h3><p class="card__meta">With Enrico Pulieri · in preparation</p><p class="card__text">Central bank independence is half the story. Monetary policy and debt management read as one architecture rather than two literatures.</p></a>
        </div>
      </section>

      <section class="theme" id="defence" aria-labelledby="t-defence">
        <h2 class="theme__title reveal" id="t-defence">Defence and security economics</h2>
        <p class="theme__text reveal">Capability is downstream of industrial structure and financing.</p>
        <div class="cards">
          <a class="card reveal" href="/research/defence-economics"><h3 class="card__title">Modelling the defence-industrial base</h3><p class="card__meta">Applied work · 2025–2026</p><p class="card__text">Input-Output models of linkage and dependency, gravity models of defence trade, and the fiscal sustainability of rearmament.</p></a>
        </div>
      </section>

      <section class="theme" id="shipping" aria-labelledby="t-shipping">
        <h2 class="theme__title reveal" id="t-shipping">Shipping and trade finance</h2>
        <p class="theme__text reveal">The freight rate is the output; the credit chain is the mechanism.</p>
        <div class="cards">
          <a class="card reveal" href="/cargo-and-collateral"><h3 class="card__title">Cargo &amp; Collateral</h3><p class="card__meta">Newsletter · ongoing</p><p class="card__text">Chartering, freight rates, port throughput, forwarder and carrier working capital and trade finance, read as claims and obligations.</p></a>
        </div>
      </section>
    </div>
  </main>
```

- [ ] **Step 2: `research/balance-sheet-modelling.html`** — TITLE `Balance-sheet modelling and monetary architecture — Matteo Giordano`; DESCRIPTION `Money as a hierarchy of interlocking balance sheets: the Monetary Architecture framework, long-run financial flows, and crisis dynamics through balance sheets.`; PATH `/research/balance-sheet-modelling`; THEME `Monetary architecture`; H1 `Balance-sheet modelling and monetary architecture`; META `Ongoing · Associate Researcher, Global Climate Forum · OBFA-TRANSFORM`; PREV `<span></span>`; NEXT `/research/eurozone` "Eurozone asymmetries".

BODY:
```html
        <p class="abstract">Money is a hierarchy of interlocking balance sheets, and a crisis is the moment they stop clearing. Balance-sheet modelling makes the structure visible, traces how elasticity and stress propagate through it, and carries both historical analysis and forward scenarios. It is the methodological core of most of my research.</p>
        <h2>The Monetary Architecture framework</h2>
        <p>As Associate Researcher at the Global Climate Forum I contribute to the <a href="https://obfa-transform.eu" rel="noopener">OBFA-TRANSFORM Project</a> and helped build the <a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a>: the euro area's architecture rendered as navigable, practitioner-facing balance-sheet analysis, open to anyone.</p>
        <h2>Long-run financial-flow dynamics</h2>
        <p>Trade, capital and financial flows from 1870 to the present, read for structural breaks and regime shifts in globalisation and financial integration, and linked to scenarios for financing large-scale transformation.</p>
        <h2>Crisis dynamics through balance sheets</h2>
        <p>Structured process-tracing combined with balance-sheet visualisation, used to explain crisis-driven institutional change. Applied to the euro area from the Global Financial Crisis onward in the <a href="/research/gegi-study">GEGI study</a>.</p>
        <h2>Method</h2>
        <p>Balance-sheet mapping and visualisation, stock-flow-consistent accounting, long-run time-series analysis, and scenario frameworks, on primary and secondary data across private and public sectors.</p>
        <h2>Outputs</h2>
        <ul class="links"><li><a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a></li><li><a href="https://obfa-transform.eu/key-concepts/monetary-architecture" rel="noopener">The framework, OBFA-TRANSFORM</a></li></ul>
        <h2>Related publications</h2>
        <ul class="papers">
          <li>Murau, S., Goghie, A., Giordano, M. and Reimer, F. (2025). Transformation of the Eurozone Architecture. <em>GEGI Study</em>, Boston University. <a href="https://doi.org/10.2139/ssrn.5648890" rel="noopener">DOI</a></li>
          <li>Murau, S., Goghie, A., Giordano, M. and Reimer, F. (forthcoming). The Monetary Architecture Framework. <em>GEGI Study</em>, Boston University.</li>
        </ul>
```

- [ ] **Step 3: `research/eurozone.html`** — TITLE `Asymmetries, imbalances and fragmentation in the eurozone — Matteo Giordano`; DESCRIPTION `The euro area's imbalances traced to its infrastructure: monetary hierarchies, selective fragmentation, and the hybrid refinancing behind TARGET balances.`; PATH `/research/eurozone`; THEME `Monetary architecture`; H1 `Asymmetries, imbalances and fragmentation in the eurozone`; META `Ongoing · Three empirical pillars on official datasets`; PREV `/research/balance-sheet-modelling` "Balance-sheet modelling"; NEXT `/research/subordination` "Monetary subordination".

BODY:
```html
        <p class="abstract">The euro area's imbalances are built into its infrastructure. This project traces them to the plumbing, CCPs, CSDs, the ECB and the national central banks, and to the link between monetary integration and the financialisation of the member economies. Three empirical pillars, built on official datasets that are largely unused.</p>
        <figure class="figure"><img src="/img/figures/T2_EoP_plot.png" alt="TARGET2 balances by national central bank, end of period, 2008 to 2023." width="1600" height="889" loading="lazy" decoding="async"><figcaption class="figure__caption">TARGET2 balances, end of period.<a class="figure__link" href="/img/figures/full/T2_EoP_plot.png">Full size</a></figcaption></figure>
        <h2>Monetary hierarchies in the EMU</h2>
        <p>Jurisdictions are tiered and legacy euros persist. TARGET is the backstop that holds the tiering together.</p>
        <figure class="figure"><img src="/img/figures/Liabilities_nonEA_Euro_Plot.png" alt="Euro-denominated liabilities to non-euro-area residents, by central bank, 2016 to 2021." width="1600" height="889" loading="lazy" decoding="async"><figcaption class="figure__caption">Euro liabilities outside the euro area.<a class="figure__link" href="/img/figures/full/Liabilities_nonEA_Euro_Plot.png">Full size</a></figcaption></figure>
        <h2>Fragmentation and selective integration</h2>
        <p>Money markets fragment even with liquidity in excess. The shortage that binds is collateral.</p>
        <figure class="figure"><img src="/img/figures/Origin_Collateral_plot.png" alt="Origin of government collateral used by euro-area banks in secured transactions, domestic versus non-domestic, by reporting agent, 2018 to 2020." width="1600" height="889" loading="lazy" decoding="async"><figcaption class="figure__caption">Origin of collateral in secured transactions.<a class="figure__link" href="/img/figures/full/Origin_Collateral_plot.png">Full size</a></figcaption></figure>
        <h2>Capital and liquidity in hybrid refinancing</h2>
        <p>Where TARGET balances actually come from, and how the hybrid working of the mechanism produces them.</p>
        <figure class="figure"><img src="/img/figures/Italy_T2_Fdec_BoP_Cumulative_Plot.png" alt="Italy's cumulative balance of payments decomposed by component against its TARGET2 balance, 2008 to 2021." width="1600" height="889" loading="lazy" decoding="async"><figcaption class="figure__caption">Italy: balance of payments and TARGET balances, cumulative flows.<a class="figure__link" href="/img/figures/full/Italy_T2_Fdec_BoP_Cumulative_Plot.png">Full size</a></figcaption></figure>
        <h2>Related publications</h2>
        <ul class="papers">
          <li>Giordano, M. (2025). Tiered Euro-Monies: Perpetrating Monetary Hierarchies from the ECU to the Euro. <em>Review of Evolutionary Political Economy</em>, 6: 565–587. <a href="https://doi.org/10.1007/s43253-025-00154-4" rel="noopener">DOI</a></li>
          <li>Murau, S., Goghie, A. and Giordano, M. (2025). Encumbered Security? Vertical and Horizontal Repos in the Euro Area and Their Inherent Ambiguity. <em>Journal of Financial Regulation</em>, 11(2). <a href="https://doi.org/10.1093/jfr/fjaf003" rel="noopener">DOI</a></li>
          <li>Murau, S. and Giordano, M. (2024). Forging Monetary Unification through Novation: The TARGET System and the Politics of Central Banking in Europe. <em>Socio-Economic Review</em>, 22(3): 1283–1312. <a href="https://doi.org/10.1093/ser/mwad067" rel="noopener">DOI</a></li>
        </ul>
```

- [ ] **Step 4: `research/subordination.html`** — TITLE `Monetary subordination in the eurozone — Matteo Giordano`; DESCRIPTION `Monetary hierarchies, hybrid money and selective fragmentation as the three pillars of subordination inside a monetary union. PhD thesis, SOAS University of London.`; PATH `/research/subordination`; THEME `Monetary architecture`; H1 `Monetary subordination in the eurozone`; META `PhD thesis, SOAS University of London, 2025 · Supervisor: Prof. Costas Lapavitsas`; PREV `/research/eurozone` "Eurozone asymmetries"; NEXT `/research/gegi-study` "Eurozone architecture".

BODY:
```html
        <p class="abstract">Subordination inside a monetary union is obvious in aggregate, persistent yield spreads, divergent productivity, and elusive in its specific forms. This thesis identifies the forms. A monetary union is the most extreme form of monetary integration, which makes subordination more visible in appearance and more subtle in mechanism at the same time. Shared money formalises it.</p>
        <figure class="figure"><img src="/img/figures/Subordination_EMU.png" alt="Conceptual map of the thesis: macro-structure, monetary hierarchy and hybrid money feeding structural subordination in the EMU, its reproduction and hegemony." width="841" height="595" loading="lazy" decoding="async"><figcaption class="figure__caption">The conceptual framework behind subordination and its distribution across the chapters.<a class="figure__link" href="/img/figures/full/Subordination_EMU.png">Full size</a></figcaption></figure>
        <h2>Three pillars</h2>
        <p>Monetary subordination in the EMU rests on monetary hierarchies, hybrid money, and the selective fragmentation and integration of euro-area markets and institutions. Each is taken twice: as it appears, and through the mechanisms that sustain it, with empirical support from official datasets that are largely unused, balance-sheet analysis and graphical representation.</p>
        <h2>Consequences</h2>
        <p><strong>Italy.</strong> The single currency did not remove subordination; it reframed it. The centre shifted from the USD-based international system to a euro-centric form, with direct consequences for domestic economic development.</p>
        <p><strong>Six member states.</strong> A comparative analysis of financialisation shows subordinated EMU members behaving like subordinated emerging markets: their financialisation is shaped by their position in the hierarchy.</p>
        <h2>Outputs</h2>
        <ul class="links"><li><a href="https://soas-repository.worktribe.com/output/461747" rel="noopener">The thesis, SOAS repository</a></li></ul>
        <h2>Related publications</h2>
        <ul class="papers">
          <li>Giordano, M. (2025). Monetary Subordination in the Eurozone: Pillars and Asymmetries. <em>Competition &amp; Change</em>. <a href="https://doi.org/10.1177/10245294251400025" rel="noopener">DOI</a></li>
          <li>Giordano, M. and Pulieri, E. (forthcoming). From International to 'Regional' Financial Subordination: Italian Monetary Integration in the Eurozone. <em>Cambridge Journal of Economics</em>.</li>
          <li>Giordano, M. and Lapavitsas, C. (2023). Persistent institutional malfunctioning in the Eurozone. <em>The Japanese Political Economy</em>, 49(4): 295–307. <a href="https://doi.org/10.1080/2329194X.2023.2289883" rel="noopener">DOI</a></li>
        </ul>
```

- [ ] **Step 5: `research/gegi-study.html`** — TITLE `Transformation of the eurozone architecture — Matteo Giordano`; DESCRIPTION `Crises and institutional change in the offshore US-dollar system: how contagion through repo markets and the collateral framework reshaped the EMU. GEGI Study, Boston University.`; PATH `/research/gegi-study`; THEME `Monetary architecture`; H1 `Transformation of the eurozone architecture`; META `GEGI Study, Global Development Policy Center, Boston University, 2025 · S. Murau, A. S. Goghie, M. Giordano and F. Reimer`; PREV `/research/subordination` "Monetary subordination"; NEXT `/research/macro-structures-dmo` "Macro-structure and DMOs".

BODY:
```html
        <figure class="figure figure--cover"><img src="/img/figures/GEGIStudy.jpg" alt="Cover of the GEGI Study, Transformation of the Eurozone Architecture." width="209" height="297" loading="lazy" decoding="async"></figure>
        <p class="abstract">The Eurocrisis is usually explained by excessive sovereign issuance, a weak Stability and Growth Pact, or missing supranational supervision. None of those explains how a US-centric run on shadow money reached some EMU treasuries and not others. Our answer: it travelled through euro-area repo markets and the Eurosystem's collateral framework.</p>
        <h2>Argument</h2>
        <p>Contagion across the private and public balance sheets of the eurozone and US monetary architectures was the endogenous force that determined the EMU's transformation into its contemporary shape, from the Global Financial Crisis to the 2014 asset purchase programmes.</p>
        <h2>Method</h2>
        <p>Structured process-tracing combined with balance-sheet visualisation of crisis dynamics, built on the macro-financial model in Murau (2020) and on primary and secondary sources. The scheme runs in three steps: on-balance-sheet contraction; activation of inbuilt elasticity-provision mechanisms; and, where those fail, innovation: enhanced elasticity space, new instruments, or new institutions.</p>
        <h2>Outputs</h2>
        <ul class="links"><li><a href="https://doi.org/10.2139/ssrn.5648890" rel="noopener">Read the study on SSRN</a></li><li><a href="https://obfa-transform.eu/key-concepts/monetary-architecture" rel="noopener">The framework</a></li><li><a href="https://monetary-architecture.com/" rel="noopener">The tool</a></li><li><a href="https://www.youtube.com/watch?v=NAsoo08rG9k&amp;t=3004s" rel="noopener">Methodological presentation, 2023</a></li></ul>
        <h2>Related publications</h2>
        <ul class="papers">
          <li>Murau, S., Goghie, A. and Giordano, M. (2025). Encumbered Security? Vertical and Horizontal Repos in the Euro Area and Their Inherent Ambiguity. <em>Journal of Financial Regulation</em>, 11(2). <a href="https://doi.org/10.1093/jfr/fjaf003" rel="noopener">DOI</a></li>
          <li>Giordano, M. and Goghie, A. (2023). From Policy to Regime: the changing posture of the ECB between liquidity and collateral. <em>SocArXiv Working Paper</em>. <a href="https://doi.org/10.31235/osf.io/rw3ms" rel="noopener">DOI</a></li>
        </ul>
```

- [ ] **Step 6: Run chrome + check** — expected problems: only `broken link /research/macro-structures-dmo` and `/research/defence-economics` (Task 5). Confirm each project page's nav has `aria-current` on both its own dropdown link and the Research link (`grep -c aria-current research/eurozone.html` → 2).
- [ ] **Step 7: Commit** — subject `Research hub and monetary-architecture project pages`.

---

### Task 5: Macro-structure and defence project pages, Advisory

**Files:**
- Create: `research/macro-structures-dmo.html`, `research/defence-economics.html`
- Rewrite: `advisory.html`

- [ ] **Step 1: `research/macro-structures-dmo.html`** — TITLE `Macro-structure, DMOs and monetary regimes — Matteo Giordano`; DESCRIPTION `Monetary policy and debt management read as one architecture: the macro-structure of financialised capitalism, debt management office independence, and the monetary regime.`; PATH `/research/macro-structures-dmo`; THEME `Macro-financial strategy`; H1 `Macro-structure, DMOs and monetary regimes`; META `With Enrico Pulieri · In preparation`; PREV `/research/gegi-study` "Eurozone architecture"; NEXT `/research/defence-economics` "Defence-industrial base".

BODY:
```html
        <p class="abstract">Central bank independence is half the story. Sovereign debt is managed by a separate institution with its own claim to independence, and the two postures interact. This project reads monetary policy and debt management as one architecture rather than two literatures, and situates both inside the systemic structure of financialised capitalism.</p>
        <figure class="figure"><img src="/img/figures/Macro_Structure.png" alt="Stylised diagram of the EMU macro-structure: debt management office, banks, central counterparty, infrastructure and national central bank linked by government securities, collateral, repos and liquidity." width="1178" height="1020" loading="lazy" decoding="async"><figcaption class="figure__caption">Stylised representation of the EMU macro-structure.<a class="figure__link" href="/img/figures/full/Macro_Structure.png">Full size</a></figcaption></figure>
        <h2>Macro-structure</h2>
        <p>A conceptualisation of the systemic relations, architectures and tendencies running through financialised capitalism.</p>
        <h2>Debt management operations</h2>
        <p>The political economy of debt management: whether DMO "independence" holds, and where debt management offices work with the central bank or against it.</p>
        <h2>Monetary regime</h2>
        <p>Central-bank posture is not readable from policy decisions alone. Placing those decisions inside the financial architecture and the instruments available is what makes the regime visible.</p>
        <h2>Related publications</h2>
        <ul class="papers">
          <li>Giordano, M. and Pulieri, E. (forthcoming). Debt Management (in-)Dependence: The missing side of Central Banks and the Legacy of CBI.</li>
          <li>Giordano, M. and Goghie, A. (2023). From Policy to Regime: the changing posture of the ECB between liquidity and collateral through the lens of Monetary Regime. <em>SocArXiv Working Paper</em>. <a href="https://doi.org/10.31235/osf.io/rw3ms" rel="noopener">DOI</a></li>
          <li>Lapavitsas, C. and Giordano, M. (2026). ECB monetary policy in a quandary. <em>European Law Open</em>. <a href="https://doi.org/10.1017/elo.2025.10043" rel="noopener">DOI</a></li>
        </ul>
```

- [ ] **Step 2: `research/defence-economics.html`** — TITLE `Modelling the defence-industrial base — Matteo Giordano`; DESCRIPTION `Defence and security economics: industrial linkages, supply-chain resilience, alliances and burden-sharing, and the fiscal sustainability of rearmament.`; PATH `/research/defence-economics`; THEME `Defence economics`; H1 `Modelling the defence-industrial base`; META `Applied work, 2025–2026 · UKDSC, then Garrison Sterling`; PREV `/research/macro-structures-dmo` "Macro-structure and DMOs"; NEXT `<span></span>`.

BODY:
```html
        <p class="abstract">Capability is downstream of industrial structure and financing. This strand applies macro-financial and structural economics to defence, asking of the defence-industrial base the questions that run through the rest of my research: how a system absorbs shocks, where dependencies concentrate, what it costs to hold capability over time.</p>
        <p>It was the substance of my work as a defence economist at the UKDSC to September 2026. It continues commercially at <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a>, the defence economics firm I co-founded and direct, and as research here: applied, quantitative, and aimed at decision-relevant intelligence for policy and industry.</p>
        <h2>Industrial structure and resilience</h2>
        <p>Where supply-chain and strategic dependencies concentrate, and what industrial resilience actually requires. Input-Output modelling traces inter-sectoral linkages and spillovers across strategic sectors.</p>
        <h2>Alliances, trade and burden-sharing</h2>
        <p>Gravity models of bilateral defence and industrial flows, including NATO and allied contexts, and the structural forces shaping them.</p>
        <h2>Fiscal sustainability of defence</h2>
        <p>Whether elevated defence commitments can be financed over the long run: defence spending connected to sovereign debt dynamics, fiscal-monetary interaction, and the macroeconomic constraints studied elsewhere on this site.</p>
        <h2>Capability, productivity and measurement</h2>
        <p>Frameworks for measuring defence-industrial productivity and performance, and scenario-based assessment of investment gaps and capability shortfalls. Stock-flow-consistent accounting, VAR models and scenario analysis.</p>
        <h2>Outputs</h2>
        <ul class="links"><li><a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a></li><li><a href="/cargo-and-collateral">Rearmament as a financing problem, in Cargo &amp; Collateral</a></li></ul>
        <p class="note">This page describes research themes and methods only. It does not represent the views, positions, or outputs of the UK Defence Solutions Centre, the Ministry of Defence, Garrison Sterling, or any defence industry partner. See the <a href="/disclaimer">disclaimer</a>.</p>
```

- [ ] **Step 3: `advisory.html`** — TITLE `Advisory — Matteo Giordano`; DESCRIPTION `Macro-financial strategy for institutions that need to know how a system clears before they need to know where it trades: shipping and trade finance, sovereign and monetary structure, balance-sheet modelling.`; PATH `/advisory`.

```html
  <main id="main">
    <header class="page-head">
      <div class="col">
        <p class="eyebrow reveal">Advisory</p>
        <h1 class="page-title reveal">Macro-financial strategy for institutions that need to know how a system clears before they need to know where it trades.</h1>
        <p class="lede lede--ink reveal">Commissioned work from two directions. Ship finance and freight: lenders, lessors, owners, marine insurers and platforms. Allocators and credit funds: euro-area sovereign and monetary risk read structurally rather than off the spread. The brief is usually the same one: below the headline, what is the actual structure of claims here, where does the pressure sit, and what breaks first.</p>
        <div class="actions reveal"><a class="btn" href="mailto:mg.macroeconomics@gmail.com?subject=Advisory%20brief" data-mailto data-subject="Advisory brief">Discuss a brief</a></div>
      </div>
    </header>

    <section class="section" aria-labelledby="areas-title">
      <div class="col col--wide">
        <div class="section__head reveal"><h2 class="section__title" id="areas-title">Areas</h2></div>
        <div class="cards cards--3">
          <div class="card reveal"><h3 class="area__title">Shipping and trade finance</h3><p class="area__text">Freight exposure is working-capital exposure. Chartering and freight-rate risk, tonne-mile and throughput demand, forwarder and carrier working capital, trade finance structures, and the capital stack behind a fleet, including Greek and Mediterranean maritime economics. Written up in <a href="/cargo-and-collateral">Cargo &amp; Collateral</a>.</p></div>
          <div class="card reveal"><h3 class="area__title">Sovereign credit and monetary structure</h3><p class="area__text">Read at the level of the mechanism, not the spread. Sovereign risk and debt management, monetary transmission, collateral and repo, fragmentation and the settlement plumbing beneath it. Where the view comes from: <a href="/research/eurozone">the eurozone</a>, <a href="/research/subordination">subordination</a>, <a href="/research/macro-structures-dmo">macro-structure and DMOs</a>.</p></div>
          <div class="card reveal"><h3 class="area__title">Balance-sheet modelling</h3><p class="area__text">For questions that need a structure rather than a forecast. Bespoke modelling of a monetary architecture, a sector or a firm as interlocking balance sheets, built to be interrogated rather than believed. Method: <a href="/research/balance-sheet-modelling">balance-sheet modelling</a>.</p></div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="engage-title">
      <div class="col">
        <div class="section__head reveal"><h2 class="section__title" id="engage-title">Ways to engage</h2></div>
        <ul class="engage reveal">
          <li><strong>Expert calls.</strong> A single conversation on a specific question.</li>
          <li><strong>Commissioned notes and models.</strong> A defined question, a defined deliverable, a fixed deadline.</li>
          <li><strong>Speaking and workshops.</strong> Talks, seminars and closed-door briefings.</li>
        </ul>
        <p class="note">Anything where the exposure is defence, whether defence-industrial, rearmament, or macro-financial work on the defence economy, goes through <a href="https://garrisonsterling.com" rel="noopener">Garrison Sterling</a>. Shipping, sovereign and monetary work is taken here, in a personal capacity.</p>
      </div>
    </section>

    <section class="section" aria-labelledby="delivered-title">
      <div class="col">
        <div class="section__head reveal"><h2 class="section__title" id="delivered-title">Delivered work</h2></div>
        <!-- Append anonymised engagements in the same pattern: <li><strong>[Who, by type and geography].</strong> [The question.] [What was delivered.]</li> -->
        <ul class="delivered reveal">
          <li><strong>A public analytical tool.</strong> The <a href="https://monetary-architecture.com/" rel="noopener">Monetary Architecture Online Tool</a>, built with the Global Climate Forum: the euro area's monetary architecture as navigable, practitioner-facing balance-sheet analysis.</li>
          <li><strong>Models built to be interrogated.</strong> Balance-sheet and stock-flow-consistent models of monetary architectures; Input-Output and scenario models of the defence-industrial base; long-run financial-flow analysis.</li>
          <li><strong>Briefings to government and industry.</strong> Strategic briefings and economic assessments at the UKDSC, inside the Ministry of Defence ecosystem; reports that contributed to shaping MoD policy on defence-industrial productivity, programme viability, supply-chain resilience and industrial readiness.</li>
        </ul>
      </div>
    </section>

    <section class="closing" aria-label="Get in touch">
      <div class="col">
        <p class="closing__line reveal">To discuss a brief, write to me. Background: <a class="link" href="/about">About</a> and <a class="link" href="/publications">Publications</a>.</p>
        <div class="actions reveal"><a class="btn" href="mailto:mg.macroeconomics@gmail.com?subject=Advisory%20brief" data-mailto data-subject="Advisory brief">mg.macroeconomics@gmail.com</a></div>
        <p class="note reveal">All engagements are undertaken in a personal capacity and are independent of any employer, past or present, and of Garrison Sterling. Nothing produced under them is investment advice. See the <a href="/disclaimer">disclaimer</a>.</p>
      </div>
    </section>
  </main>
```

- [ ] **Step 4: Run chrome + check** → `check: 0 problem(s)` expected (every target now exists) apart from sitemap lines for the six new pages (fixed in Task 6).
- [ ] **Step 5: Commit** — subject `Project pages: macro-structure, defence; Advisory v2`.

---

### Task 6: Publications, Cargo & Collateral, sitemap, redirects, README

**Files:**
- Rewrite: `publications.html`, `cargo-and-collateral.html`, `sitemap.xml`
- Modify: `vercel.json`, `README.md`, `disclaimer.html`, `404.html` (wrapper class only)

- [ ] **Step 1: `publications.html`** — TITLE `Publications — Matteo Giordano`; DESCRIPTION `Journal articles, books and studies, and working papers on monetary economics, financial regulation and European political economy, with selected talks.`; PATH `/publications`.

```html
  <main id="main">
    <header class="page-head">
      <div class="col col--wide">
        <p class="eyebrow reveal">Publications</p>
        <!-- DRAFT -->
        <h1 class="page-title reveal">Journal articles, books and studies, working papers.</h1>
        <p class="lede reveal">Monetary economics, financial regulation, European political economy. Full record on <a class="link" href="https://orcid.org/0000-0002-1588-6735" data-link="ORCID_URL" rel="noopener" target="_blank">ORCID</a> and in the <a class="link" href="https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt" data-link="CV_ACADEMIC_URL" rel="noopener" target="_blank">academic CV</a>.</p>
        <!-- /DRAFT -->
      </div>
    </header>

    <section class="section" id="articles" aria-labelledby="articles-title">
      <div class="col col--wide">
        <div class="section__head reveal"><h2 class="section__title" id="articles-title">Journal articles</h2></div>
        <ol class="pubs reveal">
          <li>Lapavitsas, C. and Giordano, M. (2026). ECB monetary policy in a quandary. <em>European Law Open</em>. <a href="https://doi.org/10.1017/elo.2025.10043" rel="noopener">DOI</a></li>
          <li>Giordano, M. (2025). Monetary Subordination in the Eurozone: Pillars and Asymmetries. <em>Competition &amp; Change</em>. <a href="https://doi.org/10.1177/10245294251400025" rel="noopener">DOI</a></li>
          <li>Giordano, M. (2025). Displacement and Complementarity between Cryptocurrencies and Legacy Money. <em>The Japanese Political Economy</em>. <a href="https://doi.org/10.1080/2329194X.2025.2547035" rel="noopener">DOI</a></li>
          <li>Giordano, M. (2025). Tiered Euro-Monies: Perpetrating Monetary Hierarchies from the ECU to the Euro. <em>Review of Evolutionary Political Economy</em>, 6: 565–587. <a href="https://doi.org/10.1007/s43253-025-00154-4" rel="noopener">DOI</a></li>
          <li>Murau, S., Goghie, A. and Giordano, M. (2025). Encumbered Security? Vertical and Horizontal Repos in the Euro Area and Their Inherent Ambiguity. <em>Journal of Financial Regulation</em>, 11(2). <a href="https://doi.org/10.1093/jfr/fjaf003" rel="noopener">DOI</a></li>
          <li>Murau, S. and Giordano, M. (2024). Forging Monetary Unification through Novation: The TARGET System and the Politics of Central Banking in Europe. <em>Socio-Economic Review</em>, 22(3): 1283–1312. <a href="https://doi.org/10.1093/ser/mwad067" rel="noopener">DOI</a></li>
          <li>Giordano, M. and Lapavitsas, C. (2023). Persistent institutional malfunctioning in the Eurozone. <em>The Japanese Political Economy</em>, 49(4): 295–307. <a href="https://doi.org/10.1080/2329194X.2023.2289883" rel="noopener">DOI</a></li>
          <li>Giordano, M. and Pulieri, E. (forthcoming). From International to 'Regional' Financial Subordination: Italian Monetary Integration in the Eurozone. <em>Cambridge Journal of Economics</em>.</li>
        </ol>
      </div>
    </section>

    <section class="section" id="books" aria-labelledby="books-title">
      <div class="col col--wide">
        <div class="section__head reveal"><h2 class="section__title" id="books-title">Books and studies</h2></div>
        <ol class="pubs reveal">
          <li>Murau, S., Goghie, A., Giordano, M. and Reimer, F. (2025). Transformation of the Eurozone Architecture: Crises and Institutional Change in the Offshore US-Dollar System. <em>GEGI Study</em>, Global Development Policy Center, Boston University. <a href="https://doi.org/10.2139/ssrn.5648890" rel="noopener">DOI</a></li>
          <li>Giordano, M. (2025). <em>Monetary Subordination in the Eurozone: Fragmentation and tiering of markets and institutions</em>. PhD thesis, SOAS University of London. <a href="https://soas-repository.worktribe.com/output/461747" rel="noopener">Repository</a></li>
          <li id="state-of-capitalism">Lapavitsas, C. and the EReNSEP Writing Collective (2023). <em>The State of Capitalism: Economy, Society, and Hegemony after the Pandemic</em>. London: Verso. <a href="https://www.versobooks.com/en-gb/products/2727-the-state-of-capitalism" rel="noopener">Verso</a></li>
        </ol>
      </div>
    </section>

    <section class="section" id="working-papers" aria-labelledby="wp-title">
      <div class="col col--wide">
        <div class="section__head reveal"><h2 class="section__title" id="wp-title">Working papers and reports</h2></div>
        <ol class="pubs reveal">
          <li>Murau, S., Goghie, A., Giordano, M. and Reimer, F. (forthcoming). The Monetary Architecture Framework. <em>GEGI Study</em>, Boston University.</li>
          <li>Giordano, M. and Pulieri, E. (forthcoming). Debt Management (in-)Dependence: The missing side of Central Banks and the Legacy of CBI.</li>
          <li>Giordano, M. (2024). Monetary Subordination in the Eurozone: Pillars and Asymmetries. <em>SSRN Working Paper</em>. <a href="https://ssrn.com/abstract=4911906" rel="noopener">SSRN</a></li>
          <li>Murau, S., Goghie, A. and Giordano, M. (2024). Encumbered Security? Conceptualising Vertical and Horizontal Repos in the Euro Area. <em>SOAS Working Paper 262</em>. <a href="https://www.soas.ac.uk/sites/default/files/2024-04/economics-wp262.pdf" rel="noopener">PDF</a></li>
          <li>Giordano, M. and Goghie, A. (2023). From Policy to Regime: the changing posture of the ECB between liquidity and collateral through the lens of Monetary Regime. <em>SocArXiv Working Paper</em>. <a href="https://doi.org/10.31235/osf.io/rw3ms" rel="noopener">DOI</a></li>
          <li>Murau, S. and Giordano, M. (2022). European Monetary Unification through Novation: The Political Economy of the TARGET System. <em>SocArXiv Working Paper</em>. <a href="https://osf.io/preprints/socarxiv/k3nbh" rel="noopener">Preprint</a></li>
          <li>Lapavitsas, C., Meadway, J., Nicholls, D. and Giordano, M. (2022). The True Causes of Inflation: Weak Production and High Profits. PEF and GFTU. <a href="https://www.nautilusint.org/globalassets/public-resources/pdfs/the_real_causes_of_inflation_gftu.pdf" rel="noopener">PDF</a></li>
        </ol>
      </div>
    </section>

    <section class="section" id="talks" aria-labelledby="talks-title">
      <div class="col col--wide">
        <div class="section__head reveal"><h2 class="section__title" id="talks-title">Selected talks</h2><a class="section__more" href="https://app.box.com/s/mgfbjyrewx6zxsc6ow1i5185mtrgsagt" data-link="CV_ACADEMIC_URL" rel="noopener" target="_blank">Full list in the academic CV</a></div>
        <ul class="pubs pubs--plain reveal">
          <li>Tiered Euro-Monies: Perpetrating Monetary Hierarchies from the ECU to the Euro. <span class="where">Euromemo Group 30th Annual Conference, Vienna, September 2024.</span></li>
          <li>Encumbered Security? Vertical and Horizontal Repos in the Euro Area. <span class="where">Association for Heterodox Economics, UWE Bristol, July 2024.</span></li>
          <li>Forging Monetary Unification through Novation (with S. Murau). <span class="where">Money View Symposium, Institute for New Economic Thinking, February 2024.</span></li>
          <li>The State of Capitalism: Imperialism, Subordination, and Beyond. <span class="where">Rethinking Economics, SOAS University of London, February 2024.</span></li>
          <li>Off-Balance-Sheet Fiscal Agencies and the Role of the State in Financing the Green Transition. <span class="where">Money in Open Economies, University of Leeds, September 2023.</span></li>
          <li>Hegemony in Europe: Allowing the EMU to tick over (with C. Lapavitsas). <span class="where">Musashi University International Symposium, Tokyo, May 2023.</span></li>
        </ul>
      </div>
    </section>
  </main>
```
(The 2020 independently published book is dropped from the site; it remains in the academic CV.)

- [ ] **Step 2: `cargo-and-collateral.html`** — TITLE `Cargo & Collateral — Matteo Giordano`; DESCRIPTION `Cargo & Collateral: macro-finance and shipping, read through balance sheets and monetary architecture. A newsletter by Matteo Giordano on Substack.`; PATH `/cargo-and-collateral`.

```html
  <main id="main">
    <header class="page-head">
      <div class="col">
        <p class="eyebrow reveal">Cargo &amp; Collateral</p>
        <img class="wordmark reveal" src="/img/cargo-and-collateral-wordmark.png" alt="Cargo & Collateral" width="1000" height="190">
        <h1 class="page-title reveal">Macro-finance and shipping, read through balance sheets and monetary architecture.</h1>
        <p class="lede lede--ink reveal">Seaborne trade and monetary systems can be read the same way: as claims and obligations. Forwarder and carrier working capital, chartering and freight rates, chokepoint transits and tonne-mile demand, ship finance and marine insurance on one side; repo markets, debt management offices, central-bank balance sheets and the euro-area settlement plumbing on the other. Defence appears occasionally and on the same terms: rearmament as a working-capital problem before a capability one.</p>
        <div class="actions reveal">
          <a class="btn" href="https://cargoandcollateral.substack.com/" data-link="SUBSTACK_URL" rel="noopener" target="_blank">Read it on Substack</a>
          <a class="btn" href="https://cargoandcollateral.substack.com/subscribe" data-link="SUBSTACK_SUBSCRIBE_URL" rel="noopener" target="_blank">Subscribe</a>
        </div>
      </div>
    </header>

    <section class="section" aria-labelledby="cc-recent">
      <div class="col">
        <div class="section__head reveal"><h2 class="section__title" id="cc-recent">Recent entries</h2><a class="section__more" href="https://cargoandcollateral.substack.com/archive" data-link="SUBSTACK_ARCHIVE_URL" rel="noopener" target="_blank">Full archive</a></div>
        <ol class="writing reveal" id="writing-list" hidden></ol>
        <p id="writing-empty" class="reveal">Latest entries on <a class="link" href="https://cargoandcollateral.substack.com/archive" data-link="SUBSTACK_ARCHIVE_URL" rel="noopener" target="_blank">Substack</a>.</p>
      </div>
    </section>
  </main>
```

- [ ] **Step 3: Disclaimer and 404 wrappers** — in `disclaimer.html` and `404.html` replace `class="wrap"` with `class="col"` and `class="prose"` on the disclaimer section with `class="prose-page prose"`; nothing else changes.

- [ ] **Step 4: `sitemap.xml`** — 13 `<url>` entries: the seven existing plus `/research/balance-sheet-modelling`, `/research/eurozone`, `/research/subordination`, `/research/gegi-study`, `/research/macro-structures-dmo`, `/research/defence-economics`.

- [ ] **Step 5: `vercel.json` redirects** — replace the seven `/research-projects/...` entries with:
```json
    { "source": "/research-projects/research-projects", "destination": "/research", "permanent": true },
    { "source": "/research-projects/eurozone", "destination": "/research/eurozone", "permanent": true },
    { "source": "/research-projects/gegi-study", "destination": "/research/gegi-study", "permanent": true },
    { "source": "/research-projects/balance-sheet-modelling", "destination": "/research/balance-sheet-modelling", "permanent": true },
    { "source": "/research-projects/subordination", "destination": "/research/subordination", "permanent": true },
    { "source": "/research-projects/defence-and-security-economics", "destination": "/research/defence-economics", "permanent": true },
    { "source": "/research-projects/macro-structures-and-dmo", "destination": "/research/macro-structures-dmo", "permanent": true },
    { "source": "/research-projects/(.*)", "destination": "/research", "permanent": true },
```
Keep the publications and talks redirects; change `/publications/the-state-of-capitalism` destination to `/publications#state-of-capitalism` (unchanged) and `/talks-and-conferences/(.*)` to `/publications#talks` (unchanged). Validate with `python3 -c "import json;json.load(open('vercel.json'))"`.

- [ ] **Step 6: README** — update the file map: add `research/<slug>.html  six project pages` and note the nav partial carries the Research sub-menu (edit `tools/chrome/nav.html` to add a project).

- [ ] **Step 7: Run everything** — `python3 tools/chrome.py && python3 tools/check.py && python3 -m unittest discover -s tools/tests 2>&1 | tail -1` → `check: 0 problem(s)`, `OK`. `python3 tools/check.py --strict` lists only the DRAFT lines (index, about, research, publications, disclaimer).
- [ ] **Step 8: Commit** — subject `Publications and Cargo & Collateral v2; sitemap, redirects, README`.

---

### Task 7: Browser verification (controller)

Same procedure as v1 Task 11 with the browser pane: every page at desktop and 375px, mark `.reveal` visible via a debug script before layout screenshots, console clean, no external requests, the Research dropdown opens on hover and on keyboard focus and lists six projects, the mobile overlay shows the nested list, `aria-current` on project pages marks both links, anchors (`/research#monetary-architecture`) land below the nav, word counts per budget. Save screenshots and send to the user. Stop for review of screenshots and DRAFT lines.

### Task 8: Launch

As v1 Task 12: `check.py --strict` clean, `gh repo create dr-mpfg/mg-website --public --source . --remote origin --push`, repoint the Vercel project behind mg-macro.vercel.app (user's login), verify live URLs and the old-slug redirects (now to project pages), archive `dr-mpfg/mg_macro` only on the user's say-so.
