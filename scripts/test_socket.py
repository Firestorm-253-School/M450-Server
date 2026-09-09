"""Small manual client for testing the game WebSocket."""

import argparse
import asyncio

from websockets.asyncio.client import connect


async def test_player_connection(url: str, player_id: str) -> str:
    websocket_url = f"{url.rstrip('/')}/ws/game?player_id={player_id}"

    print(f"Connecting as {player_id!r} ...")
    async with connect(websocket_url) as websocket:
        print("Connected. Player was created or loaded.")
        await websocket.send('{"type": "create_game"}')
        created = await websocket.recv()
        print(f"Created game: {created}")
        game_id = __import__("json").loads(created)["game_id"]

    print("Disconnected.")
    print("Reconnecting with the same player ID ...")

    async with connect(websocket_url):
        print("Reconnected. The existing player ID was accepted.")

    return game_id


async def test_join_game(url: str, player_id: str, game_id: str) -> None:
    websocket_url = f"{url.rstrip('/')}/ws/game?player_id={player_id}"

    async with connect(websocket_url) as websocket:
        await websocket.send(
            f'{{"type": "join_game", "game_id": "{game_id}"}}'
        )
        response = await websocket.recv()
        print(f"Joined game: {response}")

    print("Game create/join test passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        default="ws://127.0.0.1:8000",
        help="WebSocket server URL without /ws/game (default: %(default)s)",
    )
    parser.add_argument(
        "--player-id",
        default="manual-test-player",
        help="Player ID to create and reuse (default: %(default)s)",
    )
    args = parser.parse_args()

    game_id = asyncio.run(test_player_connection(args.url, args.player_id))
    asyncio.run(test_join_game(args.url, "second-test-player", game_id))


if __name__ == "__main__":
    main()