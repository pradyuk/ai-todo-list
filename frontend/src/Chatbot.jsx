import { useState } from "react";
import axios from "axios";

const CHAT_API_URL = "/api/chat/";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");

    try {
      const response = await axios.post(CHAT_API_URL, { history: updatedMessages });
      const aiMessage = response.data;

      setMessages([...updatedMessages, aiMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div>
      <h2>Chatbot</h2>
      <div style={{ height: "300px", overflowY: "auto", border: "1px solid black", padding: "10px" }}>
        {messages.map((msg, index) => (
          <p key={index}>
            <strong>{msg.role === "user" ? "You: " : "Bot: "}</strong> {msg.content}
          </p>
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
}
