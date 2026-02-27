#!/usr/bin/env python3
"""
BEATRIX Seed Manifest Generator
================================

Generiert und prueft SHA-256 Content Hashes fuer alle SSOT Seeds.

Zwei Modi:
  --local   Liest Dateien vom Dateisystem (Entwicklung, CI)
  --remote  Liest Dateien via GitHub API (Production, BEATRIX)

Usage:
    python scripts/generate_seed_manifest.py                    # Local: SSOT manifest
    python scripts/generate_seed_manifest.py --local --kb-seed  # Local: KB-Seed manifest
    python scripts/generate_seed_manifest.py --remote           # Remote: via GitHub API
    python scripts/generate_seed_manifest.py --check            # Pruefen ob Seeds aktuell
    python scripts/generate_seed_manifest.py --json             # JSON fuer API-Integration
"""

import os
import sys
import json
import hashlib
import argparse
import urllib.request
import base64
import ssl
from datetime import datetime, timezone
from pathlib import Path
import re

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = "FehrAdvice-Partners-AG/complementarity-context-framework"
REGISTRY_PATH = "data/beatrix/ssot-seed-registry.yaml"
MANIFEST_PATH_SSOT = "data/beatrix/seed-manifest.yaml"
MANIFEST_PATH_KB = "data/beatrix/kb-seed/seed-manifest.yaml"
KB_SEED_DIR = Path("data/beatrix/kb-seed")

# SSL context for GitHub API
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# =============================================================================
# SHARED UTILITIES
# =============================================================================

def compute_hash(content: bytes | str) -> str:
    """Compute SHA-256 hash of content."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


# =============================================================================
# LOCAL MODE — reads files from disk
# =============================================================================

def extract_kb_metadata(filepath: Path) -> dict:
    """Extract title and SSOT source from KB-Seed markdown."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.strip().split("\n")

    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    ssot_source = ""
    for line in lines:
        match = re.search(r"\*\*SSOT:\*\*\s*`([^`]+)`", line)
        if match:
            ssot_source = match.group(1)
            break

    tags = []
    for line in lines:
        match = re.search(r"\*\*Upload-Tags?:\*\*\s*(.+)", line)
        if match:
            tags = [t.strip() for t in match.group(1).split(",")]
            break

    return {
        "title": title,
        "ssot_source": ssot_source,
        "tags": tags,
        "word_count": len(text.split()),
    }


def generate_kb_manifest() -> dict:
    """Generate manifest for KB-Seed files (local)."""
    seeds = []
    for filepath in sorted(KB_SEED_DIR.glob("KB-*.md")):
        content = filepath.read_bytes()
        meta = extract_kb_metadata(filepath)
        seeds.append({
            "id": filepath.stem,
            "file": filepath.name,
            "content_hash": compute_hash(content),
            "title": meta["title"],
            "ssot_source": meta["ssot_source"],
            "tags": meta["tags"],
            "word_count": meta["word_count"],
        })

    return {
        "manifest_version": "1.0",
        "type": "kb-seed",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_seeds": len(seeds),
        "seeds": seeds,
    }


def generate_ssot_manifest_local() -> dict:
    """Generate manifest for SSOT files by reading registry + local files."""
    registry_path = Path(REGISTRY_PATH)
    if not registry_path.exists():
        print(f"❌ Registry not found: {REGISTRY_PATH}", file=sys.stderr)
        return {"manifest_version": "1.0", "type": "ssot", "seeds": []}

    # Parse registry YAML manually (no PyYAML dependency)
    seeds = []
    current = {}
    for line in registry_path.read_text().split("\n"):
        line = line.strip()
        if line.startswith("- path:"):
            if current:
                seeds.append(current)
            current = {"path": line.split('"')[1]}
        elif line.startswith("title:") and current:
            current["title"] = line.split('"')[1]
        elif line.startswith("tags:") and current:
            tags_str = line.split("[")[1].split("]")[0] if "[" in line else ""
            current["tags"] = [t.strip() for t in tags_str.split(",")]
    if current:
        seeds.append(current)

    manifest_seeds = []
    for seed in seeds:
        filepath = Path(seed["path"])
        if filepath.exists():
            content = filepath.read_bytes()
            manifest_seeds.append({
                "path": seed["path"],
                "title": seed.get("title", ""),
                "sha256": compute_hash(content),
                "size_bytes": len(content),
            })
        else:
            manifest_seeds.append({
                "path": seed["path"],
                "title": seed.get("title", ""),
                "sha256": "ERROR_FILE_NOT_FOUND",
                "size_bytes": 0,
            })

    return {
        "version": "1.0",
        "type": "ssot",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seeds": manifest_seeds,
    }


# =============================================================================
# REMOTE MODE — reads files via GitHub API
# =============================================================================

def fetch_github_file(path: str) -> str | None:
    """Fetch file content from GitHub."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "BEATRIX"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        data = json.loads(resp.read())
        return base64.b64decode(data.get("content", "")).decode("utf-8")
    except Exception as e:
        print(f"⚠️  Could not fetch {path}: {e}", file=sys.stderr)
        return None


def load_registry_remote() -> list:
    """Load seed registry from GitHub."""
    content = fetch_github_file(REGISTRY_PATH)
    if not content:
        return []
    # Simple YAML parse (same as local)
    seeds = []
    current = {}
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("- path:"):
            if current:
                seeds.append(current)
            current = {"path": line.split('"')[1]}
        elif line.startswith("title:") and current:
            current["title"] = line.split('"')[1]
        elif line.startswith("tags:") and current:
            tags_str = line.split("[")[1].split("]")[0] if "[" in line else ""
            current["tags"] = [t.strip() for t in tags_str.split(",")]
    if current:
        seeds.append(current)
    return seeds


def generate_ssot_manifest_remote() -> dict:
    """Generate manifest via GitHub API (production mode)."""
    seeds = load_registry_remote()
    if not seeds:
        print("❌ No seeds found in registry")
        return {"version": "1.0", "type": "ssot-remote", "seeds": []}

    manifest_seeds = []
    for seed in seeds:
        content = fetch_github_file(seed["path"])
        if content:
            manifest_seeds.append({
                "path": seed["path"],
                "title": seed.get("title", ""),
                "sha256": compute_hash(content),
                "size_bytes": len(content),
            })
        else:
            manifest_seeds.append({
                "path": seed["path"],
                "title": seed.get("title", ""),
                "sha256": "ERROR",
                "size_bytes": 0,
            })

    return {
        "version": "1.0",
        "type": "ssot-remote",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seeds": manifest_seeds,
    }


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def write_yaml_manifest(manifest: dict, output_path: str) -> None:
    """Write manifest as YAML (no PyYAML dependency)."""
    lines = []
    lines.append("# =============================================================================")
    lines.append("# BEATRIX SEED MANIFEST — AUTO-GENERATED")
    lines.append("# =============================================================================")
    lines.append(f"# Generated: {manifest.get('generated_at', manifest.get('generated', ''))}")
    lines.append("# Generator: python scripts/generate_seed_manifest.py")
    lines.append(f"# Type: {manifest.get('type', 'unknown')}")
    lines.append("#")
    lines.append("# HOW TO USE:")
    lines.append("#   1. BEATRIX stores content_hash at upload time")
    lines.append("#   2. Compare stored hash with manifest hash")
    lines.append("#   3. If hashes differ → seed is outdated → re-upload needed")
    lines.append("# =============================================================================")
    lines.append("")

    # Write top-level fields
    for key in ["version", "manifest_version", "type", "generated_at", "generated", "total_seeds"]:
        if key in manifest:
            lines.append(f'{key}: "{manifest[key]}"' if isinstance(manifest[key], str) else f"{key}: {manifest[key]}")
    lines.append("")
    lines.append("seeds:")

    for seed in manifest.get("seeds", []):
        if "id" in seed:
            # KB-Seed format
            lines.append(f'  - id: "{seed["id"]}"')
            lines.append(f'    file: "{seed["file"]}"')
            lines.append(f'    content_hash: "{seed["content_hash"]}"')
            lines.append(f'    title: "{seed["title"]}"')
            lines.append(f'    ssot_source: "{seed.get("ssot_source", "")}"')
            if seed.get("tags"):
                tags_str = ", ".join(f'"{t}"' for t in seed["tags"])
                lines.append(f"    tags: [{tags_str}]")
            else:
                lines.append("    tags: []")
            lines.append(f'    word_count: {seed.get("word_count", 0)}')
        else:
            # SSOT format
            lines.append(f'  - path: "{seed["path"]}"')
            lines.append(f'    title: "{seed["title"]}"')
            lines.append(f'    sha256: "{seed["sha256"]}"')
            lines.append(f'    size_bytes: {seed["size_bytes"]}')
        lines.append("")

    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ Manifest written: {output_path}")
    print(f"   {len(manifest.get('seeds', []))} seeds")


# =============================================================================
# CHECK MODE
# =============================================================================

def check_mode(manifest_path: str, manifest: dict) -> int:
    """Compare current hashes against existing manifest."""
    existing_path = Path(manifest_path)
    if not existing_path.exists():
        print(f"❌ No existing manifest at {manifest_path}. Generate first.")
        return 1

    # Parse existing hashes
    existing = {}
    current_key = None
    text = existing_path.read_text()
    for line in text.split("\n"):
        # KB-Seed format
        id_match = re.match(r'\s+- id: "(.+)"', line)
        hash_match = re.match(r'\s+content_hash: "(.+)"', line)
        # SSOT format
        path_match = re.match(r'\s+- path: "(.+)"', line)
        sha_match = re.match(r'\s+sha256: "(.+)"', line)

        if id_match:
            current_key = id_match.group(1)
        elif path_match:
            current_key = path_match.group(1)
        elif hash_match and current_key:
            existing[current_key] = hash_match.group(1)
            current_key = None
        elif sha_match and current_key:
            existing[current_key] = sha_match.group(1)
            current_key = None

    # Compare
    changed = []
    new_seeds = []
    up_to_date = []
    current_keys = {}

    for seed in manifest.get("seeds", []):
        key = seed.get("id") or seed.get("path")
        h = seed.get("content_hash") or seed.get("sha256")
        current_keys[key] = h

        if key not in existing:
            new_seeds.append(key)
        elif existing[key] != h:
            changed.append(key)
        else:
            up_to_date.append(key)

    removed = [k for k in existing if k not in current_keys]

    total = len(manifest.get("seeds", []))
    print(f"📊 Seed Version Check ({manifest.get('type', 'unknown')})")
    print(f"   Total: {total} seeds in SSOT\n")

    if up_to_date:
        print(f"✅ Up to date ({len(up_to_date)}):")
        for s in up_to_date:
            print(f"   {s}")
    if changed:
        print(f"\n⚠️  Changed — re-upload needed ({len(changed)}):")
        for s in changed:
            print(f"   {s}")
    if new_seeds:
        print(f"\n🆕 New — upload needed ({len(new_seeds)}):")
        for s in new_seeds:
            print(f"   {s}")
    if removed:
        print(f"\n🗑️  Removed from SSOT ({len(removed)}):")
        for s in removed:
            print(f"   {s}")
    if not changed and not new_seeds and not removed:
        print("\n✅ All seeds are up to date!")

    return 1 if changed or new_seeds else 0


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="BEATRIX Seed Manifest Generator",
        epilog="Examples:\n"
               "  %(prog)s                    # Local SSOT manifest\n"
               "  %(prog)s --kb-seed          # Local KB-Seed manifest\n"
               "  %(prog)s --remote           # Remote via GitHub API\n"
               "  %(prog)s --check            # Compare against existing\n"
               "  %(prog)s --check --kb-seed  # Check KB-Seeds\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--remote", action="store_true",
                        help="Fetch from GitHub API (requires GITHUB_TOKEN)")
    parser.add_argument("--kb-seed", action="store_true",
                        help="Generate manifest for KB-Seed files (kb-seed/KB-*.md)")
    parser.add_argument("--check", action="store_true",
                        help="Check if seeds are up to date vs existing manifest")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON (for API integration)")
    parser.add_argument("-o", "--output", help="Output file path (overrides default)")
    args = parser.parse_args()

    # Ensure we're in repo root
    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir.parent)

    # Determine mode and generate manifest
    if args.kb_seed:
        manifest = generate_kb_manifest()
        default_output = MANIFEST_PATH_KB
    elif args.remote:
        manifest = generate_ssot_manifest_remote()
        default_output = MANIFEST_PATH_SSOT
    else:
        manifest = generate_ssot_manifest_local()
        default_output = MANIFEST_PATH_SSOT

    output_path = args.output or default_output

    # Execute
    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0
    elif args.check:
        return check_mode(output_path, manifest)
    else:
        write_yaml_manifest(manifest, output_path)
        return 0


if __name__ == "__main__":
    sys.exit(main())
