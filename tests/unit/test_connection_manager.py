from logging import Manager
from pydantic_core.core_schema import none_schema
import pytest

from snake_game_server.services.player_service import PlayerService
from snake_game_server.sockets.connection_manager import ConnectionManager

class FakeWebSocket:
    def __init__(self, player_id: str | None):
        self.query_params = {}
        if player_id is not None:
            self.query_params["player_id"] = player_id
        self.accepted = False
        self.sent: list[dict] = []
    async def accept(self):
        self.accepted = True
    async def send_json(self, message: dict):
        self.sent.append(message)

@pytest.fixture
def test_manager():
    return ConnectionManager()

@pytest.fixture
def test_player_service():
    return PlayerService()


@pytest.mark.anyio
async def test_connect_without_player_id_none(test_manager, test_player_service):
    ws = FakeWebSocket(player_id=None)

    player = await test_manager.connect(ws, test_player_service)

    assert player is None
    assert ws.accepted is False
    assert test_manager.connections == {}

@pytest.mark.anyio
async def test_connection_with_player_id(test_manager, test_player_service):
    ws = FakeWebSocket(player_id="Test Player")

    player = await test_manager.connect(ws, test_player_service)

    assert player is not None
    assert player.id == "Test Player"
    assert ws.accepted is True
    assert test_manager.connections["Test Player"] is ws

@pytest.mark.anyio
async def test_disconnect(test_manager, test_player_service):
    ws = FakeWebSocket(player_id="Test Player")
    await test_manager.connect(ws, test_player_service)

    await test_manager.disconnect("Test Player")

    assert "Test Player" not in test_manager.connections

@pytest.mark.anyio
async def test_send_to_player(test_manager, test_player_service):
    ws = FakeWebSocket(player_id="Test Player")
    await test_manager.connect(ws, test_player_service)

    await test_manager.send_to_player("Test Player", {"type": "hello"})

    assert ws.sent == [{"type":"hello"}]
