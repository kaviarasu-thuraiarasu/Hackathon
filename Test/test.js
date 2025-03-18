import { useState, useEffect } from "react";

function ChatApp() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/ws");

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prev) => [...prev, message]);
    };

    setWs(websocket);
    return () => websocket.close();
  }, []);

  const sendInput = () => {
    if (ws && userInput.trim()) {
      ws.send(userInput);
      setMessages((prev) => [...prev, { role: "human", text: userInput }]);
      setUserInput("");
    }
  };

  return (
    <div>
      <h2>AI Assistant</h2>
      <div style={{ border: "1px solid gray", padding: "10px", minHeight: "200px" }}>
        {messages.map((msg, idx) => (
          <p key={idx}><strong>{msg.role}:</strong> {msg.text}</p>
        ))}
      </div>
      <input 
        type="text"
        value={userInput} 
        onChange={(e) => setUserInput(e.target.value)} 
        placeholder="Type a message or command..."
      />
      <button onClick={sendInput}>Send</button>
    </div>
  );
}

export default ChatApp;
