# Personal website for Dr Matteo Giordano: design

Date: 2026-10-11. Replaces the Obsidian digital garden at https://mgmacro.vercel.app.
Build location: `/Users/matteo/work_codes_offline/MG_macro_offline`.
Content source: the Obsidian vault "MG Macro" (home, About, Advisory, Research Projects, Publications, Talks, Cargo & Collateral).
Pattern source: `/Users/matteo/work_codes_offline/GS/gs-website` (static stack, serve.py, indexing switch, vercel.json).

## Purpose

An executive business card for a macro-financial strategist. It combines the academic and commercial sides, with the weight on current work and on macro-strategy roles. Short pages, few words, nothing duplicated. Every page a senior reader needs is one click from the home page.

## Decisions taken with the user

- Same stack and structure discipline as the GS site, but its own identity, its own palette, its own page rhythm. Follows the vault's structure loosely.
- Headline positioning: macro strategist in the shipping industry (employer unnamed), co-founder and Director of Garrison Sterling, Associate Researcher at the Global Climate Forum. All three on the home page.
- Vault text is the final copy, edited for the web. Only genuinely new lines (hero line, section intros, nav labels) are wrapped in `<!-- DRAFT --> ... <!-- /DRAFT -->` for approval.
- Light palette: warm paper, ink text, one accent.
- Research figures included, on the research page.
- No portrait.
- Indexed from launch at mgmacro.vercel.app. Indexing switch kept. No custom domain.
- Deployment: new GitHub repo under `dr-mpfg`, then repoint the existing Vercel project's Git source so the URL stays. The old `dr-mpfg/mg_macro` repo is left as an archive.
- Nav tab for the newsletter is labelled exactly `Cargo & Collateral`. The advisory page is titled `Advisory`, not "Work with me".
- Advisory carries a Delivered work section (track record for independent work).
- Source Serif 4 Italic may be downloaded from Google Fonts (OFL).

## Site map

Seven pages plus a 404.

| Path | Title | Nav |
|---|---|---|
| `/` | Dr Matteo Giordano | wordmark |
| `/research` | Research | Research |
| `/publications` | Publications | Publications |
| `/cargo-and-collateral` | Cargo & Collateral | Cargo & Collateral |
| `/about` | About | About |
| `/advisory` | Advisory | button `Advisory` |
| `/disclaimer` | Disclaimer | footer only |
| `/404` | Page not found | none |

Nav on every page: wordmark `Matteo Giordano` (left) · Research · Publications · Cargo & Collateral · About · outlined button `Advisory` (right). Mobile (< 900px): wordmark + Menu button, full-screen overlay. Contact is not a page: the email is in the hero link row and in every footer.

Footer on every page: wordmark · `© 2026 Matteo Giordano` · Email · LinkedIn · ORCID · Disclaimer · one-line tag "Macro-financial strategy · Shipping, monetary structures, off-balance-sheet finance". No cookies, no analytics, so no privacy page.

## Page contents

### Home `/`

1. Hero (typographic, no image, no canvas). Eyebrow `Dr Matteo Giordano`. H1: *Macro-financial strategist. Shipping, monetary structures, and off-balance-sheet finance.* Roles line: `Macro strategist, shipping industry · Co-founder and Director, Garrison Sterling · Associate Researcher, Global Climate Forum`. Link row: Email · Cargo & Collateral · CV · LinkedIn · ORCID.
2. Statement, large type: the "Financial systems are claims and obligations..." paragraph from the vault.
3. Bio, three sentences: shipping role and Greece; Garrison Sterling and the Global Climate Forum (OBFA-TRANSFORM, Monetary Architecture tool); PhD at SOAS under Prof. Lapavitsas, lecturer to 2025, defence economist at the UKDSC to September 2026, dual national.
4. Four lines of work, four blocks, each a heading, two to three sentences from the vault, one link:
   - Shipping and trade finance → `/cargo-and-collateral`
   - Macro-financial strategy and research → `/advisory`
   - Defence and security economics → `/research#defence`
   - Monetary architecture and hierarchy → `/research#monetary-architecture`
5. Selected work: the four papers listed on the vault home page, with DOI links, and a line linking to `/publications`.
6. Affiliations: one compact row of names with links (Garrison Sterling · Global Climate Forum · SOAS · UKDSC to Sept 2026 · SPARCollective · EReNSEP · YSI, INET).

Target: under 500 visible words.

### Advisory `/advisory`

1. Page head: eyebrow `Advisory`, H1 from the vault's pull line ("Macro-financial strategy for institutions that need to know how a system clears before they need to know where it trades."), the intro paragraph ("I take commissioned work from two directions...").
2. Areas (three): Shipping and trade finance; Sovereign credit and monetary structure; Balance-sheet modelling. Vault text, links to research anchors and to Cargo & Collateral.
3. Delivered work: three items from the vault About page (the public Monetary Architecture Online Tool; models built to be interrogated; briefings to government and industry). Marked up as a list so anonymised engagements can be appended later in the same pattern: who (by type and geography), the question, what was delivered. The fabricated examples in the vault are not used.
4. Ways to engage: expert calls; commissioned notes and models; speaking and workshops. Then the routing paragraph: defence work goes through Garrison Sterling; shipping, sovereign and monetary work is taken here in a personal capacity.
5. Closing: email button `Discuss a brief`, and the personal-capacity note linking to `/disclaimer`.

### Research `/research`

One page, intro line from the vault index, then four sections with anchor ids, in the order of the four lines of work:

- `#shipping` Shipping and trade finance: one paragraph, link to `/cargo-and-collateral`.
- `#macro-strategy` Macro-financial strategy and research: project *Macro-Structure, DMOs and Monetary Regimes* (figure `Macro_Structure.png`; three areas; forthcoming paper links).
- `#defence` Defence and security economics: the intro, four themes, method, the UKDSC/MoD sentence, the note pointing to the disclaimer. No figure.
- `#monetary-architecture` Monetary architecture and hierarchy, four projects:
  - Balance-Sheet Modelling & Monetary Architecture (three strands, method, tool link)
  - Asymmetries, Imbalances and Fragmentation in the Eurozone (three pillars, four figures: `T2_EoP_plot`, `Liabilities_nonEA_Euro_Plot`, `Origin_Collateral_plot`, `Italy_T2_Fdec_BoP_Cumulative_Plot`)
  - Monetary Subordination in the Eurozone (figure `Subordination_EMU.png`; three pillars; consequences)
  - Transformation of the Eurozone Architecture, GEGI Study (cover `GEGIStudy.png`; argument; method; SSRN link)

Each project: heading, 80 to 150 words, figure(s) with caption and a link to the full-size file, output links. Related-page cross references are dropped (one page now).

### Publications `/publications`

Intro line with the ORCID link. Three lists:

1. Published: the 16 entries from the vault, numbered newest first, journal names in italics, DOI/URL links. *The State of Capitalism* is an entry with the Verso link; no page of its own.
2. In preparation and review: the three entries.
3. Selected talks: six, chosen from the vault's Presentations and Talks lists (the most recent and the invited ones), with a line "Full list on request" linking to the academic CV.

### Cargo & Collateral `/cargo-and-collateral`

Wordmark image (the transparent wordmark PNG, resized), the pull line, the two description paragraphs from the vault, Read and Subscribe buttons to Substack, then `Recent entries` read from `data/writing.json` (fields: `title`, `date`, `href`; newest first; maintained by hand) with a link to the Substack archive. Empty state: "Latest entries on Substack." with the archive link.

### About `/about`

Pull line, then: Positions (four, vault text); Education (three); Methods (modelling, applied to, tools); Recognition (funding, scholarship, teaching awards in one paragraph); Personal (one line: nationality, base, languages); CV links (CV, academic CV, ORCID, LinkedIn, email). "Delivered work" lives on Advisory; "Published record" is replaced by a one-line link to Publications.

### Disclaimer `/disclaimer`

The vault's disclaimer text, plus the advisory sentence ("All engagements are undertaken in a personal capacity ... not investment advice."). Prose page.

### 404

Short line, link home.

## Look

### Tokens

| Token | Value | Use |
|---|---|---|
| `--paper` | `#F6F2EA` | page background |
| `--paper-2` | `#EDE7DB` | figure panels, code, quiet blocks |
| `--ink` | `#1B1D22` | text, headlines |
| `--muted` | `#6B6F76` | secondary text, metadata |
| `--rule` | `rgba(27,29,34,0.12)` | hairlines |
| `--accent` | `#1F6FB5` | links, button border/hover, thin accent rules. The Cargo & Collateral blue. One-token swap to the red `#B4302E` if preferred. |

Contrast: ink on paper and accent on paper both pass WCAG AA for body text.

### Type

- Source Serif 4 (Regular, Italic, Semibold) for headlines and prose.
- IBM Plex Sans (Regular, Medium, SemiBold) for nav, eyebrows, buttons, metadata, captions.
- Both self-hosted as woff2. Regular/Semibold serif and all Plex weights copied from the GS repo (`fonts/`, OFL with licence files). Source Serif 4 Italic downloaded from Google Fonts (OFL).
- Hero H1 `clamp(2.25rem, 5vw, 4rem)`, page titles `clamp(2rem, 4.5vw, 3.25rem)`, body 17px mobile / 18px desktop, line-height 1.6, prose max 62ch.

### Brand device

A T-account line mark (a horizontal rule with a vertical stem, the balance-sheet T, echoing the Cargo & Collateral logo) drawn as inline SVG: used as favicon (`favicon.svg`, `favicon.ico`, `apple-touch-icon.png`), next to the wordmark in the nav, and on the share image. One colour (ink; accent on hover in the nav).

### Motion

Fade-in on scroll, 300 ms, once, `IntersectionObserver`; everything visible immediately under `prefers-reduced-motion`. Nothing else moves.

### Layout

Max width 1120px, gutters 20px / 40px. Inner pages use the GS two-column grid (section title left, body right) at ≥ 768px, single column below. Figures span the body column, `aspect-ratio` set from the file so nothing jumps while loading, `loading="lazy"`.

## Repository layout

```
MG_macro_offline/
├── README.md                  how to run, edit, add a writing entry, flip indexing, deploy
├── index.html  research.html  publications.html  cargo-and-collateral.html
├── about.html  advisory.html  disclaimer.html  404.html
├── css/site.css               tokens, type, nav, blocks, figures, lists, legal prose
├── js/site.js                 mobile nav, reveal-on-scroll, writing list
├── js/config.js               CONTACT_EMAIL, SUBSTACK_URL, LINKEDIN_URL, ORCID_URL, CV_URL, CV_ACADEMIC_URL, INDEXING
├── data/writing.json          recent Cargo & Collateral entries, newest first
├── fonts/                     woff2 + licence files
├── img/                       figures (web-sized) + figures/full/ (originals), wordmark, og-share.png
├── favicon.svg  favicon.ico  apple-touch-icon.png
├── robots.txt  sitemap.xml  vercel.json
├── serve.py                   local server mirroring vercel.json (from GS)
├── tools/indexing.py          one switch for search-engine indexing (from GS, adapted)
├── tools/chrome.py            rewrites the shared nav + footer block in every page from one source
├── tools/check.py             stdlib checks: internal links and images resolve, no DRAFT markers, sitemap matches pages
├── .claude/launch.json        dev server entry for the browser pane
├── .gitignore
└── docs/superpowers/          specs and plans
```

Nav and footer are duplicated in every page between `<!-- CHROME:nav -->`/`<!-- /CHROME -->` and `<!-- CHROME:footer -->`/`<!-- /CHROME -->` markers; `tools/chrome.py` rewrites them from `tools/chrome/nav.html` and `tools/chrome/footer.html`, setting `aria-current` per page. No runtime injection, so pages are complete without JS.

### `js/config.js`

Links that appear in several places read from one object, as in GS: `CONTACT_EMAIL` (`mg.macroeconomics@gmail.com`), `SUBSTACK_URL`, `SUBSTACK_SUBSCRIBE_URL`, `SUBSTACK_ARCHIVE_URL`, `LINKEDIN_URL`, `ORCID_URL`, `CV_URL`, `CV_ACADEMIC_URL`, `INDEXING`. The HTML still carries the real hrefs so links work without JS; the script only updates them if the config differs (single place to change an address).

### Figures

Originals copied to `img/figures/full/` unchanged. Web versions in `img/figures/` resized with `sips` to max 1600px wide, PNG for the plots (line art) and JPEG for the two covers. Alt text and captions written from the vault's pillar headings.

### `vercel.json`

Clean URLs, no trailing slash, the GS security headers (CSP `default-src 'self'`, nosniff, DENY, referrer policy, permissions policy, HSTS), one-year immutable cache on `/fonts/` and `/img/`, and 301 redirects from the old digital-garden paths to the new ones:

| Old | New |
|---|---|
| `/about` | kept |
| `/advisory` | kept |
| `/cargo-collateral`, `/cargo-and-collateral` | `/cargo-and-collateral` |
| `/research-projects/research-projects` | `/research` |
| `/research-projects/eurozone` | `/research#eurozone` |
| `/research-projects/gegi-study` | `/research#gegi-study` |
| `/research-projects/balance-sheet-modelling` | `/research#balance-sheet-modelling` |
| `/research-projects/subordination` | `/research#subordination` |
| `/research-projects/defence-security-economics` | `/research#defence` |
| `/research-projects/macro-structures-dmo` | `/research#macro-strategy` |
| `/publications/publications` | `/publications` |
| `/publications/the-state-of-capitalism` | `/publications` |
| `/talks-conferences/talk-conferences` | `/publications#talks` |

The exact old slugs are the digital-garden plugin's slugify of the vault paths; they are verified against the live site before launch and corrected if they differ.

### SEO and sharing

`<title>`, `meta description`, canonical, OpenGraph and Twitter card tags on every page; `og:image` is `img/og-share.png` (1200×630, paper background, name, positioning line, T mark), generated by screenshotting a local HTML template in the browser pane. `sitemap.xml` lists the seven pages. `robots.txt` allows all. The indexing switch (`tools/indexing.py off`) adds `noindex, nofollow` and `Disallow: /` if ever needed.

## Error handling

- Static site: nothing to fail at runtime except the writing list fetch; on failure or an empty array the page keeps the "Latest entries on Substack" line.
- Missing JS: nav links, mailto links and content all work; only the mobile overlay toggle needs JS (links remain reachable in the overlay markup for keyboard users).
- `serve.py` reproduces the CSP so an inline-script or external-request mistake fails locally.

## Verification

- `python3 tools/check.py` passes: every internal href and `src` resolves to a file, no `DRAFT` markers remain (run before launch; during build it reports them), sitemap entries match the HTML files, every page has title, description and canonical.
- Screenshots of all seven pages and the 404 at 360, 768 and 1440 px from the built-in browser; reviewed by the user.
- Browser console clean, no network request leaves the origin (checked in the pane's network list).
- Visible word count on the home page under 500.
- Reduced-motion check: all content visible with the media query emulated.

## Launch

1. Commit in `MG_macro_offline`; create `dr-mpfg/mg-website` on GitHub with `gh`; push `main`.
2. In the Vercel dashboard (project behind mgmacro.vercel.app): Settings → Git → disconnect `dr-mpfg/mg_macro`, connect `dr-mpfg/mg-website`, framework preset Other, no build command, output directory `.`. Redeploy. User does this or Claude drives it in the browser pane with the user logged in.
3. Verify the live URL, the redirects, and the share image.
4. Optionally archive `dr-mpfg/mg_macro` on GitHub; leave the vault's digital-garden plugin disabled so it cannot republish.

## Out of scope

Custom domain, analytics, a CMS, a blog on the site itself (writing lives on Substack), comments, the GS site, the Obsidian vault.
