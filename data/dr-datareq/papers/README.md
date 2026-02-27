# Papers

> Akademische Quellen für Kontextanalyse (Ψ-Dimensionen)

## Struktur

```
papers/
├── by-psi-dimension/     ← Nach Ψ-Dimension organisiert
│   ├── kappa-time/      ← κ_TIME: Zeitliche Effekte
│   ├── kappa-default/   ← κ_DEFAULT: Default-Effekte
│   ├── kappa-frame/     ← κ_FRAME: Framing-Effekte
│   ├── kappa-social/    ← κ_SOCIAL: Soziale Normen
│   ├── kappa-arch/      ← κ_ARCH: Choice Architecture
│   ├── kappa-sal/       ← κ_SAL: Salience
│   ├── kappa-inst/      ← κ_INST: Institutionen
│   └── kappa-emo/       ← κ_EMO: Emotionale Zustände
├── meta-analyses/        ← Meta-Analysen
├── dach-specific/        ← DACH-spezifische Studien
└── replication-data/     ← Replikationsdaten
```

## Namenskonvention

### PDFs
```
{erstautor}_{jahr}_{kurztitel}.pdf
```
Beispiel: `laibson_1997_hyperbolic.pdf`

### BibTeX
Alle Papers sind in `bibliography/bcm_master.bib` mit:
- `use_for = {DR-DATAREQ, ...}` Tag
- `psi_dimension = {kappa_time, ...}` für Zuordnung

## Verknüpfung mit EBF

### Kernreferenzen nach Ψ-Dimension

| Ψ-Dimension | Kern-Paper | BibTeX-Key |
|-------------|------------|------------|
| κ_TIME | Laibson (1997) | `laibson1997golden` |
| κ_DEFAULT | Madrian & Shea (2001) | `madrian2001power` |
| κ_FRAME | Tversky & Kahneman (1981) | `tversky1981framing` |
| κ_SOCIAL | Cialdini (2003) | `cialdini2003crafting` |
| κ_ARCH | Thaler & Sunstein (2008) | `thaler2008nudge` |
| κ_SAL | Bordalo et al. (2012) | `bordalo2012salience` |
| κ_INST | Acemoglu & Robinson (2012) | `acemoglu2012whynations` |
| κ_EMO | Lerner et al. (2015) | `lerner2015emotion` |

## Paper hinzufügen

1. PDF in entsprechenden Ψ-Ordner
2. BibTeX-Eintrag in `bcm_master.bib` mit Tags
3. Replikationsdaten (falls verfügbar) in `replication-data/`
4. In Appendix DR referenzieren

## Wichtige Meta-Analysen

- DellaVigna & Linos (2022): Nudge-Metaanalyse (n=241 RCTs)
- Jachimowicz et al. (2019): Default-Metaanalyse (n=58 studies)
- Hummel & Maedche (2019): Digital Nudging Review
