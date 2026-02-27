---
name: beatrix-paper-scraper
description: Find professors' personal websites and scrape their self-hosted papers for BEATRIX Paper Finder. Self-learning — logs every failed approach in dead-ends.md so it is never repeated. Triggers on "neue Forscher", "PDFs scrapen", "Paper Finder erweitern", "Forscher entdecken", "papers finden".
---

# BEATRIX Paper Scraper

## Core Insight

**Professors host their own papers on their personal websites.** That's the source. The skill is: **find that homepage.**

## MANDATORY: Before ANY Scraping

1. **Read `references/dead-ends.md`** — contains every approach that failed before. NEVER repeat them.
2. **Read `references/working-sources.md`** — contains every approach that worked. Try these FIRST.
3. If you hit a new dead end → **immediately append it to `dead-ends.md`** on GitHub.
4. If you find a new working source → **immediately append it to `working-sources.md`** on GitHub.

## The 3-Step Process

### Step 1: Find the Personal Homepage
One web search per researcher:
```
web_search: "{Name} {Institution} personal homepage publications"
```

Looking for: own domains, faculty tilde pages (`~name`), github.io pages.
NOT looking for: university department pages, Google Scholar, ResearchGate.

### Step 2: Find the Publications Page
`web_fetch` the homepage → find `/publications`, `/research`, `/papers` link.

### Step 3: Scrape PDFs
Extract `href="*.pdf"` links. If 0 results → page is JS-rendered → try `web_fetch`. If still 0 → record homepage, count=0, **log the dead end**, move on.

## Self-Learning Rules

### When a scraping attempt FAILS:

```
IMMEDIATELY push to dead-ends.md on GitHub:

## {Researcher Name} — {Institution}
- **URL tried:** {url}
- **Method:** curl / web_fetch / urllib
- **Result:** JS-rendered / 403 / timeout / login wall / 0 PDFs
- **Date:** YYYY-MM-DD
- **Lesson:** {what to avoid next time}
```

### When a scraping attempt SUCCEEDS:

```
IMMEDIATELY push to working-sources.md on GitHub:

## {Researcher Name} — {Institution}
- **URL:** {url}
- **Method:** curl / web_fetch
- **PDFs found:** {count}
- **Pattern:** {e.g. "Harvard scholar.harvard.edu/{slug}/publications"}
- **Date:** YYYY-MM-DD
```

### GitHub push for skill updates:

```python
# Path: skills/beatrix-paper-scraper/references/dead-ends.md
# Path: skills/beatrix-paper-scraper/references/working-sources.md
# Use standard GitHub API PUT with fresh SHA
```

## Anti-Patterns (Permanent)

1. **NEVER retry a method that's logged in dead-ends.md**
2. **NEVER do multiple rounds** — one attempt per source, then move on
3. **NEVER inflate counts** — count = actual PDF URLs found, never estimates
4. **NEVER scrape Google Scholar** — always blocked, always will be
5. **NEVER batch-search SSRN/arXiv as primary strategy** — personal homepage first

## Database

Location: `complementarity-context-framework/data/paper-finder-sources.json`

### Rules:
- `count` = `len(verified_pdfs)` — never an estimate
- `status` = honest: "✅ 50 PDFs" or "📋 homepage found, 0 PDFs scraped"
- Push to GitHub after every batch. Fresh SHA before every PUT.

## Infrastructure

- **Data**: GitHub `complementarity-context-framework/data/paper-finder-sources.json`
- **Skill logs**: GitHub `complementarity-context-framework/skills/beatrix-paper-scraper/references/`
- **Backend**: Railway `GET /api/papers/sources` (5-min cache)
- **Frontend**: Vercel `www.bea-lab.io` → Paper Finder tab


## CRITICAL WORKFLOW RULE: Never Manually Transcribe

**Date learned:** 2026-02-13
**Cost of ignoring:** ~20 minutes + hundreds of tokens wasted per professor

### The Anti-Pattern (DO NOT DO THIS):
1. `web_fetch` → get HTML with paper list
2. Read the HTML visually
3. Manually type papers as Python lists: `("Title", "2024", "Journal", None)`
4. This is MECHANICAL WORK, not learning. It wastes tokens and introduces errors.

### The Correct Pattern (ALWAYS DO THIS):
1. `web_fetch` URL → get HTML content
2. **Save HTML to file:** `with open('/home/claude/professor_page.html', 'w') as f: f.write(html)`
3. **Parse programmatically:** Use regex or BeautifulSoup to extract titles, years, journals, PDF links
4. **Output JSON directly** — zero manual transcription

### Specific Source Patterns Discovered:

| Source | Method | PDF Pattern | Notes |
|--------|--------|-------------|-------|
| Stanford `people.stanford.edu` | `curl` works | `wp-content/uploads/*.pdf` | WordPress, fast |
| HBS `hbs.edu/faculty` | `web_fetch` only (curl 403) | `hbs.edu/faculty/Pages/download.aspx` | ASP.NET, structured HTML |
| Uni Bonn `econ.uni-bonn.de` | `web_fetch` works | Links to IZA, NBER, uni-bonn.de | Clean inline lists |
| ZORA API `zora.uzh.ch` | `curl` REST API | `/bitstreams/{uuid}/content` | JSON API, best coverage |

### Time Budget Per Professor:
- **Target:** < 3 minutes per professor
- **If > 5 minutes:** You're probably manually transcribing. STOP and automate.
- **Acceptable time sinks:** New institution pattern analysis (learning cost)
- **Unacceptable time sinks:** Typing paper lists by hand

### Fallback for `curl` 403 Errors:
When `curl` is blocked but `web_fetch` works:
1. Use `web_fetch` to get the page
2. The content is returned in the function result but NOT automatically saved to disk
3. **You must save it:** Write a Python script that receives the content and parses it
4. Alternative: Use `bash_tool` with `curl` + different User-Agent headers
