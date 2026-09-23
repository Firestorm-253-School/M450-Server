from ast import Raise
import pytest
from datetime import date
from unittest.mock import patch, mock_open
from uebung.bericht import report


@patch("builtins.open", new_callable=mock_open, read_data='[{"name": "A", "score": 10}, {"name": "B", "score": 20}]')
def test_medium_wird_korrekt_gelesen_medium(mock_file):
    ergebnis = report("medium")
    mock_file.assert_called_once_with("uebung/daten/medium.json", encoding="utf-8")
    assert "Bericht medium" in ergebnis
    assert "A" in ergebnis
    assert "10" in ergebnis   
    assert "Durchschnitt: 15.0" in ergebnis


def test_time():
    d = date(2026, 9, 23)
    assert d.strftime("%d.%m.%Y") == "23.09.2026"


def durchschnit(werte):
    return sum(werte)/len(werte)

@pytest.mark.parametrize(
    "werte, erwartet",
    [
        ([10, 20, 30], 20.0),
        ([5], 5.0),
        ([0, 100], 50.0),
    ],
)

def test_durchschnit(werte, erwartet):
    assert durchschnit(werte) == erwartet


@patch("builtins.open", new_callable=mock_open, read_data='[]')
def test_classic_wird_korrekt_gelesen_classic(mock_file):
    with pytest.raises(ZeroDivisionError):
        report("classic")


    