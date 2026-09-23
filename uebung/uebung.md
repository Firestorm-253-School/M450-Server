# Mocking

1. **Test-Double**: Was ist das? Nennen Sie Stub, Fake und Mock jeweils in einem Satz.
2. **`Mock()`**: Wie erzeugt man einen Mock, und wie legt man fest, was er zurückgibt (`return_value`)?
3. **`side_effect`**: Wozu dient `side_effect`?
4. **Aufrufe prüfen**: Was bewirken `assert_called_once_with(...)` und `assert_not_called()`?
5. **`spec`**: Was bewirkt `Mock(spec=MeineKlasse)`, und warum ist das nützlich?


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