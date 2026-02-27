#!/usr/bin/env python3
"""
UBS Feel Switzerland: Monte Carlo Results Visualization
========================================================

Generates 6 professional visualizations from the Monte Carlo simulation results:
1. persona_heatmap.png - Persona x Region conversion rates
2. conversion_funnel.png - IST vs SOLL conversion pipeline
3. discount_curve.png - Optimal discount depth analysis
4. benefit_attention.png - Attention decay by persona
5. fairness_framing.png - Fairness utility by framing strategy
6. regional_map.png - Regional cultural multiplier effects

Style: FehrAdvice Corporate Identity
Colors: Dark blue #024079, Light blue #549EDE, Dark gray #25212A, Light gray #F3F5F7

Author: EBF Framework / FehrAdvice & Partners AG
Date: 2026-02-13
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# FehrAdvice color palette
COLORS = {
    'darkblue': '#024079',
    'lightblue': '#549EDE',
    'darkgray': '#25212A',
    'lightgray': '#F3F5F7',
    'lilac': '#A1A0C6',
    'mint': '#7EBDAC',
    'ocher': '#DECB3F',
    'orange': '#DE9D3E',
}

# Data from Monte Carlo simulation
PERSONAS = ['Lena', 'Marco', 'Sandra', 'Thomas']
REGIONS = ['DE-CH', 'FR-CH', 'TI', 'GR']
REGION_NAMES = ['Deutschschweiz', 'Romandie', 'Ticino', 'Graubünden']

# Table 2: SOLL Conversion rates (mean)
SOLL_CONVERSION = {
    'Lena':   [86.6, 81.7, 84.1, 83.8],
    'Marco':  [87.4, 81.9, 84.4, 84.8],
    'Sandra': [91.7, 86.9, 88.8, 89.6],
    'Thomas': [58.3, 48.0, 49.6, 55.1],
}

# Confidence intervals for discount chart
DISCOUNT_LEVELS = [0.20, 0.40, 0.60, 0.80]
DISCOUNT_VALUES = {
    'mean': [0.243, 0.382, 0.383, 0.226],
    'lo':   [0.21, 0.35, 0.36, 0.22],
    'hi':   [0.29, 0.42, 0.40, 0.23],
}

# Quality signals for discount chart
QUALITY_SIGNALS = {0.20: 1.00, 0.40: 0.90, 0.60: 0.75, 0.80: 0.55}

# Optimal N* per persona
N_STAR = {
    'Lena':   6.9,
    'Marco':  6.1,
    'Sandra': 5.5,
    'Thomas': 4.8,
}

# Fairness utility by framing
FAIRNESS = {
    'earned':       {'u': 82.2, 'violation': 0.0},
    'transparent':  {'u': 80.9, 'violation': 0.0},
    'exclusive':    {'u': 78.3, 'violation': 0.0},
    'premium_only': {'u': 64.3, 'violation': 0.1},
}

# Regional multipliers
REGIONAL_MULTIPLIERS = {
    'Deutschschweiz': {'default': 1.15, 'social': 1.00, 'reciprocity': 1.25, 'events': 1.10},
    'Romandie':       {'default': 0.95, 'social': 1.15, 'reciprocity': 1.00, 'events': 1.05},
    'Ticino':         {'default': 1.05, 'social': 1.25, 'reciprocity': 0.90, 'events': 1.15},
    'Graubünden':     {'default': 1.10, 'social': 0.90, 'reciprocity': 1.10, 'events': 1.05},
}

OUTPUT_DIR = Path('/home/user/complementarity-context-framework/outputs')
OUTPUT_DIR.mkdir(exist_ok=True)

def setup_plot_style():
    """Apply FehrAdvice style to all plots."""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelcolor'] = COLORS['darkgray']
    plt.rcParams['axes.edgecolor'] = COLORS['darkgray']
    plt.rcParams['text.color'] = COLORS['darkgray']
    plt.rcParams['xtick.color'] = COLORS['darkgray']
    plt.rcParams['ytick.color'] = COLORS['darkgray']


def plot_persona_heatmap():
    """1. Heatmap: Persona x Region SOLL conversion rates."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create data matrix
    data = np.array([SOLL_CONVERSION[p] for p in PERSONAS])

    # Create heatmap
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=40, vmax=95)

    # Set ticks and labels
    ax.set_xticks(np.arange(len(REGIONS)))
    ax.set_yticks(np.arange(len(PERSONAS)))
    ax.set_xticklabels(REGION_NAMES, fontsize=11)
    ax.set_yticklabels(PERSONAS, fontsize=11)

    # Add conversion percentages in cells
    for i in range(len(PERSONAS)):
        for j in range(len(REGIONS)):
            text_color = 'white' if data[i, j] < 70 else COLORS['darkgray']
            ax.text(j, i, f"{data[i, j]:.1f}%",
                   ha="center", va="center", color=text_color,
                   fontsize=12, fontweight='bold')

    # Labels and title
    ax.set_xlabel('Swiss Region', fontsize=12, fontweight='bold')
    ax.set_ylabel('Persona', fontsize=12, fontweight='bold')
    ax.set_title('Conversion Rate by Persona × Region (SOLL Scenario)',
                fontsize=14, fontweight='bold', color=COLORS['darkblue'], pad=20)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Conversion Rate (%)', rotation=270, labelpad=20, fontsize=11)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'persona_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: persona_heatmap.png")


def plot_conversion_funnel():
    """2. Funnel chart: IST vs SOLL conversion pipeline."""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Funnel stages with IST vs SOLL values
    stages = ['Awareness', 'Consideration', 'Activation', 'Attendance', 'Repeat']
    ist_values = [100, 50, 15, 9.4, 5.0]   # IST scenario
    soll_values = [100, 85, 79.0, 70, 55]   # SOLL scenario

    y_positions = np.arange(len(stages))

    # Plot horizontal bars
    bar_height = 0.35
    ax.barh(y_positions - bar_height/2, ist_values, bar_height,
           label='IST (Opt-In)', color=COLORS['lightgray'], edgecolor=COLORS['darkgray'], linewidth=1.5)
    ax.barh(y_positions + bar_height/2, soll_values, bar_height,
           label='SOLL (Opt-Out + Nudge)', color=COLORS['darkblue'], edgecolor=COLORS['darkblue'], linewidth=1.5)

    # Add percentage labels
    for i, (ist, soll) in enumerate(zip(ist_values, soll_values)):
        ax.text(ist + 2, i - bar_height/2, f'{ist:.1f}%',
               va='center', fontsize=10, color=COLORS['darkgray'])
        ax.text(soll + 2, i + bar_height/2, f'{soll:.1f}%',
               va='center', fontsize=10, color=COLORS['darkblue'], fontweight='bold')

    # Styling
    ax.set_yticks(y_positions)
    ax.set_yticklabels(stages, fontsize=11)
    ax.set_xlabel('Conversion Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Conversion Funnel: IST vs SOLL Scenarios',
                fontsize=14, fontweight='bold', color=COLORS['darkblue'], pad=20)
    ax.set_xlim(0, 110)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'conversion_funnel.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: conversion_funnel.png")


def plot_discount_curve():
    """3. Line chart: Perceived value vs discount depth with quality signal."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    discount_pct = np.array(DISCOUNT_LEVELS) * 100
    values = DISCOUNT_VALUES['mean']
    lo = DISCOUNT_VALUES['lo']
    hi = DISCOUNT_VALUES['hi']
    quality = [QUALITY_SIGNALS[d] for d in DISCOUNT_LEVELS]

    # Primary axis: Perceived value
    ax1.plot(discount_pct, values, marker='o', markersize=10, linewidth=2.5,
            color=COLORS['darkblue'], label='Perceived Value')
    ax1.fill_between(discount_pct, lo, hi, alpha=0.3, color=COLORS['lightblue'],
                     label='95% CI')

    # Highlight optimal zone (around 40-60%)
    ax1.axvspan(35, 65, alpha=0.15, color=COLORS['mint'], label='Optimal Zone')

    # Mark optimal point
    optimal_idx = np.argmax(values)
    ax1.scatter([discount_pct[optimal_idx]], [values[optimal_idx]],
               s=200, color=COLORS['orange'], marker='*', zorder=5,
               label=f'Optimal ({discount_pct[optimal_idx]:.0f}%)')

    ax1.set_xlabel('Discount Depth (%)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Perceived Value', fontsize=12, fontweight='bold', color=COLORS['darkblue'])
    ax1.tick_params(axis='y', labelcolor=COLORS['darkblue'])
    ax1.set_ylim(0.15, 0.45)
    ax1.grid(alpha=0.3, linestyle='--')

    # Secondary axis: Quality signal
    ax2 = ax1.twinx()
    ax2.plot(discount_pct, quality, marker='s', markersize=8, linewidth=2,
            color=COLORS['orange'], linestyle='--', label='Quality Signal')
    ax2.set_ylabel('Quality Signal', fontsize=12, fontweight='bold', color=COLORS['orange'])
    ax2.tick_params(axis='y', labelcolor=COLORS['orange'])
    ax2.set_ylim(0.4, 1.1)

    # Title and legend
    ax1.set_title('Optimal Discount Depth: Perceived Value vs Quality Signal',
                 fontsize=14, fontweight='bold', color=COLORS['darkblue'], pad=20)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower left', fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'discount_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: discount_curve.png")


def plot_benefit_attention():
    """4. Attention decay curve: Marginal attention vs number of benefits."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Attention decay function: A(N) = exp(-eta * N)
    # Eta values per persona (from simulation)
    eta_values = {
        'Lena':   0.20 * 0.85,
        'Marco':  0.20 * 0.95,
        'Sandra': 0.20 * 1.05,
        'Thomas': 0.20 * 1.20,
    }

    colors_persona = {
        'Lena':   COLORS['mint'],
        'Marco':  COLORS['darkblue'],
        'Sandra': COLORS['lilac'],
        'Thomas': COLORS['orange'],
    }

    N = np.arange(1, 13)

    for persona in PERSONAS:
        eta = eta_values[persona]
        attention = np.exp(-eta * N)
        n_star = N_STAR[persona]

        ax.plot(N, attention, marker='o', linewidth=2,
               label=f'{persona} (N*={n_star:.0f})', color=colors_persona[persona])

        # Mark N* with vertical line
        ax.axvline(n_star, linestyle='--', alpha=0.5, color=colors_persona[persona])

    # Threshold line
    ax.axhline(0.3, linestyle=':', linewidth=2, color=COLORS['darkgray'],
              alpha=0.7, label='Threshold (0.3)')

    ax.set_xlabel('Number of Benefits (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Marginal Attention A(N)', fontsize=12, fontweight='bold')
    ax.set_title('Attention Decay: Optimal Benefit Count by Persona',
                fontsize=14, fontweight='bold', color=COLORS['darkblue'], pad=20)
    ax.set_xticks(N)
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'benefit_attention.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: benefit_attention.png")


def plot_fairness_framing():
    """5. Horizontal bar chart: Fairness utility by framing strategy."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sort by fairness utility (descending)
    sorted_framing = sorted(FAIRNESS.items(), key=lambda x: x[1]['u'], reverse=True)
    framing_names = [f.replace('_', ' ').title() for f, _ in sorted_framing]
    fairness_values = [data['u'] for _, data in sorted_framing]
    violation_probs = [data['violation'] for _, data in sorted_framing]

    y_positions = np.arange(len(framing_names))

    # Color bars by violation probability
    colors = [COLORS['mint'] if v == 0.0 else COLORS['orange'] for v in violation_probs]

    bars = ax.barh(y_positions, fairness_values, color=colors,
                   edgecolor=COLORS['darkgray'], linewidth=1.5)

    # Add fairness values as text
    for i, (val, viol) in enumerate(zip(fairness_values, violation_probs)):
        ax.text(val + 1, i, f'{val:.1f}%', va='center', fontsize=11,
               fontweight='bold', color=COLORS['darkgray'])
        # Add violation probability marker
        if viol > 0:
            ax.text(val - 5, i, f'⚠ {viol:.1f}%', va='center', ha='right',
                   fontsize=9, color=COLORS['orange'], fontweight='bold')

    # Add threshold line at 50%
    ax.axvline(50, linestyle='--', linewidth=2, color=COLORS['darkgray'],
              alpha=0.5, label='Violation Threshold (50%)')

    ax.set_yticks(y_positions)
    ax.set_yticklabels(framing_names, fontsize=11)
    ax.set_xlabel('Fairness Utility U (%)', fontsize=12, fontweight='bold')
    ax.set_title('Fairness Perception by Framing Strategy (Fehr-Schmidt Model)',
                fontsize=14, fontweight='bold', color=COLORS['darkblue'], pad=20)
    ax.set_xlim(0, 95)
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    # Legend
    green_patch = mpatches.Patch(color=COLORS['mint'], label='No Violation (0%)')
    orange_patch = mpatches.Patch(color=COLORS['orange'], label='Violation Risk (>0%)')
    ax.legend(handles=[green_patch, orange_patch], loc='lower right', fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fairness_framing.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: fairness_framing.png")


def plot_regional_map():
    """6. Regional cultural multiplier effects (4-quadrant chart)."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    region_order = list(REGIONAL_MULTIPLIERS.keys())
    multipliers_labels = ['Default\nCompliance', 'Social\nProof', 'Reciprocity', 'Cultural\nEvents']
    multipliers_keys = ['default', 'social', 'reciprocity', 'events']

    colors_mult = [COLORS['darkblue'], COLORS['mint'], COLORS['lilac'], COLORS['ocher']]

    for idx, (region_name, ax) in enumerate(zip(region_order, axes)):
        data = REGIONAL_MULTIPLIERS[region_name]
        values = [data[key] for key in multipliers_keys]

        # Bar chart for each region
        bars = ax.bar(multipliers_labels, values, color=colors_mult,
                      edgecolor=COLORS['darkgray'], linewidth=1.5, alpha=0.8)

        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.02,
                   f'{val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

        # Reference line at 1.0 (neutral)
        ax.axhline(1.0, linestyle='--', linewidth=1.5, color=COLORS['darkgray'], alpha=0.5)

        # Styling
        ax.set_title(region_name, fontsize=13, fontweight='bold', color=COLORS['darkblue'])
        ax.set_ylabel('Multiplier Effect', fontsize=11)
        ax.set_ylim(0.7, 1.4)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

    fig.suptitle('Regional Cultural Multiplier Effects (Swiss Regions)',
                fontsize=15, fontweight='bold', color=COLORS['darkblue'], y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(OUTPUT_DIR / 'regional_map.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: regional_map.png")


def main():
    """Generate all 6 visualizations."""
    print("\n" + "="*70)
    print("  UBS FEEL SWITZERLAND - VISUALIZATION GENERATOR")
    print("="*70)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("\nGenerating visualizations...")
    print()

    setup_plot_style()

    plot_persona_heatmap()
    plot_conversion_funnel()
    plot_discount_curve()
    plot_benefit_attention()
    plot_fairness_framing()
    plot_regional_map()

    print()
    print("="*70)
    print("  ✓ All 6 visualizations generated successfully!")
    print("="*70)
    print()
    print("Files created:")
    for filename in ['persona_heatmap.png', 'conversion_funnel.png',
                     'discount_curve.png', 'benefit_attention.png',
                     'fairness_framing.png', 'regional_map.png']:
        print(f"  • {OUTPUT_DIR / filename}")
    print()


if __name__ == "__main__":
    main()
