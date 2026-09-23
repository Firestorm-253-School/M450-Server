# Mocking & Unit-Test – Syntax mit pytest

Alles als `pytest`-Tests. Mocks kommen aus `unittest.mock` (Standard), die Tests selbst sind reine pytest-Syntax.

Ausführen:

```bash
pytest uebung/ -v
```

---

## 1. Import

```python
import pytest
from datetime import date
from unittest.mock import Mock, MagicMock, patch, mock_open
```

---

## 2. `Mock()` und `return_value`

```python
def test_mock_return_value():
    mock_repo = Mock()
    mock_repo.get_score.return_value = 42

    assert mock_repo.get_score() == 42
    assert mock_repo.get_score("Alice") == 42  # immer derselbe Wert
```

Mit `MagicMock` (z. B. Datei / Context Manager):

```python
def test_magic_mock_file():
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = '{"name": "Ada"}'

    with mock_file as f:
        assert f.read() == '{"name": "Ada"}'
```

---

## 3. `side_effect` – dynamische Antworten

```python
def test_side_effect_liste():
    mock_api = Mock()
    mock_api.fetch.side_effect = [10, 20, 30]

    assert mock_api.fetch() == 10
    assert mock_api.fetch() == 20
    assert mock_api.fetch() == 30


def test_side_effect_exception():
    mock_api = Mock()
    mock_api.fetch.side_effect = ValueError("kaputt")

    with pytest.raises(ValueError, match="kaputt"):
        mock_api.fetch()


def test_side_effect_funktion():
    mock_api = Mock()
    mock_api.fetch.side_effect = lambda x: x * 2

    assert mock_api.fetch(5) == 10
```

| | `return_value` | `side_effect` |
|---|---|---|
| Zweck | immer derselbe Wert | Liste, Exception oder Funktion |
| Wann | einfacher Stub | wechselnde / abhängige Antworten |

---

## 4. Aufrufe prüfen

```python
def test_assert_called_once_with():
    mock_db = Mock()
    mock_db.save("pro", 100)

    mock_db.save.assert_called_once_with("pro", 100)


def test_assert_not_called():
    mock_db = Mock()
    mock_db.save("pro", 100)

    mock_db.delete.assert_not_called()


def test_call_count():
    mock_db = Mock()
    mock_db.save("pro", 100)
    mock_db.save("classic", 50)

    assert mock_db.save.call_count == 2
    mock_db.save.assert_any_call("pro", 100)
```

---

## 5. `spec` – Mock an Klasse binden

```python
class PlayerService:
    def get_player(self, player_id: int):
        ...


def test_mock_mit_spec():
    mock_service = Mock(spec=PlayerService)

    mock_service.get_player(1)  # OK

    with pytest.raises(AttributeError):
        mock_service.get_playerr(1)  # Tippfehler fällt auf
```

---

## 6. `@patch` in pytest

Decorator (Argument = Mock, Reihenfolge von unten nach oben):

```python
@patch("builtins.open", new_callable=mock_open, read_data="[]")
def test_patch_decorator(mock_file):
    with open("datei.json", encoding="utf-8") as f:
        assert f.read() == "[]"

    mock_file.assert_called_once_with("datei.json", encoding="utf-8")
```

Als Context Manager (oft klarer in pytest):

```python
def test_patch_context_manager():
    with patch("modul.funktion") as mock_fn:
        mock_fn.return_value = 5

        assert mock_fn() == 5
        mock_fn.assert_called_once_with()
```

---

## 7. Unit-Tests laut Aufgabe

### Datei genau einmal mit korrektem Modus

```python
@patch("builtins.open", new_callable=mock_open, read_data='[{"name":"A","score":10}]')
def test_datei_einmal_gelesen(mock_file):
    # report("pro") aufrufen ...
    mock_file.assert_called_once_with("uebung/daten/pro.json", encoding="utf-8")
```

### Datum als Parameter

```python
def test_datum_formatierung():
    d = date(2026, 9, 23)
    assert d.strftime("%d.%m.%Y") == "23.09.2026"
```

### Durchschnitt mit `@pytest.mark.parametrize`

```python
def durchschnitt(werte):
    return sum(werte) / len(werte)


@pytest.mark.parametrize(
    "werte, erwartet",
    [
        ([10, 20, 30], 20.0),
        ([5], 5.0),
        ([0, 100], 50.0),
    ],
)
def test_durchschnitt(werte, erwartet):
    assert durchschnitt(werte) == erwartet
```

---

## 8. Mini-Beispiel alles zusammen

```python
def hole_highscore(repo, name: str) -> int:
    return repo.get(name)


def test_hole_highscore():
    repo = Mock(spec=["get"])
    repo.get.return_value = 99

    assert hole_highscore(repo, "Ada") == 99
    repo.get.assert_called_once_with("Ada")


def test_delete_wird_nicht_aufgerufen():
    repo = Mock(spec=["get", "delete"])
    repo.get.return_value = 99

    hole_highscore(repo, "Ada")

    repo.delete.assert_not_called()
```

---

## 9. pytest-Extras (häufig nützlich)

```python
# Exception erwarten
def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0


# Fixture: gemeinsames Setup
@pytest.fixture
def mock_repo():
    repo = Mock()
    repo.get.return_value = 10
    return repo


def test_mit_fixture(mock_repo):
    assert mock_repo.get("Ada") == 10
    mock_repo.get.assert_called_once_with("Ada")
```

---

## Kurzreferenz

| Syntax | Bedeutung |
|--------|-----------|
| `def test_...():` | pytest erkennt den Test |
| `assert ...` | pytest-Assertion |
| `pytest.raises(...)` | Exception prüfen |
| `@pytest.mark.parametrize` | mehrere Fälle, ein Test |
| `@pytest.fixture` | wiederverwendbares Setup |
| `Mock()` / `return_value` | fester Rückgabewert |
| `side_effect` | Liste / Exception / Funktion |
| `assert_called_once_with(...)` | genau 1× mit diesen Args |
| `assert_not_called()` | nie aufgerufen |
| `Mock(spec=...)` | nur echte Attribute |
| `@patch(...)` / `with patch(...)` | Abhängigkeit ersetzen |
