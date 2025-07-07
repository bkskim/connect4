# connect4
This is a real-time, multiplayer Connect 4 game built with a React frontend and an asynchronous Python WebSocket backend. Players can join from separate browser instances and take turns dropping discs into a shared game board until one wins or the game ends in a draw.

# Features

- Two-player Connect 4 gameplay in real time
- Live state updates using WebSockets
- Win detection (horizontal, vertical, diagonal)
- Dynamic UI with disc colors based on player ID
- Turn-based logic with stateful game coordination

# Topics Demonstrated

- ## Backend (Python)
- WebSocket Server with `websockets` for real-time bi-directional communication
- Asynchronous Programming using `async`/`await` to manage multiple clients
- Game State Management including global board state, player turns, and winner checks
- Data Serialization with `json.dumps()` / `json.loads()` for structured message exchange
- Connection Handling for player joins, disconnects, and graceful game cleanup

- ## Frontend (React)
- React Hooks: `useState`, `useEffect` for state and lifecycle management
- Conditional Rendering of game board, messages, and input based on state
- Dynamic CSS Class Assignment to highlight current player discs
- WebSocket Client: Open, message, and close event handling
- Clean UX: Game-over messages, player identities, and user prompts

# Tech Stack

- Frontend: React (JavaScript), CSS
- Backend: Python, `websockets` library
- Protocol: JSON over WebSocket
- Dev Tools: Console logging, live reload

# How to Run

1. Start the Python WebSocket server
   (python server.py)
3. Run the React frontend
   (npm start or npm run dev)

# Explanation of Differrent Folders

1. Offline Connect 4 - I started with this simple version of a Connect4 where a single file is run and two players would play Connect4 in terminal on a single computer.
2. Python Only Connect4 - then I incoporated Network Programming through sockets to create a TCP Server Model for two players to connect on different computers to play the same game.
3. src - this is the final product with a friendly User Interface coded with React.

# Walk Through

server.py holds the server-side functionality. It creates a WebSocket server, manages player connections, coordinates the game loop, and processes incoming and outgoing messages.
App.jsx contains the client-side logic and the structure of the user interface, built using React.
App.css provides the styling for the frontend components.
game_functions.py contains core game-related functions, such as create_empty_board() and check_winner().

We first run server.py in which a new websocket server is created on localhost:5050. The server waits for two players to be connected - this is done by instantiating a global `players` list, and whenever a new client is connected to the server, we append the new websocket to the list of `players`. If the length of `players` is 1, we send a message to the first player "Waiting for Player 2 to join..." If the length of `players` is 2, we start the game by sending a `start` JSON message to both players along with their player IDs. There are also helper functions to send and receive JSON messages from the websockets.

Once the server is running, we open up our terminal and run our React environment. I'm using Vite with React, so we can open up a new tab and paste the local URL it gives us. On load, useEffect runs and opens a new WebSocket connection to ws://localhost:5050. Incoming messages from the server are parsed inside `socket.onmessage`, and the app responds based on the type field in the JSON payload. For example, if a JSON message with "type: "your_turn"" is sent, then the player will be able to choose a column to place their token.

![Screenshot 2025-07-06 at 4 54 13 PM](https://github.com/user-attachments/assets/c7a320c3-abae-4284-a810-67fbe1ffe22c)

We need a second player, so we open up another tab and start another instance of the App. Now, since the length of `players` is 2, the game starts. The server sends "start" messages to both players. Player 1 is called to click on a column to place their token. When the player clicks on a column, we send the column index back to the server via JSON message. The server processes the move, updates the shared board state, checks for a win or draw, and sends the updated game state to both players. Then the turn is switched over to the next player.

![Screenshot 2025-07-06 at 5 03 20 PM](https://github.com/user-attachments/assets/ed8a7f44-b4f8-4294-94e0-fa8bee08333b)

![Screenshot 2025-07-06 at 5 04 27 PM](https://github.com/user-attachments/assets/82833050-2e87-4978-b78e-7421fd8b6e67)

![Screenshot 2025-07-06 at 5 04 34 PM](https://github.com/user-attachments/assets/31ef6b47-561b-4508-a3df-be7ee1eeaecd)

After every move, the server checks for a winner using check_winner(). If a player wins, a message with "type": "end" and the winner ID is sent to both clients. If the board is full and no winner is found, a draw message is sent.

![Screenshot 2025-07-06 at 5 05 55 PM](https://github.com/user-attachments/assets/4d550602-a26b-4128-90dc-88a6f9ef5689)

