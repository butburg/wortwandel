# Datenmodell – ER-Diagramm

## Datenbankschema (dwh_data.db)

Drei persistente Tabellen in einer SQLite-Datenbank (Bronze + Silver):

![ER-Diagramm Wortwandel](<ER diagramm wortwandel.svg>)

**Natürlicher Schlüssel** in `newspapers`: `(newspaper_name, data_published)` — idempotenter Import verhindert Duplikate bei Wiederholungsläufen.

**Datenvolumen** (Stand: 31.01.2025):
- `newspapers`: 58.775 Zeilen (Zeitung × Tag)
- `context`: 172.610 Zeilen (je eine Klima-Nennung)
- `context_processed`: 172.610 Zeilen (+ `suffix_lemma`-Spalte aus NB 05)

---

## Notebook-Pipeline (Ausführungsreihenfolge)

```mermaid
flowchart TD
    RAW[("data_input/\nRohdaten SQLite [RAW]")]

    RAW --> NB01["01_Rohdaten_ins_DWH\nETL"]
    NB01 --> BRONZE[("dwh_data.db\nnewspapers\ncontext")]

    BRONZE --> NB02["02_Experimentelle_EDA\nFrühe EDA"]
    BRONZE --> NB03["03_Datenqualität_Nullen\nCoverage & Lücken"]
    BRONZE --> NB04["04_Datenbasis_EDA\nStrukturierte EDA"]
    BRONZE --> NB05["05_Datenaufbereitung\nSilber-Aufbereitung"]

    NB02 --> NB05
    NB03 --> NB05

    NB05 --> SILVER[("dwh_data.db\ncontext_processed")]

    SILVER --> NB06["06_Klimabegriffe_Analyse\n★ Hauptanalyse"]
    SILVER --> NB07["07_optional_Vergleich_Exakt_vs_Lemma\nRobustheit"]
    SILVER --> NB08["08_optional_Suffix_Exploration\noptional"]
    BRONZE --> NB09["09_optional_DB_Vergleich_fehlerhaft_vs_bereinigt\nDB-Vergleich"]

    NB06 --> PLOTS[("data_output/plots/\n06_grafik_1,2,3.png")]

    style NB06 fill:#d4edda,stroke:#28a745
    style BRONZE fill:#fff3cd,stroke:#ffc107
    style SILVER fill:#cce5ff,stroke:#004085
```

**Legende:**
- 🟡 Bronze: Rohdaten-Ingest
- 🔵 Silver: Normalisierte Analysebasis
- 🟢 Hauptanalyse (NB 06) → Ergebnisse der Studienarbeit
