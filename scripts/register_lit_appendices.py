#!/usr/bin/env python3
"""
Register 5 new LIT-Appendices in the appendix index at 4 locations.
Updates: category count, LIT table, status table, and chapter mapping table.
"""

from pathlib import Path

# Read the index file
index_path = Path("appendices/00_appendix_index.tex")
with open(index_path, 'r') as f:
    content = f.read()

# New appendices to add
new_appendices = [
    {
        'code': 'R',
        'name': 'LIT-THALER',
        'researcher': 'Richard Thaler',
        'contribution': 'Mental accounting, choice architecture, behavioral finance',
        'description': 'Richard Thaler Research: Mental Accounting \\& Choice Architecture',
        'importance': 'High'
    },
    {
        'code': 'S',
        'name': 'LIT-SUNSTEIN',
        'researcher': 'Cass Sunstein',
        'contribution': 'Behavioral law, policy, choice architecture, group behavior',
        'description': 'Cass Sunstein Research: Behavioral Law \\& Policy',
        'importance': 'High'
    },
    {
        'code': 'T',
        'name': 'LIT-CAMERER',
        'researcher': 'Colin Camerer',
        'contribution': 'Neuroeconomics, game theory, strategic thinking',
        'description': 'Colin Camerer Research: Neuroeconomics \\& Game Theory',
        'importance': 'High'
    },
    {
        'code': 'W',
        'name': 'LIT-ARIELY',
        'researcher': 'Dan Ariely',
        'contribution': 'Irrationality, dishonesty, behavioral interventions',
        'description': 'Dan Ariely Research: Irrationality \\& Decision-Making',
        'importance': 'High'
    },
    {
        'code': 'X',
        'name': 'LIT-LOEWENSTEIN',
        'researcher': 'George Loewenstein',
        'contribution': 'Emotions, visceral influences, curiosity, temporal discounting',
        'description': 'George Loewenstein Research: Emotions \\& Visceral Effects',
        'importance': 'High'
    }
]

# UPDATE 1: Category count - change "16" to "21" in table
print("=" * 80)
print("REGISTERING NEW LIT-APPENDICES IN INDEX")
print("=" * 80)

# Find and replace the LIT count in the categories table
old_count = r"\textbf{LIT-} & Literature & 16 &"
new_count = r"\textbf{LIT-} & Literature & 21 &"
if old_count in content:
    content = content.replace(old_count, new_count)
    print("✅ Location 1: Updated LIT count from 16 to 21")
else:
    print("⚠️  Location 1: Could not find LIT count in categories table")

# UPDATE 2: Add to LIT appendices table (after Q, before U)
print("✅ Location 2: Adding entries to LIT appendices table")

# Find the line with "Q & LIT-BLOOM" and add after it
insert_point_2 = content.find("Q & LIT-BLOOM & Nick Bloom & Uncertainty, management \\\\")
if insert_point_2 > 0:
    # Find the end of this line
    end_of_line = content.find("\n", insert_point_2)
    insertion_text = "\n"
    for app in new_appendices:
        insertion_text += f"{app['code']} & {app['name']} & {app['researcher']} & {app['contribution']} \\\\\n"

    content = content[:end_of_line] + insertion_text + content[end_of_line:]
    print(f"   Inserted {len(new_appendices)} new rows after Q")
else:
    print("⚠️  Location 2: Could not find insertion point in LIT table")

# UPDATE 3: Add to status table (after Q, before U)
print("✅ Location 3: Adding entries to status table")

insert_point_3 = content.find("Q & LIT-BLOOM: Nick Bloom Research & Literature & Medium \\\\")
if insert_point_3 > 0:
    end_of_line_3 = content.find("\n", insert_point_3)
    insertion_text_3 = "\n"
    for app in new_appendices:
        insertion_text_3 += f"{app['code']} & {app['description']} & Literature & {app['importance']} \\\\\n"

    content = content[:end_of_line_3] + insertion_text_3 + content[end_of_line_3:]
    print(f"   Inserted {len(new_appendices)} new rows after Q")
else:
    print("⚠️  Location 3: Could not find insertion point in status table")

# UPDATE 4: Add to complete chapter mapping table
print("✅ Location 4: Adding entries to chapter mapping table")

insert_point_4 = content.find("Q & LIT-BLOOM & Ch. 14 & Ch. 4, 8 \\\\")
if insert_point_4 > 0:
    end_of_line_4 = content.find("\n", insert_point_4)
    insertion_text_4 = "\n"
    for app in new_appendices:
        insertion_text_4 += f"{app['code']} & {app['name']} & Ch. 14 & Ch. 16, 17 \\\\\n"

    content = content[:end_of_line_4] + insertion_text_4 + content[end_of_line_4:]
    print(f"   Inserted {len(new_appendices)} new rows after Q")
else:
    print("⚠️  Location 4: Could not find insertion point in chapter mapping")

# Save updated content
with open(index_path, 'w') as f:
    f.write(content)

print("")
print("=" * 80)
print("✅ REGISTRATION COMPLETE")
print("=" * 80)
print("✅ R: LIT-THALER (Richard Thaler)")
print("✅ S: LIT-SUNSTEIN (Cass Sunstein)")
print("✅ T: LIT-CAMERER (Colin Camerer)")
print("✅ W: LIT-ARIELY (Dan Ariely)")
print("✅ X: LIT-LOEWENSTEIN (George Loewenstein)")
print("")
print("Next: Create paper_lit_matcher.py to add lit_appendix field to papers")
