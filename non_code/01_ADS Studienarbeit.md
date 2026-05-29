
Digital Business University of Applied Sciences
Data Science & Management
ADSC11 Tools der Softwareentwicklung und Online-Daten
Prof. Dr. Marcel Hebing







# **Klima-Komposita auf deutschsprachigen Online-Titelseiten: Eine Analyse des Begriffswandels 2021–2025**



## Studienarbeit














Eingereicht von          	Edwin Wiese
Datum                           	12. Sept. 2025

## Executive Summary

Diese Studienarbeit analysiert, wie sich die Verwendung der drei häufigsten Klima-Komposita – Klimawandel, Klimaschutz und Klimakrise – auf deutschsprachigen Online-Titelseiten zwischen April 2022 und Januar 2025 entwickelt hat. Datengrundlage sind eigene Scraper-Daten von 46 Medienquellen mit insgesamt 40.667 ausgewerteten Nennungen.

**Kernergebnisse:** Klimawandel ist mit 49 % der Nennungen der dominierende Begriff und hat seinen relativen Anteil im Beobachtungszeitraum von rund 41 % auf 53 % gesteigert. Klimaschutz verliert spürbar: von 39 % auf 25 %. Klimakrise bleibt mit Anteilen zwischen 21 % und 26 % weitgehend stabil. Im direkten Vergleich dieser beiden Begriffe sinkt der Anteil alarmistischer Sprache von 33,7 % (2022Q2) auf 28,4 % (2025Q1).

**Schlussfolgerung:** Im untersuchten DACH-Ausschnitt ist keine Eskalation alarmistischer Klimasprache erkennbar – der Trend zeigt eine Verschiebung hin zu neutral-deskriptiver Terminologie. Dies steht im Kontrast zu internationalen Befunden, die seit 2019 einen Zuwachs alarmistischer Labels verzeichnen (Schäfer et al., 2023), und verweist auf nationale Medienlogiken oder unterschiedliche Beobachtungsfenster als mögliche Erklärung.

**Handlungsempfehlungen:** Erweiterung auf quellenbezogene Auswertungen und Volltextanalysen sowie eine Fortschreibung über 2025 hinaus, um die beobachtete Stabilisierung zu überprüfen. Die vorliegenden Daten eignen sich als Ausgangspunkt für Anschlussforschung zur DACH-spezifischen Klimakommunikation.

## 1. Einleitung

Die öffentliche Klimadebatte wird nicht nur über Daten und Ereignisse geführt, sondern auch über Begriffe. Ob Medien eher von Klimawandel, Klimaschutz oder Klimakrise sprechen, beeinflusst die Wahrnehmung von Dringlichkeit, Verantwortlichkeit und Handlungsbedarf. Für die gesellschaftliche Einordnung der Klimakrise sind diese sprachlichen Unterschiede relevant, weil sie als Teil journalistischer Agenda- und Framebildung wirken (Entman, 1993; McHugh et al., 2021). Die wissenschaftliche Dringlichkeit ist zugleich gut belegt, etwa laut Pressemitteilung zum AR6-Synthesebericht des IPCC (IPCC, 2023).

Internationale Befunde zeigen eine Verschiebung der Klima-Terminologie seit 2019. In einer groß angelegten automatisierten Inhaltsanalyse mit 89.887 Artikeln aus acht Ländern dokumentieren Schäfer et al. (2023), dass alarmistische Labels wie climate crisis oder climate emergency zugenommen haben, während neutral-deskriptive Begriffe insgesamt weiter dominieren. Parallel dazu änderten einzelne Leitmedien ihre Sprachrichtlinien, etwa der Guardian im Jahr 2019. Dieser Schritt gilt als wichtiger Mitfaktor der Debatte, aber nicht als alleinige Ursache der internationalen Entwicklung (Carrington, 2019; Schäfer et al., 2023).

Gleichzeitig ist die Wirkung alarmistischer Begriffe umstritten. Laut Abstract von Feldman und Hart (2021) können emergency-Formulierungen die wahrgenommene Glaubwürdigkeit von Beiträgen senken, ohne das Klima-Engagement systematisch zu erhöhen. Für Governance und Politik lassen sich ebenfalls keine einfachen linearen Effekte ableiten, sondern je nach Kontext unterschiedliche Reaktionspfade (McHugh et al., 2021). Damit entsteht eine Spannungsfrage zwischen sprachlicher Dringlichkeit und kommunikativer Anschlussfähigkeit.

Für den deutschsprachigen Raum besteht hierzu weiterhin eine Lücke. Es liegen zwar internationale und theoretische Arbeiten vor, aber nur wenige direkte Zeitreihenbefunde zur Verwendung zentraler Klima-Begriffe auf deutschsprachigen Online-Titelseiten im Zeitraum 2021 bis 2025. Genau hier setzt diese Arbeit an.

Die zentrale Forschungsfrage lautet:

**Wie hat sich die Verwendung der häufigsten Begriffe mit dem Wortstamm Klima auf deutschsprachigen Online-Titelseiten in drei Jahren bis 2025 entwickelt?**

Der Beitrag der Arbeit ist zweifach. Erstens liefert sie eine DACH-spezifische Anschlussanalyse zu internationalen Studien. Zweitens vergleicht sie neutral-deskriptive, handlungsorientierte und alarmistische Begriffe auf einer einheitlichen Datengrundlage und macht damit die Richtung des medialen Begriffswandels transparent.

## 2. Daten und Methoden

### 2.1 Datenbasis

Die empirische Grundlage bilden eigene Scraper-Daten aus ausgewählten deutschsprachigen Online-Medien. Zwischen April 2021 und Januar 2025 wurden täglich um 09:00 Uhr Titelseiten automatisiert erfasst und in einer SQLite-basierten Datenstruktur gespeichert. Insgesamt umfasst das Rohpanel 47 Medienquellen. Für die Analyse wurden zwei Ebenen genutzt:

1. Metadaten je Crawl-Einheit, einschließlich Datum, Quelle und Klima-Nennungen.
2. Kontextdaten mit den gefundenen Klima-Komposita und Textumgebung.

Diese Trennung erlaubt eine methodisch wichtige Unterscheidung zwischen echten Nullbeobachtungen und Erhebungslücken. Tage mit klima_mentions_count = 0 sind beobachtete Nullwerte, fehlende Einträge dagegen potenzielle technische Ausfälle.

### 2.2 Analysezeitraum und struktureller Bruch

Aufbauend auf dieser Quellenbasis zeigt die Coverage-Prüfung einen strukturellen Einschnitt am 21.04.2022 durch eine Änderung der Scraper-Architektur und des Quellenpanels. Um verzerrte Vorher-Nachher-Vergleiche zu vermeiden, basiert die quantitative Hauptauswertung auf dem stabileren Zeitraum vom 21.04.2022 bis 31.01.2025. Dieser Zeitraum umfasst 1.017 Kalendertage. Für diesen Zeitraum liegen Daten von 46 Medienquellen vor.

### 2.2a Auswahl deutschsprachiger Quellen

Für die inhaltliche Auswahl wurden nur Medien mit dem HTML-Attribut lang="de" berücksichtigt. Dadurch ist sichergestellt, dass ausschließlich deutschsprachige Inhalte in die Analyse eingehen. Die 46 Medienquellen stammen aus dieser gefilterten Auswahl.

### 2.3 Begriffsauswahl und Kategorisierung

Analysiert werden die drei häufigsten Klima-Komposita der Datenbasis:

- Klimawandel als neutral-deskriptiver Begriff
- Klimaschutz als handlungsorientierter Begriff
- Klimakrise als alarmistischer Begriff

Die Kategorisierung folgt der internationalen Terminologie-Debatte in der Klimakommunikationsforschung (Schäfer et al., 2023; Haueis, 2024) und wird durch lexikalische Abgrenzungen gestützt (Duden, 2025a, 2025b, 2025c).

Operationalisierung: Aus den Kontextdaten wurden alle Fundstellen extrahiert, die den Wortstamm Klima enthalten. Für die Hauptanalyse wurden anschließend alle Treffer über einfache Suffixregeln den drei Zielbegriffen zugeordnet: wandel*, krise* und schutz*. Dabei handelt es sich um Suffixmuster innerhalb des Kompositums (der Teil nach dem Präfix „Klima"). Dadurch werden beispielsweise Formen wie Klimawandels, Klimakrisen oder Klimaschutzabkommen konsistent erfasst. Gezählt wurden Vorkommen der Begriffe auf Basis der erfassten Kontexttreffer. Die Auswertung ist deskriptiv, also auf die Beschreibung beobachteter Verteilungen und Entwicklungen beschränkt, ohne kausale Wirkungen oder statistische Signifikanz zu prüfen.

### 2.4 Auswertungsschritte

Die Auswertung umfasst drei Schritte:

1. Absolute Häufigkeiten der drei Begriffe über den Gesamtzeitraum.
2. Quartalsweise relative Anteile zur Trendbeobachtung.
3. Vergleich neutral-deskriptiv vs. alarmistisch als reduziertes Zwei-Kategorien-Setting (Klimawandel vs. Klimakrise), angelehnt an internationale Vergleichslogik.

Wichtiger Hinweis zum Nenner: Relative Anteile in Kapitel 3 beziehen sich auf die Summe der drei Zielbegriffe (Top-3-Set) und nicht auf alle im Korpus vorkommenden Klima-Komposita.

Die relative Betrachtung dämpft die ohnehin subjektive Suffixzuordnung deutlich, weil kleinere Unterschiede zwischen Verfahren im Prozentvergleich kaum noch sichtbar werden. Dadurch werden die grundlegenden Beobachtungen robuster und besser vergleichbar.

Als optionaler Robustheitscheck wurde das Suffix-Matching mit einem konservativen Lemma-Gruppierungsverfahren verglichen (Notebook 07). Dabei werden morphologisch ähnliche Wortformen, z. B. Flexionsendungen wie „-s" oder „-en", zu einem Lemmacluster zusammengefasst. Die relativen Trendverläufe der drei Begriffe erwiesen sich als stabil gegenüber diesem Methodenwechsel, was die Belastbarkeit der Hauptergebnisse stützt.

### 2.5 Datenqualität und Grenzen

Die Aussagekraft der Analyse wird durch folgende Punkte begrenzt:

- Selektion der Quellen: Das Panel bildet nicht das gesamte deutschsprachige Mediensystem ab.
- Fokus auf Titelseiten: Keine Volltextanalyse der Artikelkörper.
- Technische Unsicherheit: Einzelne Ausfälle durch Website-Änderungen sind nicht vollständig vermeidbar.
- Vergleichbarkeit: Der internationale Literaturvergleich ist inhaltlich, aber nicht vollständig methodengleich.
- Statistische Unsicherheit: Es wurden keine Konfidenzintervalle oder formalen Trendtests berechnet.

### 2.6 Qualitätssicherung der Importlogik

Im Rahmen der Datenqualitätsprüfung wurde ein technischer Fehler in der ursprünglichen Importlogik identifiziert, der zu überhöhten Tageswerten führen konnte. Bei wiederholten ETL-Läufen wurden bereits importierte Zeitung-Tag-Kombinationen teilweise erneut angehängt. Dadurch konnten in nachgelagerten Merges künstliche Vervielfachungen entstehen. Die auffällige Spitze im Februar 2025 war ein zentraler Anlass für diese Diagnose.

Zur Behebung wurde die Importstrecke auf inkrementelles Verhalten umgestellt. Für die Tabelle newspapers wird eine eindeutige natürliche Schlüsselkombination aus newspaper_name und data_published verwendet. Existiert eine Kombination bereits, wird sie nicht erneut eingefügt. Kontextdaten werden nur dann geschrieben, wenn die zugehörige Zeitung-Tag-Kombination neu angelegt wurde. Damit bleiben Wiederholungsläufe idempotent und führen nicht mehr zu einer erneuten Einspielung historischer Tage.

Die Korrektur wurde mit automatisierten Tests auf Basis von pytest abgesichert. Geprüft wurden zwei für diese Arbeit zentrale Fälle: Erstens bleibt bei erneutem Import bereits vorhandener Tage die Anzahl der Zeilen in newspapers konstant. Zweitens führt das Hinzufügen eines bisher nicht vorhandenen Tages genau zu einem zusätzlichen Eintrag in newspapers, während sich die Kontexttabelle nur für diesen neuen Tag erhöht.

## 3. Ergebnisse

### 3.1 Gesamtverteilung

Im Analysezeitraum (21.04.2022 bis 31.01.2025) wurden insgesamt 40.667 Nennungen der drei Zielbegriffe gezählt.

| Begriff | Absolute Häufigkeit | Relativer Anteil |
|---------|--------------------:|----------------:|
| Klimawandel | 19.922 | 49,0 % |
| Klimaschutz | 11.463 | 28,2 % |
| Klimakrise | 9.282 | 22,8 % |

Der am häufigsten verwendete Begriff ist Klimawandel. Klimakrise bleibt mit gut einem Fünftel der Nennungen deutlich dahinter.

### 3.2 Zeitliche Entwicklung der drei Begriffe

Die quartalsweise Entwicklung im Top-3-Set zeigt folgende Trends:

- Klimawandel steigt von rund 41 % auf 53 %.
- Klimaschutz sinkt von rund 39 % auf 25 %.
- Klimakrise schwankt im Bereich von rund 21 % bis 26 % weitgehend stabil.

![Grafik 1: Zeitliche Entwicklung](../data_output/plots/grafik_1_zeitliche_entwicklung.png)

*Abbildung 1: Quartalsweise relative Anteile der drei häufigsten Klima-Komposita (2022-2025).*

### 3.3 Neutral-deskriptiv versus alarmistisch

Für den direkten Anschluss an die internationale Diskussion wurde zusätzlich das Verhältnis von Klimawandel (neutral-deskriptiv) zu Klimakrise (alarmistisch) betrachtet. Im Vergleich dieser beiden Begriffe verschiebt sich der Anteil zugunsten neutral-deskriptiver Bezeichnungen:

- Erstes Quartal im Analysefenster (2022Q2): 66,3 % neutral-deskriptiv, 33,7 % alarmistisch
- Letztes Quartal im Analysefenster (2025Q1): 71,6 % neutral-deskriptiv, 28,4 % alarmistisch

![Grafik 2: Neutral-deskriptiv versus alarmistisch](../data_output/plots/grafik_2b_neutral_vs_alarmistisch_linien.png)

*Abbildung 2: Entwicklung der Anteile neutral-deskriptiver und alarmistischer Begriffe im Zeitverlauf.*

### 3.4 Kernergebnis

Die Daten zeigen im Beobachtungszeitraum keinen ausgeprägten Aufwärtstrend für den alarmistischen Kernbegriff Klimakrise. Gleichzeitig nimmt der Anteil des neutral-deskriptiven Begriffs Klimawandel innerhalb des Top-3-Sets zu. Für den untersuchten DACH-Ausschnitt ist dies vereinbar mit einer relativen Stabilität alarmistischer Sprache bei gleichzeitiger Neuorientierung hin zu neutral-deskriptiver Terminologie.

## 4. Diskussion

### 4.1 Einordnung im Literaturkontext

Die Befunde ergänzen internationale Studien durch eine regionale Perspektive. Schäfer et al. (2023) beschreiben international einen starken Zuwachs alarmistischer Labels seit 2019. In den hier untersuchten deutschsprachigen Titelseiten von 2022 bis 2025 zeigt sich dagegen keine Fortsetzung dieses Musters. Diese Abweichung bedeutet keinen Widerspruch im strengen Sinn, sondern verweist auf unterschiedliche Untersuchungsfenster, Samples und nationale Medienlogiken (Lück et al., 2018).

### 4.2 Interpretation der drei Trends

Erstens bleibt Klimakrise im Zeitverlauf weitgehend stabil. Das liefert im untersuchten Zeitraum keinen Hinweis auf eine fortlaufende Eskalation der Krisenrhetorik.

Zweitens steigt Klimawandel deutlich. Das kann auf sprachliche Normalisierung, redaktionelle Standardisierung oder strategische Anschlussfähigkeit an ein breiteres Publikum hindeuten. Eine plausible, aber hier nicht getestete Erklärung ist eine stärkere Orientierung an anschlussfähigen Standardbegriffen.

Drittens sinkt Klimaschutz relativ stark. Das deutet auf eine Verschiebung von lösungsbezogenen Begriffen zu problembeschreibenden Begriffen hin. Diese Entwicklung ist relevant, weil Kommunikationsforschung zeigt, dass Frame-Wirkungen je nach Problem- versus Handlungsfokus unterschiedlich ausfallen können (Abstract Feldman & Hart, 2021; Stoknes, 2014).

### 4.3 Aussagekraft und Grenzen der Befunde

Die Arbeit erlaubt robuste deskriptive Aussagen zur Begriffsverteilung auf Titelseiten im untersuchten Panel. Sie zeigt, wie sich die Verwendung der zentralen Klima-Komposita im Zeitverlauf verschiebt, ohne daraus kausale Wirkzusammenhänge ableiten zu können. Aussagen darüber, warum Redaktionen bestimmte Begriffe wählen, wären mit dieser Datenbasis zu weitreichend. Plausibler ist eine Kombination aus redaktionellen Richtlinien, politischen Ereignissen und länderspezifischen Öffentlichkeiten (Carrington, 2019; McHugh et al., 2021).

### 4.4 Handlungsempfehlungen

1. Erweiterung auf Volltextdaten, um Titelseiten- und Artikelsprachgebrauch systematisch zu vergleichen.
2. Ergänzung um quellen-spezifische Zeitreihen, um Unterschiede zwischen Medientypen sichtbar zu machen.
3. Kombination mit qualitativer Redaktionsforschung, um Begriffsentscheidungen nachvollziehen zu können.
4. Anschlussanalyse für 2025+, um zu prüfen, ob Stabilität von Klimakrise anhält oder kippt.

## Anhang

### A1: Absolute Häufigkeiten (Grafik)

![Grafik 3: Absolute Häufigkeiten](../data_output/plots/grafik_3_absolute_haeufigkeiten.png)

*Abbildung 3: Absolute Häufigkeiten der drei Klima-Komposita im Gesamtzeitraum (2022–2025).*

### A2: Quartalsweise Häufigkeiten (absolute Zählungen)

Vollständige Quartalsdaten als Grundlage der Ergebnisdarstellung (Notebook 06, Analyse 2b):

| Quartal | Klimakrise | Klimaschutz | Klimawandel | Gesamt |
|---------|----------:|------------:|------------:|-------:|
| 2022Q2 | 592 | 1.120 | 1.167 | 2.879 |
| 2022Q3 | 1.102 | 1.273 | 2.081 | 4.456 |
| 2022Q4 | 877 | 1.424 | 1.547 | 3.848 |
| 2023Q1 | 1.044 | 1.257 | 1.779 | 4.080 |
| 2023Q2 | 956 | 1.489 | 1.715 | 4.160 |
| 2023Q3 | 916 | 1.142 | 2.141 | 4.199 |
| 2023Q4 | 789 | 851 | 1.762 | 3.402 |
| 2024Q1 | 536 | 564 | 1.488 | 2.588 |
| 2024Q2 | 766 | 754 | 2.018 | 3.538 |
| 2024Q3 | 643 | 542 | 1.857 | 3.042 |
| 2024Q4 | 876 | 824 | 1.900 | 3.600 |
| 2025Q1 | 185 | 223 | 467 | 875 |
| **Gesamt** | **9.282** | **11.463** | **19.922** | **40.667** |

### A3: Quartalsweise relative Anteile (%)

| Quartal | Klimakrise % | Klimaschutz % | Klimawandel % |
|---------|-------------:|--------------:|---------------:|
| 2022Q2 | 20,6 | 38,9 | 40,5 |
| 2022Q3 | 24,7 | 28,6 | 46,7 |
| 2022Q4 | 22,8 | 37,0 | 40,2 |
| 2023Q1 | 25,6 | 30,8 | 43,6 |
| 2023Q2 | 23,0 | 35,8 | 41,2 |
| 2023Q3 | 21,8 | 27,2 | 51,0 |
| 2023Q4 | 23,2 | 25,0 | 51,8 |
| 2024Q1 | 20,7 | 21,8 | 57,5 |
| 2024Q2 | 21,7 | 21,3 | 57,0 |
| 2024Q3 | 21,1 | 17,8 | 61,1 |
| 2024Q4 | 24,3 | 22,9 | 52,8 |
| 2025Q1 | 21,1 | 25,5 | 53,4 |

### A4: Neutral-deskriptiv vs. alarmistisch pro Quartal (%)

Zweikategorien-Vergleich Klimawandel (neutral) vs. Klimakrise (alarmistisch):

| Quartal | Neutral (Klimawandel) % | Alarmistisch (Klimakrise) % |
|---------|------------------------:|----------------------------:|
| 2022Q2 | 66,3 | 33,7 |
| 2022Q3 | 65,4 | 34,6 |
| 2022Q4 | 63,8 | 36,2 |
| 2023Q1 | 63,0 | 37,0 |
| 2023Q2 | 64,2 | 35,8 |
| 2023Q3 | 70,0 | 30,0 |
| 2023Q4 | 69,1 | 30,9 |
| 2024Q1 | 73,5 | 26,5 |
| 2024Q2 | 72,5 | 27,5 |
| 2024Q3 | 74,3 | 25,7 |
| 2024Q4 | 68,4 | 31,6 |
| 2025Q1 | 71,6 | 28,4 |

### A5: Datenbankschema (ER-Diagramm)

Die Analysedatenbank `dwh_data.db` enthält drei persistente Tabellen in zwei Verarbeitungsstufen. Das ER-Diagramm zeigt die zentrale Entität `newspapers` als Zeitung-Tag-Ebene sowie die beiden Kontexttabellen für Roh- und aufbereitete Trefferkontexte.

| Tabelle | Stufe | Zeilen | Schlüssel |
|---------|-------|-------:|-----------|
| `newspapers` | Bronze | 58.775 | `newspaper_id` (PK), `(newspaper_name, data_published)` Nat.-Key |
| `context` | Bronze | 172.610 | `context_id` (PK), `newspaper_id` (FK) |
| `context_processed` | Silver | 172.610 | `newspaper_id` (FK), + `suffix_lemma` |

![ER-Diagramm der Analysedatenbank](<ER diagramm wortwandel.svg>)

Der natürliche Schlüssel in `newspapers` verhindert doppelte Zeitung-Tag-Einträge bei wiederholten Importläufen. `context_processed` erweitert die Rohkontexte um die in Notebook 05 gebildeten Lemma-Cluster und bildet damit die Grundlage für die Silver-Analysen.

### A6: Notebook-Ablauf

Der Projektaufbau trennt den reproduzierbaren Kernlauf der Studienarbeit von optionalen Robustheits- und Diagnoseauswertungen. Die Rohdaten werden zunächst in die Bronze-Tabellen `newspapers` und `context` überführt, anschließend in `context_processed` als Silver-Analysebasis aufbereitet und schließlich in den Analyse- und Vergleichsnotebooks ausgewertet.

![Projektaufbau und Notebook-Ablauf](<projektaufbau.png>)

Kernlauf für die Studienarbeit: **01 → 02 → 03 → 04 → 05 → 06**.

## Quellenverzeichnis

Carrington, D. (2019, 17. Mai). Why the Guardian is changing the language it uses about the environment. The Guardian. https://www.theguardian.com/environment/2019/may/17/why-the-guardian-is-changing-the-language-it-uses-about-the-environment

Duden. (2025a). Klimawandel. https://www.duden.de/rechtschreibung/Klimawandel

Duden. (2025b). Klimakrise. https://www.duden.de/rechtschreibung/Klimakrise

Duden. (2025c). Klimaschutz. https://www.duden.de/rechtschreibung/Klimaschutz

Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. Journal of Communication, 43(4), 51-58. https://doi.org/10.1111/j.1460-2466.1993.tb01304.x

Feldman, L. A., & Hart, P. S. (2021). Upping the ante? The effects of emergency and crisis framing in climate change news. Climatic Change, 169, 31. https://doi.org/10.1007/s10584-021-03219-5

Haueis, P. (2024). Climate concepts for supporting political goals of mitigation and adaptation: The case for climate crisis. WIREs Climate Change, 15(5), e893. https://doi.org/10.1002/wcc.893

IPCC. (2023). AR6 synthesis report: Climate change 2023. https://www.ipcc.ch/2023/03/20/press-release-ar6-synthesis-report/

Lück, J., Wozniak, A., & Wessler, H. (2018). Counterbalancing global media frames with nationally colored narratives: A comparative study of news narratives and news framing in the climate change coverage of five countries. Journalism, 19(12), 1635-1656. https://doi.org/10.1177/1464884916680372

McHugh, L. H., Lemos, M. C., & Morrison, T. H. (2021). Risk? Crisis? Emergency? Implications of the new climate emergency framing for governance and policy. WIREs Climate Change, 12(6), e736. https://doi.org/10.1002/wcc.736

Schäfer, M. S., Hase, V., Mahl, D., & Krayss, X. (2023). From climate change to climate crisis? Bergen Language and Linguistics Studies, 13(1), 161-183. https://doi.org/10.15845/bells.v13i1.3980

Stoknes, P. E. (2014). Rethinking climate communications and the climate crisis: A public health perspective. Energy Research & Social Science, 1, 161-170. https://doi.org/10.1016/j.erss.2014.03.007
