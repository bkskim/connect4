import React, { useState, useEffect } from "react";
import "./App.css";

const ROWS = 6

function createEmptyBoard() {
  return Array.from({ length: 6 }, () => Array(7).fill(null));
}

function App() {
  const [board, setBoard] = useState(createEmptyBoard());
  const [turn, setTurn] = useState(0);
  const [ws, setWs] = useState(null);
  const [playerId, setPlayerId] = useState(null);
  const [message, setMessage] = useState("");
  const [showInput, setShowInput] = useState(false);
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:5050");

    socket.onopen = () => {
      console.log("[CLIENT] Connected to server");
    };

    socket.onmessage = (event) => {
      console.log("[CLIENT] Raw message from server:", event.data);
      const response = JSON.parse(event.data);

      if (response.type === "message") {
        console.log(`[CLIENT] Message from Server: ${response.memo}`);
        setMessage(response.memo);
      } else if (response.type === "start") {
        const thisPlayer = response.player_id + 1;
        setPlayerId(response.player_id);
        setMessage(`You are Player ${thisPlayer}!`);
      } else if (response.type === "your_turn") {
        setMessage("Your turn! Choose a column (1-7).");
        setShowInput(true);
      } else if (response.type === "state") {
        setBoard(response.board);
        setTurn(response.turn);
        setMessage("Move submitted. Here's the current board.");
        setShowInput(false);
      } else if (response.type === "invalid") {
        setMessage(response.reason);
        setShowInput(true);
      } else if (response.type === "end") {
        if (response.winner !== undefined) {
          setMessage(`GAME OVER!! The winner is Player ${response.winner}`);
          setShowInput(false);
        }
        else if (response.draw === true) {
          setMessage("GAME OVER!! It's a draw - no winner.");
          setShowInput(false);
        }

        setTimeout(() => {
        console.log("[CLIENT] Closing socket after game ends");
        socket.close(1000, "Game over");
      }, 2000);
    }

    };

    setWs(socket);

    return () => {
    if (socket.readyState === WebSocket.OPEN) {
      socket.close(1000, "Component unmounted");
    }
  };
}, []);

  const handleClick = (col) => {
    if (!showInput || ws === null) return;
      ws.send(JSON.stringify({ type: "move", col }));
  };    

  return (
    <div className="app">
      <h1>Connect 4</h1>
      <p>Current Turn: Player {turn + 1}</p>
      <p>{message}</p>
      <div className="board">
        {board.map((row, rowIndex) =>
          row.map((cell, colIndex) => (
            <div
              key={`${rowIndex}-${colIndex}`}
              className="cell"
              onClick={() => handleClick(colIndex)}
            >
              {cell !== null && (
                console.log("cell:", cell, "playerId:", playerId),
                <div
                  className={`disc ${cell == 1 ? "red" : "yellow"}`}
                ></div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
