#!/usr/bin/env python3
"""Enrich AWE002 context vectors with EBF fields (psi_dimension, core_10c).

Adds to each factor:
  - psi_dimension: Primary Psi dimension(s) from the 8 Psi framework
  - core_10c: Primary 10C CORE dimension(s)

Mapping is dimension-based with factor-level keyword overrides.
"""

import yaml
import sys
import os

# ============================================================================
# DIMENSION → PSI / 10C MAPPING
# ============================================================================

# Projektvektor (00)
PROJEKT_MAP = {
    "Projektmandat & Zielarchitektur": {
        "psi": ["Psi_I"],
        "core": ["WHEN"],
    },
    "Wirkungs- & Erfolgsmesslogik": {
        "psi": ["Psi_I", "Psi_C"],
        "core": ["WHERE", "AWARE"],
    },
    "Problem- & Verhaltensstruktur": {
        "psi": ["Psi_C", "Psi_S"],
        "core": ["WHAT", "AWARE"],
    },
    "Akteurs- & Stakeholderstruktur": {
        "psi": ["Psi_S"],
        "core": ["WHO"],
    },
    "Institutionelle & regulatorische Rahmenbedingungen": {
        "psi": ["Psi_I"],
        "core": ["WHEN"],
    },
    "Markt- & Systemrestriktionen": {
        "psi": ["Psi_E", "Psi_M"],
        "core": ["HOW"],
    },
    "Ressourcen- & Organisationsstruktur (intern)": {
        "psi": ["Psi_E"],
        "core": ["READY"],
    },
    "Zeitliche Dynamik & Sequenzierung": {
        "psi": ["Psi_T"],
        "core": ["STAGE"],
    },
    "Unsicherheits- & Legitimationsdimension": {
        "psi": ["Psi_C", "Psi_S"],
        "core": ["AWARE", "READY"],
    },
}

# Unternehmensvektor (01)
UNTERNEHMEN_MAP = {
    "Institutionelle Legitimation & Mandat": {
        "psi": ["Psi_I"],
        "core": ["WHEN"],
    },
    "Strategische Zielarchitektur": {
        "psi": ["Psi_I"],
        "core": ["WHAT"],
    },
    "Politische Macht- & Abhängigkeitsstruktur": {
        "psi": ["Psi_S", "Psi_I"],
        "core": ["WHO", "HIERARCHY"],
    },
    "Organisations- & Entscheidungsstruktur": {
        "psi": ["Psi_I"],
        "core": ["HIERARCHY"],
    },
    "Operative Leistungsfähigkeit": {
        "psi": ["Psi_M"],
        "core": ["READY"],
    },
    "Ressourcen- & Kompetenzbasis": {
        "psi": ["Psi_E"],
        "core": ["WHERE"],
    },
    "Instrumente & faktische Einflussreichweite": {
        "psi": ["Psi_I", "Psi_M"],
        "core": ["HOW"],
    },
    "Externe Koordinations- & Netzwerkstruktur": {
        "psi": ["Psi_S"],
        "core": ["WHO"],
    },
    "Organisationskultur & Legitimitätsposition": {
        "psi": ["Psi_K", "Psi_S"],
        "core": ["AWARE"],
    },
}

# Kantonsvektor (02)
KANTON_MAP = {
    "Governance- und Regulierungsarchitektur": {
        "psi": ["Psi_I"],
        "core": ["WHEN"],
    },
    "Energiesystem- und Infrastrukturstruktur": {
        "psi": ["Psi_M"],
        "core": ["HOW"],
    },
    "Markt- und Preisstruktur": {
        "psi": ["Psi_E"],
        "core": ["WHAT"],
    },
    "Soziale Entscheidungs- und Vergleichsstruktur": {
        "psi": ["Psi_S", "Psi_C"],
        "core": ["WHO", "AWARE"],
    },
    "Institutionelle Umsetzungskapazität": {
        "psi": ["Psi_I"],
        "core": ["READY"],
    },
    "Unsicherheits- und Erwartungsstruktur": {
        "psi": ["Psi_C"],
        "core": ["AWARE"],
    },
    "Transformations- und Systemdynamik": {
        "psi": ["Psi_T", "Psi_E"],
        "core": ["STAGE"],
    },
    "Raum- und Geografiestruktur": {
        "psi": ["Psi_F"],
        "core": ["WHERE"],
    },
}

# ============================================================================
# KEYWORD OVERRIDES (factor-level refinement)
# ============================================================================

KEYWORD_PSI_OVERRIDES = {
    # Keywords that force additional Psi dimensions
    "soziale norm": "Psi_S",
    "peer": "Psi_S",
    "nachbar": "Psi_S",
    "vergleich": "Psi_S",
    "vertrauen": "Psi_S",
    "gemeinde": "Psi_S",
    "stigma": "Psi_S",
    "reputation": "Psi_S",
    "default": "Psi_I",
    "gesetz": "Psi_I",
    "regulier": "Psi_I",
    "vorschrift": "Psi_I",
    "pflicht": "Psi_I",
    "förder": "Psi_I",
    "subvention": "Psi_E",
    "kosten": "Psi_E",
    "preis": "Psi_E",
    "invest": "Psi_E",
    "budget": "Psi_E",
    "kredit": "Psi_E",
    "finanz": "Psi_E",
    "digital": "Psi_M",
    "portal": "Psi_M",
    "technolog": "Psi_M",
    "infrastruktur": "Psi_M",
    "frist": "Psi_T",
    "deadline": "Psi_T",
    "zeitdruck": "Psi_T",
    "sequenz": "Psi_T",
    "phase": "Psi_T",
    "unsicherheit": "Psi_C",
    "komplex": "Psi_C",
    "information": "Psi_C",
    "wissen": "Psi_C",
    "wahrnehmung": "Psi_C",
    "kognitiv": "Psi_C",
    "kultur": "Psi_K",
    "werte": "Psi_K",
    "tradition": "Psi_K",
    "identität": "Psi_K",
    "geograf": "Psi_F",
    "räumlich": "Psi_F",
    "ländlich": "Psi_F",
    "urban": "Psi_F",
    "standort": "Psi_F",
}

KEYWORD_10C_OVERRIDES = {
    "segment": "WHO",
    "zielgruppe": "WHO",
    "akteur": "WHO",
    "stakeholder": "WHO",
    "nutzen": "WHAT",
    "motivation": "WHAT",
    "anreiz": "WHAT",
    "barriere": "WHAT",
    "kosten": "WHAT",
    "instrument": "HOW",
    "massnahme": "HOW",
    "intervention": "HOW",
    "kanal": "HOW",
    "kommunikation": "HOW",
    "kontext": "WHEN",
    "regulier": "WHEN",
    "rahmen": "WHEN",
    "parameter": "WHERE",
    "messung": "WHERE",
    "indikator": "WHERE",
    "kpi": "WHERE",
    "bewusst": "AWARE",
    "salienz": "AWARE",
    "information": "AWARE",
    "wissen": "AWARE",
    "wahrnehmung": "AWARE",
    "bereit": "READY",
    "kapazität": "READY",
    "fähigkeit": "READY",
    "ressource": "READY",
    "phase": "STAGE",
    "journey": "STAGE",
    "sequenz": "STAGE",
    "zeitlich": "STAGE",
    "hierarchie": "HIERARCHY",
    "ebene": "HIERARCHY",
    "entscheidung": "HIERARCHY",
    "kompetenz": "HIERARCHY",
}


def enrich_factor(factor, dim_map):
    """Add psi_dimension and core_10c to a factor based on dimension + keywords."""
    dim = factor.get("dimension", "")
    mapping = dim_map.get(dim, {"psi": ["Psi_C"], "core": ["WHAT"]})

    # Start with dimension-level defaults
    psi_set = set(mapping["psi"])
    core_set = set(mapping["core"])

    # Apply keyword overrides from factor text
    text = " ".join(
        str(v).lower() for v in [
            factor.get("faktor", ""),
            factor.get("definition", ""),
            factor.get("kontext", ""),
        ] if v
    )

    for keyword, psi in KEYWORD_PSI_OVERRIDES.items():
        if keyword in text and psi not in psi_set:
            psi_set.add(psi)

    for keyword, core in KEYWORD_10C_OVERRIDES.items():
        if keyword in text and core not in core_set:
            core_set.add(core)

    # Order consistently
    psi_order = ["Psi_I", "Psi_S", "Psi_C", "Psi_K", "Psi_E", "Psi_T", "Psi_M", "Psi_F"]
    core_order = ["WHO", "WHAT", "HOW", "WHEN", "WHERE", "AWARE", "READY", "STAGE", "HIERARCHY", "EIT"]

    factor["psi_dimension"] = [p for p in psi_order if p in psi_set]
    factor["core_10c"] = [c for c in core_order if c in core_set]

    return factor


def yaml_val(val):
    """Format a value for YAML output."""
    if val is None:
        return "null"
    if isinstance(val, list):
        return "[" + ", ".join(str(v) for v in val) + "]"
    s = str(val).strip()
    if not s:
        return "null"
    try:
        float(s)
        return s
    except ValueError:
        pass
    needs_quote = False
    if s.startswith(("{", "[", "'", '"', "&", "*", "!", "|", ">", "%", "@", "`")):
        needs_quote = True
    if ":" in s or "#" in s or "\n" in s:
        needs_quote = True
    if s.lower() in ("true", "false", "yes", "no", "null", "on", "off"):
        needs_quote = True
    if needs_quote or len(s) > 80 or "," in s or ";" in s:
        escaped = s.replace("'", "''")
        return f"'{escaped}'"
    return s


def write_enriched_yaml(data, output_path):
    """Write enriched YAML with EBF fields."""
    meta = data["metadata"]
    faktoren = data["faktoren"]

    # Group by dimension
    dims = []
    dim_map = {}
    for f in faktoren:
        d = f.get("dimension", "Unknown")
        if d not in dim_map:
            dim_map[d] = []
            dims.append(d)
        dim_map[d].append(f)

    # Determine all keys
    key_order = [
        "id", "dimension", "faktor", "definition", "kontext",
        "salienz", "indikator", "gruende", "datenpunkt",
        "trend", "unsicherheit", "risiko_chance", "staerke_schwaeche",
        "beeinflussbarkeit", "status",
        "psi_dimension", "core_10c",
    ]
    all_keys = set()
    for f in faktoren:
        all_keys.update(f.keys())
    used_keys = [k for k in key_order if k in all_keys]

    lines = []
    lines.append("# -----------------------------------------------------------")
    lines.append(f"# {meta['titel']}")
    lines.append(f"# Projekt: {meta['projekt']}")
    lines.append(f"# Ebene: {meta['ebene']}")
    lines.append(f"# Quelle: {meta['quelle']}")
    lines.append(f"# Konvertiert: {meta['konvertiert']}")
    lines.append(f"# Faktoren: {meta['faktoren_total']}")
    lines.append(f"# Dimensionen: {meta['dimensionen_total']}")
    lines.append(f"# EBF-Mapping: psi_dimension, core_10c")
    lines.append("# -----------------------------------------------------------")
    lines.append("")
    lines.append("metadata:")
    lines.append(f"  titel: {yaml_val(meta['titel'])}")
    lines.append(f"  projekt: {yaml_val(meta['projekt'])}")
    lines.append(f"  ebene: {yaml_val(meta['ebene'])}")
    lines.append(f"  quelle: {yaml_val(meta['quelle'])}")
    lines.append(f"  konvertiert: '{meta['konvertiert']}'")
    lines.append(f"  faktoren_total: {meta['faktoren_total']}")
    lines.append(f"  dimensionen_total: {meta['dimensionen_total']}")
    lines.append("  ebf_mapping: true")
    lines.append("  dimensionen:")
    for d in dims:
        lines.append(f"    - name: {yaml_val(d)}")
        lines.append(f"      faktoren: {len(dim_map[d])}")
    lines.append("")
    lines.append("faktoren:")

    for d in dims:
        lines.append("")
        lines.append(f"  # === {d} ({len(dim_map[d])} Faktoren) ===")
        for f in dim_map[d]:
            lines.append("")
            lines.append(f"  - id: {yaml_val(f.get('id'))}")
            lines.append(f"    dimension: {yaml_val(f.get('dimension'))}")
            for key in used_keys:
                if key in ("id", "dimension"):
                    continue
                val = f.get(key)
                lines.append(f"    {key}: {yaml_val(val)}")

    lines.append("")

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    return len(faktoren)


def process_file(yaml_path, dim_mapping):
    """Load, enrich, and rewrite a YAML file."""
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    # Collect psi/10c stats
    psi_counts = {}
    core_counts = {}

    for factor in data["faktoren"]:
        enrich_factor(factor, dim_mapping)
        for p in factor.get("psi_dimension", []):
            psi_counts[p] = psi_counts.get(p, 0) + 1
        for c in factor.get("core_10c", []):
            core_counts[c] = core_counts.get(c, 0) + 1

    n = write_enriched_yaml(data, yaml_path)

    return n, psi_counts, core_counts


def main():
    base = "data/customers/awe-sg/projects/AWE002/Kontextvektoren"

    configs = [
        (os.path.join(base, "CV_AWE002_00_projektvektor.yaml"), PROJEKT_MAP, "Projektvektor"),
        (os.path.join(base, "CV_AWE002_01_unternehmen.yaml"), UNTERNEHMEN_MAP, "Unternehmen"),
        (os.path.join(base, "CV_AWE002_02_kanton_sg.yaml"), KANTON_MAP, "Kanton SG"),
    ]

    total = 0
    for path, mapping, name in configs:
        n, psi, core = process_file(path, mapping)
        total += n
        print(f"\n=== {name} ({n} Faktoren) ===")
        print("  Psi-Verteilung:")
        for p in ["Psi_I", "Psi_S", "Psi_C", "Psi_K", "Psi_E", "Psi_T", "Psi_M", "Psi_F"]:
            bar = "█" * (psi.get(p, 0) // 2)
            print(f"    {p:6s}: {psi.get(p, 0):3d} {bar}")
        print("  10C-Verteilung:")
        for c in ["WHO", "WHAT", "HOW", "WHEN", "WHERE", "AWARE", "READY", "STAGE", "HIERARCHY"]:
            bar = "█" * (core.get(c, 0) // 2)
            print(f"    {c:10s}: {core.get(c, 0):3d} {bar}")

    print(f"\nTotal: {total} Faktoren mit EBF-Mapping angereichert.")


if __name__ == "__main__":
    main()
