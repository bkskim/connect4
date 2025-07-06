import socket, json, game_functions

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname('localhost')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#helper function for sending JSON
def send_json(conn, data):
    message = json.dumps(data).encode(FORMAT)
    msg_length = len(message)
    header = str(msg_length).encode(FORMAT)
    header += b' ' * (HEADER - len(header))
    conn.sendall(header + message)

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

# JSON Message Protocol
# start - Server to Client
# your_turn - Server to Client
# move - Client to Server
# invalid - Server to Client
# state - Server to Clients
# end - Server to Clients

while True:
    response = receive_json(client)
    if response["type"] == "message":
        print(f"[CLIENT] Messaged received from Server: {response["memo"]}")
    elif response["type"] == "start":
        this_player = response["player_id"] + 1
        print(f"You are Player {this_player}!")
    elif response["type"] == "your_turn":
        colNum = int(input("Choose a column to place your token. "))
        while colNum < 1 or colNum > 7:
            colNum = int(input("Invalid column number. Enter a column number 1 through 7. "))
        send_json(client, {"type": "move", "col": colNum})
    elif response["type"] == "state":
        print(f"Move submitted. Here is the current board:")
        game_functions.printBoard(response["board"])
    elif response["type"] == "invalid":
        print(f"{response["reason"]}.")
    elif response["type"] == "end" and response.get("winner") is not None:
        print(f"GAME OVER!! The winner is Player {response["winner"]}")
        break
    elif response["type"] == "end" and response.get("draw") is True:
        print(f"GAME OVER!! It is a draw - no winner.")
        break

client.close()
