# Industry Templates

Pre-configured parameter sets for quick customer setup using `/new-customer --template <industry>`.

## Available Templates

| Template | File | Revenue Range | Key Characteristics |
|----------|------|---------------|---------------------|
| `manufacturing` | manufacturing.yaml | EUR 100M - 10B | High capex, global operations, B2B |
| `retail` | retail.yaml | EUR 50M - 50B | Low margin, inventory, B2C, omnichannel |
| `financial_services` | financial_services.yaml | EUR 500M - 50B | Regulated, IT-heavy, fee+interest income |

## Usage

```bash
# Create new customer with industry template
/new-customer "CompanyName" 1500 "Europe,APAC" --template manufacturing

# Template provides defaults for:
# - Financial benchmarks (margins, growth, capex)
# - Organizational structure (headcount distribution)
# - Regional patterns
# - Model parameters (CLV, CAC, Monte Carlo, Valuation)
# - ESG defaults
# - Risk profile
```

## Template Structure

Each template contains:

```yaml
industry:
  name: "Industry Name"
  sub_types: [...]

financial_benchmarks:
  revenue_growth_rate: 0.05
  ebitda_margin: 0.10
  ...

organizational_benchmarks:
  revenue_per_employee: 200000
  headcount_distribution: {...}
  ...

regional_defaults:
  regions: [...]

capex_defaults:
  categories: [...]

model_parameters:
  clv: {...}
  cac: {...}
  monte_carlo: {...}
  valuation: {...}

esg_defaults: {...}

risk_profile: {...}
```

## Adding New Templates

1. Copy an existing template
2. Adjust parameters for the new industry
3. Update this README
4. Test with `/new-customer --template <new_template>`

## Template Sources

- **Manufacturing**: Based on ALPLA, PORR, industry benchmarks
- **Retail**: Public retailer data, McKinsey retail reports
- **Financial Services**: ECB data, Basel requirements, bank filings

---

Version: 1.0.0 | Created: 2026-01-16
