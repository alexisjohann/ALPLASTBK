# Proven Scraping Patterns

## Pattern 1: Harvard scholar.harvard.edu (WORKS)

```python
url = f"https://scholar.harvard.edu/{author_slug}/publications"
html = fetch(url)
# PDFs at: /sites/g/files/omnuum{ID}/files/{year}/{filename}.pdf
pdfs = re.findall(r'href="(/sites/g/files/[^"]*\.pdf[^"]*)"', html)
# Make absolute:
pdfs = [f"https://scholar.harvard.edu{p}" for p in pdfs]
```

**Works for:** Laibson, Goldin, Stantcheva, Shleifer, Gabaix, Xavier, Chetty (via OI)

## Pattern 2: UZH DAM (WORKS — best source)

```python
# Ernst Fehr proof-of-concept: 114 PDFs
# URL pattern: https://www.econ.uzh.ch/dam/jcr:{UUID}/{filename}.pdf
# UUIDs are stable and permanent
# Note: Department listing pages are JS-rendered, but DAM URLs are direct
```

**Works for:** Fehr (114), any UZH researcher with known DAM UUIDs

## Pattern 3: Static Berkeley/Stanford homepages (WORKS)

```python
# Old-school faculty pages with direct HTML
urls = {
    "saez": "https://eml.berkeley.edu/~saez/",           # 217 PDFs!
    "card": "https://davidcard.berkeley.edu/papers.html",  # 155 PDFs
    "niederle": "https://web.stanford.edu/~niederle/",     # 68 PDFs
    "gentzkow": "https://web.stanford.edu/~gentzkow/research/",  # 50 PDFs
}
```

## Pattern 4: SSRN search (WORKS ~50%)

```python
query = quote(f"{author_name}")
url = f"https://papers.ssrn.com/sol3/results.cfm?txtKey_Words={query}&npage=1&rpp=50"
html = fetch(url)
# Extract abstract IDs
aids = set(re.findall(r'abstract_id=(\d+)', html))
# Construct PDF URLs
pdfs = [f"https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_{aid}.pdf?abstractid={aid}" for aid in aids]
```

**Note:** SSRN sometimes blocks. Don't retry — move to next source.

## Pattern 5: arXiv (WORKS for technical researchers)

```python
url = f"https://arxiv.org/search/?query={quote(name)}&searchtype=author&start=0"
html = fetch(url)
ids = set(re.findall(r'/abs/(\d+\.\d+)', html))
pdfs = [f"https://arxiv.org/pdf/{aid}.pdf" for aid in ids]
```

**Best for:** AI+Econ (Kleinberg, Kasy), Neuro (some), Decision Theory

## Pattern 6: Opportunity Insights (WORKS — Chetty's team)

```python
url = "https://opportunityinsights.org/paper/"
html = fetch(url)
# 50+ papers with direct PDF links
pdfs = extract_pdfs(html, url)
```

## DOES NOT WORK — Skip These:

```python
# ❌ NBER author pages — JS-rendered
fetch("https://www.nber.org/people/david_laibson")  # Returns HTML shell, no data

# ❌ Google Scholar — always blocked
fetch("https://scholar.google.com/citations?user=XXX")  # 403 or CAPTCHA

# ❌ Google Sites — JS-rendered
fetch("https://sites.google.com/view/some-researcher/research")  # Empty

# ❌ Most .edu department pages — React/Angular
fetch("https://economics.mit.edu/people/faculty/esther-duflo")  # Shell only

# ❌ ResearchGate — login wall
fetch("https://www.researchgate.net/profile/Name")  # Blocked

# ❌ ZORA search — JS-rendered
fetch("https://www.zora.uzh.ch/cgi/search/...")  # Empty results
```

## Top Researchers by Scrapability

| Researcher | Source | PDFs | Why it works |
|-----------|--------|------|-------------|
| Ockenfels | cologne homepage | 224 | Static HTML, full bibliography |
| Saez | berkeley homepage | 217 | Old-school HTML page |
| Vohs | umn homepage | 176 | Static faculty page |
| Card | berkeley homepage | 155 | Static HTML |
| Mullainathan | harvard scholar | 126 | scholar.harvard.edu pattern |
| Kleinberg | cornell homepage | 114 | Static HTML |
| Fehr | UZH DAM | 114 | DAM UUID pattern |
| Niederle | stanford homepage | 68 | Static HTML |
| Pathak | MIT homepage | 64 | Static elements |
| Thaler | chicago booth | 63 | Mixed but partially works |
