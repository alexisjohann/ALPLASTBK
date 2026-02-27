# ═══════════════════════════════════════════════════════════════════════════════
# EVIDENCE-BASED FRAMEWORK (EBF) — Canonical Definition (SSOT)
# ═══════════════════════════════════════════════════════════════════════════════
# Priority: HIGHEST — replaces all previous EBF entries in Knowledge Base
# Tags: canonical, ebf, framework, ssot
# Last Updated: 2026-02-15
# ═══════════════════════════════════════════════════════════════════════════════

meta:
  name: "Evidence-Based Framework"
  acronym: "EBF"
  version: "2.0"
  status: "canonical"
  ssot: true
  owner: "FehrAdvice & Partners AG"
  scientific_partner: "Prof. Ernst Fehr, Universität Zürich"

# ═══════════════════════════════════════════════════════════════════════════════
# CORE DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════

definition:
  description: |
    Das Evidence-Based Framework (EBF) ist ein integratives wissenschaftliches 
    Framework für ökonomisches und soziales Verhalten, entwickelt von FehrAdvice 
    & Partners AG in Zusammenarbeit mit Prof. Ernst Fehr (Universität Zürich).

# ═══════════════════════════════════════════════════════════════════════════════
# CENTRAL INNOVATION
# ═══════════════════════════════════════════════════════════════════════════════

innovation:
  paradigm_shift:
    traditional:
      formula: "θ = Konstante"
      example: "λ = 2.25 (immer)"
      interpretation: "Loss Aversion IST 2.25"
      
    ebf:
      formula: "θ = f(Ψ, 10C)"
      example: "λ(Ψ, 10C) = variabel"
      interpretation: |
        Loss Aversion in welfare mit stigma = 2.5, 
        aber in workplace mit peers = 1.8
        
  key_insight: "DIE VARIATION IST NICHT NOISE — SIE IST DAS SIGNAL!"

# ═══════════════════════════════════════════════════════════════════════════════
# PARAMETER CONTEXT TRANSFORMATION (PCT)
# ═══════════════════════════════════════════════════════════════════════════════

pct:
  name: "Parameter Context Transformation"
  formula: "θ_B = θ_A × ∏ᵢ M(ΔΨᵢ) × ∏ⱼ N(Δ10Cⱼ)"
  
  variables:
    θ_A: "Parameter im Anchor-Kontext (aus Paper)"
    θ_B: "Parameter im Target-Kontext (Vorhersage)"
    ΔΨᵢ: "Kontext-Differenz"
    "M(·)": "Ψ-Multiplikator"

# ═══════════════════════════════════════════════════════════════════════════════
# SCIENTIFIC BASIS
# ═══════════════════════════════════════════════════════════════════════════════

scientific_basis:
  resources:
    - type: "Papers (BibTeX)"
      count: 2347
    - type: "Theorien"
      count: 153
    - type: "Cases"
      count: 852
    - type: "Kontextfaktoren (CH)"
      count: "404+"
    - type: "Parameter"
      count: "64+"

# ═══════════════════════════════════════════════════════════════════════════════
# 8 PSI CONTEXT DIMENSIONS
# ═══════════════════════════════════════════════════════════════════════════════

psi_framework:
  name: "8 Kontext-Dimensionen"
  dimensions:
    - symbol: "Ψ_I"
      name: "Institutional"
      question: "Welche Regeln, Gesetze, Defaults gelten?"
    - symbol: "Ψ_S"
      name: "Social"
      question: "Wer ist dabei? Welche sozialen Normen?"
    - symbol: "Ψ_C"
      name: "Cognitive"
      question: "Müde? Gestresst? Aufmerksam? Motiviert?"
    - symbol: "Ψ_K"
      name: "Cultural"
      question: "Welche Werte, Traditionen, Religion?"
    - symbol: "Ψ_E"
      name: "Economic"
      question: "Wieviel Budget, Zeit, Energie verfügbar?"
    - symbol: "Ψ_T"
      name: "Temporal"
      question: "Wann? Zeitdruck? Welche Lebensphase?"
    - symbol: "Ψ_M"
      name: "Material"
      question: "Welche Technologie, Infrastruktur, Objekte?"
    - symbol: "Ψ_F"
      name: "Physical"
      question: "Wo physisch? Zuhause, Büro, öffentlich?"

# ═══════════════════════════════════════════════════════════════════════════════
# 10C CORE FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════════

ten_c_framework:
  description: "10 komplementäre Dimensionen die gemeinsam menschliches Verhalten erklären"
  ssot: "docs/frameworks/core-framework-definition.yaml"
  
  cores:
    - id: 1
      name: "WHO"
      question: "Wer hat Utility?"
      output: "Welfare Hierarchy: Individual → Dyad → Group → Society"
    - id: 2
      name: "WHAT"
      question: "Was ist Utility?"
      output: "FEPSDE: Financial, Emotional, Physical, Social, Digital, Ecological"
    - id: 3
      name: "HOW"
      question: "Wie interagieren Dimensionen?"
      output: "Komplementarität γ"
    - id: 4
      name: "WHEN"
      question: "Wann zählt Kontext?"
      output: "8 Ψ-Dimensionen"
    - id: 5
      name: "WHERE"
      question: "Woher die Zahlen?"
      output: "Parameter-Kalibrierung, 4-Tier BBB"
    - id: 6
      name: "AWARE"
      question: "Wie bewusst?"
      output: "Awareness-Filter A(·) ∈ [0,1]"
    - id: 7
      name: "READY"
      question: "Handlungsbereit?"
      output: "Willingness WAX ≥ θ"
    - id: 8
      name: "STAGE"
      question: "Wo in der Journey?"
      output: "Behavioral Change Journey S(t)"
    - id: 9
      name: "HIERARCHY"
      question: "Wie stratifizieren Entscheidungen?"
      output: "L0-L3"
    - id: 10
      name: "EIT"
      question: "Wie emergieren Interventionen?"
      output: "Vektor I⃗ ∈ [0,1]⁹"

# ═══════════════════════════════════════════════════════════════════════════════
# EBF AXIOMS
# ═══════════════════════════════════════════════════════════════════════════════

axioms:
  - id: 1
    name: "Empirische Fundierung"
    rule: "Parameter basieren auf 2,347+ Papers, nicht auf Annahmen"
    
  - id: 2
    name: "Parameter-Hierarchie (BBB 4-Tier)"
    rule: "Literature → LLMMC → Empirical → Expert"
    
  - id: 3
    name: "Referentielle Integrität"
    rule: "Jeder Parameter verweist auf die Parameter-Registry"
    
  - id: 4
    name: "Komplementarität ist begründet"
    rule: "γ ≠ 0 Werte haben Paper-Quellen"
    
  - id: 5
    name: "Additivität ist Default"
    rule: "Komplementarität nur wenn Additivität nicht ausreicht"

# ═══════════════════════════════════════════════════════════════════════════════
# WHAT EBF IS NOT
# ═══════════════════════════════════════════════════════════════════════════════

not_ebf:
  - claim: "Kein Chatbot"
    reality: "Es ist ein wissenschaftliches Analyse-Framework"
    
  - claim: "Kein Big-Data-System"
    reality: "Es nutzt Smart Data (kuratierte Kontextfaktoren)"
    
  - claim: "Keine Black Box"
    reality: "Alle Parameter sind transparent und nachvollziehbar"
    
  - claim: "Keine Meinungsmaschine"
    reality: "Jede Aussage hat eine Quellenangabe"

# ═══════════════════════════════════════════════════════════════════════════════
# RELATED COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

related:
  bcm:
    name: "Behavioral Change Model"
    ssot: "data/knowledge/canonical/bcm.yaml"
    relationship: "BCM is the core model within EBF"
    
  ten_c:
    name: "10C CORE Framework"
    ssot: "docs/frameworks/core-framework-definition.yaml"
    relationship: "10C provides the structural dimensions of EBF"
    
  terminology:
    name: "Terminology Registry"
    ssot: "data/beatrix/terminology-registry.yaml"
    relationship: "Enforces correct naming conventions"
