#!/usr/bin/env python3
"""
SPÖ Portfolio Dashboard Sync Script

Synchronisiert PORTFOLIO_DASHBOARD.yaml automatisch aus ANFRAGEN_REGISTER.yaml.
Wird bei jedem Commit via Pre-Commit Hook oder manuell ausgeführt.

Usage:
    python scripts/sync_spo_portfolio.py              # Sync ausführen
    python scripts/sync_spo_portfolio.py --dry-run    # Nur prüfen, nicht schreiben
    python scripts/sync_spo_portfolio.py --stats      # Statistiken anzeigen
"""

import yaml
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Pfade
BASE_PATH = Path(__file__).parent.parent
REGISTER_PATH = BASE_PATH / "data/customers/spo/database/ANFRAGEN_REGISTER.yaml"
DASHBOARD_PATH = BASE_PATH / "data/customers/spo/database/PORTFOLIO_DASHBOARD.yaml"


def load_yaml(path: Path) -> dict:
    """Lädt YAML-Datei (unterstützt Multi-Document YAML)."""
    with open(path, 'r', encoding='utf-8') as f:
        # Lade alle Dokumente und merge sie
        docs = list(yaml.safe_load_all(f))
        if not docs:
            return {}
        # Erstes Dokument als Basis, rest mergen
        result = docs[0] if docs[0] else {}
        for doc in docs[1:]:
            if doc and isinstance(doc, dict):
                result.update(doc)
        return result


def save_yaml(path: Path, data: dict):
    """Speichert YAML-Datei mit Kommentaren erhalten."""
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)


def extract_clusters_from_register(register: dict) -> list:
    """Extrahiert alle Cluster (ANFs) mit ihren Maßnahmen (INTs) aus dem Register."""
    clusters = []

    anfragen = register.get('anfragen', [])

    for anf in anfragen:
        anf_id = anf.get('id', '')

        # Nur ANFs mit re_audit_details haben INTs
        re_audit = anf.get('re_audit_details', {})
        if not re_audit:
            continue

        interventionen = re_audit.get('interventionen', [])
        if not interventionen:
            continue

        # Monte Carlo Daten
        monte_carlo = re_audit.get('monte_carlo', {})
        sensitivitaet = re_audit.get('sensitivitaets_analyse', {})

        cluster = {
            'cluster_id': anf_id,
            'name': anf.get('thema', 'Unbekannt'),
            'typ': anf.get('typ', 'Unbekannt'),
            'status': anf.get('status', 'offen'),
            'monte_carlo': {
                'p_positiv': monte_carlo.get('p_netto_positiv', 0),
                'median_delta': monte_carlo.get('median_delta', 'n/a')
            },
            'massnahmen': []
        }

        # INTs extrahieren
        for idx, int_data in enumerate(interventionen):
            if isinstance(int_data, dict):
                int_id = int_data.get('id', f'INT-XXX-{idx+1:03d}')
                massnahme = {
                    'id': int_id,
                    'name': int_data.get('name', 'Unbekannt'),
                    'target': int_data.get('target', 'AWARE'),
                    'beschreibung': int_data.get('beschreibung', ''),
                    'empfehlung': int_data.get('empfehlung', ''),
                    'prioritaet': idx + 1
                }

                # Warnung übernehmen falls vorhanden
                if 'warnung' in int_data:
                    massnahme['warnung'] = int_data['warnung']

                cluster['massnahmen'].append(massnahme)

        # Impact aus Sensitivitätsanalyse ableiten (falls vorhanden)
        if sensitivitaet and cluster['massnahmen']:
            # Versuche Sensitivitätswerte den INTs zuzuordnen
            sens_values = list(sensitivitaet.values())
            for idx, m in enumerate(cluster['massnahmen']):
                if idx < len(sens_values):
                    val = sens_values[idx]
                    if isinstance(val, str) and '%' in val:
                        m['impact'] = val

        clusters.append(cluster)

    return clusters


def calculate_aggregations(clusters: list) -> dict:
    """Berechnet Portfolio-Aggregationen."""

    # Zähler
    total_ints = 0
    by_target = defaultdict(int)
    by_priority = defaultdict(list)
    p_values = []

    for cluster in clusters:
        for m in cluster.get('massnahmen', []):
            total_ints += 1
            target = m.get('target', 'UNKNOWN')
            by_target[target] += 1

            prio = m.get('prioritaet', 4)
            by_priority[f'prio_{prio}'].append(m['id'])

        p_val = cluster.get('monte_carlo', {}).get('p_positiv', 0)
        if p_val:
            # Handle both float (0.89) and string ("78%") formats
            if isinstance(p_val, str):
                p_val = float(p_val.replace('%', '')) / 100 if '%' in p_val else float(p_val)
            p_values.append(p_val)

    # Durchschnittliche P(positiv)
    avg_p = sum(p_values) / len(p_values) if p_values else 0

    return {
        'anzahl_cluster': len(clusters),
        'anzahl_massnahmen': total_ints,
        'durchschnitt_pro_cluster': round(total_ints / len(clusters), 1) if clusters else 0,
        'gewichteter_p_positiv': round(avg_p, 2),
        'nach_target': {t: {'anzahl': c, 'anteil': f"{c/total_ints*100:.1f}%"}
                       for t, c in sorted(by_target.items())},
        'nach_prioritaet': dict(by_priority)
    }


def extract_conflicts(clusters: list) -> list:
    """Extrahiert Konflikte/Warnungen aus den INTs."""
    conflicts = []

    for cluster in clusters:
        for m in cluster.get('massnahmen', []):
            if 'warnung' in m:
                conflicts.append({
                    'konflikt_id': f"KONF-{m['id']}",
                    'int': m['id'],
                    'risiko': 'HOCH' if 'POLAR' in m['warnung'].upper() or 'NUR' in m['warnung'].upper() else 'MITTEL',
                    'beschreibung': m['warnung']
                })

    return conflicts


def sync_dashboard(clusters: list, dry_run: bool = False) -> dict:
    """Synchronisiert das Dashboard mit den extrahierten Clustern."""

    # Existierendes Dashboard laden (für manuelle Ergänzungen)
    if DASHBOARD_PATH.exists():
        dashboard = load_yaml(DASHBOARD_PATH)
    else:
        dashboard = {}

    # Metadata aktualisieren
    dashboard['metadata'] = dashboard.get('metadata', {})
    dashboard['metadata'].update({
        'projekt_id': 'PRJ-SPO-2026-STRATEGIE',
        'projekt_name': 'SPÖ Strategische Kommunikation 2026',
        'aktualisiert': datetime.now().strftime('%Y-%m-%d'),
        'status': 'aktiv'
    })

    # Statistiken
    agg = calculate_aggregations(clusters)
    dashboard['metadata']['statistik'] = {
        'anzahl_cluster': agg['anzahl_cluster'],
        'anzahl_massnahmen': agg['anzahl_massnahmen'],
        'durchschnitt_pro_cluster': agg['durchschnitt_pro_cluster']
    }

    # Cluster überschreiben
    dashboard['cluster'] = clusters

    # Aggregationen
    dashboard['portfolio_aggregation'] = {
        'gesamt_performance': {
            'gewichteter_p_positiv': agg['gewichteter_p_positiv'],
            'stabilitaet': 'HOCH' if agg['gewichteter_p_positiv'] > 0.85 else 'MITTEL'
        },
        'nach_target': agg['nach_target'],
        'nach_prioritaet': agg['nach_prioritaet']
    }

    # Konflikte extrahieren
    conflicts = extract_conflicts(clusters)
    if conflicts:
        dashboard['konflikte'] = dashboard.get('konflikte', {})
        dashboard['konflikte']['kritisch'] = conflicts

    # Changelog
    dashboard['changelog'] = dashboard.get('changelog', [])
    dashboard['changelog'].append({
        'datum': datetime.now().strftime('%Y-%m-%d'),
        'aenderung': f"Auto-Sync: {agg['anzahl_cluster']} Cluster, {agg['anzahl_massnahmen']} Maßnahmen",
        'quelle': 'sync_spo_portfolio.py'
    })

    if not dry_run:
        save_yaml(DASHBOARD_PATH, dashboard)

    return dashboard


def print_stats(clusters: list):
    """Gibt Statistiken aus."""
    agg = calculate_aggregations(clusters)

    print("\n" + "="*60)
    print("  SPÖ PORTFOLIO STATISTIKEN")
    print("="*60)
    print(f"\n  Cluster (ANFs):        {agg['anzahl_cluster']}")
    print(f"  Maßnahmen (INTs):      {agg['anzahl_massnahmen']}")
    print(f"  Ø pro Cluster:         {agg['durchschnitt_pro_cluster']}")
    print(f"  Ø P(positiv):          {agg['gewichteter_p_positiv']:.0%}")

    print("\n  Nach Target-Dimension:")
    for target, data in agg['nach_target'].items():
        print(f"    {target:12} {data['anzahl']:3} ({data['anteil']})")

    print("\n  Cluster-Details:")
    for c in clusters:
        n_ints = len(c.get('massnahmen', []))
        p_val = c.get('monte_carlo', {}).get('p_positiv', 0)
        # Handle both float (0.89) and string ("78%") formats
        if isinstance(p_val, str):
            p_val = float(p_val.replace('%', '')) / 100 if '%' in p_val else float(p_val)
        print(f"    {c['cluster_id']}: {c['name'][:25]:25} | {n_ints} INTs | P={p_val:.0%}")

    conflicts = extract_conflicts(clusters)
    if conflicts:
        print(f"\n  ⚠️  Konflikte/Warnungen: {len(conflicts)}")
        for cf in conflicts:
            print(f"    - {cf['int']}: {cf['beschreibung'][:50]}...")

    print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='SPÖ Portfolio Dashboard Sync')
    parser.add_argument('--dry-run', action='store_true', help='Nur prüfen, nicht schreiben')
    parser.add_argument('--stats', action='store_true', help='Statistiken anzeigen')
    args = parser.parse_args()

    # Register laden
    if not REGISTER_PATH.exists():
        print(f"❌ ANFRAGEN_REGISTER.yaml nicht gefunden: {REGISTER_PATH}")
        return 1

    register = load_yaml(REGISTER_PATH)

    # Cluster extrahieren
    clusters = extract_clusters_from_register(register)

    if not clusters:
        print("⚠️  Keine Cluster mit INTs gefunden im Register")
        return 0

    if args.stats:
        print_stats(clusters)
        return 0

    # Sync
    dashboard = sync_dashboard(clusters, dry_run=args.dry_run)

    agg = calculate_aggregations(clusters)

    if args.dry_run:
        print(f"\n🔍 DRY-RUN: Würde {agg['anzahl_cluster']} Cluster mit {agg['anzahl_massnahmen']} INTs synchronisieren")
        print_stats(clusters)
    else:
        print(f"\n✅ PORTFOLIO_DASHBOARD.yaml synchronisiert:")
        print(f"   → {agg['anzahl_cluster']} Cluster")
        print(f"   → {agg['anzahl_massnahmen']} Maßnahmen")
        print(f"   → Ø P(positiv): {agg['gewichteter_p_positiv']:.0%}")

    return 0


if __name__ == '__main__':
    exit(main())
