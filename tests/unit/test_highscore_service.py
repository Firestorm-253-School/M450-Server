import pytest

from snake_game_server.services.highscore_service import normalisiere, speichere, uebersicht, highscores, HINWEIS_LEER, HINWEIS_LEER_MODUS

# T1
@pytest.mark.parametrize('modus', ['classic', 'medium', 'pro'])
def test_normalisiere_valid(modus):
  result = normalisiere(modus)

  assert result == modus

# T1
def test_normalisiere_case():
  modus = 'ClaSSic'

  result = normalisiere(modus)

  assert result == 'classic'

# T1
def test_normalisiere_unknown_mode():
  modus = 'ultra'

  with pytest.raises(ValueError):
    normalisiere(modus)

# T1
def test_normalisiere_invalid_datatype():
  modus = None

  with pytest.raises(TypeError):
      normalisiere(modus)
  




# T2
def test_speichere():
  name = 'Janick'
  modus = 'pro'
  score = 100

  num_highscores_before = len(highscores)

  speichere(name, score, modus)

  assert len(highscores) == num_highscores_before + 1

# T2
def test_speichere_empty_name():
  name = ''
  score = 10
  modus = 'pro'
  with pytest.raises(ValueError):
    speichere(name, score, modus)

# T2
def test_speichere_invalid_name():
  name = '.<?'
  score = 10
  modus = 'pro'
  with pytest.raises(ValueError):
    speichere(name, score, modus)

# T2
def test_speichere_name_too_long():
  name = 'HelloWorld1234'
  score = 10
  modus = 'pro'
  with pytest.raises(ValueError):
    speichere(name, score, modus)

# T2
def test_speichere_negative_score():
  name = 'Hello'
  score = -1
  modus = 'pro'
  with pytest.raises(ValueError):
    speichere(name, score, modus)

# T2
def test_speichere_unknown_mode():

  num_highscores_before = len(highscores)

  name = 'Hello'
  score = 10
  modus = 'pros'

  with pytest.raises(ValueError):
    speichere(name, score, modus)


# T3
def test_uebersicht_empty():
  modus = None

  highscores.clear

  result = uebersicht(modus)

  assert result["hinweis"] == HINWEIS_LEER

# T3
def test_uebersicht_modus_empty():
  modus = 'pro'

  highscores.clear()

  result = uebersicht(modus)

  assert result["hinweis"] == HINWEIS_LEER_MODUS

# T3
def test_uebersicht_full():
  modus = None

  for i in range(1, 15):
    highscores.append({"name": 'test', "score": 10, "modus": 'pro'})

  result = uebersicht(modus)

  assert len(result["highscore"]) == 10