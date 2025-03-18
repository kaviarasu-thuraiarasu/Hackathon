import { useState, useEffect } from "react";
export default function App() {
  const [messages, setMessages] = useState([]); // ✅ Corrected empty array
  const [input, setInput] = useState("");
  const [ws, setWs] = useState(null);
  const [interrupted, setInterrupted] = useState(false);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]); // ✅ Append new messages properly

        // Check if workflow interrupted
        if (typeof data === "object" && "interruption" in data) {
          setInterrupted(true);
        }
      } catch (error) {
        console.error("Error parsing message:", error);
      }
    };

    setWs(socket);
    return () => socket.close();
  }, []);

  const sendInput = () => {
    if (ws && input) {
      ws.send(input);
      setInput("");
      setInterrupted(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 className="text-2xl font-bold mb-4">AI Workflow Streaming</h1>
      <div className="w-full max-w-2xl p-4 bg-gray-800 rounded-lg shadow-md">
        <div className="h-80 overflow-y-auto p-2 bg-gray-700 rounded-md">
          {messages.map((msg, i) => (
            <div key={i} className="mb-2">
              {typeof msg === "string" ? msg : <strong>{msg.interruption}</strong>}
            </div>
          ))}
        </div>
        {interrupted && (
          <div className="mt-4 flex">
            <input
              type="text"
              className="w-full p-2 bg-gray-600 text-white rounded-l-md"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button
              className="bg-blue-500 px-4 py-2 rounded-r-md"
              onClick={sendInput}
            >
              Send
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
