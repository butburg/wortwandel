# wortwandel

Analyse des Begriffswandels von Klima-Komposita auf deutschsprachigen Online-Titelseiten (2021–2025).

## Projektstruktur

```
code_generated/   Finale Analyse-Notebooks (01–10)
pylib/            Wiederverwendbare Python-Module
data_input/       Rohdaten (SQLite-Quelldatenbank)
data_output/      Ergebnisdatenbank (dwh_data.db) und Plots
non_code/         Studienarbeit (Markdown, PDF) und Eigenständigkeitserklärung
tests/            pytest-Tests zur Importlogik
```

## Ausführung (Kernlauf)

Notebooks in dieser Reihenfolge ausführen:

1. `01_lake_to_dwh.ipynb` – ETL: Rohdaten → DWH (`dwh_data.db`)
2. `02_experiment_eda.ipynb` – Frühe EDA auf Bronze-Daten
3. `03_Datenqualität_Nullen.ipynb` – Coverage- und Lückenanalyse
4. `04_Datenbasis_EDA.ipynb` – Strukturierte EDA der Datenbasis
5. `05_Processing.ipynb` – Aufbereitung (`context_processed`)
6. `06_Klima_Begriffe_Analyse.ipynb` – Hauptanalyse und Visualisierungen

Notebooks 07–10 sind optionale Robustheitschecks und Diagnoseschritte.

## Abhängigkeiten

```bash
pip install pipenv
pipenv install
```

Alternativ mit pip:

```bash
pip install -r requirements.txt
```

## Code-Dokumentation (Sphinx)

Die Module in `pylib/` sind mit Sphinx-kompatiblen RST-Docstrings dokumentiert
(`:param:`, `:type:`, `:returns:`, `:rtype:`-Annotationen).

Dokumentation generieren:

```bash
pip install sphinx sphinx-autodoc-typehints
sphinx-apidoc -o docs/ pylib/
cd docs && make html
```

Die generierten HTML-Seiten erscheinen dann unter `docs/_build/html/index.html`.

## Tests

```bash
pipenv run pytest tests/
```
