import React, { useState, useEffect } from "react";
import { FaFolder, FaFileAlt, FaPaperPlane, FaUpload } from "react-icons/fa";

export default function App() {
  const [files, setFiles] = useState([
    { name: "Project", type: "folder" },
    { name: "index.js", type: "file" },
    { name: "style.css", type: "file" },
  ]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [nodeResponse, setNodeResponse] = useState("Select a file to see response");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [ws, setWs] = useState(null);
  const [dragging, setDragging] = useState(false);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => console.log("WebSocket Connected!");
    socket.onmessage = (event) => {
      setMessages((prev) => [...prev, { text: event.data, sender: "server" }]);
    };
    socket.onclose = () => console.log("WebSocket Disconnected");
    setWs(socket);

    return () => socket.close();
  }, []);

  const sendInput = () => {
    if (ws && input.trim() !== "") {
      setMessages((prev) => [...prev, { text: input, sender: "user" }]);
      ws.send(input);
      setInput("");
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files).map((file) => ({ name: file.name, type: "file" }));
    setFiles((prev) => [...prev, ...droppedFiles]);
  };

  return (
    <div className="min-h-screen flex bg-gray-900 text-white">
      {/* Left Sidebar: File Explorer */}
      <div 
        className={`w-1/4 bg-gray-800 p-4 border-r border-gray-700 ${dragging ? "bg-gray-700" : ""}`} 
        onDragOver={handleDragOver} 
        onDragLeave={handleDragLeave} 
        onDrop={handleDrop}
      >
        <h2 className="text-lg font-bold mb-4 flex items-center">📁 Files & Folders <FaUpload className="ml-2 text-yellow-400" /></h2>
        <ul>
          {files.map((file, index) => (
            <li
              key={index}
              className={`cursor-pointer flex items-center space-x-2 p-2 rounded-md hover:bg-gray-700 ${
                selectedFile === file.name ? "bg-blue-500" : ""
              }`}
              onClick={() => setSelectedFile(file.name)}
            >
              {file.type === "folder" ? <FaFolder /> : <FaFileAlt />}
              <span>{file.name}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Middle Panel: Final Node Response */}
      <div className="w-1/2 p-4 border-r border-gray-700 flex flex-col justify-center items-center">
        <h2 className="text-xl font-bold mb-4">📜 Final Node Response</h2>
        <div className="p-6 bg-gray-700 rounded-lg shadow-md text-lg w-full text-center">
          {nodeResponse}
        </div>
      </div>

      {/* Right Sidebar: Streaming Chat */}
      <div className="w-1/4 bg-gray-800 p-4 flex flex-col">
        <h2 className="text-lg font-bold mb-4">💬 Streaming Chat</h2>
        <div className="h-80 overflow-y-auto p-2 bg-gray-700 rounded-md flex flex-col space-y-2">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`p-2 rounded-md max-w-[80%] ${
                msg.sender === "user" ? "bg-blue-500 self-end" : "bg-gray-600 self-start"
              }`}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div className="mt-4 flex">
          <input
            type="text"
            className="w-full p-2 bg-gray-600 text-white rounded-l-md"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
          />
          <button className="bg-blue-500 px-4 py-2 rounded-r-md" onClick={sendInput}>
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </div>
  );
}