# Code Generated - Notebooks & Analysen

Dieser Ordner speichert alle Jupyter Notebooks und generierten Analysen für die Studienarbeit:
**"Klima-Komposita auf deutschsprachigen Online-Titelseiten: Eine Analyse des Begriffswandels 2021–2025"**

## Struktur & Benennungskonvention

Jedes Notebook hat einen klaren Fokus:

- `01_Daten_Exploration.ipynb` – Erste Daten-Struktur, Häufigkeiten, Überblick
- `02_Häufigkeiten_Trends.ipynb` – Analyse der Häufigkeiten, Zeitreihen
- `03_Medien_Vergleiche.ipynb` – Unterschiede zwischen Medien
- `04_Datenqualität.ipynb` – Scraper-Probleme, Lücken, Status-Codes
- etc.

**Nummerierung**: Hilft dem Student-Agent, die Reihenfolge zu verstehen

## Code-Stil (WICHTIG!)

1. **Kurze Zellen**: 10–20 Zeilen max. pro Zelle
2. **klare Kommentare**: Was macht diese Zelle? Warum?
3. **Default-Plots**: Nutze pandas/matplotlib Standard-Plots (nicht fancy/über-personalisiert)
4. **PyLib nutzen**: Verwende [../pylib/handle_data_processing.py](../pylib/handle_data_processing.py) für Standard-Funktionen
5. **Keine Copy-Paste**: Code sollte wiederverwertbar sein

## Notebook-Struktur

```python
# 1. Importe & Setup
import pandas as pd
import numpy as np
from pylib import handle_data_processing as hdp

# 2. Daten laden
df = hdp.load_data(...)

# 3. Analyse (kleine, fokussierte Schritte)
# Zelle 1: Daten-Check
# Zelle 2: Erste Berechnung
# Zelle 3: Grafik erstellen

# 4. Erkenntnisse am Ende
## Erkenntnisse
- [Befund 1]
- [Befund 2]
- Qualitäts-Hinweise: [Lücken, Probleme]
```

## Was wird hier gemacht?

- ✅ **Code & Analysen**: Der Code-Agent schreibt Python-Code für Student-Anforderungen
- ✅ **Grafiken**: Schwarz-weiß, einfach, aussagekräftig
- ✅ **Tabellen**: Für wichtige Zahlenergebnisse
- ✅ **Datenqualitäts-Berichte**: Dokumentation von Lücken & Problemen
- ❌ **Nicht**: Finale Textdokumente (=Student-Agent), Recherche (=Research-Agent)

## Student-Agent & Code-Agent Workflow

1. **Student sagt**: "Ich brauche eine Grafik mit Häufigkeiten der 3 Begriffe"
2. **Code-Agent erstellt**: Neues Notebook oder aktualisiert Bestehendes
3. **Code-Agent zeigt**: Grafik + Erkenntnisse im Notebook
4. **Student-Agent schaut**: Sich das Notebook an und nutzt die Erkenntnisse für die Finaldokument

## Wichtig

- **Nicht** in [../notebooks/](../notebooks/) arbeiten (die sind Ideen-Geber, nicht Arbeitsfläche)
- **Hier neue Analysen** erstellen und lagern
- **Student-Agent schaut** sich die Notebooks an, **kopiert aber nicht einfach** – er nutzt die Erkenntnisse für seinen Text

---

*Diese Notebooks sind Arbeitsdokumente – sie können refaktoriert/gelöscht werden, wenn die Arbeit fertig ist oder neue Analysen die alten ersetzen.*
