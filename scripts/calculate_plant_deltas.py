#!/usr/bin/env python3
"""
ALPLA Plant Delta Calculator
Berechnet paarweise Distanzen zwischen allen 17 US-Werken
basierend auf PCI (strukturell) und IFI (Interventions-Fit)

Output:
- Distanzmatrix (17x17)
- Optimale Matched Pairs
- Cluster-Homogenität
"""

import yaml
import csv
import numpy as np
from pathlib import Path

# Pfade
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# =============================================================================
# DATEN LADEN
# =============================================================================

def load_pci_data():
    """Lade PCI-Schätzungen aus CSV"""
    plants = {}
    with open(DATA_DIR / "alpla-pci-estimates.csv", "r") as f:
        # Filter comments and empty lines
        lines = [line for line in f if line.strip() and not line.startswith('#')]
        reader = csv.DictReader(lines)
        for row in reader:
            plant_id = row['plant_id']
            plants[plant_id] = {
                'name': row['plant_name'],
                'type': row['plant_type'],
                'S2': int(row['S2_employees']),
                'S3': int(row['S3']),
                'S4': float(row['S4']),
                'S5': int(row['S5']),
                'S6': int(row['S6']),
                'O1': int(row['O1']),
                'BC_pct': int(row['BC_pct']),
                'WC_pct': int(row['WC_pct']),
                'P1_BC': float(row['P1_BC']),
                'P1_WC': float(row['P1_WC']),
                'P1_total': float(row['P1_total']),
            }
    return plants

def load_labor_data():
    """Lade Labor Market Daten aus CSV"""
    labor = {}
    with open(DATA_DIR / "alpla-usa-labor-market-data.csv", "r") as f:
        # Filter comments and empty lines
        lines = [line for line in f if line.strip() and not line.startswith('#')]
        reader = csv.DictReader(lines)
        for row in reader:
            plant_id = row['plant_id']
            labor[plant_id] = {
                'L1_unemployment': float(row['L1_unemployment_pct']),
                'L2_mfg_establishments': int(row['L2_mfg_establishments']),
                'L3_urbanization': int(row['L3_urbanization']),
                'L4_wage': float(row['L4_mfg_wage_hr']),
                'L5_coli': float(row['L5_coli']),
            }
    return labor

def load_ifi_data():
    """Lade IFI-Scores aus YAML"""
    with open(DATA_DIR / "alpla-intervention-fit-index.yaml", "r") as f:
        data = yaml.safe_load(f)

    ifi = {}
    for key, value in data['plant_scores'].items():
        plant_id = value['plant_id']
        ifi[plant_id] = {
            'I1': value['ifi_scores']['I1_rotation_fit'],
            'I2': value['ifi_scores']['I2_career_fit'],
            'I3': value['ifi_scores']['I3_skill_pay_fit'],
            'I4': value['ifi_scores']['I4_workload_fit'],
            'I5': value['ifi_scores']['I5_autonomy_fit'],
            'cluster': value['ifi_profile']['cluster'],
        }
    return ifi

# =============================================================================
# NORMALISIERUNG
# =============================================================================

def normalize(value, min_val, max_val):
    """Normalisiere auf [0, 1]"""
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)

def get_normalization_bounds(plants, labor):
    """Berechne Min/Max für alle Dimensionen"""
    bounds = {
        'S2': (min(p['S2'] for p in plants.values()), max(p['S2'] for p in plants.values())),
        'S3': (min(p['S3'] for p in plants.values()), max(p['S3'] for p in plants.values())),
        'S4': (min(p['S4'] for p in plants.values()), max(p['S4'] for p in plants.values())),
        'S5': (min(p['S5'] for p in plants.values()), max(p['S5'] for p in plants.values())),
        'O1': (min(p['O1'] for p in plants.values()), max(p['O1'] for p in plants.values())),
        'P1': (min(p['P1_total'] for p in plants.values()), max(p['P1_total'] for p in plants.values())),
        'L1': (min(l['L1_unemployment'] for l in labor.values()), max(l['L1_unemployment'] for l in labor.values())),
        'L2': (min(l['L2_mfg_establishments'] for l in labor.values()), max(l['L2_mfg_establishments'] for l in labor.values())),
        'L4': (min(l['L4_wage'] for l in labor.values()), max(l['L4_wage'] for l in labor.values())),
        'L5': (min(l['L5_coli'] for l in labor.values()), max(l['L5_coli'] for l in labor.values())),
    }
    return bounds

# =============================================================================
# DISTANZ-BERECHNUNG
# =============================================================================

def calculate_pci_distance(p1_id, p2_id, plants, labor, bounds):
    """
    Berechne PCI-Distanz (strukturelle Ähnlichkeit)
    Gewichteter euklidischer Abstand in normalisiertem Raum
    """
    p1, p2 = plants[p1_id], plants[p2_id]
    l1, l2 = labor[p1_id], labor[p2_id]

    # Gewichte für PCI-Dimensionen
    weights = {
        'S2': 0.20,   # Mitarbeiteranzahl
        'S3': 0.05,   # Produktionslinien
        'O1': 0.15,   # Kundenabhängigkeit
        'P1': 0.20,   # Churn-Rate
        'L1': 0.10,   # Arbeitslosenquote
        'L2': 0.10,   # Mfg Density
        'L4': 0.10,   # Lohnniveau
        'L5': 0.10,   # Lebenshaltungskosten
    }

    # Plant Type Penalty (verschiedene Typen = höhere Distanz)
    type_penalty = 0 if p1['type'] == p2['type'] else 0.15

    # Normalisierte Differenzen
    diffs = {
        'S2': normalize(p1['S2'], *bounds['S2']) - normalize(p2['S2'], *bounds['S2']),
        'S3': normalize(p1['S3'], *bounds['S3']) - normalize(p2['S3'], *bounds['S3']),
        'O1': normalize(p1['O1'], *bounds['O1']) - normalize(p2['O1'], *bounds['O1']),
        'P1': normalize(p1['P1_total'], *bounds['P1']) - normalize(p2['P1_total'], *bounds['P1']),
        'L1': normalize(l1['L1_unemployment'], *bounds['L1']) - normalize(l2['L1_unemployment'], *bounds['L1']),
        'L2': normalize(l1['L2_mfg_establishments'], *bounds['L2']) - normalize(l2['L2_mfg_establishments'], *bounds['L2']),
        'L4': normalize(l1['L4_wage'], *bounds['L4']) - normalize(l2['L4_wage'], *bounds['L4']),
        'L5': normalize(l1['L5_coli'], *bounds['L5']) - normalize(l2['L5_coli'], *bounds['L5']),
    }

    # Gewichteter euklidischer Abstand
    distance = np.sqrt(sum(weights[k] * (diffs[k] ** 2) for k in weights))
    distance += type_penalty

    return round(distance, 3)

def calculate_ifi_distance(p1_id, p2_id, ifi):
    """
    Berechne IFI-Distanz (Interventions-Fit Ähnlichkeit)
    Euklidischer Abstand im 5D IFI-Raum
    """
    i1, i2 = ifi[p1_id], ifi[p2_id]

    # Alle 5 Dimensionen gleichgewichtet (bereits 0-100 skaliert)
    diff_I1 = (i1['I1'] - i2['I1']) / 100
    diff_I2 = (i1['I2'] - i2['I2']) / 100
    diff_I3 = (i1['I3'] - i2['I3']) / 100
    diff_I4 = (i1['I4'] - i2['I4']) / 100
    diff_I5 = (i1['I5'] - i2['I5']) / 100

    distance = np.sqrt((diff_I1**2 + diff_I2**2 + diff_I3**2 + diff_I4**2 + diff_I5**2) / 5)

    # Cluster Penalty (verschiedene Cluster = höhere Distanz)
    cluster_penalty = 0 if i1['cluster'] == i2['cluster'] else 0.10

    return round(distance + cluster_penalty, 3)

def calculate_combined_distance(pci_dist, ifi_dist, pci_weight=0.5, ifi_weight=0.5):
    """Kombinierte Distanz aus PCI und IFI"""
    return round(pci_weight * pci_dist + ifi_weight * ifi_dist, 3)

# =============================================================================
# MATRIX-GENERIERUNG
# =============================================================================

def generate_distance_matrices(plants, labor, ifi, bounds):
    """Generiere alle Distanzmatrizen"""
    plant_ids = sorted(plants.keys())
    n = len(plant_ids)

    pci_matrix = np.zeros((n, n))
    ifi_matrix = np.zeros((n, n))
    combined_matrix = np.zeros((n, n))

    for i, p1 in enumerate(plant_ids):
        for j, p2 in enumerate(plant_ids):
            if i == j:
                continue
            pci_dist = calculate_pci_distance(p1, p2, plants, labor, bounds)
            ifi_dist = calculate_ifi_distance(p1, p2, ifi)
            combined_dist = calculate_combined_distance(pci_dist, ifi_dist)

            pci_matrix[i, j] = pci_dist
            ifi_matrix[i, j] = ifi_dist
            combined_matrix[i, j] = combined_dist

    return plant_ids, pci_matrix, ifi_matrix, combined_matrix

def find_optimal_pairs(plant_ids, combined_matrix, ifi):
    """Finde optimale Matched Pairs basierend auf kombinierter Distanz"""
    n = len(plant_ids)
    pairs = []

    for i in range(n):
        for j in range(i+1, n):
            p1, p2 = plant_ids[i], plant_ids[j]
            distance = combined_matrix[i, j]
            same_cluster = ifi[p1]['cluster'] == ifi[p2]['cluster']
            pairs.append({
                'plant_1': p1,
                'plant_2': p2,
                'combined_distance': distance,
                'same_cluster': same_cluster,
                'cluster': ifi[p1]['cluster'] if same_cluster else 'mixed',
            })

    # Sortiere nach Distanz (kleinste zuerst)
    pairs.sort(key=lambda x: (not x['same_cluster'], x['combined_distance']))

    return pairs

# =============================================================================
# OUTPUT
# =============================================================================

def print_distance_matrix(name, plant_ids, matrix, plants):
    """Drucke formatierte Distanzmatrix"""
    print(f"\n{'='*100}")
    print(f"{name} DISTANCE MATRIX")
    print(f"{'='*100}")

    # Header
    header = "Plant".ljust(12) + " | " + " | ".join(f"{pid[-3:]}" for pid in plant_ids)
    print(header)
    print("-" * len(header))

    # Rows
    for i, pid in enumerate(plant_ids):
        row = f"{plants[pid]['name'][:10]}".ljust(12) + " | "
        row += " | ".join(f"{matrix[i,j]:.2f}" if i != j else " -- " for j in range(len(plant_ids)))
        print(row)

def print_delta_analysis(plant_ids, pci_matrix, ifi_matrix, combined_matrix, plants, ifi):
    """Drucke Delta-Analyse für jedes Werk"""
    print(f"\n{'='*100}")
    print("DELTA ANALYSIS: Was unterscheidet jedes Werk?")
    print(f"{'='*100}\n")

    for i, pid in enumerate(plant_ids):
        print(f"--- {pid}: {plants[pid]['name']} ({plants[pid]['type']}) ---")
        print(f"    Cluster: {ifi[pid]['cluster']}")
        print(f"    IFI Scores: I1={ifi[pid]['I1']}, I2={ifi[pid]['I2']}, I3={ifi[pid]['I3']}, I4={ifi[pid]['I4']}, I5={ifi[pid]['I5']}")

        # Finde nächste Nachbarn
        distances = [(plant_ids[j], combined_matrix[i,j]) for j in range(len(plant_ids)) if i != j]
        distances.sort(key=lambda x: x[1])

        print(f"    Nächste Nachbarn:")
        for neighbor, dist in distances[:3]:
            cluster_match = "✓" if ifi[pid]['cluster'] == ifi[neighbor]['cluster'] else "✗"
            print(f"      {neighbor} ({plants[neighbor]['name'][:15]}): Δ={dist:.3f} [{cluster_match} Cluster]")

        print(f"    Fernste Werke:")
        for neighbor, dist in distances[-2:]:
            print(f"      {neighbor} ({plants[neighbor]['name'][:15]}): Δ={dist:.3f}")
        print()

def print_optimal_pairs(pairs, plants, n_pairs=10):
    """Drucke optimale Matched Pairs"""
    print(f"\n{'='*100}")
    print(f"TOP {n_pairs} OPTIMAL MATCHED PAIRS (für Feldexperiment)")
    print(f"{'='*100}\n")

    print(f"{'Rank':<5} | {'Plant 1':<25} | {'Plant 2':<25} | {'Delta':<8} | {'Cluster':<20}")
    print("-" * 95)

    for rank, pair in enumerate(pairs[:n_pairs], 1):
        p1_name = plants[pair['plant_1']]['name'][:22]
        p2_name = plants[pair['plant_2']]['name'][:22]
        cluster = pair['cluster'] if pair['same_cluster'] else f"MIXED"
        marker = "⭐" if pair['same_cluster'] and pair['combined_distance'] < 0.15 else ""

        print(f"{rank:<5} | {p1_name:<25} | {p2_name:<25} | {pair['combined_distance']:<8.3f} | {cluster:<15} {marker}")

def print_cluster_homogeneity(plant_ids, combined_matrix, ifi, plants):
    """Analysiere Homogenität innerhalb Clustern"""
    print(f"\n{'='*100}")
    print("CLUSTER HOMOGENEITY ANALYSIS")
    print(f"{'='*100}\n")

    clusters = {}
    for i, pid in enumerate(plant_ids):
        cluster = ifi[pid]['cluster']
        if cluster not in clusters:
            clusters[cluster] = []
        clusters[cluster].append((i, pid))

    for cluster, members in sorted(clusters.items()):
        print(f"\n{cluster} ({len(members)} Werke):")
        print("-" * 50)

        # Intra-Cluster Distanzen
        intra_distances = []
        for k, (i, p1) in enumerate(members):
            for (j, p2) in members[k+1:]:
                intra_distances.append((p1, p2, combined_matrix[i, j]))

        if intra_distances:
            avg_dist = np.mean([d[2] for d in intra_distances])
            max_dist = max(d[2] for d in intra_distances)
            min_dist = min(d[2] for d in intra_distances)

            print(f"  Intra-Cluster Distanz: Ø={avg_dist:.3f}, Min={min_dist:.3f}, Max={max_dist:.3f}")
            print(f"  Beste Paare im Cluster:")
            for p1, p2, dist in sorted(intra_distances, key=lambda x: x[2])[:3]:
                print(f"    {plants[p1]['name'][:15]} ↔ {plants[p2]['name'][:15]}: Δ={dist:.3f}")
        else:
            print(f"  Nur 1 Werk - keine Intra-Cluster Vergleiche möglich")

def export_to_csv(plant_ids, pci_matrix, ifi_matrix, combined_matrix, plants, ifi):
    """Exportiere Distanzmatrizen als CSV"""

    # Combined Distance Matrix
    output_path = DATA_DIR / "alpla-plant-distance-matrix.csv"
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header comments
        f.write("# ALPLA Plant Distance Matrix (Combined PCI + IFI)\n")
        f.write("# Generated by calculate_plant_deltas.py\n")
        f.write("# Lower values = more similar plants\n")
        f.write("#\n")

        # Header row
        header = ['plant_id', 'plant_name', 'cluster'] + [pid for pid in plant_ids]
        writer.writerow(header)

        # Data rows
        for i, pid in enumerate(plant_ids):
            row = [pid, plants[pid]['name'], ifi[pid]['cluster']]
            row += [f"{combined_matrix[i,j]:.3f}" if i != j else "0.000" for j in range(len(plant_ids))]
            writer.writerow(row)

    print(f"\nExported to: {output_path}")

    # Optimal Pairs
    pairs_path = DATA_DIR / "alpla-optimal-pairs.csv"
    pairs = find_optimal_pairs(plant_ids, combined_matrix, ifi)

    with open(pairs_path, 'w', newline='') as f:
        writer = csv.writer(f)
        f.write("# ALPLA Optimal Matched Pairs for Field Experiment\n")
        f.write("# Sorted by combined distance (PCI + IFI)\n")
        f.write("#\n")

        writer.writerow(['rank', 'plant_1', 'plant_1_name', 'plant_2', 'plant_2_name',
                        'combined_distance', 'same_cluster', 'cluster'])

        for rank, pair in enumerate(pairs, 1):
            writer.writerow([
                rank,
                pair['plant_1'],
                plants[pair['plant_1']]['name'],
                pair['plant_2'],
                plants[pair['plant_2']]['name'],
                pair['combined_distance'],
                pair['same_cluster'],
                pair['cluster'],
            ])

    print(f"Exported to: {pairs_path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 100)
    print("ALPLA PLANT DELTA CALCULATOR")
    print("Paarweise Vergleiche aller 17 US-Werke")
    print("=" * 100)

    # Daten laden
    print("\n[1/4] Loading data...")
    plants = load_pci_data()
    labor = load_labor_data()
    ifi = load_ifi_data()
    bounds = get_normalization_bounds(plants, labor)

    print(f"  Loaded {len(plants)} plants")
    print(f"  PCI dimensions: S2, S3, O1, P1, L1, L2, L4, L5")
    print(f"  IFI dimensions: I1, I2, I3, I4, I5")

    # Distanzmatrizen berechnen
    print("\n[2/4] Calculating distance matrices...")
    plant_ids, pci_matrix, ifi_matrix, combined_matrix = generate_distance_matrices(
        plants, labor, ifi, bounds
    )
    print(f"  Generated {len(plant_ids)}x{len(plant_ids)} matrices")

    # Optimale Paare finden
    print("\n[3/4] Finding optimal pairs...")
    pairs = find_optimal_pairs(plant_ids, combined_matrix, ifi)

    # Output
    print("\n[4/4] Generating reports...")

    # Delta Analysis pro Werk
    print_delta_analysis(plant_ids, pci_matrix, ifi_matrix, combined_matrix, plants, ifi)

    # Optimale Paare
    print_optimal_pairs(pairs, plants, n_pairs=15)

    # Cluster Homogenität
    print_cluster_homogeneity(plant_ids, combined_matrix, ifi, plants)

    # Export
    export_to_csv(plant_ids, pci_matrix, ifi_matrix, combined_matrix, plants, ifi)

    print("\n" + "=" * 100)
    print("DONE!")
    print("=" * 100)

if __name__ == "__main__":
    main()
