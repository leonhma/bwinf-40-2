# Rechenrätsel

❔ A2 👤 61015 🧑 Leonhard Masche 📆 11.04.2022

## Inhaltsverzeichnis

1. [Lösungsidee](#lösungsidee)
    1. [Verbesserungen](#verbesserungen)
    2. [Aufbau](#aufbau)
2. [Umsetzung](#umsetzung)
3. [Beispiele](#beispiele)
4. [Quellcode](#quellcode)

## Lösungsidee

Zuerst wird ein zufälliges Rechenrätsel von gewünschter Länge generiert.
Dieses Rätsel wird nach dem Prinzip von rejection sampling auf mehrere Kriterien getestet:

- Keine Multiplikation/Division mit 1
    > Beide haben den gleichen Effekt und sind somit nicht eindeutig
- Keine Zahl gefolgt von derselben
    > Vorgabe der Aufgabe
- Kein 'x*n+x'-Muster
    > Schließt fälle wie `3*4+3` oder `7*4*6*3+4*7` aus
- Keine sich-aufhebenden Multiplikationen/Divisionen in den Summanden
    > Schließt z.B. `5/2*4/2` aus
- Keine sich-aufhebenden Additionen/Subtraktionen im Rätsel
    > Schließt Fälle wie `1+4-4` und `3+6/3+1-8/4` aus
- Keine nicht-Integer Zwischenergebnisse
- Kein negatives Ergebnis

### Verbesserungen

#### Effizienz

Um die beiden häufigsten Fehler in den Rätseln zu verhindern, werden die `Division/Multiplikation mit 1`, die `nicht-Integer Zwischenergebnisse` und `eine Zahl gefolgt von derselben` schon während der Generierung verhindert.

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
