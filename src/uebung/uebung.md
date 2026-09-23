#  Mocking

1. **Test-Double**: Was ist das? Nennen Sie Stub, Fake und Mock jeweils in einem Satz.
  Stub: ist ein rückgabewert der vordefiniert wurde.
  Fake: z.b. für Eine db die nur im memory ist und nicht eine echte anbindung
  Mock: ist einfach bei einer Api das es mit vordefinierte antworten zurück gibt.
2. `Mock()`: Wie erzeugt man einen Mock, und wie legt man fest, was er zurückgibt (`return_value`)?

xxx = Mock()
3. `side_effect`: Wozu dient `side_effect`?
  Dynamische Antworten
4. **Aufrufe prüfen**: Was bewirken `assert_called_once_with(...)` und `assert_not_called()`?
  Ob die funktion nur einmal aufgerufen wurde
5. `spec`: Was bewirkt `Mock(spec=MeineKlasse)`, und warum ist das nützlich?
  Verhindert rechtschreibfehler

# Problem beheben: Debugging-Protokoll (Mangel M-01)

**Fehlermeldung:**

```text
avg = s / len(e)
```

**Fundstelle (Datei, Zeile):** line 29

**Ursache:** es wird versucht durch 0 zu telen

**Gewählte Korrekturmassnahme und Begründung:** vorher schon eine abbruch bedingung zum schauen ob die liste leer ist

# Code Review

- Code lesen und Mängel notieren
  - Mindestens 3 Stellen nennen, die verbessert werden sollten und das Testen erschweren.

# Unit-Test

- **Datei wird genau einmal mit dem korrekten Modus gelesen**
  - Mock mit `assert_called_once_with("pro")` prüfen.
- **Datum**
  - Datum als Parameter übergeben, z. B. `date(2026, 9, 23)`, und auf `"23.09.2026"` prüfen.
- **Durchschnitt**
  - `durchschnitt()` direkt aufrufen und mit `@pytest.mark.parametrize` testen.

---

# Probeaufgaben (zu `bericht.py`)

Weitere Unit-Tests für `report()` in `tests/unit/test_uebung.py`. Datei weiterhin mit `mock_open` mocken.

## P1 – Berichtstext enthält Modus und Namen

- `read_data='[{"name": "Alice", "score": 90}]'`
- `report("pro")` aufrufen
- Rückgabe prüfen: enthält `"Bericht pro"` und `"Alice"` und `"90"`

## P2 – Durchschnitt im Bericht

- `read_data='[{"name": "A", "score": 10}, {"name": "B", "score": 20}]'`
- `report("medium")` aufrufen
- Rückgabe prüfen: enthält `"Durchschnitt: 15.0"`
- und `open` wurde mit `"uebung/daten/medium.json"` aufgerufen

## P3 – Leere Liste → ZeroDivisionError (Mangel M-01)

- `read_data='[]'`
- mit `pytest.raises(ZeroDivisionError)` prüfen, dass `report("classic")` abstürzt
  (Division durch `len(e)` in Zeile 29)

## P4 – Alle drei Modi (parametrize)

- mit `@pytest.mark.parametrize("modus", ["classic", "medium", "pro"])`
- für jeden Modus `report(modus)` aufrufen (Datei mocken)
- prüfen: `open` mit `f"uebung/daten/{modus}.json"` und `encoding="utf-8"`

