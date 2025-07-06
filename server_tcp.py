import socket, threading, json, game_functions

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname('localhost')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

#creating the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = []
board = game_functions.create_empty_board()

#if there is only one player, it waits. If there are two players, the game starts.
def handle_client(conn, addr, player_id):
    if player_id == 0:
        send_json(conn, {"type": "message", "memo": "Waiting for Player 2 to join...\n"})
    elif player_id == 1:
        print("[INFO] Both players connected. Starting game...")
        game_loop(players[0][0], players[1][0])

#server starts by listening for two clients. We start new threads for each client.
def start():
    server.listen()
    print(f"[Listening] Server is listening on {SERVER}")
    player_id = 0
    while len(players) < 2:
        conn, addr = server.accept()
        players.append((conn, addr))
        print(f"[CONNECTED] {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()
        player_id += 1

#helper function for receiving JSON
def receive_json(conn):
    header = conn.recv(HEADER).decode(FORMAT)
    if not header:
        return None
    msg_length = int(header.strip())
    data = b''
    while len(data) < msg_length:
        data += conn.recv(msg_length - len(data))
    return json.loads(data.decode(FORMAT))

#helper function for sending JSON
def send_json(conn, data):
    message = json.dumps(data).encode(FORMAT)
    msg_length = len(message)
    header = str(msg_length).encode(FORMAT)
    header += b' ' * (HEADER - len(header))
    conn.sendall(header + message)

# JSON Message Protocol
# message - Sever to Clients
# start - Server to Client
# your_turn - Server to Client
# move - Client to Server
# invalid - Server to Client
# state - Server to Clients
# end - Server to Clients

def game_loop(conn0, conn1, turn=0):

    print("[DEBUG] Starting game loop")
    
    send_json(conn0, {"type": "start", "player_id": 0})
    send_json(conn1, {"type": "start", "player_id": 1})
    
    while True:
        current_conn = players[turn][0]
        other_conn = players[1 - turn][0]

        send_json(current_conn, {"type": "your_turn"})
        send_json(other_conn, {"type": "message", "memo": "Waiting for other player's move..."})
        
        move = receive_json(current_conn)
        print(f"[SERVER] Messaged received from Player {1 - turn}: {move}")

        if move["type"] == "move":
            col = move["col"]
            success = game_functions.apply_move(board, col, turn)
            if not success:
                send_json(current_conn, {"type": "invalid", "reason": "Column full"})
                continue  # same player's turn

            winner = game_functions.check_winner(board)
            is_draw = game_functions.check_draw(board)

            send_json(current_conn, {"type": "state", "board": board, "turn": turn})
            send_json(other_conn, {"type": "state", "board": board, "turn": turn})

            if winner is not None:
                send_json(current_conn, {"type": "end", "winner": winner})
                send_json(other_conn, {"type": "end", "winner": winner})
                break
            elif is_draw:
                send_json(conn0, {"type": "end", "draw": True})
                send_json(conn1, {"type": "end", "draw": True})
                break

            turn = 1 - turn

print("Server is starting...")
try:
    start()

except:
    players[0][0].close()
    players[1][0].close()
    server.close()