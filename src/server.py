import asyncio
import websockets
import json
import game_functions

HEADER = 64
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

players = []
board = game_functions.create_empty_board()
turn = 0 

async def receive_json(websocket):
    message = await websocket.recv()
    return json.loads(message)

async def send_json(websocket, data):
    message = json.dumps(data)
    await websocket.send(message)


async def handle_client(websocket):
    print("[DEBUG] handle_client running")
    try:
        print(f"[INFO] New connection from {websocket.remote_address}")
        global board, turn, players
        players.append(websocket)
        print(f"Players connected: {len(players)}")
        
        if len(players) == 1:
            await send_json(players[0], {"type": "message", "memo": "Waiting for Player 2 to join..."})
        elif len(players) == 2:
            await send_json(players[0], {"type": "start", "player_id": 1})
            await send_json(players[1], {"type": "start", "player_id": 2})
            print("[INFO] Both players connected. Starting game...")

            await game_loop(players, turn)

        while True:
            await asyncio.sleep(1)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
        players.pop()

async def game_loop(players, turn):
    print("[INFO] Running Game Loop...")
    try:
        while True:
            current_conn = players[turn]
            other_conn = players[1 - turn]

            await send_json(current_conn, {"type": "your_turn"})
            await send_json(other_conn, {"type": "message", "memo": "Waiting for other player's move..."})
        
            data = await receive_json(current_conn)
            print(f"[SERVER] Messaged received from Player {1 + turn}: {data}")

            if data["type"] == "move":
                col = data["col"]
                if game_functions.apply_move(board, col, turn):
                    # Send the updated board to both players
                    await send_json(current_conn, {"type": "state", "board": board, "turn": 1 - turn})
                    await send_json(other_conn, {"type": "state", "board": board, "turn": 1 - turn})

                    winner = game_functions.check_winner(board)
                    is_draw = game_functions.check_draw(board)

                    if winner is not None:
                        await send_json(current_conn, {"type": "end", "winner": winner})
                        await send_json(other_conn, {"type": "end", "winner": winner})
                        break  # End the game
                    elif is_draw:
                        await send_json(current_conn, {"type": "end", "draw": True})
                        await send_json(other_conn, {"type": "end", "draw": True})
                        break
                    turn = 1 - turn  # Switch turns
                else:
                    # Send invalid move message if column is full
                    await send_json(current_conn, {"type": "invalid", "reason": "Column full"})
    except websockets.exceptions.ConnectionClosed:
        print("[INFO] A player has disconnected")
    finally:
        if current_conn in players:
            players.remove(current_conn)
        if other_conn in players:
            players.remove(other_conn)

async def main():
    async with websockets.serve(handle_client, SERVER, PORT):
        await asyncio.Future()  # Run the server forever

if __name__ == "__main__":
    print(f"[INFO] Server is listening on ws://{SERVER}:{PORT}")
    asyncio.run(main())
