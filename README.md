# connect4
This is a real-time, multiplayer Connect 4 game built with a React frontend and an asynchronous Python WebSocket backend. Players can join from separate browser instances and take turns dropping discs into a shared game board until one wins or the game ends in a draw.

# Features

- Two-player Connect 4 gameplay in real time
- Live state updates using WebSockets
- Win detection (horizontal, vertical, diagonal)
- Dynamic UI with disc colors based on player ID
- Turn-based logic with stateful game coordination

# Topics Demonstrated

- Backend (Python)
- WebSocket Server with `websockets` for real-time bi-directional communication
- Asynchronous Programming using `async`/`await` to manage multiple clients
- Game State Management including global board state, player turns, and winner checks
- Data Serialization with `json.dumps()` / `json.loads()` for structured message exchange
- Connection Handling for player joins, disconnects, and graceful game cleanup

- Frontend (React)
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
   python server.py
3. Run the React frontend
   npm start or npm run dev

# Walk Through

