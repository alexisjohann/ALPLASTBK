# Working Sources — Try These FIRST

Every successful scraping approach is logged here. **Try these patterns before searching.**

---

## Harvard scholar.harvard.edu — Laibson, Goldin, Stantcheva, Shleifer, Gabaix
- **URL:** `scholar.harvard.edu/{slug}/publications`
- **Method:** curl
- **PDFs found:** 6-14 per researcher
- **Pattern:** Static HTML. PDFs at `/sites/g/files/omnuum{ID}/files/{year}/{filename}.pdf`
- **Date:** 2026-02-13

## Berkeley tilde pages — Saez (217!), Card (155), DellaVigna
- **URL:** `eml.berkeley.edu/~{name}/`
- **Method:** curl
- **PDFs found:** 50-217 per researcher
- **Pattern:** Old-school static HTML with direct PDF links
- **Date:** 2026-02-13

## David Card — dedicated subdomain
- **URL:** `davidcard.berkeley.edu/papers.html`
- **Method:** curl
- **PDFs found:** 155
- **Pattern:** Static HTML bibliography page
- **Date:** 2026-02-13

## Stanford tilde pages — Niederle (68), Gentzkow (50)
- **URL:** `web.stanford.edu/~{name}/research/`
- **Method:** curl
- **PDFs found:** 50-68
- **Pattern:** Static HTML
- **Date:** 2026-02-13

## Axel Ockenfels — Cologne
- **URL:** Personal homepage (uni-koeln.de)
- **Method:** curl
- **PDFs found:** 224 (!)
- **Pattern:** Best academic homepage for scraping. Full bibliography with direct PDFs.
- **Date:** 2026-02-13

## Kathleen Vohs — Minnesota
- **URL:** Faculty homepage
- **Method:** curl
- **PDFs found:** 176
- **Pattern:** Static faculty page with many PDF links
- **Date:** 2026-02-13

## Sendhil Mullainathan — MIT/Harvard
- **URL:** scholar.harvard.edu pattern
- **Method:** curl
- **PDFs found:** 126
- **Pattern:** Harvard scholar site
- **Date:** 2026-02-13

## Jon Kleinberg — Cornell
- **URL:** Personal homepage
- **Method:** curl
- **PDFs found:** 114
- **Pattern:** Static HTML computer science homepage
- **Date:** 2026-02-13

## Ernst Fehr — UZH DAM
- **URL:** `econ.uzh.ch/dam/jcr:{UUID}/{filename}.pdf`
- **Method:** Direct DAM links (not search)
- **PDFs found:** 114
- **Pattern:** UZH DAM uses stable UUID-based URLs. Must know UUIDs in advance.
- **Date:** 2026-02-13

## Raj Chetty — Opportunity Insights
- **URL:** `opportunityinsights.org/paper/`
- **Method:** curl
- **PDFs found:** 50
- **Pattern:** Project website, not personal homepage. Static HTML.
- **Date:** 2026-02-13

## Emir Kamenica — Chicago
- **URL:** Faculty page
- **Method:** curl
- **PDFs found:** 46
- **Pattern:** Partially static Chicago Booth page
- **Date:** 2026-02-13

## Parag Pathak — MIT
- **URL:** Personal homepage
- **Method:** curl
- **PDFs found:** 64
- **Pattern:** Static elements despite MIT being generally JS-heavy
- **Date:** 2026-02-13

## Muriel Niederle — Stanford
- **URL:** `web.stanford.edu/~niederle/`
- **Method:** curl
- **PDFs found:** 68
- **Pattern:** Stanford tilde page
- **Date:** 2026-02-13

## Simon Gächter — Nottingham
- **URL:** Personal/department page
- **Method:** curl
- **PDFs found:** 43 PDFs + 30 DOIs
- **Pattern:** Static page with both PDF links and DOI references
- **Date:** 2026-02-13

## James Andreoni — UCSD
- **URL:** `econweb.ucsd.edu/~jandreon/WorkingPapers/`
- **Method:** curl
- **PDFs found:** 29
- **Pattern:** UCSD tilde page
- **Date:** 2026-02-13

## Stantcheva — Dropbox links
- **URL:** `scholar.harvard.edu/stantcheva/publications`
- **Method:** curl
- **PDFs found:** 10 (Dropbox-hosted PDFs)
- **Pattern:** Harvard scholar page, but PDFs hosted on Dropbox. Links work.
- **Date:** 2026-02-13

## Roberto Weber — Personal domain
- **URL:** `robertoweber.com/publications`
- **Method:** web_fetch (JS-rendered but navigable)
- **PDFs found:** CV found, publications page exists
- **Pattern:** Squarespace site — needs web_fetch, not curl
- **Date:** 2026-02-13

## Armin Falk — briq Institute
- **URL:** Personal/institutional page
- **Method:** curl
- **PDFs found:** 40
- **Pattern:** Working papers with direct PDF links
- **Date:** 2026-02-13

## Paul Milgrom — Stanford
- **URL:** Personal page
- **Method:** curl
- **PDFs found:** 25
- **Pattern:** Working papers section with PDFs
- **Date:** 2026-02-13

## Daron Acemoglu — MIT
- **URL:** Personal page (not MIT department page)
- **Method:** curl
- **PDFs found:** 45
- **Pattern:** Acemoglu has a personal page that works, unlike MIT's department pages
- **Date:** 2026-02-13

## ZORA API (DSpace 7 REST) — ALL UZH researchers (BEST SOURCE)
- **Base URL:** `https://www.zora.uzh.ch/server/api/`
- **Method:** REST API (JSON), no JS rendering needed
- **Pipeline:**
  1. Search: `discover/search/objects?query=author:"Lastname, Firstname"&dsoType=ITEM&size=20&page=N`
  2. Get bundles: `core/items/{item_uuid}/bundles?size=20`
  3. Find bundle named "ORIGINAL"
  4. Get bitstreams: `core/bundles/{bundle_id}/bitstreams`
  5. PDF URL: `https://www.zora.uzh.ch/server/api/core/bitstreams/{bs_uuid}/content`
- **Success rate:** 95%+ (only embargoed items fail)
- **Tested:** Ernst Fehr — 288 items → 321 PDFs, 0 errors
- **Date:** 2026-02-13
- **Lesson:** ZORA *search pages* are JS-rendered (dead end), but the REST API is pure JSON. Use `author:"Lastname, Firstname"` format for best results. Paginate with `&page=N`. Some items have multiple PDFs (e.g. appendices). All bitstream URLs are stable UUIDs.

---
### Stanford people.stanford.edu — WordPress Publications Pages
- **Date:** 2026-02-13
- **Pattern:** `https://{name}.people.stanford.edu/publications/`
- **PDF Pattern:** `wp-content/uploads/{year}/{month}/{filename}.pdf`
- **Example:** Paul Milgrom → 98 direct PDF links
- **Method:** `curl -sL {url} | grep -oP 'href="[^"]*\.pdf[^"]*"'`
- **Success Rate:** 95%+ (static WordPress, no JS needed)
- **Note:** Some links point to Google Drive or external sites — filter for `people.stanford.edu` domain
- **Distinction from tilde pages:** These are NOT `~name` URLs but `name.people.stanford.edu` subdomains running WordPress

### ZORA Bitstream API — Paper Title Sanitization Required
- **Date:** 2026-02-13
- **Issue:** ZORA paper titles contain literal double quotes (e.g. `Putting the "finance" into "public finance"`)
- **Impact:** When embedded as JSON in HTML, `\"` sequences break JavaScript parser
- **Fix:** Always replace `"` with `'` in ALL scraped text fields BEFORE json.dumps()
- **Rule:** `title = title.replace('"', "'")` on every scraped string
