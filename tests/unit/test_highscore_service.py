import pytest

from snake_game_server.services import highscore_service as service

# T1: gültige Modis
@pytest.mark.parametrize("modus", ["classic", "medium", "pro"])
def test_normalisiere_akzeptiert_gueltige_modi(modus):
    assert service.normalisiere(modus) == modus

# T1: Spezialfall
def test_normalisiere_ignoriert_gross_kleinschreibung():
    assert service.normalisiere("PRO") == "pro"

# T1: ungültiger Modi
def test_normalisiere_lehnt_unbekannten_modus_ab():
    with pytest.raises(ValueError):
        service.normalisiere("extreme")

# T1: falscher Datentyp
def test_normalisiere_lehnt_falshen_datentyp_ab():
    with pytest.raises(TypeError):
        service.normalisiere(42)


@pytest.fixture(autouse=True)
def clear_highscores():
    service.highscores.clear()


# T2: gültiger Eintrag
def test_speichere_gueltigen_eintrag():
    eintrag = service.speichere("Anna", 120, "classic")

    assert eintrag == {"name": "Anna", "score": 120, "modus": "classic"}
    assert eintrag in service.highscores


# T2: ungültiger Name (leer), prüft zusätzlich, dass nichts gespeichert wurde
def test_speichere_lehnt_leeren_namen_ab():
    with pytest.raises(ValueError):
        service.speichere("", 120, "classic")

    assert service.highscores == []


# T2: ungültiger Name (unerlaubte Zeichen)
def test_speichere_lehnt_namen_mit_unerlaubten_zeichen_ab():
    with pytest.raises(ValueError):
        service.speichere("Ann@", 120, "classic")


# T2: ungültiger Name (zu lang)
def test_speichere_lehnt_zu_langen_namen_ab():
    with pytest.raises(ValueError):
        service.speichere("AbcdEfghIjklM", 120, "classic")


# T2: negativer score
def test_speichere_lehnt_negative_punktezahl_ab():
    with pytest.raises(ValueError):
        service.speichere("Anna", -5, "classic")


# T2: unbekannter Modus
def test_speichere_lehnt_unbekannten_modus_ab():
    with pytest.raises(ValueError):
        service.speichere("Anna", 120, "extreme")


# T3: keine Einträge vorhanden, kein Modus angegeben
def test_uebersicht_ohne_eintraege_zeigt_allgemeinen_hinweis():
    result = service.uebersicht()

    assert result == {"highscore": [], "hinweis": service.HINWEIS_LEER}


# T3: keine Einträge vorhanden, Modus angegeben
def test_uebersicht_ohne_eintraege_fuer_modus_zeigt_modus_hinweis():
    result = service.uebersicht("classic")

    assert result == {
        "highscore": [],
        "hinweis": service.HINWEIS_LEER_MODUS.format(modus="classic"),
    }


# T3: Einträge vorhanden, absteigend sortiert, kein Hinweis
def test_uebersicht_mit_eintraegen_sortiert_absteigend_ohne_hinweis():
    service.speichere("Anna", 50, "classic")
    service.speichere("Ben", 100, "classic")

    result = service.uebersicht()

    assert result["hinweis"] == ""
    assert [eintrag["name"] for eintrag in result["highscore"]] == ["Ben", "Anna"]


# T3: Filterung nach Modus
def test_uebersicht_filtert_nach_modus():
    service.speichere("Anna", 50, "classic")
    service.speichere("Ben", 100, "pro")

    result = service.uebersicht("pro")

    assert result["highscore"] == [{"name": "Ben", "score": 100, "modus": "pro"}]
    assert result["hinweis"] == ""


# T3: Grenzwert - Rangliste ist auf die Top 10 begrenzt
def test_uebersicht_begrenzt_auf_top_10():
    for i in range(15):
        service.speichere(f"P{i}", i, "classic")

    result = service.uebersicht()

    assert len(result["highscore"]) == 10
    assert result["highscore"][0]["score"] == 14


# T3: unbekannter Modus wird abgelehnt
def test_uebersicht_lehnt_unbekannten_modus_ab():
    with pytest.raises(ValueError):
        service.uebersicht("extreme")