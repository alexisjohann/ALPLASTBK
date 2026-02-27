#!/usr/bin/env python3
"""
EBF Graphics Generator
======================
Generiert Grafiken aus Session-Daten für PPTX-Präsentationen.

Unterstützte Chart-Typen:
- Bar Charts (horizontal/vertikal)
- Line Charts (mit Annotationen)
- Pie/Donut Charts
- Heatmaps
- Formula Render (LaTeX)

Usage:
    python generate_graphics.py <session_id> [--output-dir <dir>]
    python generate_graphics.py EBF-S-2026-01-26-COG-001

Author: FehrAdvice & Partners AG
Version: 1.0
Date: January 2026
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Matplotlib imports
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not installed. Install with: pip install matplotlib")

# =============================================================================
# CONFIGURATION
# =============================================================================

# Pfade relativ zum Repository-Root
REPO_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates" / "pptx"
DATA_DIR = REPO_ROOT / "data"
ASSETS_DIR = REPO_ROOT / "assets"
OUTPUTS_DIR = REPO_ROOT / "outputs" / "sessions"

# FehrAdvice Farben
FA_COLORS = {
    "darkblue": "#024079",
    "lightblue": "#549EDE",
    "darkgray": "#25212A",
    "lightgray": "#F3F5F7",
    "lilac": "#A1A0C6",
    "mint": "#7EBDAC",
    "ocher": "#DECB3F",
    "orange": "#DE9D3E",
    "success": "#7EBDAC",
    "error": "#C94C4C",
}

FA_COLOR_SEQUENCE = [
    FA_COLORS["darkblue"],
    FA_COLORS["lightblue"],
    FA_COLORS["lilac"],
    FA_COLORS["mint"],
    FA_COLORS["ocher"],
    FA_COLORS["orange"],
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_yaml(filepath: Path) -> Dict:
    """Lädt eine YAML-Datei."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def ensure_dir(path: Path) -> Path:
    """Stellt sicher, dass ein Verzeichnis existiert."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def setup_fa_style():
    """Setzt den FehrAdvice Style für matplotlib."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Open Sans', 'Roboto', 'Arial', 'Helvetica'],
        'font.size': 12,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'axes.edgecolor': FA_COLORS["lightgray"],
        'axes.linewidth': 0.5,
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 11,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'savefig.edgecolor': 'none',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
    })


# =============================================================================
# CHART GENERATORS
# =============================================================================

def generate_bar_horizontal(
    data: Dict[str, float],
    title: str,
    output_path: Path,
    xlabel: str = "Anteil (%)",
    colors: Optional[List[str]] = None,
    show_values: bool = True,
    figsize: Tuple[float, float] = (8, 5)
) -> Path:
    """
    Generiert einen horizontalen Balkendiagramm.

    Args:
        data: Dict mit {label: value}
        title: Titel des Charts
        output_path: Ausgabepfad
        xlabel: X-Achsen-Beschriftung
        colors: Liste von Farben (optional)
        show_values: Werte anzeigen
        figsize: Figurengrösse

    Returns:
        Path zur generierten Datei
    """
    setup_fa_style()

    labels = list(data.keys())
    values = list(data.values())

    if colors is None:
        colors = FA_COLOR_SEQUENCE[:len(labels)]

    fig, ax = plt.subplots(figsize=figsize)

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, height=0.6, edgecolor='none')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=12)
    ax.set_xlabel(xlabel, fontsize=12, color=FA_COLORS["darkgray"])
    ax.set_title(title, fontsize=16, fontweight='bold', color=FA_COLORS["darkblue"], pad=20)

    # Werte anzeigen
    if show_values:
        for bar, val in zip(bars, values):
            width = bar.get_width()
            ax.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                   f'{val:.0%}', va='center', ha='left',
                   fontsize=11, color=FA_COLORS["darkgray"])

    # X-Achse als Prozent
    ax.set_xlim(0, max(values) * 1.2)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))

    # Nur linke und untere Achse
    ax.spines['left'].set_color(FA_COLORS["darkgray"])
    ax.spines['bottom'].set_color(FA_COLORS["lightgray"])

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    return output_path


def generate_line_chart(
    x_data: List[float],
    y_data: List[float],
    title: str,
    output_path: Path,
    xlabel: str = "X",
    ylabel: str = "Y",
    labels: Optional[List[str]] = None,
    x_scale: str = "linear",
    show_annotations: bool = True,
    figsize: Tuple[float, float] = (8, 5)
) -> Path:
    """
    Generiert ein Liniendiagramm mit optionalen Annotationen.
    """
    setup_fa_style()

    fig, ax = plt.subplots(figsize=figsize)

    # Linie zeichnen
    ax.plot(x_data, y_data,
            color=FA_COLORS["darkblue"],
            linewidth=2.5,
            marker='o',
            markersize=10,
            markerfacecolor=FA_COLORS["darkblue"],
            markeredgecolor='white',
            markeredgewidth=2)

    # Annotationen
    if show_annotations and labels:
        for x, y, label in zip(x_data, y_data, labels):
            ax.annotate(label,
                       xy=(x, y),
                       xytext=(15, 5),
                       textcoords='offset points',
                       fontsize=10,
                       color=FA_COLORS["darkgray"],
                       ha='left')

    ax.set_xlabel(xlabel, fontsize=12, color=FA_COLORS["darkgray"])
    ax.set_ylabel(ylabel, fontsize=12, color=FA_COLORS["darkgray"])
    ax.set_title(title, fontsize=16, fontweight='bold', color=FA_COLORS["darkblue"], pad=20)

    if x_scale == "log":
        ax.set_xscale('log')

    # Grid
    ax.grid(True, alpha=0.3, color=FA_COLORS["lightgray"])
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    return output_path


def generate_donut_chart(
    data: Dict[str, float],
    title: str,
    output_path: Path,
    center_text: Optional[str] = None,
    colors: Optional[List[str]] = None,
    figsize: Tuple[float, float] = (6, 6)
) -> Path:
    """
    Generiert ein Donut-Diagramm.
    """
    setup_fa_style()

    labels = list(data.keys())
    values = list(data.values())

    if colors is None:
        colors = FA_COLOR_SEQUENCE[:len(labels)]

    fig, ax = plt.subplots(figsize=figsize)

    # Donut erstellen
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,
        colors=colors,
        autopct='%1.0f%%',
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )

    # Prozent-Labels stylen
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')

    # Legende
    ax.legend(wedges, labels,
             title="Parameter",
             loc="center left",
             bbox_to_anchor=(1, 0, 0.5, 1),
             fontsize=11)

    # Center Text
    if center_text:
        ax.text(0, 0, center_text,
               ha='center', va='center',
               fontsize=16, fontweight='bold',
               color=FA_COLORS["darkblue"])

    ax.set_title(title, fontsize=16, fontweight='bold', color=FA_COLORS["darkblue"], pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    return output_path


def generate_table_graphic(
    data: List[List[str]],
    headers: List[str],
    title: str,
    output_path: Path,
    figsize: Tuple[float, float] = (10, 4)
) -> Path:
    """
    Generiert eine Tabelle als Grafik.
    """
    setup_fa_style()

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')

    # Farben für Zeilen
    row_colors = [[FA_COLORS["lightgray"] if i % 2 else 'white'
                   for _ in range(len(headers))]
                  for i in range(len(data))]

    table = ax.table(
        cellText=data,
        colLabels=headers,
        cellLoc='center',
        loc='center',
        colColours=[FA_COLORS["darkblue"]] * len(headers),
        cellColours=row_colors
    )

    # Styling
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)

    # Header weiss
    for i in range(len(headers)):
        table[(0, i)].set_text_props(color='white', fontweight='bold')

    ax.set_title(title, fontsize=16, fontweight='bold', color=FA_COLORS["darkblue"], pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    return output_path


def generate_formula_png(
    formula: str,
    output_path: Path,
    fontsize: int = 24,
    figsize: Tuple[float, float] = (10, 1.5)
) -> Path:
    """
    Rendert eine LaTeX-Formel als PNG.
    """
    setup_fa_style()

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')

    # LaTeX Formel rendern
    ax.text(0.5, 0.5, formula,
           transform=ax.transAxes,
           fontsize=fontsize,
           ha='center', va='center',
           color=FA_COLORS["darkgray"])

    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                transparent=True, pad_inches=0.1)
    plt.close()

    return output_path


# =============================================================================
# SESSION DATA EXTRACTION
# =============================================================================

def load_session_data(session_id: str) -> Dict[str, Any]:
    """
    Lädt alle relevanten Daten für eine Session.
    """
    # Model Registry laden
    model_registry = load_yaml(DATA_DIR / "model-registry.yaml")

    # Passendes Modell finden
    model_data = None
    for model in model_registry.get('models', []):
        if model.get('created_in_session') == session_id:
            model_data = model
            break
        if session_id in model.get('evolved_in_sessions', []):
            model_data = model
            break

    # Output Registry laden
    output_registry = load_yaml(DATA_DIR / "output-registry.yaml")

    # Passenden Output finden
    output_data = None
    for output in output_registry.get('outputs', []):
        if output.get('session_id') == session_id:
            output_data = output
            break

    return {
        'session_id': session_id,
        'model': model_data,
        'output': output_data
    }


def extract_cognitive_hierarchy(model_data: Dict) -> Optional[Dict[str, float]]:
    """
    Extrahiert Cognitive Hierarchy Daten aus dem Modell.
    """
    if not model_data:
        return None

    ch = model_data.get('cognitive_hierarchy', {}).get('distribution', {})
    if not ch:
        return None

    return {
        'Level 0': ch.get('L0', {}).get('proportion', 0),
        'Level 1': ch.get('L1', {}).get('proportion', 0),
        'Level 2': ch.get('L2', {}).get('proportion', 0),
        'Level 3+': ch.get('L3_plus', {}).get('proportion', 0),
    }


def extract_situations(model_data: Dict) -> Optional[Tuple[List, List, List]]:
    """
    Extrahiert Situations-Daten für Line Chart.
    """
    if not model_data:
        return None

    situations = model_data.get('example_results', {}).get('situations', [])
    if not situations:
        return None

    x = [s.get('n', 0) for s in situations]
    y = [s.get('V', 0) for s in situations]
    labels = [s.get('name', '') for s in situations]

    return x, y, labels


def extract_sensitivity(model_data: Dict) -> Optional[Dict[str, float]]:
    """
    Extrahiert Sensitivitäts-Daten für Donut Chart.
    """
    if not model_data:
        return None

    drivers = model_data.get('sensitivity', {}).get('main_drivers', [])
    if not drivers:
        return None

    return {d.get('parameter', '?'): d.get('influence', 0) for d in drivers}


# =============================================================================
# MAIN GENERATOR
# =============================================================================

def generate_all_graphics(session_id: str, output_dir: Optional[Path] = None) -> List[Path]:
    """
    Generiert alle Grafiken für eine Session.

    Args:
        session_id: Session-ID (z.B. EBF-S-2026-01-26-COG-001)
        output_dir: Ausgabeverzeichnis (optional)

    Returns:
        Liste der generierten Dateien
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Error: matplotlib required for graphics generation")
        return []

    # Output-Verzeichnis
    if output_dir is None:
        output_dir = OUTPUTS_DIR / session_id / "graphics"
    output_dir = ensure_dir(output_dir)

    print(f"Generating graphics for session: {session_id}")
    print(f"Output directory: {output_dir}")

    # Session-Daten laden
    session_data = load_session_data(session_id)
    model_data = session_data.get('model')

    if not model_data:
        print(f"Warning: No model data found for session {session_id}")
        return []

    generated_files = []

    # 1. Cognitive Hierarchy Bar Chart
    ch_data = extract_cognitive_hierarchy(model_data)
    if ch_data:
        output_path = output_dir / "cognitive_hierarchy_bar.png"
        generate_bar_horizontal(
            data=ch_data,
            title="Cognitive Hierarchy: Wie weit denken Menschen?",
            output_path=output_path,
            colors=[FA_COLORS["lightblue"], FA_COLORS["darkblue"],
                   FA_COLORS["lilac"], FA_COLORS["mint"]]
        )
        generated_files.append(output_path)
        print(f"  ✓ Generated: cognitive_hierarchy_bar.png")

    # 2. V(n) Decay Line Chart
    situations = extract_situations(model_data)
    if situations:
        x, y, labels = situations
        output_path = output_dir / "v_n_decay_line.png"
        generate_line_chart(
            x_data=x,
            y_data=y,
            title="Verständnis V(n) nach Systemkomplexität",
            output_path=output_path,
            xlabel="Anzahl Elemente (n)",
            ylabel="Verständnis V",
            labels=labels,
            x_scale="log",
            show_annotations=True
        )
        generated_files.append(output_path)
        print(f"  ✓ Generated: v_n_decay_line.png")

    # 3. Sensitivity Donut Chart
    sens_data = extract_sensitivity(model_data)
    if sens_data:
        output_path = output_dir / "sensitivity_donut.png"
        # Haupttreiber für Center-Text
        main_driver = max(sens_data.items(), key=lambda x: x[1])
        center_text = f"{main_driver[0]}\n{main_driver[1]:.0%}"

        generate_donut_chart(
            data=sens_data,
            title="Was treibt (mangelndes) Verständnis?",
            output_path=output_path,
            center_text=center_text
        )
        generated_files.append(output_path)
        print(f"  ✓ Generated: sensitivity_donut.png")

    # 4. Formula Render
    formula = model_data.get('functional_form', {}).get('formula', '')
    if formula:
        output_path = output_dir / "formula_render.png"
        # Vereinfachte LaTeX-Version
        latex_formula = r"$V(n) = \frac{(\kappa + \lambda \cdot E) \cdot \psi \cdot (1 + \mu \cdot S)}{n^{\alpha} \cdot (1+\tau)^{\beta} \cdot (1+\sigma)^{\gamma}}$"
        generate_formula_png(
            formula=latex_formula,
            output_path=output_path
        )
        generated_files.append(output_path)
        print(f"  ✓ Generated: formula_render.png")

    # 5. Domain Heatmap (falls vorhanden)
    domain_exp = model_data.get('domain_exponents', {})
    if domain_exp:
        output_path = output_dir / "domain_heatmap.png"
        # Tabelle als Grafik
        headers = ["Domain", "α (Komplexität)", "β (Zeit)", "γ (Distanz)"]
        data = []
        for domain, values in domain_exp.items():
            data.append([
                domain,
                f"{values.get('alpha', 0):.2f}",
                f"{values.get('beta', 0):.2f}",
                f"{values.get('gamma', 0):.2f}"
            ])

        generate_table_graphic(
            data=data,
            headers=headers,
            title="Domain-spezifische Parameter",
            output_path=output_path
        )
        generated_files.append(output_path)
        print(f"  ✓ Generated: domain_heatmap.png")

    print(f"\nTotal graphics generated: {len(generated_files)}")
    return generated_files


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate graphics for EBF session presentations"
    )
    parser.add_argument(
        "session_id",
        help="Session ID (e.g., EBF-S-2026-01-26-COG-001)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        help="Output directory (default: outputs/sessions/<session_id>/graphics/)"
    )
    parser.add_argument(
        "--list-only", "-l",
        action="store_true",
        help="Only list what would be generated, don't create files"
    )

    args = parser.parse_args()

    if args.list_only:
        print(f"Would generate graphics for: {args.session_id}")
        session_data = load_session_data(args.session_id)
        if session_data.get('model'):
            print("  - cognitive_hierarchy_bar.png")
            print("  - v_n_decay_line.png")
            print("  - sensitivity_donut.png")
            print("  - formula_render.png")
            print("  - domain_heatmap.png (if data available)")
        else:
            print("  Warning: No model data found")
        return

    generated = generate_all_graphics(args.session_id, args.output_dir)

    if generated:
        print("\n✅ Graphics generation complete!")
        for f in generated:
            print(f"   {f}")
    else:
        print("\n❌ No graphics generated")
        sys.exit(1)


if __name__ == "__main__":
    main()
