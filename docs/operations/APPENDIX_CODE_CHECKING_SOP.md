# Appendix Code Availability Checking - SOP

**Standard Operating Procedure for Assigning New Appendix Codes**

## CRITICAL RULE

❌ **NEVER create a new appendix without first checking code availability!**

## How to Check

### Quick Check (Recommended)

```bash
python scripts/check_appendix_available.py BD
```

Output:
- ✅ **Code BD is AVAILABLE** → You can use it
- ❌ **Code BD is ALREADY IN USE** → Use suggested code instead

### View All Used Codes

```bash
python scripts/check_appendix_available.py --status
```

Shows:
- Total codes in use
- List of all codes
- Next available code

### Get Suggestion

```bash
python scripts/check_appendix_available.py --suggest
```

Returns the next available code (e.g., `BF`)

## Workflow: Creating a New Appendix

1. **FIRST: Check availability**
   ```bash
   python scripts/check_appendix_available.py <YOUR_CODE>
   ```

2. **IF AVAILABLE** (✅ shown)
   - Create file: `appendices/<CODE>_descriptive_name.tex`
   - Use label: `\label{app:lit-<code>}` (lowercase)
   - Add to index: `appendices/00_appendix_index.tex`

3. **IF IN USE** (❌ shown)
   - Use the suggested code instead
   - OR run `--suggest` to find next available

## Common Codes to Avoid

✅ Single letters A-Z: Most are taken. Last available: Y, Z

✅ Range AA-AZ: All are taken (except few)

✅ Range BA-BC: Taken

✅ Range BD-BZ: **CURRENTLY AVAILABLE** (recommended for new appendices)

## Example Workflow

```bash
# User wants to create new LIT-ALESINA appendix
$ python scripts/check_appendix_available.py AH
❌ Code AH is ALREADY IN USE

# Script suggests:
Use this instead: BF

# User checks BF
$ python scripts/check_appendix_available.py BF
✅ Code BF is AVAILABLE ✓

# User creates file:
appendices/BD_alesina.tex

# User adds to index with code BD
```

## Historical Problem (Fixed in January 2026)

**Before this SOP:**
- Appendix codes were assigned without checking existing codes
- Duplicate codes discovered: AL, AH, etc.
- Caused conflicts and confusion

**After this SOP:**
- Check code availability BEFORE creation
- Prevents all code conflicts
- Maintains clean registry

## References

- **Source of Truth:** `appendices/00_appendix_index.tex`
- **Code Registry (outdated):** `docs/operations/APPENDIX_CODE_REGISTRY.yaml` (for historical reference only)
- **Checker Script:** `scripts/check_appendix_available.py`

## Exit Codes

```
0 = Code AVAILABLE
1 = Code IN USE
2 = Invalid format or error
```

## Questions?

If code availability is unclear:
1. Run `python scripts/check_appendix_available.py --status`
2. Check the index file directly: `appendices/00_appendix_index.tex`
3. Search for your code: `grep "^<CODE> &" appendices/00_appendix_index.tex`

---

**Last Updated:** January 18, 2026
**Status:** ACTIVE
**Owner:** EBF Framework Team
