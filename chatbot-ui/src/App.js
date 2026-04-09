import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMessage = { sender: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", {
        query: query,
      });

      const botReply =
        res.data.answer?.content ||
        res.data.answer?.message?.content ||
        "No response";

      const botMessage = { sender: "bot", text: botReply };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div>
      {/* Floating Button */}
      <div className="chat-icon" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? "✖" : "💬"}
      </div>

      {/* Chat Window */}
      <div className={`chat-wrapper ${isOpen ? "open" : ""}`}>
        <div className="chat-container">
          
          {/* Header */}
          <div className="chat-header">
            <span>GIMS Assistant</span>
            <button onClick={() => setIsOpen(false)}>✖</button>
          </div>

          {/* Messages */}
          <div className="chat-box">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`message ${msg.sender === "user" ? "user" : "bot"}`}
              >
                {msg.text}
              </div>
            ))}

            {/* Typing Indicator */}
            {loading && <div className="message bot typing">Typing...</div>}

            <div ref={chatEndRef}></div>
          </div>

          {/* Input */}
          <div className="input-box">
            <input
              type="text"
              placeholder="Type your message..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button onClick={sendMessage}>➤</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;