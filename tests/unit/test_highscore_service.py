import pytest

from snake_game_server.services.highscore_service import normalisiere, speichere


# -------- T1 --------

@pytest.mark.parametrize(
    "modus, expected",
    [
        ("CLASSIC", "classic"),
        ("medium", "medium"),
        ("Pro", "pro"),
        ("MedIUm", "medium"),
    ],
)
def test_normalisiere_valid_modis(modus: str, expected: str):
    result = normalisiere(modus)

    assert result == expected


def test_normalisiere_invalid_modus_type():
    with pytest.raises(TypeError):
        normalisiere(0.3)

@pytest.mark.parametrize(
    "modus",
    [
        "randomShit",
        "MMEDIUM"
    ],
)
def test_normalisiere_invalid_modus_unknown(modus):
    with pytest.raises(ValueError):
        normalisiere(modus)



# -------- T2 --------

@pytest.mark.parametrize(
    "name, score, modus",
    [
        ("Laurin", 10, "classic"),
        ("Janick", 5, "pro")
    ],
)
def test_speichere_valid(name: str, score: int, modus: str):
    result = speichere(name, score, modus)

    assert result is not None

    
def test_speichere_invalid_name_type():
    with pytest.raises(TypeError):
        speichere(0.5, 10, "classic")


def test_speichere_invalid_score_type():
    with pytest.raises(TypeError):
        speichere("Laurin", 3.5, "classic")


# -------- T3 --------
...