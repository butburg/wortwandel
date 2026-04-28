# Code Generated - Finale Analyse-Notebooks

Dieser Ordner ist die **verbindliche Arbeitsflaeche** fuer die finale Abgabe der Studienarbeit:
**"Klima-Komposita auf deutschsprachigen Online-Titelseiten: Eine Analyse des Begriffswandels 2021-2025"**

## Zweck

Hier liegen alle aktiv gepflegten Notebooks fuer:
- ETL und Datenaufbereitung
- Datenqualitaetsanalyse
- Hauptanalyse und optionale Robustheitschecks
- Diagnose- und Vergleichsnotebooks zur Dokumentation technischer Befunde

Legacy-Notebooks wurden aus dem aktiven Bereich entfernt und ins Archiv verschoben:
- `../archive/notebooks_legacy/from_folder/`
- `../archive/notebooks_legacy/from_root/`

## Struktur und Reihenfolge

- `01_lake_to_dwh.ipynb` - Rohdaten in `data_output/dwh_data.db` ueberfuehren (`newspapers`, `context`)
- `02_experiment_eda.ipynb` - fruehe EDA auf Bronze-Daten
- `03_Datenqualität_Nullen.ipynb` - Coverage-, Nullen- und Lueckenanalyse
- `04_Datenbasis_EDA.ipynb` - strukturierte EDA auf der Datenbasis
- `05_Processing.ipynb` - Aufbereitung und Build von `*_processed` Tabellen
- `06_Klima_Begriffe_Analyse.ipynb` - Hauptanalyse und zentrale Visualisierungen
- `07_optional_Vergleich_Exact_vs_Lemma.ipynb` - optionaler Robustheitsvergleich
- `08_optional_Suffix_EDA.ipynb` - optionale Suffix-Exploration
- `09_diagnose_Feb2025_Qualitaet.ipynb` - Datenqualitaetsdiagnose zur Feb-2025-Anomalie
- `10_compare_faulty_vs_clean_db.ipynb` - Vergleich `faulty` vs `clean` Datenbank

Kernlauf fuer die Abgabe: `01` bis `06`.

## Konventionen

- Primaere Datenquelle ist `../data_output/dwh_data.db`.
- Kernanalysen laden Inputs aus der DB (nicht aus CSV als Primaerquelle).
- CSV-Exporte sind als Artefakte erlaubt.
- Kurze, nachvollziehbare Zellen mit klaren Zwischenschritten.
- Wiederverwendbare Logik in `../pylib/` halten.

## Hinweis zur Abgabe

Dieser Ordner repraesentiert den aktuellen, abgaberelevanten Stand.
Archivierte Notebooks sind nur noch Referenzmaterial und werden nicht weiter gepflegt.
