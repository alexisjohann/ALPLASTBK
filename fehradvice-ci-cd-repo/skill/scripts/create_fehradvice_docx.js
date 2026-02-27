#!/usr/bin/env node
/**
 * FehrAdvice & Partners AG — DOCX Generator
 *
 * Reusable template for generating CI/CD-compliant documents.
 * Adapt the CONTENT SECTION below for each document.
 *
 * Usage: node create_fehradvice_docx.js
 * Output: ./output.docx (or set OUTPUT_PATH env var)
 */

const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
        ImageRun } = require("docx");

// ============================================================
// 1. CONSTANTS — Do not change
// ============================================================

const NAVY    = "1B365D";
const TEAL    = "2A7F8E";
const ORANGE  = "E8A33D";
const BLACK   = "1A1A1A";
const WHITE   = "FFFFFF";
const GRAY    = "6B7280";
const LIGHT_GRAY = "F2F4F7";
const FONT    = "Calibri";

// Resolve asset paths relative to this script
const SKILL_DIR = path.resolve(__dirname, "..");
const LOGO_FULL_PATH = path.join(SKILL_DIR, "assets", "logo_full.png");
const LOGO_ICON_PATH = path.join(SKILL_DIR, "assets", "logo_icon.png");

const logoFullBuffer = fs.readFileSync(LOGO_FULL_PATH);
const logoIconBuffer = fs.readFileSync(LOGO_ICON_PATH);

const OUTPUT_PATH = process.env.OUTPUT_PATH || "/mnt/user-data/outputs/output.docx";

// Table styling
const border  = { style: BorderStyle.SINGLE, size: 1, color: "DDDDDD" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

// ============================================================
// 2. HELPER FUNCTIONS
// ============================================================

/** Heading 1 — Navy, bold, uppercase, with page break */
function h1(text, options = {}) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    pageBreakBefore: options.noPageBreak ? false : true,
    children: [new TextRun({ text, bold: true, font: FONT, size: 28, color: NAVY })]
  });
}

/** Heading 2 — Navy, bold */
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 120 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 22, color: NAVY })]
  });
}

/** Body paragraph — justified, black */
function para(...runs) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 60, after: 60 },
    children: runs
  });
}

/** Normal text run */
function normal(text) {
  return new TextRun({ text, font: FONT, size: 20, color: BLACK });
}

/** Bold text run */
function bold(text) {
  return new TextRun({ text, bold: true, font: FONT, size: 20, color: BLACK });
}

/** Italic text run */
function italic(text) {
  return new TextRun({ text, italics: true, font: FONT, size: 18, color: GRAY });
}

/** Vertical spacer */
function spacer(pts = 200) {
  return new Paragraph({ spacing: { before: pts } });
}

/** Standard table with navy header row */
function makeTable(headers, rows, colWidths) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  const headerRow = new TableRow({
    children: headers.map((h, i) => new TableCell({
      borders, width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: NAVY, type: ShadingType.CLEAR },
      margins: cellMargins,
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, font: FONT, size: 18, color: WHITE })] })]
    }))
  });
  const dataRows = rows.map(row => new TableRow({
    children: row.map((cell, i) => {
      const children = Array.isArray(cell) ? cell : [new Paragraph({ children: [new TextRun({ text: String(cell), font: FONT, size: 18 })] })];
      return new TableCell({
        borders, width: { size: colWidths[i], type: WidthType.DXA },
        margins: cellMargins, children
      });
    })
  }));
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows]
  });
}

/**
 * Nutzen-Box — Signature FehrAdvice element
 * @param {string[]} items - Array of benefit bullet points
 */
function nutzenBox(items) {
  const navyTopBorder = { style: BorderStyle.SINGLE, size: 12, color: NAVY };
  const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: "DDDDDD" };

  const contentParagraphs = [
    new Paragraph({
      spacing: { before: 80, after: 80 },
      children: [new TextRun({ text: "\u{1F44D} Ihr Nutzen", bold: true, font: FONT, size: 20, color: NAVY })]
    }),
    ...items.map(item => new Paragraph({
      spacing: { before: 40, after: 40 },
      indent: { left: 360 },
      children: [new TextRun({ text: `\u2022 ${item}`, font: FONT, size: 18 })]
    }))
  ];

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({
      children: [new TableCell({
        borders: { top: navyTopBorder, bottom: thinBorder, left: thinBorder, right: thinBorder },
        shading: { fill: LIGHT_GRAY, type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 200, right: 200 },
        children: contentParagraphs
      })]
    })]
  });
}

/**
 * "Über FehrAdvice & Partners" standard section
 * @param {"kurz"|"standard"|"lang"} variant - Length variant
 */
function ueberFehrAdvice(variant = "standard") {
  const elements = [];
  elements.push(h1("\u00dcber FehrAdvice & Partners"));

  const kurz = "FehrAdvice & Partners AG ist eines der f\u00fchrenden Beratungsunternehmen f\u00fcr Verhaltens\u00f6konomie in Europa. Wir sind \u00fcberzeugt, dass Wirtschafts- und Unternehmensberatung nur dann relevante Ergebnisse bringt, wenn sie den Menschen ins Zentrum stellt. Unsere L\u00f6sungen basieren auf den neuesten Erkenntnissen der verhaltens\u00f6konomischen Forschung. Wir verkn\u00fcpfen empirisches Wissen mit Ihren Daten und entwickeln daraus innovative, wachstumsorientierte L\u00f6sungen, die Sie schnell testen und erfolgsversprechend umsetzen k\u00f6nnen.";

  const prinzipien = "Unsere Arbeit folgt drei Prinzipien: Wir sind modellbasiert \u2014 jedes Engagement beginnt mit einem verhaltens\u00f6konomischen Modell. Wir arbeiten evidenzbasiert \u2014 orientiert an den Methoden und Erkenntnissen der Verhaltens\u00f6konomie an der Schnittstelle von \u00d6konomie, Psychologie, Soziologie und Neurowissenschaften. Und wir denken implementierbar \u2014 jede Erkenntnis muss zu umsetzbaren Massnahmen f\u00fchren.";

  const beatrix = "Unser Behavioral Design Ansatz differenziert sich durch die Werte Wissenschaftlichkeit, Fairness und Spitzenleistung. Mit Tools wie BEAtrix \u2014 der weltweit ersten wissenschaftlich validierten Engine zur Analyse und nachhaltigen Ver\u00e4nderung von Verhalten \u2014 machen wir Verhaltens\u00f6konomie in Unternehmen direkt anwendbar. Unsere Mission: Mit #Experimentability die Welt ein bisschen besser machen.";

  elements.push(para(normal(kurz)));
  if (variant === "standard" || variant === "lang") {
    elements.push(para(normal(prinzipien)));
  }
  if (variant === "lang") {
    elements.push(para(normal(beatrix)));
  }

  return elements;
}

/**
 * Kontakt section
 * @param {Array<{name: string, role: string}>} contacts
 * @param {string} [closingText] - Optional closing paragraph
 */
function kontaktSection(contacts, closingText) {
  const elements = [];
  elements.push(h1("Kontakt"));

  if (closingText) {
    elements.push(para(normal(closingText)));
    elements.push(spacer(100));
  }

  elements.push(makeTable(
    ["Name", "Rolle"],
    contacts.map(c => [c.name, c.role]),
    [4680, 4680]
  ));

  return elements;
}

/**
 * Manual Table of Contents
 * @param {Array<{num: string, title: string, level: 1|2}>} entries
 */
function tableOfContents(entries) {
  const elements = [];
  elements.push(new Paragraph({
    spacing: { before: 200, after: 400 },
    children: [new TextRun({ text: "Inhaltsverzeichnis", bold: true, font: FONT, size: 32, color: NAVY })]
  }));

  for (const entry of entries) {
    const indent = entry.level === 2 ? 720 : 0;
    const fontSize = entry.level === 2 ? 20 : 22;
    const label = entry.num ? `${entry.num}    ` : "       ";
    elements.push(new Paragraph({
      spacing: { before: entry.level === 1 ? 180 : 80, after: 0 },
      indent: { left: indent },
      children: [
        new TextRun({ text: label, bold: entry.level === 1, font: FONT, size: fontSize, color: NAVY }),
        new TextRun({ text: entry.title, bold: entry.level === 1, font: FONT, size: fontSize, color: NAVY }),
      ]
    }));
  }

  return elements;
}

/**
 * Cover page
 * @param {object} opts
 * @param {string} opts.title - Main title
 * @param {string} opts.subtitle - Subtitle
 * @param {string[]} opts.meta - Additional metadata lines
 * @param {string} opts.date - Date string
 */
function coverPage({ title, subtitle, meta = [], date }) {
  const elements = [];

  // Logo right-aligned
  elements.push(new Paragraph({
    alignment: AlignmentType.RIGHT, spacing: { before: 200, after: 200 },
    children: [new ImageRun({ data: logoFullBuffer, transformation: { width: 200, height: 86 }, type: "png" })]
  }));

  // Navy separator
  elements.push(new Paragraph({
    spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: NAVY, space: 1 } },
    children: []
  }));

  elements.push(spacer(200));

  // Title
  elements.push(new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text: title, bold: true, font: FONT, size: 40, color: BLACK })]
  }));

  // Subtitle
  elements.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ text: subtitle, font: FONT, size: 22, color: NAVY })]
  }));

  // Meta lines
  elements.push(spacer(100));
  for (const line of meta) {
    elements.push(new Paragraph({
      spacing: { after: 40 },
      children: [new TextRun({ text: line, font: FONT, size: 18, color: BLACK })]
    }));
  }

  // Separator + Date
  elements.push(spacer(100));
  elements.push(new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: NAVY, space: 1 } },
    children: []
  }));
  elements.push(new Paragraph({
    spacing: { before: 80 },
    children: [new TextRun({ text: date, font: FONT, size: 18, color: GRAY })]
  }));

  elements.push(new Paragraph({ children: [new PageBreak()] }));

  return elements;
}

// ============================================================
// 3. DOCUMENT ASSEMBLY
// ============================================================

/**
 * Build and save the complete document
 * @param {Paragraph[]} contentChildren - All paragraphs/tables
 * @param {string} headerContext - Text for header (e.g. project name)
 */
async function buildDocument(contentChildren, headerContext = "") {
  const headerText = headerContext
    ? `FEHRADVICE & PARTNERS AG \u2014 ${headerContext}    `
    : "FEHRADVICE & PARTNERS AG    ";

  const doc = new Document({
    features: { updateFields: true },
    styles: {
      default: {
        document: { run: { font: FONT, size: 20, color: BLACK } },
        heading1: { run: { font: FONT, size: 28, bold: true, color: NAVY } },
        heading2: { run: { font: FONT, size: 22, bold: true, color: NAVY } },
      }
    },
    numbering: {
      config: [{ reference: "default-numbering", levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.START, style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }] }]
    },
    sections: [{
      properties: {
        page: {
          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
          size: { width: 11906, height: 16838 }
        }
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            spacing: { after: 50 },
            children: [
              new TextRun({ text: headerText, font: FONT, size: 14, color: GRAY }),
              new ImageRun({ data: logoIconBuffer, transformation: { width: 28, height: 28 }, type: "png" })
            ]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Seite ", font: FONT, size: 16, color: GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: GRAY })
            ]
          })]
        })
      },
      children: contentChildren
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(OUTPUT_PATH, buffer);
  console.log(`\u2705 Document saved to ${OUTPUT_PATH}`);
}

// ============================================================
// 4. CONTENT SECTION — ADAPT THIS FOR EACH DOCUMENT
// ============================================================

async function main() {
  const children = [];

  // --- COVER ---
  children.push(...coverPage({
    title: "DOKUMENTTITEL",
    subtitle: "Untertitel des Dokuments",
    meta: [
      "FehrAdvice & Partners AG",
    ],
    date: new Date().toLocaleDateString("de-CH", { year: "numeric", month: "long", day: "numeric" })
  }));

  // --- TOC ---
  children.push(...tableOfContents([
    { num: "1", title: "Ausgangslage & Zielsetzung", level: 1 },
    { num: "2", title: "Vorgehen", level: 1 },
    { num: "3", title: "Der n\u00e4chste Schritt", level: 1 },
    { num: "4", title: "Kontakt", level: 1 },
    { num: "", title: "", level: 1 },
    { num: "", title: "\u00dcber FehrAdvice & Partners", level: 1 },
  ]));
  children.push(new Paragraph({ children: [new PageBreak()] }));

  // --- CONTENT ---
  children.push(h1("1  Ausgangslage & Zielsetzung"));
  children.push(para(normal("Hier die Ausgangslage beschreiben...")));

  children.push(h1("2  Vorgehen"));
  children.push(para(normal("Hier das Vorgehen beschreiben...")));

  // Example Nutzen-Box
  children.push(spacer(100));
  children.push(nutzenBox([
    "Nutzen-Punkt 1",
    "Nutzen-Punkt 2",
    "Nutzen-Punkt 3",
  ]));

  // --- NEXT STEP ---
  children.push(h1("3  Der n\u00e4chste Schritt"));
  children.push(para(normal(
    "Mit diesem Projektansatz legen wir gemeinsam den Grundstein daf\u00fcr, dass [KUNDE] " +
    "[ZIEL] \u2014 differenzierend, vertrauensstiftend und emotional anschlussf\u00e4hig. " +
    "Wir w\u00fcrden vorschlagen, in einem Follow-up Termin die Inhalte im Detail zu diskutieren, " +
    "und freuen uns auf die n\u00e4chsten Schritte."
  )));

  // --- KONTAKT ---
  children.push(...kontaktSection(
    [
      { name: "Gerhard Fehr", role: "Gr\u00fcnder & Managing Partner" },
      { name: "J\u00f6rg Macke", role: "Head of Behavioral Design & Consulting" },
    ],
  ));

  // --- ÜBER FEHRADVICE (always!) ---
  children.push(...ueberFehrAdvice("standard"));

  // --- BUILD ---
  await buildDocument(children, "PROJEKTNAME");
}

main().catch(err => { console.error(err); process.exit(1); });
