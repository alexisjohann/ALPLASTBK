#!/usr/bin/env python3
"""
Convert Markdown report to PDF using WeasyPrint.
Based on official FehrAdvice Corporate Identity Guide (October 2023).

Source: assets/Corporate-Identity-Guide-FAP-EN-231007 2.pdf
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

# Read the markdown file
md_file = Path(__file__).parent / "F3_alpla_steinabrueckl_strategy_v1.md"
md_content = md_file.read_text(encoding='utf-8')

# Convert markdown to HTML
html_content = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'codehilite']
)

# =============================================================================
# FEHRADVICE OFFICIAL CORPORATE IDENTITY GUIDE - October 2023
# =============================================================================
#
# PRIMÄRFARBEN:
#   Dunkelblau:  #024079  RGB(2,64,121)    - Überschriften, Links, Akzente
#   Hellblau:    #549EDE  RGB(84,158,222)  - Sekundäre Elemente
#   Dunkelgrau:  #25212A  RGB(37,33,42)    - Fliesstext
#   Hellgrau:    #F3F5F7  RGB(243,245,247) - Hintergründe
#
# SEKUNDÄRFARBEN:
#   Flieder:     #A1A0C6  - Akzente, Diagramme
#   Mintgrün:    #7EBDAC  - Akzente, Diagramme
#   Ocker:       #DECB3F  - Hervorhebungen
#   Orange:      #DE9D3E  - Warnungen, Call-to-Action
#
# TYPOGRAFIE (aus offiziellem CI Guide, S. 11):
#   Headlines:      Roboto Bold
#   Subheadlines:   Roboto Regular
#   Fliesstext:     Open Sans Regular
#   Akzente/Zitate: Playfair Display
#   Code:           Consolas
#
# =============================================================================

css = CSS(string='''
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&family=Playfair+Display:ital@0;1&family=Roboto:wght@400;500;700&display=swap');

@page {
    size: A4;
    margin: 25mm 20mm 20mm 25mm;

    @top-center {
        content: "ALPLA Steinabrückl: Management Team Strategy 2030";
        font-family: "Open Sans", Arial, sans-serif;
        font-size: 9pt;
        color: #25212A;
    }

    @bottom-left {
        content: "FehrAdvice & Partners AG";
        font-family: "Open Sans", Arial, sans-serif;
        font-size: 8pt;
        color: #024079;
    }

    @bottom-right {
        content: "Seite " counter(page) " von " counter(pages);
        font-family: "Open Sans", Arial, sans-serif;
        font-size: 8pt;
        color: #25212A;
    }
}

/* Base Typography - Open Sans for body */
body {
    font-family: "Open Sans", Arial, sans-serif;
    font-size: 11pt;
    line-height: 16pt;
    font-weight: 400;  /* Regular */
    color: #25212A;    /* Dunkelgrau - Fliesstext */
}

/* Headlines - Roboto, All in Dunkelblau #024079 */
h1, h2, h3, h4 {
    font-family: "Roboto", Arial, sans-serif;
    color: #024079;
}

h1 {
    font-size: 28pt;
    line-height: 34pt;
    font-weight: 700;  /* Bold */
    margin-top: 0;
    margin-bottom: 18pt;
    border-bottom: 2px solid #024079;
    padding-bottom: 8pt;
}

h2 {
    font-size: 22pt;
    line-height: 28pt;
    font-weight: 700;  /* Bold */
    margin-top: 24pt;
    margin-bottom: 14pt;
    border-bottom: 1px solid #549EDE;  /* Hellblau */
    padding-bottom: 4pt;
}

h3 {
    font-size: 16pt;
    line-height: 22pt;
    font-weight: 400;  /* Regular */
    margin-top: 18pt;
    margin-bottom: 10pt;
}

h4 {
    font-size: 13pt;
    line-height: 18pt;
    font-weight: 400;  /* Regular */
    margin-top: 14pt;
    margin-bottom: 8pt;
}

/* Paragraphs */
p {
    text-align: justify;
    margin-bottom: 10pt;
}

/* Strong/Bold text in Dunkelblau */
strong {
    color: #024079;
    font-weight: 700;
}

/* Links in Dunkelblau */
a {
    color: #024079;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Lists */
ul, ol {
    margin-left: 15pt;
    margin-bottom: 10pt;
}

li {
    margin-bottom: 6pt;
}

/* Tables - FehrAdvice Style with Roboto headers */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 15pt 0;
    font-size: 10pt;
    font-weight: 400;  /* Regular for tables */
}

th {
    font-family: "Roboto", Arial, sans-serif;
    background-color: #024079;  /* Dunkelblau */
    color: #FFFFFF;
    padding: 8pt;
    text-align: left;
    font-weight: 700;  /* Bold */
    font-size: 9pt;
    border: 0.5pt solid #E0E0E0;
}

td {
    padding: 8pt;
    border-bottom: 0.5pt solid #E0E0E0;
    color: #25212A;
}

/* Alternating row colors - corrected Hellgrau */
tr:nth-child(even) {
    background-color: #F3F5F7;  /* Hellgrau (korrigiert) */
}

tr:nth-child(odd) {
    background-color: #FFFFFF;
}

/* Code - Consolas */
code {
    font-family: Consolas, Monaco, "Courier New", monospace;
    background-color: #F3F5F7;
    padding: 2pt 4pt;
    border-radius: 2pt;
    font-size: 10pt;
    color: #25212A;
}

pre {
    background-color: #25212A;  /* Dunkelgrau */
    color: #F3F5F7;
    padding: 12pt;
    border-radius: 4pt;
    overflow-x: auto;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 9pt;
    line-height: 14pt;
    border-left: 4pt solid #024079;  /* Dunkelblau accent */
}

pre code {
    background-color: transparent;
    padding: 0;
    color: inherit;
}

/* Horizontal Rule */
hr {
    border: none;
    border-top: 1px solid #549EDE;  /* Hellblau */
    margin: 24pt 0;
}

/* Blockquotes - Playfair Display for accent */
blockquote {
    font-family: "Playfair Display", Georgia, serif;
    border-left: 4pt solid #024079;
    padding-left: 12pt;
    margin-left: 0;
    color: #024079;
    font-style: italic;
    background-color: #F3F5F7;
    padding: 10pt 12pt;
}

/* Session metadata at top */
p:first-of-type {
    font-size: 10pt;
    color: #25212A;
    background-color: #F3F5F7;
    padding: 8pt 12pt;
    border-left: 4pt solid #024079;
}

/* Highlight boxes (for key insights) */
.highlight {
    background-color: #F3F5F7;
    border-left: 4pt solid #7EBDAC;  /* Mintgrün */
    padding: 10pt 12pt;
    margin: 12pt 0;
}

/* Warning boxes */
.warning {
    background-color: #FFF8E6;
    border-left: 4pt solid #DE9D3E;  /* Orange */
    padding: 10pt 12pt;
    margin: 12pt 0;
}

/* Call-to-action */
.cta {
    background-color: #024079;
    color: #FFFFFF;
    padding: 12pt 16pt;
    border-radius: 4pt;
    text-align: center;
    margin: 16pt 0;
}

/* Emoji styling (for option markers) */
.emoji {
    font-size: 14pt;
}

/* Caption text */
.caption {
    font-size: 9pt;
    line-height: 12pt;
    color: #25212A;
    font-style: italic;
}

/* Footnotes */
.footnote {
    font-size: 8pt;
    line-height: 10pt;
    font-weight: 400;
}
''')

# Wrap in full HTML document
full_html = f'''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>ALPLA Steinabrückl: Management Team Strategy 2030</title>
</head>
<body>
{html_content}
</body>
</html>
'''

# Generate PDF
output_pdf = Path(__file__).parent / "F3_alpla_steinabrueckl_strategy_v1.pdf"
HTML(string=full_html).write_pdf(output_pdf, stylesheets=[css])

print(f"✅ PDF erstellt mit offiziellem FehrAdvice CI/CD")
print(f"   Quelle: Corporate-Identity-Guide-FAP-EN-231007 2.pdf")
print()
print("Verwendete Farben:")
print("  • Dunkelblau #024079 - Headlines, Akzente")
print("  • Hellblau   #549EDE - Sekundäre Elemente")
print("  • Dunkelgrau #25212A - Fliesstext")
print("  • Hellgrau   #F3F5F7 - Hintergründe (korrigiert)")
print()
print("Verwendete Fonts:")
print("  • Roboto        - Headlines (H1-H4)")
print("  • Open Sans     - Fliesstext")
print("  • Playfair Display - Zitate/Akzente")
print()
print(f"Output: {output_pdf}")
