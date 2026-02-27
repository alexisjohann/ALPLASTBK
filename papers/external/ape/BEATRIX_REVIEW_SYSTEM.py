# ============================================================================
# BEATRIX Review Endpoint – Behavioral Economics Paper Reviewer
# POST /api/documents/{doc_id}/review
# POST /api/review/external (for APE papers via URL)
# ============================================================================

"""
BEATRIX als 6. Reviewer im APE-System:

Die 5 bestehenden APE-Reviewer:
  1. Claude Code (Internal)     → Format, Statistik, Konsistenz
  2. GPT-5-mini (External)      → Methodology, Identification, Literature
  3. Grok-4.1-Fast (External)   → Same focus, different perspective
  4. Gemini-3-Flash (External)  → Same focus, different perspective  
  5. GPT-5.2 (Scan + Final)    → Integrity Check, Final Gate

Was NIEMAND abdeckt:
  ❌ Behavioral mechanisms beyond rational choice
  ❌ Present bias, hyperbolic discounting
  ❌ Social norms, identity utility
  ❌ Choice architecture, defaults, nudges
  ❌ BCM Ψ-Dimensions
  ❌ Practical intervention design

→ BEATRIX füllt genau diese Lücke.
"""

BEATRIX_REVIEW_SYSTEM_PROMPT = """Du bist BEATRIX, ein Behavioral Economics Reviewer. 
Du bist der 6. Reviewer in einem System mit 5 statistisch/methodisch orientierten Reviewern.

Deine EINZIGARTIGE Perspektive:
- Du bewertest Papers durch die Linse der Verhaltensökonomie
- Du nutzt das BCM 2.0 Framework (Behavioral Complementarity Model)
- Du analysierst die 8 Ψ-Dimensionen
- Du identifizierst behavioral mechanisms, die statistische Reviewer übersehen
- Du gibst praktische Gestaltungsempfehlungen für Policy-Interventionen

Du prüfst NICHT (das machen die anderen 5 Reviewer):
- Statistische Korrektheit
- Identifikationsstrategie
- Formale Anforderungen
- Datenqualität

Du prüfst NUR:
1. BEHAVIORAL MECHANISM ANALYSIS
   - Welche behavioral mechanisms sind im Spiel?
   - Welche werden im Paper diskutiert, welche fehlen?
   - Present bias, defaults, social norms, framing, anchoring, loss aversion, etc.

2. Ψ-DIMENSIONS MAPPING
   - Welche der 8 Ψ-Dimensionen sind relevant?
   - Ψ₁ Risk Perception, Ψ₂ Time Preferences, Ψ₃ Social Preferences
   - Ψ₄ Reference Dependence, Ψ₅ Attention/Salience, Ψ₆ Self-Control
   - Ψ₇ Beliefs & Mental Models, Ψ₈ Identity & Self-Image
   - Wie gut deckt das Paper sie ab?

3. POLICY DESIGN IMPLICATIONS
   - Wie könnte die Intervention behavioral verbessert werden?
   - Commitment devices, framing, choice architecture, nudges
   - Heterogeneous effects by behavioral type

4. LITERATURE GAPS
   - Welche behavioral economics Literatur fehlt?
   - Nur relevante Referenzen, max. 7

5. SCORING
   - BCM Relevance (0-25)
   - Methodological Rigor (0-25) — dein Eindruck, nicht Duplikat der anderen
   - Data Novelty (0-25)
   - Practical Applicability (0-25)
   - Total (0-100) → PURSUE (>65) / CONSIDER (45-65) / SKIP (<45)

6. VERDICT
   - ACCEPT / CONDITIONAL ACCEPT / MAJOR REVISION / REJECT
   - Immer aus behavioral Perspektive, nicht statistisch

7. KB INTEGRATION TAGS
   - bcm_dimensions, psi_dimensions, behavioral_mechanisms
   - application_areas, connections to other papers

Antworte IMMER im Markdown-Format mit den 7 Sections oben.
Sei konkret und spezifisch – keine generischen Behavioral-Economics-Platitüden.
Beziehe dich auf exakte Textstellen aus dem Paper.
"""

BEATRIX_REVIEW_USER_TEMPLATE = """Bitte erstelle ein BEATRIX Behavioral Economics Review für folgendes Paper:

**Paper ID:** {paper_id}
**Titel:** {title}
**Methode:** {method}
**Authoring Model:** {authoring_model}

**Abstract:**
{abstract}

**Paper-Inhalt (Auszug):**
{content}

---

Erstelle das Review im BEATRIX-Format mit allen 7 Sections.
Fokussiere auf das, was die 5 statistischen Reviewer NICHT abdecken.
"""

# ============================================================================
# FastAPI Endpoint Implementation
# ============================================================================

REVIEW_ENDPOINT_CODE = '''
@app.post("/api/documents/{doc_id}/review")
async def create_beatrix_review(doc_id: str, token: str = Depends(get_current_user)):
    """Generate a BEATRIX Behavioral Economics Review for a document in the KB."""
    
    # 1. Fetch document from DB
    doc = await get_document(doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    
    # 2. Prepare prompt
    prompt = BEATRIX_REVIEW_USER_TEMPLATE.format(
        paper_id=doc_id,
        title=doc["title"],
        method=next((t for t in doc.get("tags",[]) if t in ["DiD","RDD","RCT","SCM"]), "unknown"),
        authoring_model=next((t for t in doc.get("tags",[]) if "claude" in t or "gpt" in t), "unknown"),
        abstract=doc["content"][:2000],
        content=doc["content"][:30000]  # ~7500 tokens
    )
    
    # 3. Call Claude API
    review = await call_claude(
        system=BEATRIX_REVIEW_SYSTEM_PROMPT,
        user=prompt,
        model="claude-sonnet-4-20250514",
        max_tokens=4096
    )
    
    # 4. Parse scoring from review
    score = extract_score(review)  # Regex for "Total Score: XX/100"
    verdict = extract_verdict(review)  # Regex for verdict line
    tags = extract_tags(review)  # Parse JSON block
    
    # 5. Store review in DB
    review_doc = {
        "title": f"BEATRIX Review: {doc['title'][:80]}",
        "content": review,
        "category": "study",
        "tags": ["BEATRIX-review", "behavioral-economics"] + tags.get("bcm_dimensions", []),
        "metadata": {
            "reviewed_doc_id": doc_id,
            "score": score,
            "verdict": verdict,
            "psi_dimensions": tags.get("psi_dimensions", []),
            "behavioral_mechanisms": tags.get("behavioral_mechanisms", [])
        }
    }
    review_id = await store_document(review_doc, token)
    
    # 6. Push to GitHub
    await push_to_github(
        path=f"papers/reviews/{doc_id}/review_beatrix.md",
        content=review,
        message=f"review: BEATRIX BE Review of {doc['title'][:60]}"
    )
    
    return {
        "review_id": review_id,
        "score": score,
        "verdict": verdict,
        "tags": tags
    }


@app.post("/api/review/external")
async def review_external_paper(
    paper_url: str = Body(...),
    paper_id: str = Body(None),
    token: str = Depends(get_current_user)
):
    """Review an external paper (e.g., from APE GitHub) without importing it first."""
    
    # 1. Fetch paper content from URL
    if "github.com" in paper_url:
        content = await fetch_github_content(paper_url)
    elif paper_url.endswith(".pdf"):
        content = await extract_pdf_text(paper_url)
    else:
        raise HTTPException(400, "Unsupported URL format")
    
    # 2. Extract metadata if available
    metadata = {}
    if paper_id and "ape-papers" in paper_url:
        metadata = await fetch_ape_metadata(paper_id)
    
    # 3. Generate review
    prompt = BEATRIX_REVIEW_USER_TEMPLATE.format(
        paper_id=paper_id or "external",
        title=metadata.get("title", "External Paper"),
        method=metadata.get("method", "unknown"),
        authoring_model=metadata.get("authoring_model", "unknown"),
        abstract=content[:2000],
        content=content[:30000]
    )
    
    review = await call_claude(
        system=BEATRIX_REVIEW_SYSTEM_PROMPT,
        user=prompt,
        model="claude-sonnet-4-20250514",
        max_tokens=4096
    )
    
    return {
        "review": review,
        "score": extract_score(review),
        "verdict": extract_verdict(review)
    }


@app.post("/api/review/batch")
async def batch_review_ape_papers(
    paper_ids: list[str] = Body(...),
    token: str = Depends(get_current_user)
):
    """Batch review multiple APE papers. Returns review summaries."""
    
    results = []
    for pid in paper_ids:
        try:
            # Fetch from APE GitHub
            tex_url = f"https://raw.githubusercontent.com/SocialCatalystLab/ape-papers/main/{pid}/v1/paper.tex"
            meta_url = f"https://raw.githubusercontent.com/SocialCatalystLab/ape-papers/main/{pid}/v1/metadata.json"
            
            content = await fetch_url(tex_url)
            metadata = json.loads(await fetch_url(meta_url))
            
            # Generate review
            review = await call_claude(
                system=BEATRIX_REVIEW_SYSTEM_PROMPT,
                user=BEATRIX_REVIEW_USER_TEMPLATE.format(
                    paper_id=pid,
                    title=metadata.get("title", pid),
                    method=metadata.get("method", "unknown"),
                    authoring_model=metadata.get("authoring_model", "unknown"),
                    abstract=content[:2000],
                    content=content[:25000]
                ),
                model="claude-sonnet-4-20250514",
                max_tokens=3000
            )
            
            results.append({
                "paper_id": pid,
                "title": metadata.get("title"),
                "score": extract_score(review),
                "verdict": extract_verdict(review),
                "review_preview": review[:500]
            })
            
        except Exception as e:
            results.append({"paper_id": pid, "error": str(e)})
    
    return {"reviews": results, "total": len(results)}
'''

# ============================================================================
# Helper Functions
# ============================================================================

HELPER_CODE = '''
import re
import json

def extract_score(review_text: str) -> int:
    """Extract total score from review markdown."""
    patterns = [
        r"Total Score:\s*(\d+)/100",
        r"Total:\s*(\d+)/100",
        r"\*\*Total Score:\s*(\d+)",
        r"Score:\s*(\d+)/100\s*→\s*(PURSUE|CONSIDER|SKIP)"
    ]
    for pattern in patterns:
        match = re.search(pattern, review_text)
        if match:
            return int(match.group(1))
    return 0


def extract_verdict(review_text: str) -> str:
    """Extract verdict from review markdown."""
    patterns = [
        r"BEATRIX Verdict[:\s]*\*?\*?(ACCEPT|CONDITIONAL ACCEPT|MAJOR REVISION|REJECT)",
        r"Verdict[:\s]*\*?\*?(ACCEPT|CONDITIONAL ACCEPT|MAJOR REVISION|REJECT)",
        r"\*\*(ACCEPT|CONDITIONAL ACCEPT|MAJOR REVISION|REJECT)\*\*"
    ]
    for pattern in patterns:
        match = re.search(pattern, review_text, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    return "UNKNOWN"


def extract_tags(review_text: str) -> dict:
    """Extract KB integration tags from JSON block in review."""
    try:
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', review_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
    except:
        pass
    return {}
'''

print("=" * 60)
print("BEATRIX Review System – Architecture Summary")
print("=" * 60)
print()
print("Endpoints:")
print("  POST /api/documents/{doc_id}/review     → Review KB document")
print("  POST /api/review/external               → Review external paper")
print("  POST /api/review/batch                   → Batch review APE papers")
print()
print("Integration Points:")
print("  → Claude API (claude-sonnet-4-20250514)")
print("  → BEATRIX DB (PostgreSQL)")
print("  → GitHub (complementarity-context-framework)")
print("  → APE GitHub (SocialCatalystLab/ape-papers)")
print()
print("Review Framework:")
print("  1. Behavioral Mechanism Analysis")
print("  2. Ψ-Dimensions Mapping (BCM 2.0)")
print("  3. Policy Design Implications")
print("  4. Literature Gaps")
print("  5. Scoring (0-100)")
print("  6. Verdict")
print("  7. KB Integration Tags")
print()
print("Unique Value vs. APE's 5 Reviewers:")
print("  → The ONLY reviewer with Behavioral Economics expertise")
print("  → The ONLY reviewer that maps to BCM Ψ-Dimensions")
print("  → The ONLY reviewer that suggests intervention design improvements")
print("  → The ONLY reviewer that connects to FehrAdvice consulting context")
PYEOF