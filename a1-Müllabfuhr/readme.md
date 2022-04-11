# Müllabfuhr

❔ A1 👤 61015 🧑 Leonhard Masche 📆 10.04.2022

## Inhaltsverzeichnis

1. [Lösungsidee](#lösungsidee)
    1. [Verbesserungen](#verbesserungen)
    2. [Aufbau](#aufbau)
2. [Umsetzung](#umsetzung)
3. [Beispiele](#beispiele)
4. [Quellcode](#quellcode)

## Lösungsidee

Zuerst wird das Straßennetz in einer Adjacency-List Datenstruktur gespeichert. Nun wird von der Basis (Vertex 0) ausgehend ein modifizierter Breadth-First-Search Algorithmus verwendet, um die in Frage kommenden Routen zu erhalten. Der Algorithmus speichert die aktuelle Node zusammen mit dem Pfad der bis dorthin beschritten wurde in `visited`, und zeichnet alle Möglichkeiten von der derzeitigen Node weiterzugehen (rückwärtsgehen ausgeschlossen), zusammen mit der dann entstehenden Länge des Pfades auf. Wenn ein Pfad auf eine Vertex aus dem `visited`-Set trifft, wird der jetzige Pfad mit dem in `visited` gespeicherten Pfad zusammengefügt und als Ergebnis des Algorithmus in der Liste `paths` gespeichert. Wenn alle Straßen vom Algorithmus abgedeckt wurden, ist dieser Schritt fertig.

Nun ist allerdings nicht garantiert, dass `paths` die richtige Länge (z.B. 5 Tage) hat.
Deshalb werden, solange die Länge von `paths` größer als die Anzahl der Tage ist, die beiden kürzesten Pfade kombiniert. Somit wird eine zu lange Liste verkürzt. Ist sie jedoch zu kurz, wird sie mit Nullen (Wagen bleibt in der Zentrale) aufgefüllt.

### Verbesserungen

#### Nicht-Integer Gewichte

Eine vorgenommene Verbesserung ist das Einlesen von Fließkommazahl-Gewichtungen der Straßen. Es ist unrealistisch dass in einem echten Szenario Straßen eine Länge von z.B. genau 480m haben. Um das zu implementieren wird der dritte Wert aus den Beispieldateien als
<i style="color:orange">float</i>
eingelesen.

#### Arbiträre Anzahl Tage

Auch kann eine Anzahl an Tagen eingegeben werden, für die geplant werden soll. So kann zum Beipiel ein Fahrplan für zwei Wochen erstellt werden. Dazu werden einfach die merging- und padding-Schritte am Ende der `get_paths` Funktion angepasst.

#### (Einbahnstraßen)

Die Repräsentation als adjacency-list lässt theoretisch auch das Implementieren von Einbahnstraßen zu. Da das aber ein anderes Format der Beispieldaten erfordern würde, ist diese Funktion nicht einfach realisierbar.

### Aufbau

*utility.py*

**def remove_by_exp(exp: Callable[[Any], bool], lst: List)**
> Removes the first item from the list where `exp` evaluates to true (inplace modification).

<br>

*citygraph.py*

**class CityGraph**
> Klasse die ein Straßennetz (ungerichteter gewichteter Graph) repräsentiert.

**def __init\_\_(vertices: List[int], edges: List[Tuple[int, int, float]])**
> Initialisiert den CityGraph mit einer Liste der Vertices und der adjacency-list.

**@classmethod <br> def _from_bwinf_file(path: str) -> 'CityGraph'**
> Liest eine Beispieldatei ein, und gibt einen CityGraph zurück.

**def _contains_all_edges(paths: Iterable[Iterable[int]]) -> bool**
> Gibt als Wahrheitswert zurück, ob die gegebene Liste an Pfaden alle 'Straßen' im Graph abdeckt.

**def get_paths(days: int = 5) -> List[Tuple[float, Tuple[int, ...]]]**
> Gibt eine Liste zurück, die Tuples mit dem Pfad, und der Länge dessen an erster Stelle, enthält.

## Umsetzung

Das Programm ist in der Sprache Python umgesetzt. Der Aufgabenordner enthält neben dieser Dokumentation eine ausführbare Python-Datei. Diese Datei ist mit einer Python-Umgebung ab der Version `3.6` ausführbar.

Wird das Programm gestartet, wird zuerst eine Eingabe in Form einer einstelligen Zahl erwartet, um ein bestimmtes Beispiel auszuwählen. *(Das heißt: `0` für Beispiel `muellabfuhr0.txt`)*

Nun wird die Logik des Programms angewandt und die Ausgabe erscheint in der Kommandozeile.

## Beispiele

Hier wird das Programm auf die neun Beispiele aus dem Git-Repo, und ein eigenes angewendet:

---

`FILENAME0.txt`

```
CONTENT
```

Ausgabe zu `FILENAME0.txt`

```
OUTPUT
```

## Quellcode

```python
CODE

```
