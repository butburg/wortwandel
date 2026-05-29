# Code Generated – Finale Analyse-Notebooks

Dieser Ordner ist die **verbindliche Arbeitsfläche** für die finale Abgabe der Studienarbeit:
**"Klima-Komposita auf deutschsprachigen Online-Titelseiten: Eine Analyse des Begriffswandels 2021-2025"**

## Zweck

Hier liegen alle aktiv gepflegten Notebooks für:
- ETL und Datenaufbereitung
- Datenqualitätsanalyse
- Hauptanalyse und optionale Robustheitschecks
- Diagnose- und Vergleichsnotebooks zur Dokumentation technischer Befunde

Legacy-Notebooks wurden aus dem aktiven Bereich entfernt und ins Archiv verschoben:
- `../archive/notebooks_legacy/from_folder/`
- `../archive/notebooks_legacy/from_root/`

## Struktur und Reihenfolge

- `01_Rohdaten_ins_DWH.ipynb` - Rohdaten in `data_output/dwh_data.db` überführen (`newspapers`, `context`)
- `02_Experimentelle_EDA.ipynb` - frühe EDA auf Bronze-Daten
- `03_Datenqualität_Nullen.ipynb` - Coverage-, Nullen- und Lückenanalyse
- `04_Datenbasis_EDA.ipynb` - strukturierte EDA auf der Datenbasis
- `05_Datenaufbereitung.ipynb` - Aufbereitung und Build von `*_processed` Tabellen
- `06_Klimabegriffe_Analyse.ipynb` - Hauptanalyse und zentrale Visualisierungen
- `07_optional_Vergleich_Exakt_vs_Lemma.ipynb` - optionaler Robustheitsvergleich
- `08_optional_Suffix_Exploration.ipynb` - optionale Suffix-Exploration
- `09_optional_DB_Vergleich_fehlerhaft_vs_bereinigt.ipynb` - optionaler Vergleich zwischen fehlerhafter und bereinigter Datenbank

Kernlauf für die Abgabe: `01` bis `06`.

## Konventionen

- Primäre Datenquelle ist `../data_output/dwh_data.db`.
- Kernanalysen laden Inputs aus der DB (nicht aus CSV als Primärquelle).
- CSV-Exporte sind als Artefakte erlaubt.
- Kurze, nachvollziehbare Zellen mit klaren Zwischenschritten.
- Wiederverwendbare Logik in `../pylib/` halten.

## Hinweis zur Abgabe

Dieser Ordner repräsentiert den aktuellen, abgaberelevanten Stand.
Archivierte Notebooks sind nur noch Referenzmaterial und werden nicht weiter gepflegt.
