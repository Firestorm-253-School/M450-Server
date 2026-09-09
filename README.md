# M450-Server (snake_game_server)

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC)

Backend server for a multiplayer Snake game, built for the M450 school module. It exposes a FastAPI application with a WebSocket endpoint that lets connected players create, join, and leave games.

> Package name (per `pyproject.toml`): `snake_game_server`

## Overview

The server is intentionally small and service-oriented:

- **`PlayerService`** looks up or creates an in-memory `Player` for a given `player_id`.
- **`ConnectionManager`** tracks the active WebSocket connection per player and can send a message to a single player or broadcast to all connected players.
- **`GameService`** owns all `Game` instances, maps each player to the game they are currently in, and handles the `create_game` / `join_game` / `leave_game` message types coming from the WebSocket.
- **`Game`** and **`Player`** are simple dataclasses (`src/snake_game_server/models/`) representing domain state. `Game` currently tracks `id`, `players`, a `started` flag, and a `tick` counter.

All state is kept in memory (plain Python dicts) — there is no database or persistence layer in this codebase.

## Architecture

```
src/snake_game_server/
├── app.py                     # FastAPI app, wires up routers
├── __main__.py                # `python -m snake_game_server` entry point (runs uvicorn)
├── api/
│   └── players.py             # APIRouter mounted at /api/players (no routes defined yet)
├── models/
│   ├── game.py                 # Game dataclass
│   └── player.py                # Player dataclass (frozen)
├── services/
│   ├── game_service.py          # Game lifecycle + message handling
│   └── player_service.py       # Player lookup/creation
└── sockets/
    ├── connection_manager.py    # Tracks player_id -> WebSocket
    └── game_socket.py           # /ws/game WebSocket endpoint
```

The players router (`/api/players`) is currently mounted with no endpoints defined; all interactive gameplay happens over the `/ws/game` WebSocket.

## WebSocket protocol

**Endpoint:** `ws://<host>:<port>/ws/game?player_id=<player-id>`

- `player_id` is a required query parameter. If it is missing, the connection is closed immediately with close code `1008` (policy violation).
- Reconnecting with the same `player_id` reuses the existing `Player` instance (players are not deleted when they disconnect).
- Messages are sent and received as JSON. On an unhandled error (unknown message type, invalid payload, etc.), the server removes the player from the `ConnectionManager` and closes the connection with code `1011` (internal error).

### Client → server messages

| `type`        | Required fields   | Behavior                                                                 |
| ------------- | ------------------ | ------------------------------------------------------------------------ |
| `create_game` | –                   | Leaves the player's current game (if any), creates a new `Game` with a random UUID, and adds the player to it. |
| `join_game`   | `game_id` (string)  | Leaves the player's current game (if any) and adds them to the game with the given `game_id`. Raises an error if `game_id` is missing, not a string, or does not exist. |
| `leave_game`  | –                   | Removes the player from their current game. If the game becomes empty, it is deleted. |

Any other or missing `type` raises an error, which closes the connection with code `1011`.

### Server → client responses

| `type`         | Fields                                | Sent in response to |
| -------------- | -------------------------------------- | -------------------- |
| `game_created` | `game_id`                              | `create_game`        |
| `game_joined`  | `game_id`, `player_count`              | `join_game`           |
| `game_left`    | `game_id` (may be `null`)              | `leave_game`          |

Example exchange:

```json
// client -> server
{"type": "create_game"}

// server -> client
{"type": "game_created", "game_id": "b3f1..."}
```

```json
// client -> server
{"type": "join_game", "game_id": "b3f1..."}

// server -> client
{"type": "game_joined", "game_id": "b3f1...", "player_count": 2}
```

## Requirements

- Python **3.12+** (declared in `pyproject.toml` via `requires-python`)
- Dependencies (installed automatically, see `pyproject.toml`):
  - `fastapi`
  - `uvicorn`
  - `websockets`
  - `pytest`
  - `pytest-cov`

## Installation

Clone the repository and install it in editable mode into a virtual environment.

```powershell
git clone https://github.com/Firestorm-253-School/M450-Server.git
cd M450-Server

python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1

pip install -e .
```

## Running the server

With the virtual environment activated, start the FastAPI app with `uvicorn` (auto-reload enabled):

```powershell
uvicorn snake_game_server.app:app --reload
```

Alternatively, use the packaged entry point, which runs the same app on `127.0.0.1:8000` with `reload=True`:

```powershell
python -m snake_game_server
```

The WebSocket endpoint is then available at:

```
ws://127.0.0.1:8000/ws/game?player_id=<player-id>
```

### Manual WebSocket client

`scripts/test_socket.py` is a small manual client (using the `websockets` library) that connects, creates a game, reconnects with the same player ID, and has a second player join that game. Useful for smoke-testing the server without a full client app.

```powershell
python scripts/test_socket.py --url ws://127.0.0.1:8000 --player-id manual-test-player
```

Both `--url` (default `ws://127.0.0.1:8000`) and `--player-id` (default `manual-test-player`) are optional.

## Testing

Automated tests run with `pytest` and are configured in `pyproject.toml`:

```powershell
pytest
```

Test discovery is restricted to `tests/` (`[tool.pytest.ini_options] testpaths = ["tests"]`). The repository currently has `tests/unit/` and `tests/integration/` directories scaffolded (each with a `.gitkeep`), matching the layout described in `docs/test-documentation.md`.

Coverage is configured via `pytest-cov` / `coverage`:

```powershell
pytest --cov
```

Coverage settings (from `pyproject.toml`):
- Source measured: `snake_game_server`
- Branch coverage: enabled
- Missing lines shown in the report (`show_missing = true`)
- Build fails if coverage drops below **80%** (`fail_under = 80`)

## Documentation

- [`docs/test-documentation.md`](docs/test-documentation.md) — German-language test documentation (Testdokumentation) covering requirements (`ANF-xx`), equivalence classes, test cases (`TC-xx`), a requirement-to-test traceability matrix, and a test evaluation summary for the player/game/WebSocket functionality.

## Project structure

```
M450-Server/
├── docs/
│   └── test-documentation.md
├── scripts/
│   └── test_socket.py
├── src/
│   └── snake_game_server/
│       ├── api/
│       ├── models/
│       ├── services/
│       └── sockets/
├── tests/
│   ├── integration/
│   └── unit/
├── pyproject.toml
└── README.md
```

## License

This repository does not currently include a license file. Contact the maintainers before reusing or redistributing this code.
