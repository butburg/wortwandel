# Projekt-Übersicht: Klima-Komposita Studienarbeit

**Stand**: 20. Maerz 2026
**Titel**: "Klima-Komposita auf deutschsprachigen Online-Titelseiten: Eine Analyse des Begriffswandels 2021–2025"

---

## 🎯 Projektziel

Studienarbeit im Rahmen von **ADSC11 Tools der Softwareentwicklung und Online-Daten** (Prof. Dr. Marcel Hebing).

**Zentrale Forschungsfrage**:
*"Wie hat sich die Verwendung der häufigsten Begriffe mit dem Wortstamm 'Klima' auf deutschsprachigen Online-Titelseiten zwischen 2021 und 2025 entwickelt?"*

**Fokus-Begriffe**: Klimawandel (neutral), Klimakrise (alarmistisch), Klimaschutz (handlungsorientiert)

---

## 📁 Repository-Struktur

```
wortwandel/
├── .github/agents/          # Custom Agents für VS Code Copilot
│   ├── student.agent.md     # Haupt-Orchestrator, schreibt die Arbeit
│   ├── code.agent.md        # Programmiert Analysen & Grafiken
│   ├── research.agent.md    # Recherchiert Literatur & Events
│   ├── examiner.agent.md    # Prüfer (für User), bewertet Qualität
│   └── proofreader.agent.md # Lektorat, Grammatik, Stil, Zitation
├── data_input/              # Rohdaten (nicht versioniert)
├── data_output/             # Verarbeitete Daten
├── pylib/                   # Python-Bibliotheken (wiederverwendbare Funktionen)
├── notebooks/               # Alte/Experimentelle Notebooks (Ideen-Geber, NICHT bearbeiten!)
├── code_generated/          # Neue Notebooks für die Studienarbeit (Code-Agent arbeitet hier!)
├── research_findings/       # Research-Agent speichert hier
│   ├── README.md            # Erklärung der Struktur
│   ├── Quellen.md           # Wissenschaftliche Literatur, Links, Kernaussagen
│   ├── Zitate.md            # Direkte Zitate mit Seitenzahlen
│   ├── Events_2021-2025.md  # Chronologie von Klima-Events (Gipfel, Kampagnen)
│   └── PDFs/                # Original-Arbeiten (vom User oder Research-Agent abgelegt)
│
├── non_code/                # Wissen, Anleitungen, finale Arbeit
├── tableau sources/         # Tableau-Datenquellen (für externe Visualisierungen)
├── setup/                   # Setup-Scripte
│   └── init_project_script.sh
├── Pipfile                  # Python-Abhängigkeiten
├── README.md                # Projekt-README
├── LICENSE                  # Lizenz
└── PROJECT_OVERVIEW.md      # DIESE DATEI (Kontext für Agents)
```

---

## 🤖 Agent-System

### Workflow-Prinzip: **Student-Agent orchestriert**

Der Student-Agent ist der **zentrale Koordinator**. Die anderen Agents sind **Spezialisten**, die auf Anfrage arbeiten.

```
User
  ↓
Student-Agent (Orchestrator)
  ├─→ Code-Agent (Datenanalyse, Grafiken)
  ├─→ Research-Agent (Literatur, Events)
  └─→ Proofreader-Agent (Lektorat)

User (direkt)
  └─→ Examiner-Agent (Qualitätsprüfung)
```

---

## 📊 Datenstruktur

### SQLite-Datenbank: `data_output/dwh_data.db`

**Tabelle `newspapers`** (Metadaten):
- `newspaper_id` (PK)
- `newspaper_name` (z.B. "spiegel", "faz")
- `data_published` (Datum)
- `klima_mentions_count` (Anzahl "Klima"-Erwähnungen, **kann 0 sein!**)

**Tabelle `context`** (Klima-Kontext):
- `newspaper_id` (FK)
- `pre_context` (Text vor "Klima")
- `post_context` (Text nach "Klima")
- `prefix` (Wort vor "Klima", z.B. "die", "des")
- `suffix` (Wort nach "Klima", z.B. "wandel", "krise", "schutz")

**Wichtig**: `metadata` enthält **ALLE gecrawlten Tage**, auch mit `klima_mentions_count = 0`.
→ Grau in Visualisierung = "kein Klima", Weiß = echte Lücke (nicht gecrawlt)

---

## 🔍 Kritische Daten-Erkenntnis

### Scraper-Update am 21.04.2022
- **Vorher**: 53 Zeitungen
- **Nachher**: 64 Zeitungen (+11, 3 entfernt)
- **Konsequenz**: Analysen sollten ab 21.04.2022 starten (konsistente Datenbasis)

### Datenqualität
- Nicht alle Zeitungen haben vollständige Coverage ab 21.04.2022
- Lücken durch Scraper-Fehler, Server-Ausfälle, etc.
- Coverage-Analyse in [code_generated/03_Datenqualität_Nullen.ipynb](code_generated/03_Datenqualit%C3%A4t_Nullen.ipynb)

---

## 📝 Workflow der Studienarbeit


### Allgemein
1. Datenbasis verstehen
2. Datenqualität prüfen
   - Coverage-Analyse ab 21.04.2022
   - Nullen-Visualisierung (Blau=Klima, Grau=kein Klima, Weiß=Lücke)
   - Welche Zeitungen haben >90% Coverage?

3. 🔄 Daten filtern (nächster Schritt)
   - Nur ab 21.04.2022
   - Nur deutsche Zeitungen (keine englischen wie BBC, CNN)
   - Nur Zeitungen mit >90% Coverage
   - Nur deutsche Suffixe (kein "change", "crisis")

4. 🔄 **Suffix-Analyse** (folgt)
   - Häufigste deutsche Klima-Komposita
   - Sollte zeigen: Klimaschutz, Klimawandel, Klimakrise (Top 3)

5. 🔄 **Trend-Analyse** (folgt)
   - Zeitverlauf ab 21.04.2022
   - Grafik mit 3 Linien: Klimaschutz, Klimawandel, Klimakrise


### Pipeline 01 bis 06 (Kern) + 07/08 (optional)

1. **01_lake_to_dwh**
   - Datei: [code_generated/01_lake_to_dwh.ipynb](code_generated/01_lake_to_dwh.ipynb)
   - Aufgabe: Rohdaten aus data lake in `data_output/dwh_data.db` schreiben (`newspapers`, `context`)

2. **02_experiment_eda**
   - Datei: [code_generated/02_experiment_eda.ipynb](code_generated/02_experiment_eda.ipynb)
   - Aufgabe: Explorative Voranalyse auf Bronze-Daten, Grundlage fuer spaetere Processing-Entscheidungen

3. **03_Datenqualität_Nullen**
   - Datei: [code_generated/03_Datenqualität_Nullen.ipynb](code_generated/03_Datenqualit%C3%A4t_Nullen.ipynb)
   - Aufgabe: Qualitaetsanalyse frueh im Prozess (Nullen, Luecken, Coverage)

4. **04_Processing**
   - Datei: [code_generated/04_Processing.ipynb](code_generated/04_Processing.ipynb)
   - Aufgabe: Feature-Erweiterungen und Normalisierung (u.a. `suffix_lemma`) in `*_processed`
   - Persistenz: weiterhin in derselben DB (`dwh_data.db`) als neue Tabellen `newspapers_processed`, `context_processed`

5. **05_Datenbasis_EDA**
   - Datei: [code_generated/05_Datenbasis_EDA.ipynb](code_generated/05_Datenbasis_EDA.ipynb)
   - Aufgabe: strukturierte EDA auf dem verarbeiteten Stand

6. **06_Klima_Begriffe_Analyse**
   - Datei: [code_generated/06_Klima_Begriffe_Analyse.ipynb](code_generated/06_Klima_Begriffe_Analyse.ipynb)
   - Aufgabe: Hauptanalyse fuer die Arbeit, Grafikausgabe nach `data_output/plots`

7. **07_optional_Vergleich_Exact_vs_Lemma** (optional)
   - Datei: [code_generated/07_optional_Vergleich_Exact_vs_Lemma.ipynb](code_generated/07_optional_Vergleich_Exact_vs_Lemma.ipynb)
   - Aufgabe: Robustheitsvergleich (optional)

8. **08_optional_Suffix_EDA** (optional)
   - Datei: [code_generated/08_optional_Suffix_EDA.ipynb](code_generated/08_optional_Suffix_EDA.ipynb)
   - Aufgabe: offene Suffix-Exploration (optional)

### Datenzugriffskonvention
- Primäre Datenquelle fuer Notebooks ist `data_output/dwh_data.db`.
- `pd.read_csv(...)` fuer Kerninputs wird vermieden.
- CSV-Dateien bleiben als optionale Exporte fuer Weitergabe/Anhang erlaubt.
- Generische Spalten-Erkennung (`*_candidates`) in stabilen Kernnotebooks vermeiden, stattdessen klare erwartete Spalten nutzen.

### Phase 2: Recherche (Research-Agent führt aus)
- ✅ Literatur zu Klima-Begriffsgebrauch gesammelt (8 Quellen)
- ✅ Definitionen (Duden) für Klimawandel, Klimakrise, Klimaschutz
- 🔄 Event-Chronologie 2021-2025 (Klimagipfel, FFF-Kampagnen)

### Phase 3: Schreiben (Student-Agent führt aus)
1. 🔄 **Methodenkapitel** (basierend auf echten Code-Notebooks)
   - Data Lake → SQLite DWH ([notebooks/01_lake_to_dwh.ipynb](notebooks/01_lake_to_dwh.ipynb) beschreiben)
   - Filterkriterien begründen
   - Datenqualität transparent machen

2. 🔄 **Ergebnisse** (basierend auf Trend-Analyse)
   - Häufigkeiten der 3 Begriffe
   - Zeitverlauf-Grafik (zentral im Hauptteil)
   - Weitere Befunde in Anhang

3. 🔄 **Einleitung** (nach Ergebnissen!)
   - Problemstellung, Kontext, Relevanz
   - Forschungsfrage
   - 3-10 Quellen (aus [research_findings/Quellen.md](research_findings/Quellen.md))

4. 🔄 **Diskussion** (basierend auf Ergebnissen)
   - Interpretation
   - Rückbezug zur Einleitung
   - Handlungsempfehlungen
   - Event-Bezüge (aus [research_findings/Events_2021-2025.md](research_findings/Events_2021-2025.md))

5. 🔄 **Executive Summary** (ganz am Ende)

### Phase 4: Lektorat (Proofreader-Agent)
- 🔄 Grammatik, Stil, Konsistenz
- 🔄 Zitierweise prüfen
- 🔄 Lesbarkeit optimieren

### Phase 5: Qualitätsprüfung (Examiner-Agent)
- 🔄 Vollständigkeit & Struktur
- 🔄 Quellenanzahl
- 🔄 Grafiken (1-2 zentral, Rest Anhang)
- 🔄 Umfang (6-8 Seiten Hauptteil)

**Aktueller Stand**:
- Pipeline in [code_generated/](code_generated/) auf 01 bis 08 strukturiert
- Kernlauf ist 01 bis 06, 07 und 08 sind optional
- Research-Findings vorhanden (8 Quellen, Definitionen)
- Finale Arbeit noch im Entwurfsstadium

---

**Letzte Aktualisierung**: 20. Maerz 2026
**Nächster Schritt**: Notebook-Code auf DB-only Input vereinheitlichen
