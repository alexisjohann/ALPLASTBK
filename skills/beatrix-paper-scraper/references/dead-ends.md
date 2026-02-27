# Dead Ends — DO NOT REPEAT

Every failed scraping approach is logged here. **Read this BEFORE any scraping task.**

---

## Google Scholar — ALL researchers
- **URL tried:** `scholar.google.com/citations?user=*`
- **Method:** curl, urllib, web_fetch
- **Result:** 403 / CAPTCHA — always blocked
- **Date:** 2026-02-13
- **Lesson:** Google Scholar blocks all automated access. Never try.

## NBER Author Pages — ALL researchers
- **URL tried:** `nber.org/people/{name}`
- **Method:** curl, urllib
- **Result:** JS-rendered, returns HTML shell with no paper data
- **Date:** 2026-02-13
- **Lesson:** NBER uses React. curl gets empty shell. Don't bother.

## ZORA UZH Search — Weber, Bartling, Maréchal, Alós-Ferrer, Hare, Ruff, Tobler
- **URL tried:** `zora.uzh.ch/cgi/search/simple?q={name}`
- **Method:** curl, urllib
- **Result:** JS-rendered, 0 results in HTML
- **Date:** 2026-02-13
- **Lesson:** ZORA search is JS-rendered. BUT: the ZORA REST API works perfectly! See working-sources.md for the full pipeline.

## UZH Department Publication Pages — Weber, Bartling, Maréchal, etc.
- **URL tried:** `econ.uzh.ch/en/people/faculty/{name}/publications.html`
- **Method:** curl
- **Result:** JS-rendered, 0 PDFs extracted
- **Date:** 2026-02-13
- **Lesson:** UZH faculty pages use JS rendering. Use personal homepages or DAM links instead.

## Google Sites — Kőszegi, Charness, Englmaier, Dufwenberg, Kuhnen, Rustichini
- **URL tried:** `sites.google.com/view/{name}/research`
- **Method:** curl, urllib
- **Result:** JS-rendered, returns empty HTML shell
- **Date:** 2026-02-13
- **Lesson:** Google Sites always needs JS. Never scrape with curl.

## IDEAS/RePEc — DellaVigna, Rabin, Kőszegi, Laibson, Sunstein, Gneezy, List, Charness, Bowles, Duflo, Karlan, Allcott, Duckworth, Chetty, Angrist
- **URL tried:** `ideas.repec.org/e/{id}.html`
- **Method:** curl, urllib
- **Result:** No direct PDF links — only metadata and journal links
- **Date:** 2026-02-13
- **Lesson:** RePEc has metadata only, no PDFs. Skip as primary source.

## ResearchGate — ALL researchers
- **URL tried:** `researchgate.net/profile/{name}`
- **Method:** curl
- **Result:** Login wall / restricted access
- **Date:** 2026-02-13
- **Lesson:** ResearchGate requires authentication. Never try automated.

## SSRN Search — Gneezy, Benartzi, Rockenbach, Engelmann, Glimcher, Krajbich, Field, Fischhoff, Shafir, Gilovich, Nordgren, Englmaier, Kessler, Volpp, Gintis, Dufwenberg, Herz, Persson, Kuhnen, Soutschek, Service
- **URL tried:** `papers.ssrn.com/sol3/results.cfm?txtKey_Words={name}`
- **Method:** curl
- **Result:** 0 results — SSRN blocks or returns empty for many names
- **Date:** 2026-02-13
- **Lesson:** SSRN works ~50% of the time. Don't rely on it. Personal homepage first.

## MIT Economics Faculty Pages — Duflo, Angrist, Banerjee
- **URL tried:** `economics.mit.edu/people/faculty/{name}`
- **Method:** curl
- **Result:** JS-rendered React app, 0 content
- **Date:** 2026-02-13
- **Lesson:** MIT Economics uses React. curl gets nothing.

## Santa Fe Institute — Bowles
- **URL tried:** `santafe.edu/people/profile/samuel-bowles`
- **Method:** curl
- **Result:** No PDF links on profile page
- **Date:** 2026-02-13
- **Lesson:** SFI profiles don't list papers with PDFs.

## Raj Chetty — rajchetty.com
- **URL tried:** `rajchetty.com/research/`
- **Method:** curl
- **Result:** JS-rendered, 0 PDFs
- **Date:** 2026-02-13
- **Lesson:** But `opportunityinsights.org/paper/` works! → see working-sources.md

## Hunt Allcott — huntallcott.com
- **URL tried:** `huntallcott.com/research/papers/`
- **Method:** curl
- **Result:** JS-rendered, 0 PDFs
- **Date:** 2026-02-13
- **Lesson:** Own domain but JS-rendered. Try web_fetch next time.

---
### Embedding unsanitized JSON in HTML Script Tags
- **Date:** 2026-02-13
- **What happened:** Scraped ZORA paper titles contained `"double quotes"`. When embedded as `const DATA = {json};` in a 700KB monolithic `<script>` tag, the escaped quotes `\"` caused a JS parse error that killed ALL functions in the entire script block.
- **Symptom:** Page loads but section shows "Loading..." forever — no error visible because entire script failed silently.
- **Root cause:** Single large `<script>` tag = single point of failure. One bad character anywhere kills everything.
- **Fix applied:** (1) Sanitize all strings: replace `"` → `'`, (2) Use `ensure_ascii=True`, (3) Isolate new code in separate `<script>` tags
- **RULE: Never embed scraped data into monolithic JS. Always sanitize + isolate.**

---
### Manual Paper Transcription
- **Date:** 2026-02-13
- **What happened:** After fetching Roth (HBS) and Falk (Bonn) pages via web_fetch, manually typed 140+ papers as Python tuples instead of parsing HTML programmatically.
- **Time wasted:** ~25 minutes + hundreds of tokens on mechanical copy work
- **Root cause:** Treating web_fetch output as "read-only visual" instead of parseable data
- **Fix:** ALWAYS save fetched HTML to file → parse with regex/BeautifulSoup → output JSON
- **RULE: If you're typing paper titles by hand, you're doing it wrong. STOP and write a parser.**
