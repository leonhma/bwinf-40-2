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

Das Programm ist in der Sprache Python umgesetzt. Der Aufgabenordner enthält neben dieser Dokumentation eine ausführbare Python-Datei `program.py`. Diese Datei ist mit einer Python-Umgebung ab der Version `3.8` ausführbar.

Wird das Programm gestartet, wird zuerst eine Eingabe in Form einer einstelligen Zahl erwartet, um die Länge des gewünschten Rätsels auszuwählen. Auf meinem chromebook lassen sich Rätsel bis zur Länge `22` in unter fünf Sekunden generieren.

Nun wird die Logik des Programms angewandt und die Ausgabe erscheint in der Kommandozeile.

## Beispiele

Hier werden Rätsel der Länge 2, 3, 7, 15 und 22 generiert:

---

Rätsel von Länge `2`

```
+5+2=7
5◦2=7
```

---

Rätsel von Länge `3`

```
+4-2-1=1
4◦2◦1=1
```

---

Rätsel von Länge `7`

```
+9*8*3*2*9-3+8=3893
9◦8◦3◦2◦9◦3◦8=3893
```

---

Rätsel von Länge `15`

```
+6*8/4+7+9*6+7-6+1+9*5-1*8*5+7=87
6◦8◦4◦7◦9◦6◦7◦6◦1◦9◦5◦1◦8◦5◦7=87
```

---

Rätsel von Länge `22`

```
+5*7*2*3*4*2+9/3*4/2*4*9-3+9/3*7-2+5*7*6+2*3=2128
5◦7◦2◦3◦4◦2◦9◦3◦4◦2◦4◦9◦3◦9◦3◦7◦2◦5◦7◦6◦2◦3=2128
```

## Quellcode

```python
from collections import Counter
from typing import Generator
from secrets import choice
from typing import Callable, List, Union

import regex as re


def is_sum_of_list_items(i: int, lst: List[int], add_action: Callable = lambda i, j: i-j) -> bool:
    """
    Check if the given number is the sum of multiple items in the given list.
    """
    if i in lst:
        return True
    for j in lst:
        new_lst = lst.copy()
        new_lst.remove(j)
        if is_sum_of_list_items(add_action(i, j), new_lst, add_action):
            return True
    return False


def cancelling_muls_divs_in_summand(summands):
    for summand in summands:
        divs = [int(x) for x in re.findall(r'(?<=\/)\d', summand)]
        muls = [int(x) for x in re.findall(r'(?<=\*)\d', summand)]

        for div in divs:
            if is_sum_of_list_items(div, muls, lambda i, j: i/j):
                return True
        for mul in muls:
            if is_sum_of_list_items(mul, divs, lambda i, j: i/j):
                return True


def xnx_case(challenge):
    parts = re.findall(
        r'(?<=[+-])(?:(?:\d\*?)+\+(?:\*?\d){2,}|(?:\d\*?){2,}\+(?:\*?\d)+)(?=[+-]|$)',
        challenge, overlapped=True)

    for part in parts:
        i = part.find('+')
        if i < (len(part)-1)/2:
            left = Counter(re.findall(r'\d', part[:i]))
            right = Counter(re.findall(r'\d', part[-i:]))
            left.subtract(right)
            if not left-Counter():
                return True
        elif i > (len(part)-1)/2:
            left = Counter(re.findall(r'\d', part[:len(part)-i]))
            right = Counter(re.findall(r'\d', part[i+1:]))
            left.subtract(right)
            if not left-Counter():
                return True


def check_challenge(challenge: str) -> Union[None, str]:
    # ---- invalid if division/multiplication by 1 ----
    if re.search(r'[/*]1', challenge):
        return

    # ---- check that there's not one number followed by the same number again
    if re.search(r'(\d)[*-+/]\1', challenge):
        return

    # ---- check for 3*4+3 case ----
    if xnx_case(challenge):
        return

    # split into summands
    summands = re.findall(r'[+-].*?(?=[+-]|$)', challenge)

    # ---- check for cancelling muls/divs in summand ----
    if cancelling_muls_divs_in_summand(summands):
        return

    # ---- calculate each summand's result while checking for non-int temporary results ----
    pluses: List[int] = []
    minuses: List[int] = []

    for summand in summands:
        sum_ = 0
        sum_ = int(summand[:2])
        if len(summand) > 2:
            for i in range(len(summand))[2::2]:
                if summand[i] == '/':
                    sum_ /= int(summand[i+1])
                elif summand[i] == '*':
                    sum_ *= int(summand[i+1])
                if sum_ % 1:
                    return

        if sum_ < 0:
            minuses.append(-int(sum_))
        elif sum_ > 0:
            pluses.append(int(sum_))

    # ---- check for cancelling summands/minuends ----
    for plus in pluses:
        if is_sum_of_list_items(plus, minuses):
            return
    for minus in minuses:
        if is_sum_of_list_items(minus, pluses):
            return

    res = sum(pluses) - sum(minuses)
    if res < 0:
        return

    return res

def generate_challenge(length: int = 5) -> Generator[str, None, None]:
    nums = (1,2,3,4,5,6,7,8,9)
    while True:
        challenge = '+' + choice('123456789')
        previous = challenge[-1]
        for _ in range(length-1):
            op = choice('*-+') if previous in '12357' else choice('*-+/')  # cant divide with primes
            challenge += op
            if op == '*':
                challenge += str(choice([num for num in nums if num != 1 and num != int(previous)]))
            elif op == '/':
                challenge += str(choice([num for num in (2,3,4,5,6,7,8,9) if int(previous) % num == 0 and num != int(previous)]))
            elif op in '+-':
                challenge += str(choice([num for num in nums if num != int(previous)]))
            previous = challenge[-1]
        yield challenge

def get_challenge(length: int = 5) -> str:
    for challenge in generate_challenge(length):
        if res := check_challenge(challenge):  # walrus
            return f'{challenge}={res}'

while True:
    try:
        i = int(input("Bitte die Länge des Rätsels eingeben: "))
        challenge = get_challenge(i)
        print(challenge)
        print(re.sub(r'[*/+-]', '◦', challenge[1:]))
    except Exception as e:
        print(e)

```
