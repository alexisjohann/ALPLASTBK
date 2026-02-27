#!/usr/bin/env python3
"""
EBF Quality Checker
Automatische Analyse von Appendices auf Qualitätsindikatoren.

Prüft:
- Epistemic Tag Coverage
- Zitationsstruktur
- Parameter-Dokumentation
- Bekannte problematische Referenzen
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class QualityReport:
    """Qualitätsbericht für eine Appendix."""
    filename: str
    epistemic_tags: Dict[str, int]
    untagged_params: int
    total_params: int
    citations: Dict[str, str]  # ref -> status
    problematic_refs: List[str]
    warnings: List[str]
    
    @property
    def tag_coverage(self) -> float:
        if self.total_params == 0:
            return 0.0
        tagged = sum(self.epistemic_tags.values())
        return tagged / self.total_params * 100


# Bekannte problematische Referenzen
PROBLEMATIC_REFS = {
    "Chen et al. (2025)": "NOT_VERIFIED - r-Decomposability paper existence unclear",
    "Chen et al., 2025": "NOT_VERIFIED - r-Decomposability paper existence unclear",
    "Baldwin (2024)": "NOT_VERIFIED - DSMC paper status unclear",
    "Baldwin, 2024": "NOT_VERIFIED - DSMC paper status unclear",
}

# Working Papers (legitimate but should be noted)
WORKING_PAPERS = {
    "Horton (2023)": "NBER Working Paper - not peer-reviewed",
    "Horton, 2023": "NBER Working Paper - not peer-reviewed",
    "Argyle et al. (2023)": "LLM methodology - controversial",
}

# Epistemic Tag Patterns
TAG_PATTERNS = {
    'EMP': r'\[EMP[:\s]|\{EMP\}|\\tagEMP|epistemic.*EMP',
    'THR': r'\[THR[:\s]|\{THR\}|\\tagTHR|epistemic.*THR',
    'LLM': r'\[LLM[:\s]|\{LLM\}|\\tagLLM|epistemic.*LLM',
    'ILL': r'\[ILL[:\s]|\{ILL\}|\\tagILL|epistemic.*ILL',
    'HYP': r'\[HYP[:\s]|\{HYP\}|\\tagHYP|epistemic.*HYP',
}

# Parameter Detection Pattern
PARAM_PATTERNS = [
    r'\\gamma_?\{?[A-Za-z]+\}?',  # γ_XX
    r'\\delta_?\{?[A-Za-z]+\}?',  # δ_XX
    r'\\lambda_?\{?[A-Za-z]+\}?',  # λ_XX
    r'\\beta\s*=\s*[\d.]+',       # β = X.XX
    r'\\alpha\s*=\s*[\d.]+',      # α = X.XX
    r'\\Psi_?\{?[A-Za-z]+\}?',    # Ψ_X
    r'[=≈]\s*\d+\.\d+',           # = X.XX (numerical values)
]


def analyze_file(filepath: str) -> QualityReport:
    """Analysiere eine LaTeX-Datei auf Qualitätsindikatoren."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = Path(filepath).name
    
    # 1. Epistemic Tags zählen
    epistemic_tags = {}
    for tag, pattern in TAG_PATTERNS.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        epistemic_tags[tag] = len(matches)
    
    # 2. Parameter zählen
    total_params = 0
    for pattern in PARAM_PATTERNS:
        matches = re.findall(pattern, content)
        total_params += len(matches)
    
    # Deduplizieren (grob)
    total_params = total_params // 2  # Konservative Schätzung
    
    tagged = sum(epistemic_tags.values())
    untagged = max(0, total_params - tagged)
    
    # 3. Zitationen analysieren
    citations = {}
    
    # Problematische Referenzen suchen
    problematic = []
    for ref, status in PROBLEMATIC_REFS.items():
        if ref in content:
            problematic.append(f"❌ {ref}: {status}")
            citations[ref] = "PROBLEMATIC"
    
    # Working Papers suchen
    for ref, status in WORKING_PAPERS.items():
        if ref in content:
            problematic.append(f"⚠️ {ref}: {status}")
            citations[ref] = "WORKING_PAPER"
    
    # 4. Warnungen generieren
    warnings = []
    
    tag_cov = tagged / total_params * 100 if total_params > 0 else 0
    if tag_cov < 20:
        warnings.append(f"🔴 Sehr niedrige Tag-Coverage: {tag_cov:.1f}%")
    elif tag_cov < 50:
        warnings.append(f"🟡 Niedrige Tag-Coverage: {tag_cov:.1f}%")
    
    if epistemic_tags.get('ILL', 0) > tagged * 0.5:
        warnings.append("⚠️ Mehr als 50% der Tags sind ILL (illustrativ)")
    
    if epistemic_tags.get('HYP', 0) > 5:
        warnings.append("⚠️ Viele hypothetische Behauptungen (HYP)")
    
    # Prüfe auf "illustrative" ohne Tag
    ill_mentions = len(re.findall(r'illustrati', content, re.IGNORECASE))
    if ill_mentions > epistemic_tags.get('ILL', 0) + 5:
        warnings.append("⚠️ 'Illustrative' erwähnt aber nicht getaggt")
    
    return QualityReport(
        filename=filename,
        epistemic_tags=epistemic_tags,
        untagged_params=untagged,
        total_params=total_params,
        citations=citations,
        problematic_refs=problematic,
        warnings=warnings
    )


def print_report(report: QualityReport):
    """Drucke formatierten Report."""
    
    print("=" * 70)
    print(f"QUALITY REPORT: {report.filename}")
    print("=" * 70)
    
    print("\n📊 EPISTEMIC TAG COVERAGE")
    print("-" * 40)
    
    total_tagged = sum(report.epistemic_tags.values())
    
    for tag, count in sorted(report.epistemic_tags.items()):
        bar = "█" * min(count // 2, 20)
        print(f"   {tag}: {count:4d} {bar}")
    
    print(f"\n   Total Tagged:   {total_tagged}")
    print(f"   Total Params:   {report.total_params}")
    print(f"   Untagged:       {report.untagged_params}")
    print(f"   Coverage:       {report.tag_coverage:.1f}%")
    
    if report.problematic_refs:
        print("\n⚠️  PROBLEMATIC REFERENCES")
        print("-" * 40)
        for ref in report.problematic_refs:
            print(f"   {ref}")
    
    if report.warnings:
        print("\n🚨 WARNINGS")
        print("-" * 40)
        for warning in report.warnings:
            print(f"   {warning}")
    
    # Grade
    print("\n" + "=" * 70)
    cov = report.tag_coverage
    if cov >= 80:
        grade = "✅ GOOD"
    elif cov >= 50:
        grade = "⚠️ ACCEPTABLE"
    elif cov >= 20:
        grade = "🟡 NEEDS WORK"
    else:
        grade = "🔴 CRITICAL"
    
    print(f"   TAG COVERAGE GRADE: {grade}")
    print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_quality.py <file.tex>")
        print("\nAnalyzes LaTeX files for quality indicators:")
        print("  - Epistemic tag coverage (EMP/THR/LLM/ILL/HYP)")
        print("  - Parameter documentation")
        print("  - Problematic references")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    report = analyze_file(filepath)
    print_report(report)


if __name__ == "__main__":
    main()
