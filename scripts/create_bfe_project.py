#!/usr/bin/env python3
"""
BFE Project Creator - Erstellt BFE-Projekte mit 10C-basiertem Workflow

Usage:
    python scripts/create_bfe_project.py --interactive
    python scripts/create_bfe_project.py --schnell
    python scripts/create_bfe_project.py --name "Heizung" --who efh --what heat
    python scripts/create_bfe_project.py --list
    python scripts/create_bfe_project.py --status BFE-2026-001
    python scripts/create_bfe_project.py --close BFE-2026-001

Author: FehrAdvice & Partners AG
Version: 1.0
Date: 2026-01-23
"""

import argparse
import os
import sys
import yaml
import shutil
from datetime import datetime
from pathlib import Path

# Pfade
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
BFE_DIR = REPO_ROOT / "data" / "dr-datareq" / "sources" / "clients" / "bfe"
PROJECTS_DIR = BFE_DIR / "projects"
TEMPLATE_DIR = PROJECTS_DIR / "template"
MESO_FILE = REPO_ROOT / "data" / "dr-datareq" / "sources" / "industry" / "energy" / "BCM2_MESO_energy_ch.yaml"
MIKRO_FILE = BFE_DIR / "external" / "BCM2_MIKRO_BFE_context.yaml"
ENRICHMENTS_FILE = BFE_DIR / "learnings" / "BFE_context_enrichments.yaml"

# =============================================================================
# KONFIGURATION: Zielgruppen, Domains, Momente, Interventionen
# =============================================================================

TARGET_GROUPS = {
    "efh": {
        "id": "TG-HH-EFH",
        "name": "Eigentümer EFH",
        "size_estimate": "~1.1 Mio Haushalte",
        "decision_autonomy": "hoch",
        "key_barriers": ["Upfront-Kosten", "Komplexität", "Status Quo Bias"],
        "key_enablers": ["Förderung", "Nachbarschafts-Norm", "Wertsteigerung"]
    },
    "mfh": {
        "id": "TG-HH-MFH",
        "name": "Eigentümer MFH/Stockwerk",
        "size_estimate": "~0.5 Mio Haushalte",
        "decision_autonomy": "mittel",
        "key_barriers": ["Koordinationsproblem", "Heterogene Präferenzen"],
        "key_enablers": ["Facilitierte Prozesse", "Mehrheitsentscheid"]
    },
    "mieter": {
        "id": "TG-HH-MIETER",
        "name": "Mieter",
        "size_estimate": "~2.5 Mio Haushalte",
        "decision_autonomy": "niedrig",
        "key_barriers": ["Split Incentives", "Keine Investitionsmacht"],
        "key_enablers": ["Verbrauchs-Feedback", "Tarifwahl"]
    },
    "kmu": {
        "id": "TG-KMU",
        "name": "KMU",
        "size_estimate": "~600'000 Unternehmen",
        "decision_autonomy": "mittel bis hoch",
        "key_barriers": ["Kerngeschäft-Fokus", "Liquidität"],
        "key_enablers": ["Beratung", "Branchenlösungen"]
    },
    "industrie": {
        "id": "TG-GI",
        "name": "Grossindustrie",
        "size_estimate": "~1'500 Unternehmen",
        "decision_autonomy": "hoch",
        "key_barriers": ["Internationale Wettbewerbsfähigkeit"],
        "key_enablers": ["Zielvereinbarungen", "CO2-Rückerstattung"]
    },
    "kantone": {
        "id": "TG-KAN",
        "name": "Kantone",
        "role": "Implementierungspartner",
        "relevance": "Vollzug Gebäudevorschriften"
    },
    "gemeinden": {
        "id": "TG-GEM",
        "name": "Gemeinden",
        "role": "Multiplikator",
        "relevance": "Lokale Energieplanung"
    }
}

DOMAINS = {
    "heat": {
        "id": "DOM-HEAT",
        "name": "Heizungsersatz",
        "description": "Umstieg von fossil auf erneuerbar",
        "current_behavior": "Fossile Heizung weiter betreiben",
        "desired_behavior": "Wärmepumpe/Fernwärme installieren",
        "meso_factors": ["ENE-REG-06", "ENE-PSY-02", "ENE-SOC-04", "ENE-ECO-02"],
        "utility_mapping": {
            "u_F": "Kosteneinsparung langfristig",
            "u_E": "CO2-Reduktion",
            "u_P": "Komforterhalt",
            "u_S": "Norm-Konformität"
        }
    },
    "solar": {
        "id": "DOM-SOLAR",
        "name": "Solar-Adoption",
        "description": "Installation von PV-Anlagen",
        "current_behavior": "Kein Solar installiert",
        "desired_behavior": "PV-Anlage installieren",
        "meso_factors": ["ENE-REG-02", "ENE-SOC-01", "ENE-ECO-03", "ENE-PSY-03"],
        "utility_mapping": {
            "u_F": "Stromkostenreduktion",
            "u_E": "Erneuerbare Produktion",
            "u_S": "Sichtbares Commitment",
            "u_X": "Selbstversorgung"
        }
    },
    "mobility": {
        "id": "DOM-MOBILITY",
        "name": "Elektromobilität",
        "description": "Umstieg auf E-Fahrzeuge",
        "current_behavior": "Verbrenner fahren",
        "desired_behavior": "E-Auto kaufen/leasen",
        "meso_factors": ["ENE-SOC-02", "ENE-PSY-05", "ENE-REG-07"],
        "utility_mapping": {
            "u_F": "Tiefere Betriebskosten",
            "u_E": "Emissionsreduktion",
            "u_P": "Fahrerlebnis",
            "u_S": "Innovator-Image"
        }
    },
    "efficiency": {
        "id": "DOM-EFFICIENCY",
        "name": "Energieeffizienz",
        "description": "Reduktion Energieverbrauch",
        "current_behavior": "Gewohnter Verbrauch",
        "desired_behavior": "Bewusster/reduzierter Verbrauch",
        "meso_factors": ["ENE-PSY-01", "ENE-PSY-07", "ENE-PSY-08", "ENE-SOC-03"],
        "utility_mapping": {
            "u_F": "Kosteneinsparung",
            "u_E": "Ressourcenschonung",
            "u_P": "Komforterhalt"
        }
    }
}

CRITICAL_MOMENTS = {
    "defekt": {
        "name": "Heizungsdefekt",
        "window": "2-4 Wochen",
        "detection": "EVU-Meldung, Installateur-Netzwerk"
    },
    "hauskauf": {
        "name": "Hauskauf/-bau",
        "window": "3-6 Monate",
        "detection": "Grundbuch, Hypothekaranträge"
    },
    "renovation": {
        "name": "Renovation",
        "window": "2-3 Monate",
        "detection": "Baubewilligungen"
    },
    "tarif": {
        "name": "Tarifwechsel möglich",
        "window": "1-2 Monate",
        "detection": "EVU-Kalender"
    },
    "saison": {
        "name": "Saisonal",
        "window": "Herbst/Frühling",
        "detection": "Kalender-basiert"
    },
    "leben": {
        "name": "Lebensereignis",
        "window": "variabel",
        "detection": "Pensionierung, Erbschaft"
    }
}

# 10C Intervention Dimensions (emergent continuous space, NOT discrete types)
# Legacy T1-T8 notation is DEPRECATED - use I_AWARE, I_WHO, etc.
INTERVENTION_TYPES = {
    "I_AWARE": {"name": "Information", "target": "AWARE", "delta": "A(·)↑"},
    "I_AWARE_k": {"name": "Feedback", "target": "AWARE", "delta": "κ_AWX↑"},
    "I_WHEN": {"name": "Choice Architecture", "target": "WHEN", "delta": "κ_ARCH→"},
    "I_WHEN_t": {"name": "Timing/Deadlines", "target": "WHEN", "delta": "κ_JNY→"},
    "I_WHO": {"name": "Selbstkonzept", "target": "WHAT(X)", "delta": "W_base↑"},
    "I_WHO_o": {"name": "Social/Normen", "target": "WHAT(S)", "delta": "u_S↑"},
    "I_WHAT_F": {"name": "Financial", "target": "WHAT(F)", "delta": "u_F↑"},
    "I_HOW": {"name": "Pre-Commitment", "target": "HOW", "delta": "γ_ij→"}
}

# Crowding-Out Risiken (10C dimensions)
CROWDING_RISKS = [
    {"pair": ["I_WHO_o", "I_WHAT_F"], "gamma": -0.2, "warning": "Financial kann Social untergraben"},
    {"pair": ["I_WHAT_F", "I_HOW"], "gamma": -0.3, "warning": "Financial kann Intrinsic untergraben"}
]

# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def get_next_project_id():
    """Generiert die nächste Projekt-ID im Format BFE-YYYY-NNN"""
    year = datetime.now().year
    existing = list(PROJECTS_DIR.glob(f"{year}_*"))
    next_num = len(existing) + 1
    return f"BFE-{year}-{next_num:03d}"


def slugify(name):
    """Konvertiert Namen zu Slug für Ordnernamen"""
    return name.lower().replace(" ", "_").replace("-", "_").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")


def load_yaml(path):
    """Lädt YAML-Datei"""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(data, path):
    """Speichert YAML-Datei"""
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def print_header(title):
    """Druckt formatierte Überschrift"""
    print(f"\n{'━' * 50}")
    print(f"  {title}")
    print(f"{'━' * 50}\n")


def print_options(options, prompt):
    """Druckt nummerierte Optionen und fragt nach Auswahl"""
    print(f"\n{prompt}")
    for i, (key, opt) in enumerate(options.items(), 1):
        name = opt.get('name', key)
        desc = opt.get('description', opt.get('size_estimate', ''))
        if desc:
            print(f"  [{i}] {name} - {desc}")
        else:
            print(f"  [{i}] {name}")

    while True:
        try:
            choice = input("\n> ").strip()
            if choice.lower() == 'q':
                sys.exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return list(options.keys())[idx]
            print("Ungültige Auswahl. Bitte erneut versuchen.")
        except ValueError:
            # Check if user entered key directly
            if choice.lower() in options:
                return choice.lower()
            print("Bitte eine Zahl eingeben.")


def check_crowding_risks(interventions):
    """Prüft auf Crowding-Out Risiken"""
    warnings = []
    for risk in CROWDING_RISKS:
        if all(t in interventions for t in risk['pair']):
            warnings.append(f"⚠️  {risk['pair'][0]} + {risk['pair'][1]}: {risk['warning']} (γ = {risk['gamma']})")
    return warnings


# =============================================================================
# PROJEKT ERSTELLEN
# =============================================================================

def create_project_interactive(schnell=False):
    """Erstellt ein neues BFE-Projekt interaktiv"""

    print_header("BFE Projekt erstellen" + (" (Schnellmodus)" if schnell else ""))

    # Metadaten
    project_id = get_next_project_id()
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"Projekt-ID: {project_id}")
    print(f"Datum: {today}")

    # Projektname
    name = input("\nProjektname (kurz, beschreibend): ").strip()
    if not name:
        name = "Unnamed Project"

    description = input("Kurzbeschreibung (1-2 Sätze): ").strip()

    # WHO
    who_key = print_options(TARGET_GROUPS, "1️⃣  WHO: Wer ist die Zielgruppe?")
    who = TARGET_GROUPS[who_key]

    # WHAT
    what_key = print_options(DOMAINS, "2️⃣  WHAT: Welches Verhalten?")
    what = DOMAINS[what_key]

    # WHEN
    when_key = print_options(CRITICAL_MOMENTS, "3️⃣  WHEN: Kritischer Moment?")
    when = CRITICAL_MOMENTS[when_key]

    # WHERE (vereinfacht)
    print("\n4️⃣  WHERE: Default ändern?")
    print(f"   Aktuell: {what['current_behavior']}")
    print(f"   Neu: {what['desired_behavior']} als Standard")
    default_change = input("Default ändern? [j/n]: ").strip().lower() == 'j'

    # HOW - Interventions-Mix
    print("\n5️⃣  HOW: Interventions-Mix wählen")
    print("   Verfügbare Typen:")
    for key, t in INTERVENTION_TYPES.items():
        print(f"   {key}: {t['name']} ({t['target']} {t['delta']})")

    print("\n   Empfohlene Kombinationen:")
    print("   [1] I_WHEN + I_WHO_o + I_WHAT_F (Default + Social + Financial)")
    print("   [2] I_AWARE + I_WHEN (Information + Default)")
    print("   [3] I_AWARE + I_AWARE_k + I_WHO_o (Info + Feedback + Social)")
    print("   [4] Custom (kommasepariert, z.B. I_AWARE,I_WHEN,I_WHO_o)")

    mix_choice = input("\n> ").strip()

    if mix_choice == '1':
        interventions = ['I_WHEN', 'I_WHO_o', 'I_WHAT_F']
    elif mix_choice == '2':
        interventions = ['I_AWARE', 'I_WHEN']
    elif mix_choice == '3':
        interventions = ['I_AWARE', 'I_AWARE_k', 'I_WHO_o']
    else:
        interventions = [t.strip() for t in mix_choice.split(',')]

    # Crowding-Out Check
    warnings = check_crowding_risks(interventions)
    if warnings:
        print("\n⚠️  Crowding-Out Risiken erkannt:")
        for w in warnings:
            print(f"   {w}")
        proceed = input("\nTrotzdem fortfahren? [j/n]: ").strip().lower()
        if proceed != 'j':
            print("Abgebrochen. Bitte Interventions-Mix anpassen.")
            return None

    # Predictions (nur im vollständigen Modus)
    predictions = {}
    if not schnell:
        print("\n6️⃣  PREDICTIONS: Erwartete Ergebnisse")
        predictions['primary_metric'] = input("   Primäre Metrik (z.B. Anzahl Heizungsersatz): ").strip()
        predictions['baseline'] = input("   Baseline (aktueller Wert): ").strip()
        predictions['target'] = input("   Zielwert: ").strip()

    # Projekt-Ordner erstellen
    year = datetime.now().year
    folder_name = f"{year}_{slugify(name)}"
    project_dir = PROJECTS_DIR / folder_name

    if project_dir.exists():
        print(f"\n⚠️  Ordner existiert bereits: {project_dir}")
        overwrite = input("Überschreiben? [j/n]: ").strip().lower()
        if overwrite != 'j':
            return None
        shutil.rmtree(project_dir)

    # Template kopieren
    shutil.copytree(TEMPLATE_DIR, project_dir)

    # model.yaml ausfüllen
    model_path = project_dir / "model.yaml"
    model = load_yaml(model_path)

    # Metadaten
    model['metadata']['project_id'] = project_id
    model['metadata']['name'] = name
    model['metadata']['description'] = description
    model['metadata']['status'] = 'planning'
    model['metadata']['created'] = today
    model['metadata']['last_updated'] = today

    # WHO
    model['who']['primary_target'] = {
        'segment': who['name'],
        'size_estimate': who.get('size_estimate', ''),
        'decision_autonomy': who.get('decision_autonomy', ''),
        'key_barriers': who.get('key_barriers', []),
        'key_enablers': who.get('key_enablers', [])
    }

    # WHAT
    model['what']['target_behavior'] = {
        'current': what['current_behavior'],
        'desired': what['desired_behavior'],
        'domain': what['id']
    }
    model['what']['utility_dimensions'] = what['utility_mapping']

    # WHEN
    model['when']['critical_moments'] = [{
        'moment': when['name'],
        'opportunity_window': when['window'],
        'detection_mechanism': when['detection']
    }]

    # WHERE
    model['where']['choice_architecture'] = {
        'current_default': what['current_behavior'],
        'proposed_default': what['desired_behavior'] if default_change else what['current_behavior'],
        'default_changed': default_change
    }

    # HOW
    model['how']['intervention_mix'] = {
        'interventions': [{
            'type': t,
            'name': INTERVENTION_TYPES[t]['name'],
            'target': INTERVENTION_TYPES[t]['target'],
            'delta': INTERVENTION_TYPES[t]['delta']
        } for t in interventions if t in INTERVENTION_TYPES],
        'crowding_warnings': warnings
    }

    # Predictions
    if predictions:
        model['predictions'] = {
            'primary_outcome': {
                'metric': predictions.get('primary_metric', ''),
                'baseline': predictions.get('baseline', ''),
                'target': predictions.get('target', '')
            }
        }

    save_yaml(model, model_path)

    # context_subset.yaml ausfüllen
    context_path = project_dir / "context_subset.yaml"
    context = load_yaml(context_path)

    context['metadata']['project_id'] = project_id
    context['metadata']['project_name'] = name
    context['metadata']['created'] = today
    context['metadata']['last_updated'] = today

    # Auto-selektierte MESO-Faktoren
    context['meso_factors']['description'] = f"Auto-selektiert für Domain {what['id']}"
    context['meso_factors']['selected'] = what['meso_factors']

    save_yaml(context, context_path)

    # Erfolg
    print_header("Projekt erstellt!")
    print(f"📁 Pfad: {project_dir}")
    print(f"\nDateien:")
    print(f"  - model.yaml (10C-Modell ausgefüllt)")
    print(f"  - context_subset.yaml ({len(what['meso_factors'])} MESO-Faktoren selektiert)")
    print(f"  - learnings.yaml (Template)")

    print(f"\n📋 Nächste Schritte:")
    print(f"  1. model.yaml verfeinern (Details, Predictions)")
    print(f"  2. context_subset.yaml ergänzen (Hypothesen)")
    print(f"  3. Intervention implementieren")
    print(f"  4. /bfe-project close {project_id} nach Abschluss")

    return project_id


def list_projects():
    """Listet alle BFE-Projekte auf"""
    print_header("BFE Projekte")

    projects = [d for d in PROJECTS_DIR.iterdir() if d.is_dir() and d.name != 'template']

    if not projects:
        print("Keine Projekte gefunden.")
        return

    print(f"{'ID':<15} {'Name':<30} {'Status':<12} {'Erstellt'}")
    print("-" * 70)

    for p in sorted(projects):
        model_path = p / "model.yaml"
        if model_path.exists():
            model = load_yaml(model_path)
            meta = model.get('metadata', {})
            print(f"{meta.get('project_id', 'N/A'):<15} {meta.get('name', p.name):<30} {meta.get('status', 'unknown'):<12} {meta.get('created', 'N/A')}")
        else:
            print(f"{'N/A':<15} {p.name:<30} {'no model':<12}")


def show_status(project_id):
    """Zeigt Status eines Projekts"""
    # Find project by ID
    for p in PROJECTS_DIR.iterdir():
        if p.is_dir() and p.name != 'template':
            model_path = p / "model.yaml"
            if model_path.exists():
                model = load_yaml(model_path)
                if model.get('metadata', {}).get('project_id') == project_id:
                    print_header(f"Projekt: {project_id}")
                    meta = model['metadata']
                    print(f"Name: {meta.get('name')}")
                    print(f"Status: {meta.get('status')}")
                    print(f"Erstellt: {meta.get('created')}")
                    print(f"Zuletzt aktualisiert: {meta.get('last_updated')}")

                    who = model.get('who', {}).get('primary_target', {})
                    print(f"\nZielgruppe: {who.get('segment')}")

                    what = model.get('what', {}).get('target_behavior', {})
                    print(f"Domain: {what.get('domain')}")
                    print(f"Verhalten: {what.get('current')} → {what.get('desired')}")

                    how = model.get('how', {}).get('intervention_mix', {})
                    interventions = how.get('interventions', [])
                    print(f"\nInterventionen: {', '.join([i['type'] for i in interventions])}")

                    return

    print(f"Projekt {project_id} nicht gefunden.")


def close_project(project_id):
    """Schliesst ein Projekt ab und erfasst Learnings"""
    print_header(f"Projekt abschliessen: {project_id}")

    # Find project
    project_dir = None
    for p in PROJECTS_DIR.iterdir():
        if p.is_dir() and p.name != 'template':
            model_path = p / "model.yaml"
            if model_path.exists():
                model = load_yaml(model_path)
                if model.get('metadata', {}).get('project_id') == project_id:
                    project_dir = p
                    break

    if not project_dir:
        print(f"Projekt {project_id} nicht gefunden.")
        return

    model_path = project_dir / "model.yaml"
    learnings_path = project_dir / "learnings.yaml"

    model = load_yaml(model_path)
    learnings = load_yaml(learnings_path)

    # Status aktualisieren
    model['metadata']['status'] = 'completed'
    model['metadata']['last_updated'] = datetime.now().strftime("%Y-%m-%d")

    # Learnings erfassen
    learnings['metadata']['project_id'] = project_id
    learnings['metadata']['project_name'] = model['metadata']['name']
    learnings['metadata']['completion_date'] = datetime.now().strftime("%Y-%m-%d")
    learnings['metadata']['status'] = 'completed'

    print("\n📊 Ergebnisse erfassen:")

    predictions = model.get('predictions', {}).get('primary_outcome', {})
    if predictions.get('metric'):
        print(f"\nPrimäre Metrik: {predictions.get('metric')}")
        print(f"Vorhergesagt: {predictions.get('target')}")
        actual = input("Tatsächlicher Wert: ").strip()

        learnings['results_vs_predictions'] = {
            'primary_outcome': {
                'metric': predictions.get('metric'),
                'predicted': predictions.get('target'),
                'actual': actual
            }
        }

    # Key Learnings
    print("\n📝 Key Learnings (Enter für fertig):")
    key_learnings = []
    i = 1
    while True:
        learning = input(f"  Learning {i}: ").strip()
        if not learning:
            break
        key_learnings.append(learning)
        i += 1

    learnings['summary'] = {'key_learnings': key_learnings}

    # Neue Faktoren?
    print("\n🔍 Neue Kontextfaktoren entdeckt?")
    new_factor = input("Neuen Faktor erfassen? [j/n]: ").strip().lower()
    if new_factor == 'j':
        factor_name = input("  Faktor-Name: ").strip()
        factor_def = input("  Definition: ").strip()
        factor_value = input("  Beobachteter Wert (0-1): ").strip()

        learnings['context_updates'] = {
            'new_factors_meso': [{
                'factor': {
                    'name': factor_name,
                    'definition': factor_def,
                    'salienz': float(factor_value) if factor_value else None
                },
                'evidence': {'source': project_id},
                'propagation_status': 'pending'
            }]
        }

    # Speichern
    save_yaml(model, model_path)
    save_yaml(learnings, learnings_path)

    print_header("Projekt abgeschlossen!")
    print(f"✅ Status: completed")
    print(f"📁 Learnings: {learnings_path}")

    print("\n📋 Nächste Schritte:")
    print("  1. Learnings in BFE_context_enrichments.yaml aggregieren")
    print("  2. Review durch Senior Consultant")
    print("  3. Propagation in MESO/MAKRO")


# =============================================================================
# MAIN
# =============================================================================

def create_project_batch(name, who_key, what_key, when_key, default_change, interventions, description=""):
    """Erstellt ein Projekt nicht-interaktiv mit allen Parametern"""

    print_header(f"BFE Projekt erstellen: {name}")

    project_id = get_next_project_id()
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"Projekt-ID: {project_id}")
    print(f"Datum: {today}")

    # Validierung
    if who_key not in TARGET_GROUPS:
        print(f"Fehler: Unbekannte Zielgruppe '{who_key}'")
        print(f"Verfügbar: {', '.join(TARGET_GROUPS.keys())}")
        return None

    if what_key not in DOMAINS:
        print(f"Fehler: Unbekannte Domain '{what_key}'")
        print(f"Verfügbar: {', '.join(DOMAINS.keys())}")
        return None

    if when_key not in CRITICAL_MOMENTS:
        print(f"Fehler: Unbekannter Moment '{when_key}'")
        print(f"Verfügbar: {', '.join(CRITICAL_MOMENTS.keys())}")
        return None

    who = TARGET_GROUPS[who_key]
    what = DOMAINS[what_key]
    when = CRITICAL_MOMENTS[when_key]

    # Interventionen parsen
    if isinstance(interventions, str):
        interventions = [t.strip().upper() for t in interventions.split(',')]

    # Crowding-Out Check
    warnings = check_crowding_risks(interventions)
    if warnings:
        print("\n⚠️  Crowding-Out Risiken erkannt:")
        for w in warnings:
            print(f"   {w}")

    # Projekt-Ordner erstellen
    year = datetime.now().year
    folder_name = f"{year}_{slugify(name)}"
    project_dir = PROJECTS_DIR / folder_name

    if project_dir.exists():
        print(f"\n⚠️  Ordner existiert bereits, wird überschrieben: {project_dir}")
        shutil.rmtree(project_dir)

    # Template kopieren
    shutil.copytree(TEMPLATE_DIR, project_dir)

    # model.yaml ausfüllen
    model_path = project_dir / "model.yaml"
    model = load_yaml(model_path)

    # Metadaten
    model['metadata']['project_id'] = project_id
    model['metadata']['name'] = name
    model['metadata']['description'] = description or f"BFE Projekt: {what['name']} für {who['name']}"
    model['metadata']['status'] = 'planning'
    model['metadata']['created'] = today
    model['metadata']['last_updated'] = today

    # WHO
    model['who']['primary_target'] = {
        'segment': who['name'],
        'size_estimate': who.get('size_estimate', ''),
        'decision_autonomy': who.get('decision_autonomy', ''),
        'key_barriers': who.get('key_barriers', []),
        'key_enablers': who.get('key_enablers', [])
    }

    # WHAT
    model['what']['target_behavior'] = {
        'current': what['current_behavior'],
        'desired': what['desired_behavior'],
        'domain': what['id']
    }
    model['what']['utility_dimensions'] = what['utility_mapping']

    # WHEN
    model['when']['critical_moments'] = [{
        'moment': when['name'],
        'opportunity_window': when['window'],
        'detection_mechanism': when['detection']
    }]

    # WHERE
    model['where']['choice_architecture'] = {
        'current_default': what['current_behavior'],
        'proposed_default': what['desired_behavior'] if default_change else what['current_behavior'],
        'default_changed': default_change
    }

    # HOW
    model['how']['intervention_mix'] = {
        'interventions': [{
            'type': t,
            'name': INTERVENTION_TYPES[t]['name'],
            'target': INTERVENTION_TYPES[t]['target'],
            'delta': INTERVENTION_TYPES[t]['delta']
        } for t in interventions if t in INTERVENTION_TYPES],
        'crowding_warnings': warnings
    }

    save_yaml(model, model_path)

    # context_subset.yaml ausfüllen
    context_path = project_dir / "context_subset.yaml"
    context = load_yaml(context_path)

    context['metadata']['project_id'] = project_id
    context['metadata']['project_name'] = name
    context['metadata']['created'] = today
    context['metadata']['last_updated'] = today

    # Auto-selektierte MESO-Faktoren
    context['meso_factors']['description'] = f"Auto-selektiert für Domain {what['id']}"
    context['meso_factors']['selected'] = what['meso_factors']

    save_yaml(context, context_path)

    # Erfolg
    print_header("Projekt erstellt!")
    print(f"📁 Pfad: {project_dir}")
    print(f"\n📋 Konfiguration:")
    print(f"   WHO:  {who['name']}")
    print(f"   WHAT: {what['name']} ({what['id']})")
    print(f"   WHEN: {when['name']}")
    print(f"   WHERE: Default {'geändert' if default_change else 'beibehalten'}")
    print(f"   HOW:  {', '.join(interventions)}")
    print(f"\n📊 MESO-Faktoren: {', '.join(what['meso_factors'])}")
    print(f"\nDateien:")
    print(f"  - model.yaml (10C-Modell ausgefüllt)")
    print(f"  - context_subset.yaml ({len(what['meso_factors'])} MESO-Faktoren)")
    print(f"  - learnings.yaml (Template)")

    return project_id


def main():
    parser = argparse.ArgumentParser(
        description="BFE Project Creator - Erstellt und verwaltet BFE-Projekte",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Interaktiv
  python scripts/create_bfe_project.py --interactive
  python scripts/create_bfe_project.py --schnell

  # Batch-Modus (nicht-interaktiv)
  python scripts/create_bfe_project.py --name "Heizung_Pilot" --who efh --what heat --when defekt --how T3,T6,T7

  # Verwaltung
  python scripts/create_bfe_project.py --list
  python scripts/create_bfe_project.py --status BFE-2026-001
  python scripts/create_bfe_project.py --close BFE-2026-001

Zielgruppen (--who):
  efh, mfh, mieter, kmu, industrie, kantone, gemeinden

Domains (--what):
  heat, solar, mobility, efficiency

Momente (--when):
  defekt, hauskauf, renovation, tarif, saison, leben

Interventionen (--how):
  T1 (Info), T2 (Feedback), T3 (Default), T4 (Timing),
  T5 (Selbstkonzept), T6 (Social), T7 (Financial), T8 (Commitment)
        """
    )

    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Neues Projekt interaktiv erstellen (vollständig)')
    parser.add_argument('--schnell', '-s', action='store_true',
                        help='Neues Projekt im Schnellmodus erstellen')
    parser.add_argument('--list', '-l', action='store_true',
                        help='Alle Projekte auflisten')
    parser.add_argument('--status', metavar='ID',
                        help='Status eines Projekts anzeigen')
    parser.add_argument('--close', metavar='ID',
                        help='Projekt abschliessen')

    # Batch-Modus Parameter
    parser.add_argument('--name', metavar='NAME',
                        help='Projektname')
    parser.add_argument('--who', choices=list(TARGET_GROUPS.keys()),
                        help='Zielgruppe')
    parser.add_argument('--what', choices=list(DOMAINS.keys()),
                        help='Interventionsfeld')
    parser.add_argument('--when', choices=list(CRITICAL_MOMENTS.keys()),
                        help='Kritischer Moment')
    parser.add_argument('--default', action='store_true', default=True,
                        help='Default ändern (Standard: ja)')
    parser.add_argument('--no-default', action='store_true',
                        help='Default NICHT ändern')
    parser.add_argument('--how', metavar='T1,T2,...',
                        help='Interventions-Mix (kommasepariert)')
    parser.add_argument('--description', metavar='TEXT',
                        help='Projektbeschreibung')

    args = parser.parse_args()

    # Keine Argumente = interaktiv
    if len(sys.argv) == 1:
        args.interactive = True

    if args.list:
        list_projects()
    elif args.status:
        show_status(args.status)
    elif args.close:
        close_project(args.close)
    elif args.interactive or args.schnell:
        create_project_interactive(schnell=args.schnell)
    elif args.name and args.who and args.what and args.when and args.how:
        # Batch-Modus
        default_change = not args.no_default
        create_project_batch(
            name=args.name,
            who_key=args.who,
            what_key=args.what,
            when_key=args.when,
            default_change=default_change,
            interventions=args.how,
            description=args.description or ""
        )
    else:
        parser.print_help()
        print("\n⚠️  Für Batch-Modus: --name, --who, --what, --when, --how erforderlich")


if __name__ == "__main__":
    main()
