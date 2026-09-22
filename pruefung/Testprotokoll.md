Alle Tests sind grün, die Coverage ist viel zu tief. Die Zeit war viel zu knapp..

============================================================================================== test session starts ==============================================================================================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Zehnder\git\privat\M450\Pruefung
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.15.1, cov-7.1.0
collected 33 items

tests/integration/test_highscore_api.py::test_api_get_highscores PASSED [ 3%]
tests/unit/test_game.py::test_move_advances_head_in_current_direction PASSED [ 6%]
tests/unit/test_game.py::test_move_keeps_body_length_constant PASSED [ 9%]
tests/unit/test_game.py::test_set_direction_ignores_reversal PASSED [ 12%]
tests/unit/test_game.py::test_set_direction_allows_turn PASSED [ 15%]
tests/unit/test_game.py::test_head_hits_wall_at_left_border PASSED [ 18%]
tests/unit/test_game.py::test_head_hits_wall_at_right_border PASSED [ 21%]
tests/unit/test_game.py::test_head_hits_wall_false_when_inside PASSED [ 24%]
tests/unit/test_game.py::test_head_hits_wall_detects_inner_obstacle PASSED [ 27%]
tests/unit/test_game_service.py::test_set_direction_does_not_move_immediately[asyncio] PASSED [ 30%]
tests/unit/test_game_service.py::test_set_direction_starts_a_tick_loop_that_moves_the_snake[asyncio] PASSED [ 33%]
tests/unit/test_game_service.py::test_tick_loop_ends_game_when_head_touches_border[asyncio] PASSED [ 36%]
tests/unit/test_game_service.py::test_create_game_uses_requested_map[asyncio] PASSED [ 39%]
tests/unit/test_game_service.py::test_tick_loop_ends_game_when_head_hits_inner_wall[asyncio] PASSED [ 42%]
tests/unit/test_game_service.py::test_set_direction_rejects_unknown_direction[asyncio] PASSED [ 45%]
tests/unit/test_game_service.py::test_handle_message_create_game[asyncio-message0] PASSED [ 48%]
tests/unit/test_game_service.py::test_handle_message_join_game[asyncio-message0-True] PASSED [ 51%]
tests/unit/test_game_service.py::test_handle_message_join_game[asyncio-message1-False] PASSED [ 54%]
tests/unit/test_game_service.py::test_handle_message_leave_game[asyncio-False] PASSED [ 57%]
tests/unit/test_game_service.py::test_handle_message_leave_game[asyncio-True] PASSED [ 60%]
tests/unit/test_game_service.py::test_handle_message_unknown_type_returns_none[asyncio] PASSED [ 63%]
tests/unit/test_game_service.py::test_handle_message_join_game_without_game_id_raises[asyncio] PASSED [ 66%]
tests/unit/test_highscore_service.py::test_normalisiere_valid_modis[CLASSIC-classic] PASSED [ 69%]
tests/unit/test_highscore_service.py::test_normalisiere_valid_modis[medium-medium] PASSED [ 72%]
tests/unit/test_highscore_service.py::test_normalisiere_valid_modis[Pro-pro] PASSED [ 75%]
tests/unit/test_highscore_service.py::test_normalisiere_valid_modis[MedIUm-medium] PASSED [ 78%]
tests/unit/test_highscore_service.py::test_normalisiere_invalid_modus_type PASSED [ 81%]
tests/unit/test_highscore_service.py::test_normalisiere_invalid_modus_unknown[randomShit] PASSED [ 84%]
tests/unit/test_highscore_service.py::test_normalisiere_invalid_modus_unknown[MMEDIUM] PASSED [ 87%]
tests/unit/test_highscore_service.py::test_speichere_valid[Laurin-10-classic] PASSED [ 90%]
tests/unit/test_highscore_service.py::test_speichere_valid[Janick-5-pro] PASSED [ 93%]
tests/unit/test_highscore_service.py::test_speichere_invalid_name_type PASSED [ 96%]
tests/unit/test_highscore_service.py::test_speichere_invalid_score_type PASSED [100%]
ERROR: Coverage failure: total of 74 is less than fail-under=80

=============================================================================================== warnings summary ================================================================================================
..\..\..\..\AppData\Roaming\Python\Python314\site-packages\starlette\testclient.py:53
C:\Users\Zehnder\AppData\Roaming\Python\Python314\site-packages\starlette\testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
\_PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

tests\integration\test_highscore_api.py:12
c:\Users\Zehnder\git\privat\M450\Pruefung\tests\integration\test_highscore_api.py:12: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo? You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
@pytest.mark.integration

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================ tests coverage =================================================================================================
**************************************\_\_\_\_************************************** coverage: platform win32, python 3.14.5-final-0 **************************************\_\_\_\_**************************************

## Name Stmts Miss Branch BrPart Cover Missing

src\snake_game_server\_\_init**.py 0 0 0 0 100%
src\snake_game_server\_\_main**.py 3 3 2 0 0% 1-4
src\snake_game_server\api\highscores.py 15 6 0 0 60% 12-13, 18-21
src\snake_game_server\api\players.py 2 0 0 0 100%
src\snake_game_server\app.py 8 0 0 0 100%
src\snake_game_server\models\game.py 29 1 2 0 97% 27
src\snake_game_server\models\maps.py 21 0 4 0 100%
src\snake_game_server\models\player.py 3 0 0 0 100%
src\snake_game_server\services\game_service.py 121 15 46 9 83% 48-50, 58-63, 72, 76->80, 80->exit, 132->136, 152, 162->175, 185, 193-198
src\snake_game_server\services\highscore_service.py 44 10 24 6 71% 20-25, 33, 37, 46, 48, 52
src\snake_game_server\services\player_service.py 10 5 2 0 42% 9-15
src\snake_game_server\sockets\connection_manager.py 22 13 6 0 32% 16-25, 29, 37-40, 44-45
src\snake_game_server\sockets\game_socket.py 24 14 2 0 38% 16-40

---

TOTAL 302 67 88 15 74%
FAIL Required test coverage of 80.0% not reached. Total coverage: 73.85%
======================================================================================== 33 passed, 2 warnings in 1.88s =========================================================================================
