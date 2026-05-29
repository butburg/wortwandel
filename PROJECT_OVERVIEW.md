# Projekt-Uebersicht: Klima-Komposita Studienarbeit

**Stand**: 28. April 2026
**Titel**: "Klima-Komposita auf deutschsprachigen Online-Titelseiten: Eine Analyse des Begriffswandels 2021-2025"

---

## Projektziel

Studienarbeit im Rahmen von **ADSC11 Tools der Softwareentwicklung und Online-Daten** (Prof. Dr. Marcel Hebing).

**Zentrale Forschungsfrage**:
*Wie hat sich die Verwendung der haeufigsten Begriffe mit dem Wortstamm "Klima" auf deutschsprachigen Online-Titelseiten zwischen 2021 und 2025 entwickelt?*

**Fokus-Begriffe**: Klimawandel (neutral), Klimakrise (alarmistisch), Klimaschutz (handlungsorientiert)

---

## Repository-Struktur (finalisiert fuer Abgabe)

```text
wortwandel/
├── .github/agents/          # Custom Agents fuer VS Code Copilot
├── archive/
│   └── notebooks_legacy/
│       ├── from_folder/     # ehemals notebooks/
│       └── from_root/       # ehemals experiment_*.ipynb, lake_*.ipynb im Repo-Root
├── code_generated/          # Aktive, abgaberelevante Notebook-Pipeline
├── data_input/              # Rohdaten (nicht versioniert)
├── data_output/             # Verarbeitete Daten und Plots
├── non_code/                # Wissens- und Textdokumente zur Arbeit
├── pylib/                   # Wiederverwendbare Python-Funktionen
├── research_findings/       # Literatur, Events, Quellenarbeit
├── setup/                   # Setup-Skripte
├── tests/                   # Pytest-Tests
├── Pipfile
├── README.md
├── LICENSE
└── PROJECT_OVERVIEW.md
```

**Wichtig**: Der Ordner `code_generated/` ist jetzt der einzige aktive Notebook-Bereich.
Alte Notebooks wurden bewusst archiviert und werden nicht mehr weiterentwickelt.

---

## Aktive Notebook-Pipeline in code_generated

1. `01_Rohdaten_ins_DWH.ipynb` - Rohdaten in SQLite DWH ueberfuehren (`newspapers`, `context`)
2. `02_Experimentelle_EDA.ipynb` - fruehe EDA auf Bronze-Daten
3. `03_Datenqualität_Nullen.ipynb` - Datenqualitaet, Nullen, Luecken, Coverage
4. `04_Datenbasis_EDA.ipynb` - EDA auf der aufbereiteten Datenbasis
5. `05_Datenaufbereitung.ipynb` - Verarbeitung und Build von `*_processed` Tabellen
6. `06_Klimabegriffe_Analyse.ipynb` - Hauptanalyse und Kernplots
7. `07_optional_Vergleich_Exakt_vs_Lemma.ipynb` - optionaler Robustheitsvergleich
8. `08_optional_Suffix_Exploration.ipynb` - optionale Suffix-Exploration
9. `09_optional_DB_Vergleich_fehlerhaft_vs_bereinigt.ipynb` - optionaler Vergleich zwischen fehlerhafter und bereinigter Datenbank

**Kernlauf fuer die Abgabe**: 01 bis 06.

---

## Datenstruktur

### SQLite-Datenbank: `data_output/dwh_data.db`

**Tabelle `newspapers`** (Metadaten):
- `newspaper_id` (PK)
- `newspaper_name`
- `data_published`
- `klima_mentions_count` (kann 0 sein)

**Tabelle `context`** (Klima-Kontexte):
- `newspaper_id` (FK)
- `pre_context`
- `post_context`
- `prefix`
- `suffix`

**Processed-Tabellen** (aus Pipeline-Schritt 05):
- `context_processed`

---

## Kritische Erkenntnisse zur Datenqualitaet

- Scraper-Update am 21.04.2022 erzeugt einen Bruch in der Zeitreihe (veraenderte Zeitungsbasis).
- Fuer vergleichbare Analysen wird der konsistente Zeitraum ab 21.04.2022 verwendet.
- Q1 2025 ist unvollstaendig (nur 8 Tage bis 08.02.2025) und muss in Vergleichen entsprechend eingeordnet werden.
- Die fruehere faulty/duplicate-Problematik wurde dokumentiert und ueber clean-vs-faulty-Vergleich nachvollziehbar gemacht.

---

## Arbeitsmodus fuer die finale Phase

1. Analysen nur noch in `code_generated/` pflegen.
2. Ergebnisse aus Kernlauf 01-06 in den Textteil ueberfuehren.
3. Optionale Notebooks 07-09 nur fuer Robustheit/Qualitaetsnachweise nutzen.
4. Archiv-Bereich unveraendert lassen, nur bei Bedarf als Referenz heranziehen.

---

## Aktueller Stand

- Repo-Struktur fuer Abgabe bereinigt (Legacy-Notebooks archiviert).
- Aktive Notebook-Pipeline konsolidiert in `code_generated/`.
- Datenqualitaets- und Importkorrekturen inklusive Tests vorhanden.
- Studienarbeitstext in `non_code/` im Ausbau.

**Letzte Aktualisierung**: 28. April 2026
