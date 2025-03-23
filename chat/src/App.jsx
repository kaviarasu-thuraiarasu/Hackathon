import { useState, useEffect, useRef } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    // Establish WebSocket connection
    socketRef.current = new WebSocket("ws://localhost:8000/ws/1");

    // Handle incoming messages
    socketRef.current.onmessage = (event) => {
      const message = event.data;
      console.log(message)
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    // Cleanup WebSocket connection
    return () => {
      socketRef.current.close();
    };
  }, []);

  // Function to send data
  const sendMessage = () => {
    if (socketRef.current.readyState === WebSocket.OPEN && input) {
      socketRef.current.send(input);
      setInput("");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>WebSocket Chat</h2>
      <div style={{ border: "1px solid #ccc", padding: "100%", height: "100%", overflowY: "auto" }}>
        {messages.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default App;
