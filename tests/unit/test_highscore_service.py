import pytest

from  snake_game_server.services.highscore_service import normalisiere, MODI

@pytest.mark.anyio
async def test_normalisiere():
    norm = await normalisiere("modus": "pro")
    assert norm(modus) == "pro"


def test_normalisiere1():
    norm = normalisiere("modus": "pro")
    print(norm)
    print(norm.modus)
    assert norm.modus() == "pro"