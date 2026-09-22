# Prüfung 2 – Wertebereiche

Klasse: gültig, Grenzwert, ungültig (Negativfall), Spezialfall

## Funktion 1: `normalisiere_modus(modus)`

| ANF-ID | Parameter | Klasse                 | Bereich / Beschreibung                                  | Vertreter | Erwartetes Ergebnis |
| ------ | --------- | ---------------------- | ------------------------------------------------------- | --------- | ------------------- |
| ANF-02 | modus     | ungültig (Negativfall) | nicht "classic", "medium", "pro"                        | "ultra"   | ValueError          |
| ANF-01 | modus     | gültig                 | "classic", "medium", "pro"                              | "classic" | "classic"           |
| ANF-02 | modus     | ungültig (Negativfall) | kein string                                             | None      | TypeError           |
| ANF-01 | modus     | Spezialfall            | "classic", "medium", "pro" Gross / Kleinschreibung egal | "MedIuM"  | "medium"            |

## Funktion 2: `speichere(name, score, modus)`

| ANF-ID | Parameter | Klasse                 | Bereich / Beschreibung                                                                 | Vertreter       | Erwartetes Ergebnis                                     |
| ------ | --------- | ---------------------- | -------------------------------------------------------------------------------------- | --------------- | ------------------------------------------------------- |
| ANF-05 | name      | ungültig (Negativfall) | kein string                                                                            | None            | TypeError                                               |
| ANF-05 | name      | ungültig (Negativfall) | leerer string                                                                          | ""              | ValueError                                              |
| ANF-05 | name      | gültig                 | string von buchstaben und zahlen mit 1 - 12 Zeichen                                    | "H4llo"         | highscores hat ein neues element {"name": "H4llo", ...} |
| ANF-05 | name      | ungültig (Negativfall) | string von buchstaben und zahlen ab 13 Zeichen                                         | "HelloWorld123" | ValueError                                              |
| ANF-05 | name      | ungültig (Negativfall) | string mit 1 - 12 Zeichen (enthält mindestens ein (nicht buchstabe oder zahl)-Zeichen) | ",.=?"          | ValueError                                              |
| ANF-05 | score     | ungültig (Negativfall) | kein string                                                                            | None            | TypeError                                               |
| ANF-05 | score     | gültig (Grenzwert)     | positive Zahl                                                                          | 0               | ValueError                                              |
| ANF-05 | score     | gültig (Grenzwert)     | positive Zahl                                                                          | 10              | highscores hat ein neues element {"score": 10, ...}     |
| ANF-05 | score     | Spezialfall (ungültig) | bool                                                                                   | True            | Type Error                                              |

======================================================================= test session starts =======================================================================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\janic\Desktop\Development\school\M450-Server\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\janic\Desktop\Development\school\M450-Server
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.15.1, cov-7.1.0
collected 37 items

tests/integration/test_highscore_api.py::test_sortiert_absteigend ERROR [ 2%]
tests/unit/test_game.py::test_move_advances_head_in_current_direction PASSED [ 5%]
tests/unit/test_game.py::test_move_keeps_body_length_constant PASSED [ 8%]
tests/unit/test_game.py::test_set_direction_ignores_reversal PASSED [ 10%]
tests/unit/test_game.py::test_set_direction_allows_turn PASSED [ 13%]
tests/unit/test_game.py::test_head_hits_wall_at_left_border PASSED [ 16%]
tests/unit/test_game.py::test_head_hits_wall_at_right_border PASSED [ 18%]
tests/unit/test_game.py::test_head_hits_wall_false_when_inside PASSED [ 21%]
tests/unit/test_game.py::test_head_hits_wall_detects_inner_obstacle PASSED [ 24%]
tests/unit/test_game_service.py::test_set_direction_does_not_move_immediately[asyncio] PASSED [ 27%]
tests/unit/test_game_service.py::test_set_direction_starts_a_tick_loop_that_moves_the_snake[asyncio] PASSED [ 29%]
tests/unit/test_game_service.py::test_tick_loop_ends_game_when_head_touches_border[asyncio] PASSED [ 32%]
tests/unit/test_game_service.py::test_create_game_uses_requested_map[asyncio] PASSED [ 35%]
tests/unit/test_game_service.py::test_tick_loop_ends_game_when_head_hits_inner_wall[asyncio] PASSED [ 37%]
tests/unit/test_game_service.py::test_set_direction_rejects_unknown_direction[asyncio] PASSED [ 40%]
tests/unit/test_game_service.py::test_handle_message_create_game[asyncio-message0] PASSED [ 43%]
tests/unit/test_game_service.py::test_handle_message_join_game[asyncio-message0-True] PASSED [ 45%]
tests/unit/test_game_service.py::test_handle_message_join_game[asyncio-message1-False] PASSED [ 48%]
tests/unit/test_game_service.py::test_handle_message_leave_game[asyncio-False] PASSED [ 51%]
tests/unit/test_game_service.py::test_handle_message_leave_game[asyncio-True] PASSED [ 54%]
tests/unit/test_game_service.py::test_handle_message_unknown_type_returns_none[asyncio] PASSED [ 56%]
tests/unit/test_game_service.py::test_handle_message_join_game_without_game_id_raises[asyncio] PASSED [ 59%]
tests/unit/test_highscore_service.py::test_normalisiere_valid[classic] PASSED [ 62%]
tests/unit/test_highscore_service.py::test_normalisiere_valid[medium] PASSED [ 64%]
tests/unit/test_highscore_service.py::test_normalisiere_valid[pro] PASSED [ 67%]
tests/unit/test_highscore_service.py::test_normalisiere_case PASSED [ 70%]
tests/unit/test_highscore_service.py::test_normalisiere_unknown_mode PASSED [ 72%]
tests/unit/test_highscore_service.py::test_normalisiere_invalid_datatype PASSED [ 75%]
tests/unit/test_highscore_service.py::test_speichere PASSED [ 78%]
tests/unit/test_highscore_service.py::test_speichere_empty_name PASSED [ 81%]
tests/unit/test_highscore_service.py::test_speichere_invalid_name PASSED [ 83%]
tests/unit/test_highscore_service.py::test_speichere_name_too_long PASSED [ 86%]
tests/unit/test_highscore_service.py::test_speichere_negative_score PASSED [ 89%]
tests/unit/test_highscore_service.py::test_speichere_unknown_mode PASSED [ 91%]
tests/unit/test_highscore_service.py::test_uebersicht_empty FAILED [ 94%]
tests/unit/test_highscore_service.py::test_uebersicht_modus_empty FAILED [ 97%]
tests/unit/test_highscore_service.py::test_uebersicht_full PASSED [100%]
ERROR: Coverage failure: total of 77 is less than fail-under=80

============================================================================= ERRORS ==============================================================================
****************************\_\_\_**************************** ERROR at setup of test_sortiert_absteigend ****************************\_\_\_\_****************************
file c:\Users\janic\Desktop\Development\school\M450-Server\tests\integration\test_highscore_api.py, line 3
def test_sortiert_absteigend(http_client):
E fixture 'http_client' not found

>       available fixtures: anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, cov, doctest_namespace, free_tcp_port, free_tcp_port_factory, free_udp_port, free_udp_port_factory, monkeypatch, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, subtests, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

c:\Users\janic\Desktop\Development\school\M450-Server\tests\integration\test_highscore_api.py:3
============================================================================ FAILURES =============================================================================
**********************************\_\_********************************** test_uebersicht_empty **********************************\_\_**********************************

    def test_uebersicht_empty():
      modus = None

      highscores.clear

      result = uebersicht(modus)

>     assert result["hinweis"] == HINWEIS_LEER
>
> E AssertionError: assert '' == 'Noch keine Spiele gespielt'
> E  
> E - Noch keine Spiele gespielt

tests\unit\test_highscore_service.py:103: AssertionError
********************************\_\_\_******************************** test_uebersicht_modus_empty ********************************\_\_\_********************************

    def test_uebersicht_modus_empty():
      modus = 'pro'

      highscores.clear()

      result = uebersicht(modus)

>     assert result["hinweis"] == HINWEIS_LEER_MODUS
>
> E AssertionError: assert 'Noch keine S... im Modus pro' == 'Noch keine S...Modus {modus}'
> E  
> E - Noch keine Spiele im Modus {modus}
> E ? ^^ ----
> E + Noch keine Spiele im Modus pro
> E ? ^^

tests\unit\test_highscore_service.py:113: AssertionError
========================================================================= tests coverage ==========================================================================
**************************\_\_\_\_************************** coverage: platform win32, python 3.13.14-final-0 ****************************\_****************************

## Name Stmts Miss Branch BrPart Cover Missing

src\snake_game_server\_\_init**.py 0 0 0 0 100%
src\snake_game_server\_\_main**.py 3 3 2 0 0% 1-4
src\snake_game_server\app.py 8 8 0 0 0% 1-13
src\snake_game_server\models\game.py 30 1 2 0 97% 27
src\snake_game_server\models\maps.py 25 0 4 0 100%
src\snake_game_server\models\player.py 4 0 0 0 100%
src\snake_game_server\services\game_service.py 121 15 46 9 83% 48-50, 58-63, 72, 76->80, 80->exit, 132->136, 152, 162->175, 185, 193-198
src\snake_game_server\services\highscore_service.py 44 5 24 4 84% 24-25, 35, 44, 50
src\snake_game_server\services\player_service.py 10 6 2 0 33% 6, 9-15
src\snake_game_server\sockets\connection_manager.py 22 13 6 0 32% 16-25, 29, 37-40, 44-45

---

TOTAL 267 51 86 13 77%
FAIL Required test coverage of 80.0% not reached. Total coverage: 77.34%
===================================================================== short test summary info =====================================================================
FAILED tests/unit/test_highscore_service.py::test_uebersicht_empty - AssertionError: assert '' == 'Noch keine Spiele gespielt'
FAILED tests/unit/test_highscore_service.py::test_uebersicht_modus_empty - AssertionError: assert 'Noch keine S... im Modus pro' == 'Noch keine S...Modus {modus}'
ERROR tests/integration/test_highscore_api.py::test_sortiert_absteigend
============================================================== 2 failed, 34 passed, 1 error in 1.63s ==============================================================
