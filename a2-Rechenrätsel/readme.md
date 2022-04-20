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

*program.py*

**def is_sum_of_list_items(i: int, lst: List[int], add_action: Callable = lambda i, j: i-j) -> bool**
> Gibt als Wahrheitswert zurück, ob `i` durch aufrufen von `add_action` mit elementen von `lst` erreicht werden kann.

**def cancelling_muls_divs_in_summand(summands)**
> Checkt, ob es in einem Summand sich kürzende Multiplikationen/Divisionen gibt (eg. `9*9/3/3`)

**def xnx_case(challenge)**
> Prüft, dass es keinen Fall wie z.B. `3*4+3` oder `5*6*7+6*5` gibt

**def check_challenge(challenge: str) -> Union[None, str]**
> Uberfrüft das Rätsel auf Eindeutigkeit und gibt das Ergebnis zurück

**def generate_challenge(length: int = 5) -> Generator[str, None, None]**
> Generiert mögliche Rätsel (noch unüberprüft)

**def get_challenge(length: int = 5) -> str**
> Gibt ein eindeutiges Rätsel mit Ergebnis zurück

## Umsetzung

Das Programm ist in der Sprache Python umgesetzt. Der Aufgabenordner enthält neben dieser Dokumentation eine ausführbare Python-Datei. Diese Datei ist mit einer Python-Umgebung ab der Version `3.8` ausführbar.

Wird das Programm gestartet, wird zuerst eine Eingabe in Form einer einstelligen Zahl erwartet, um ein bestimmtes Beispiel auszuwählen. *(Das heißt: `0` für Beispiel `muellabfuhr0.txt`)*

Nun wird die Logik des Programms angewandt und die Ausgabe erscheint in der Kommandozeile.

## Beispiele

Hier wird das Programm auf die neun Beispiele aus dem Git-Repo, und ein eigenes angewendet:

---

Rätsel von Länge `2`

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
