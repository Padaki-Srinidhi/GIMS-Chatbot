import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";
import bg from "./assets/bg.jpg";
import logo from "./assets/logo.png";

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
  <div style={{ width: "100vw", height: "100vh", position: "relative" }}>

    {/* Background Layer */}
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundImage: `url(${bg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        filter: "blur(6px) brightness(1.4)",
        transform: "scale(1.05)",
        zIndex: 0,
      }}
    />

    {/* Welcome Text Layer */}
    <div
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1,
        pointerEvents: "none", // so it doesn't block clicks
      }}
    >
      <h1
        style={{
          fontSize: "48px",
          fontWeight: "800",
          color: "white",
          textShadow: "0 4px 20px rgba(0,0,0,0.4)",
          margin: 0,
          letterSpacing: "1px",
          textAlign: "center",
        }}
      >
        Welcome to
      </h1>
      <h1
        style={{
          fontSize: "56px",
          fontWeight: "900",
          color: "white",
          textShadow: "0 4px 20px rgba(0,0,0,0.4)",
          margin: "8px 0 16px",
          letterSpacing: "2px",
          textAlign: "center",
        }}
      >
        GIMS Assistant 🎓
      </h1>
      <p
        style={{
          fontSize: "20px",
          color: "rgba(255,255,255,0.85)",
          textShadow: "0 2px 10px rgba(0,0,0,0.3)",
          margin: 0,
          textAlign: "center",
        }}
      >
        Your college companion — ask me anything!
      </p>
    </div>

    {/* All chat content sits above */}
    <div style={{ position: "relative", zIndex: 2 }}>

      {/* Floating Button */}
      {!isOpen && (
        <div className="chat-icon" onClick={() => setIsOpen(true)}>
          💬
        </div>
      )}

      {/* Full-Screen Chat Overlay */}
      {isOpen && (
        <div className="chat-fullscreen-overlay">
          <div className="chat-container">

            {/* Header */}
            <div className="chat-header">
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <img src={logo} alt="logo" style={{ width: "36px", height: "36px", borderRadius: "50%" }} />
                <span>GIMS Assistant</span>
              </div>
              <button onClick={() => setIsOpen(false)}>✖</button>
            </div>

            {/* Messages */}
            <div className="chat-box">
              {messages.map((msg, i) => (
                <div key={i} className={`message-row ${msg.sender}`}>
                  {msg.sender === "bot" && (
                    <img src={logo} alt="bot" className="bot-avatar" />
                  )}
                  <div className={`message ${msg.sender}`}>
                    {msg.text}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row bot">
                  <img src={logo} alt="bot" className="bot-avatar" />
                  <div className="message bot typing">Typing...</div>
                </div>
              )}

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
      )}

    </div>
  </div>
);
}

export default App;