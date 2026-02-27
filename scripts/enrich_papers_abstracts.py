#!/usr/bin/env python3
"""
Enrich BibTeX entries with abstracts from OpenAlex API.

Reads BibTeX entries from a file, fetches abstracts via DOI lookup on OpenAlex,
and writes enriched entries back. Papers without DOIs are skipped.

Usage:
    python scripts/enrich_papers_abstracts.py --input new_papers_bibtex.bib
    python scripts/enrich_papers_abstracts.py --input new_papers_bibtex.bib --update-master
    python scripts/enrich_papers_abstracts.py --input new_papers_bibtex.bib --batch 50 --dry-run
    python scripts/enrich_papers_abstracts.py --input new_papers_bibtex.bib --experimental

Rate Limits & Time Estimation:
    OpenAlex:   ~10 req/sec polite pool (with mailto: header). We use 0.12s delay.
    Formula:    T = N_to_fetch * delay_s + overhead_s
    Registry:   data/api-registry.yaml (API-BIB-002)
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse


def parse_bibtex_entries(filepath):
    """Parse BibTeX file into list of (key, entry_text, doi) tuples."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    # Match @type{key, ... }
    pattern = r'(@\w+\{[^,]+,.*?\n\})'
    raw_entries = re.findall(pattern, content, re.DOTALL)

    for entry_text in raw_entries:
        # Extract key
        key_match = re.match(r'@\w+\{([^,]+),', entry_text)
        key = key_match.group(1).strip() if key_match else "unknown"

        # Extract DOI
        doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry_text)
        doi = doi_match.group(1).strip() if doi_match else None

        # Check if abstract already exists
        has_abstract = bool(re.search(r'abstract\s*=\s*\{', entry_text))

        entries.append({
            "key": key,
            "text": entry_text,
            "doi": doi,
            "has_abstract": has_abstract,
        })

    return entries


def reconstruct_abstract(inverted_index):
    """Reconstruct abstract text from OpenAlex inverted index format."""
    if not inverted_index:
        return None

    # Build word-position mapping
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))

    # Sort by position and join
    word_positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in word_positions)


def fetch_abstract_openalex(doi, retries=2):
    """Fetch abstract from OpenAlex for a given DOI."""
    encoded_doi = urllib.parse.quote(doi, safe="")
    url = f"https://api.openalex.org/works/doi:{encoded_doi}?select=abstract_inverted_index,title"

    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "EBF-Framework/1.0 (mailto:research@fehradvice.com)")

            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            inverted_index = data.get("abstract_inverted_index")
            if inverted_index:
                return reconstruct_abstract(inverted_index)
            return None

        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Rate limited - wait and retry
                wait = 2 ** (attempt + 1)
                print(f"    Rate limited, waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            elif e.code == 404:
                return None
            else:
                if attempt < retries:
                    time.sleep(1)
                    continue
                return None
        except Exception:
            if attempt < retries:
                time.sleep(1)
                continue
            return None

    return None


def sanitize_abstract(text):
    """Clean abstract text for BibTeX inclusion."""
    if not text:
        return None
    # Remove/escape problematic characters for BibTeX
    text = text.replace("{", "\\{").replace("}", "\\}")
    text = text.replace("&", "\\&")
    text = text.replace("%", "\\%")
    text = text.replace("$", "\\$")
    text = text.replace("#", "\\#")
    text = text.replace("_", "\\_")
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def add_abstract_to_entry(entry_text, abstract):
    """Insert abstract field into BibTeX entry before the closing brace."""
    # Find the last line before closing }
    lines = entry_text.rstrip().split("\n")

    # Find position to insert (before closing brace, after last field)
    insert_idx = len(lines) - 1  # Before the }

    # Wrap abstract at ~80 chars for readability
    wrapped = []
    words = abstract.split()
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > 76:
            wrapped.append(current_line)
            current_line = word
        else:
            current_line = f"{current_line} {word}" if current_line else word
    if current_line:
        wrapped.append(current_line)

    abstract_field = "  abstract = {" + wrapped[0]
    for line in wrapped[1:]:
        abstract_field += "\n    " + line
    abstract_field += "},"

    lines.insert(insert_idx, abstract_field)
    return "\n".join(lines)


##############################################################################
# EXPERIMENTAL MODE: Geometric Scaling (1 → 10 → 100 → all)
##############################################################################

DEFAULT_STAGES = [1, 10, 100, 0]  # 0 = all remaining


def compute_enrichment_metrics(entries_batch, enriched_keys):
    """Compute quality metrics for a batch of enrichment attempts."""
    n = max(len(entries_batch), 1)
    with_doi = sum(1 for e in entries_batch if e.get("doi"))
    already_had = sum(1 for e in entries_batch if e.get("has_abstract"))
    newly_enriched = sum(1 for e in entries_batch
                         if e["key"] in enriched_keys)
    total_with_abstract = already_had + newly_enriched

    return {
        "total": len(entries_batch),
        "with_doi": with_doi,
        "with_doi_pct": with_doi / n * 100,
        "already_had_abstract": already_had,
        "newly_enriched": newly_enriched,
        "enrichment_rate": newly_enriched / max(with_doi - already_had, 1) * 100,
        "total_abstract_pct": total_with_abstract / n * 100,
    }


def check_enrichment_gates(metrics, prev_metrics=None):
    """Check quality gates for enrichment. Return list of problems."""
    problems = []

    # Gate 1: Enrichment rate should be > 20% (OpenAlex usually has ~60-70%)
    if metrics["total"] >= 5 and metrics["enrichment_rate"] < 20:
        problems.append(
            f"LOW ENRICHMENT: {metrics['enrichment_rate']:.0f}% (expect >20%)")

    # Gate 2: If enrichment rate drops significantly between stages
    if prev_metrics and prev_metrics["enrichment_rate"] > 0:
        drop = prev_metrics["enrichment_rate"] - metrics["enrichment_rate"]
        if drop > 25:
            problems.append(
                f"ENRICHMENT DROP: {prev_metrics['enrichment_rate']:.0f}%"
                f" → {metrics['enrichment_rate']:.0f}% (-{drop:.0f}pp)")

    return problems


def print_enrichment_stage_report(stage_num, metrics, elapsed, problems):
    """Print quality report for one enrichment stage."""
    w = 56

    def row(text):
        text = text[:w]
        print(f"  │  {text}{' ' * (w - len(text))}│")

    print()
    print(f"  ┌{'─' * (w + 2)}┐")
    row(f"STAGE {stage_num}: {metrics['total']} entries ({elapsed:.1f}s)")
    print(f"  ├{'─' * (w + 2)}┤")
    row(f"With DOI:       {metrics['with_doi']:>4}/{metrics['total']}"
        f"  ({metrics['with_doi_pct']:>5.1f}%)")
    row(f"Already had:    {metrics['already_had_abstract']:>4}")
    row(f"Newly enriched: {metrics['newly_enriched']:>4}"
        f"  ({metrics['enrichment_rate']:>5.1f}%)")
    row(f"Total abstract: {metrics['total_abstract_pct']:>5.1f}%")

    if problems:
        print(f"  ├{'─' * (w + 2)}┤")
        for p in problems:
            row(f"⚠ {p}")

    print(f"  └{'─' * (w + 2)}┘")


def run_experimental_enrichment(entries, stages, args):
    """Run enrichment in geometric stages with quality gates.

    Returns (enriched_map, stage_reports).
    """
    enriched_map = {}
    stage_reports = []
    prev_metrics = None
    processed = 0
    stopped_early = False

    print(f"\n{'=' * 60}")
    print(f"  EXPERIMENTAL MODE: {len(stages)} stages")
    print(f"  Stages: {' → '.join(str(s) if s > 0 else 'ALL' for s in stages)}")
    print(f"  Total entries: {len(entries)}")
    print(f"{'=' * 60}")

    for stage_idx, stage_size in enumerate(stages):
        stage_num = stage_idx + 1

        if stage_size == 0:
            batch = entries[processed:]
        else:
            end = min(processed + stage_size, len(entries))
            batch = entries[processed:end]

        if not batch:
            print(f"\n  Stage {stage_num}: No entries remaining. Done.")
            break

        print(f"\n  Stage {stage_num}: Processing {len(batch)} entries"
              f" (of {len(entries)} total)...")

        t_start = time.time()
        stage_enriched = {}

        for i, entry in enumerate(batch):
            doi = entry.get("doi")
            key = entry["key"]

            if not doi or entry.get("has_abstract"):
                continue

            abstract_raw = fetch_abstract_openalex(doi)
            if abstract_raw:
                abstract = sanitize_abstract(abstract_raw)
                if abstract and len(abstract) > 20:
                    stage_enriched[key] = abstract
                    enriched_map[key] = abstract

            time.sleep(args.delay)

        elapsed = time.time() - t_start
        metrics = compute_enrichment_metrics(batch, stage_enriched)
        problems = check_enrichment_gates(metrics, prev_metrics)

        print_enrichment_stage_report(stage_num, metrics, elapsed, problems)

        stage_reports.append({
            "stage": stage_num,
            "batch_size": len(batch),
            "newly_enriched": len(stage_enriched),
            "metrics": metrics,
            "problems": problems,
            "elapsed_s": elapsed,
        })

        processed += len(batch)
        prev_metrics = metrics

        # Quality gate: stop on critical problems
        critical = [p for p in problems
                    if "LOW ENRICHMENT" in p or "DROP" in p]
        if critical and stage_size != 0:
            print(f"\n  ⚠ QUALITY GATE: Stopping after stage {stage_num}.")
            print(f"    Problems: {'; '.join(critical)}")
            print(f"    Fix issues before running next stage.")
            stopped_early = True
            break

    # Final summary
    print(f"\n{'=' * 60}")
    print(f"  EXPERIMENTAL ENRICHMENT SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Stages completed:  {len(stage_reports)}"
          f"{'  (STOPPED EARLY)' if stopped_early else ''}")
    print(f"  Entries processed: {processed}/{len(entries)}")
    print(f"  Abstracts added:   {len(enriched_map)}")
    total_time = sum(r["elapsed_s"] for r in stage_reports)
    print(f"  Total time:        {total_time:.1f}s")
    if enriched_map:
        rate = len(enriched_map) / max(processed, 1) * 100
        print(f"  Overall rate:      {rate:.0f}%")
    print(f"{'=' * 60}")

    return enriched_map, stage_reports


def main():
    parser = argparse.ArgumentParser(description="Enrich BibTeX with OpenAlex abstracts")
    parser.add_argument("--input", required=True, help="Input BibTeX file")
    parser.add_argument("--output", help="Output BibTeX file (default: overwrite input)")
    parser.add_argument("--update-master", action="store_true",
                        help="Also update bibliography/bcm_master.bib")
    parser.add_argument("--batch", type=int, default=0,
                        help="Process only N entries (0 = all)")
    parser.add_argument("--delay", type=float, default=0.12,
                        help="Delay between API calls in seconds (default: 0.12)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report only, don't write files")
    parser.add_argument("--experimental", action="store_true",
                        help="Run in experimental mode: 1 → 10 → 100 → all with quality gates")
    parser.add_argument("--stages", type=str, default=None,
                        help="Custom stages (comma-separated, 0=all). Default: 1,10,100,0")
    args = parser.parse_args()

    output_file = args.output or args.input

    print(f"=== OpenAlex Abstract Enrichment ===")
    print(f"Input: {args.input}")
    print(f"Output: {output_file}")

    # Parse entries
    entries = parse_bibtex_entries(args.input)
    print(f"Total entries: {len(entries)}")

    # Filter: need DOI and no abstract yet
    to_fetch = [e for e in entries if e["doi"] and not e["has_abstract"]]
    no_doi = [e for e in entries if not e["doi"]]
    already_has = [e for e in entries if e["has_abstract"]]

    print(f"With DOI, no abstract: {len(to_fetch)}")
    print(f"Without DOI (skipped): {len(no_doi)}")
    print(f"Already have abstract: {len(already_has)}")

    # =========================================================================
    # EXPERIMENTAL MODE: Route through staged pipeline
    # =========================================================================
    if args.experimental:
        if args.stages:
            stages = [int(s.strip()) for s in args.stages.split(",")]
        else:
            stages = list(DEFAULT_STAGES)

        enriched_map, stage_reports = run_experimental_enrichment(
            entries=to_fetch, stages=stages, args=args,
        )

        if enriched_map and not args.dry_run:
            # Write enriched entries
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()

            for key, abstract in enriched_map.items():
                pattern = rf'(@\w+\{{{re.escape(key)},.*?\n\}})'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    old_entry = match.group(1)
                    new_entry = add_abstract_to_entry(old_entry, abstract)
                    content = content.replace(old_entry, new_entry, 1)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n  Written: {output_file} ({len(enriched_map)} abstracts added)")

            if args.update_master:
                master_path = "bibliography/bcm_master.bib"
                try:
                    with open(master_path, "r", encoding="utf-8") as f:
                        master_content = f.read()
                    updated = 0
                    for key, abstract in enriched_map.items():
                        pattern = rf'(@\w+\{{{re.escape(key)},.*?\n\}})'
                        match = re.search(pattern, master_content, re.DOTALL)
                        if match:
                            old_entry = match.group(1)
                            if "abstract = {" not in old_entry:
                                new_entry = add_abstract_to_entry(old_entry, abstract)
                                master_content = master_content.replace(old_entry, new_entry, 1)
                                updated += 1
                    with open(master_path, "w", encoding="utf-8") as f:
                        f.write(master_content)
                    print(f"  Updated: {master_path} ({updated} abstracts added)")
                except FileNotFoundError:
                    print(f"  WARNING: {master_path} not found")

        # Write summary
        summary = {
            "mode": "experimental",
            "total_entries": len(entries),
            "to_fetch": len(to_fetch),
            "abstracts_found": len(enriched_map),
            "stages_completed": len(stage_reports),
            "stages": [
                {
                    "stage": r["stage"],
                    "batch": r["batch_size"],
                    "enriched": r["newly_enriched"],
                    "rate": f"{r['metrics']['enrichment_rate']:.0f}%",
                    "time_s": f"{r['elapsed_s']:.1f}",
                    "problems": r["problems"],
                }
                for r in stage_reports
            ],
        }
        with open("enrichment_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        return

    # =========================================================================
    # TRADITIONAL MODE: Process all at once (original behavior)
    # =========================================================================

    if args.batch > 0:
        to_fetch = to_fetch[:args.batch]
        print(f"Batch limit: processing {len(to_fetch)}")

    if args.dry_run:
        print("\n[DRY RUN] Would fetch abstracts for:")
        for e in to_fetch[:10]:
            print(f"  - {e['key']}: {e['doi']}")
        if len(to_fetch) > 10:
            print(f"  ... and {len(to_fetch) - 10} more")
        return

    # Fetch abstracts
    success = 0
    failed = 0
    no_abstract = 0
    enriched_map = {}  # key -> abstract

    print(f"\nFetching abstracts from OpenAlex...")
    for i, entry in enumerate(to_fetch):
        doi = entry["doi"]
        key = entry["key"]

        if (i + 1) % 25 == 0 or i == 0:
            print(f"  [{i+1}/{len(to_fetch)}] Processing {key}...", file=sys.stderr)

        abstract_raw = fetch_abstract_openalex(doi)
        if abstract_raw:
            abstract = sanitize_abstract(abstract_raw)
            if abstract and len(abstract) > 20:
                enriched_map[key] = abstract
                success += 1
            else:
                no_abstract += 1
        else:
            no_abstract += 1

        # Rate limiting: OpenAlex allows ~10 req/sec for polite pool
        time.sleep(args.delay)

    failed = len(to_fetch) - success - no_abstract

    print(f"\n=== RESULTS ===")
    print(f"Abstracts found:     {success}")
    print(f"No abstract on OA:   {no_abstract}")
    print(f"Errors:              {failed}")

    if success == 0:
        print("No abstracts to add.")
        return

    # Write enriched file
    print(f"\nWriting enriched entries to {output_file}...")
    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    for key, abstract in enriched_map.items():
        # Find the entry in content and add abstract
        # Match the specific entry by key
        pattern = rf'(@\w+\{{{re.escape(key)},.*?\n\}})'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            old_entry = match.group(1)
            new_entry = add_abstract_to_entry(old_entry, abstract)
            content = content.replace(old_entry, new_entry, 1)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Written: {output_file} ({success} abstracts added)")

    # Also update master bib if requested
    if args.update_master:
        master_path = "bibliography/bcm_master.bib"
        print(f"\nUpdating {master_path}...")
        try:
            with open(master_path, "r", encoding="utf-8") as f:
                master_content = f.read()

            updated = 0
            for key, abstract in enriched_map.items():
                pattern = rf'(@\w+\{{{re.escape(key)},.*?\n\}})'
                match = re.search(pattern, master_content, re.DOTALL)
                if match:
                    old_entry = match.group(1)
                    if "abstract = {" not in old_entry:
                        new_entry = add_abstract_to_entry(old_entry, abstract)
                        master_content = master_content.replace(old_entry, new_entry, 1)
                        updated += 1

            with open(master_path, "w", encoding="utf-8") as f:
                f.write(master_content)

            print(f"  Updated: {master_path} ({updated} abstracts added)")
        except FileNotFoundError:
            print(f"  WARNING: {master_path} not found")

    # Write summary
    summary = {
        "total_entries": len(entries),
        "with_doi": len(entries) - len(no_doi),
        "without_doi": len(no_doi),
        "already_had_abstract": len(already_has),
        "attempted": len(to_fetch),
        "abstracts_found": success,
        "no_abstract_available": no_abstract,
        "errors": failed,
        "enrichment_rate": f"{success/len(to_fetch)*100:.1f}%" if to_fetch else "0%",
    }

    with open("enrichment_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSummary written to enrichment_summary.json")
    print(f"Enrichment rate: {summary['enrichment_rate']}")


if __name__ == "__main__":
    main()
