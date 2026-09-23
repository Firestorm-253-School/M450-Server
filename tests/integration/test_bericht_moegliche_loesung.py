from datetime import date
from unittest.mock import Mock

import pytest

from uebung.bericht import (
    HighscoreDatei,
    beste,
    durchschnitt,
    erstelle_bericht,
    formatiere,
)

HEUTE = date(2026, 9, 23)


def viele_eintraege(anzahl):
    eintraege = []

    for i in range(anzahl):
        eintrag = {"name": "S" + str(i), "score": i}
        eintraege.append(eintrag)

    return eintraege


@pytest.fixture
def datei():
    datei = Mock(spec=HighscoreDatei)
    datei.lade.return_value = [
        {"name": "Anna", "score": 120, "modus": "pro"},
        {"name": "Cem", "score": 140, "modus": "pro"},
        {"name": "Ben", "score": 95, "modus": "pro"},
    ]
    return datei


def test_bericht_nennt_den_besten_spieler_zuerst(datei):
    text = erstelle_bericht("pro", datei, HEUTE)

    assert "1. Cem 140" in text
    assert "2. Anna 120" in text


def test_bericht_liest_die_datei_genau_einmal(datei):
    erstelle_bericht("pro", datei, HEUTE)

    datei.lade.assert_called_once_with("pro")


def test_bericht_hat_immer_dasselbe_datum(datei):
    text = erstelle_bericht("pro", datei, HEUTE)

    assert text.startswith("Bericht pro vom 23.09.2026")


def test_bericht_zeigt_den_durchschnitt(datei):
    text = erstelle_bericht("pro", datei, HEUTE)

    assert "Durchschnitt: 118.3" in text


def test_m01_modus_ohne_spiele_stuerzt_nicht_ab():
    datei = Mock(spec=HighscoreDatei)
    datei.lade.return_value = []

    text = erstelle_bericht("pro", datei, HEUTE)

    assert "Noch keine Spiele" in text


def test_beste_sortiert_absteigend():
    eintraege = [{"name": "Anna", "score": 120}, {"name": "Cem", "score": 140}]

    ergebnis = beste(eintraege)

    assert ergebnis[0]["name"] == "Cem"
    assert ergebnis[1]["name"] == "Anna"


def test_beste_liefert_hoechstens_drei():
    eintraege = viele_eintraege(10)

    assert len(beste(eintraege)) == 3


def test_durchschnitt_leer():
    assert durchschnitt([]) == 0.0


def test_durchschnitt_ein_eintrag():
    eintraege = [{"score": 10}]

    assert durchschnitt(eintraege) == 10.0


def test_durchschnitt_zwei_eintraege():
    eintraege = [{"score": 10}, {"score": 20}]

    assert durchschnitt(eintraege) == 15.0


def test_durchschnitt_wird_gerundet():
    eintraege = [{"score": 10}, {"score": 11}]

    assert durchschnitt(eintraege) == 10.5


def test_formatiere_listet_hoechstens_drei_eintraege():
    eintraege = viele_eintraege(10)

    text = formatiere("pro", eintraege, HEUTE)

    assert text.count("\n") == 5