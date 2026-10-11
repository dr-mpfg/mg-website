# Personal website v2: hub-and-spoke structure

Date: 2026-10-11. Supersedes the page map, page contents and layout sections of `2026-10-11-personal-website-design.md`. Everything else there (palette, type, T mark, motion, plumbing, launch, decisions with the user) stands.

## Why

v1 reused the vault notes page for page under a GS-style "label left, prose right" rhythm. The result was long, dispersive pages. v2 is an index: every page fits one screen or two, projects are first-class pages, and the nav carries a Research sub-menu.

## Site map

| Path | Title | Nav | Budget |
|---|---|---|---|
| `/` | Dr Matteo Giordano | wordmark | ≤150 words |
| `/about` | About | About | ≤250 |
| `/research` | Research | Research (dropdown parent) | ≤120 |
| `/research/balance-sheet-modelling` | Balance-sheet modelling and monetary architecture | dropdown | ≤300 |
| `/research/eurozone` | Asymmetries, imbalances and fragmentation in the eurozone | dropdown | ≤300 |
| `/research/subordination` | Monetary subordination in the eurozone | dropdown | ≤300 |
| `/research/gegi-study` | Transformation of the eurozone architecture | dropdown | ≤300 |
| `/research/macro-structures-dmo` | Macro-structure, DMOs and monetary regimes | dropdown | ≤300 |
| `/research/defence-economics` | Modelling the defence-industrial base | dropdown | ≤300 |
| `/publications` | Publications | Publications | entries only |
| `/cargo-and-collateral` | Cargo & Collateral | Cargo & Collateral | ≤120 |
| `/advisory` | Advisory | button | ≤200 |
| `/disclaimer` | Disclaimer | footer | unchanged |
| `/404` | Page not found | none | unchanged |

Nav: `Matteo Giordano` · About · Research ▾ · Publications · Cargo & Collateral · `Advisory`. The Research item is a link to `/research`; hovering or focusing it (desktop, ≥900px) opens a panel listing "All research" and the six projects under their theme headings (Monetary architecture: balance-sheet modelling, eurozone, subordination, GEGI study; Macro-financial strategy: macro-structure and DMOs; Defence economics: defence-industrial base). In the mobile overlay the same list sits indented under Research, always expanded. No JS is needed for the menu; `aria-current="page"` goes on the project link and on the parent Research link when a project page is open.

## Layout

One centred column. Prose pages and project pages use a 720px column; hub pages (home, research, publications) use 1040px for card grids and lists. Cards: hairline border, title, one-line meta, one sentence, whole card clickable. No two-column label/prose grid. The hero is typographic, one screen, with the contact row.

## Page contents

**Home.** Eyebrow, H1 positioning line, roles line, contact row. Then "Four lines of work": 2×2 cards (Shipping and trade finance → `/cargo-and-collateral`; Macro-financial strategy → `/research/macro-structures-dmo`; Defence and security economics → `/research/defence-economics`; Monetary architecture and hierarchy → `/research#monetary-architecture`), each with one sentence from the vault. Then "Latest": two items, the newest newsletter entry (from `data/writing.json`, static fallback link to Substack) and the newest paper (Lapavitsas and Giordano 2026). Footer.

**About.** H1 pull line. Bio, three sentences. Positions: five one-liners (role, institution, years). Education: three one-liners. Background: one short paragraph combining methods and recognition. CV links row. Personal line in the Background paragraph.

**Research hub.** Intro line. Four theme sections with ids `shipping`, `macro-strategy`, `defence`, `monetary-architecture`; each a heading, one sentence, then cards. Cards: Cargo & Collateral (→ `/cargo-and-collateral`), Macro-structure and DMOs, Defence-industrial base, Balance-sheet modelling, Eurozone, Subordination, GEGI study.

**Project pages.** Eyebrow breadcrumb (`Research · <theme>`), H1, meta line (status, collaborators, institution, year), abstract paragraph, figure(s) with caption and full-size link, two or three short sections (h2) from the vault text, Outputs (links), Related publications (two or three entries). The defence page ends with its non-representation note.

**Publications.** Intro line. Journal articles (8), Books and studies (3), Working papers (5), each entry one line: authors (year). Title. *Journal*. Link. Selected talks: six one-liners. Academic CV link.

**Cargo & Collateral.** Wordmark, pull line, one paragraph, Read and Subscribe buttons, three recent entries from JSON, archive link.

**Advisory.** H1 pull line, two-sentence intro, three area cards (one sentence each, linking to the relevant project pages), Ways to engage (three one-liners), defence routing sentence, Delivered work (three one-liners), email button, personal-capacity note.

## Plumbing changes

- `tools/chrome.py`: also processes `research/*.html`; `page_path` returns `/research/<slug>`; `mark_current` marks the exact link and, for `/research/...`, the parent `/research` link too.
- `tools/check.py`: scans `research/*.html`; sitemap expectation includes them.
- `sitemap.xml`: 13 pages. `vercel.json` redirects: old `/research-projects/<slug>` → the project page (`defence-and-security-economics` → `/research/defence-economics`, `macro-structures-and-dmo` → `/research/macro-structures-dmo`, others same slug).
- `js/site.js`: also renders the newest writing entry into `#latest-note` on the home page when present.
