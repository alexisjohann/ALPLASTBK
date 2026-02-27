# SSRN Paper Monitoring

This directory contains results from SSRN (Social Science Research Network) paper monitoring.

## Files

- `monitor-YYYY-MM-DD.yaml` - Researcher monitoring results
- `topic-*.yaml` - Topic search results

## Usage

### Via CLI Script
```bash
# All researchers
./scripts/check_ssrn.sh

# Specific researcher
./scripts/check_ssrn.sh --researcher RES-FEHR-E

# Topic search
./scripts/check_ssrn.sh --topic "behavioral economics"
./scripts/check_ssrn.sh --topic "loss aversion"
```

### Via GitHub Actions
Trigger manually at: https://github.com/FehrAdvice-Partners-AG/complementarity-context-framework/actions/workflows/ssrn-paper-monitor.yml

### Scheduled
Runs automatically every Monday at 08:00 UTC.

## API

Uses SerpAPI (Google Scholar with `site:ssrn.com` filter) for reliable search results.
