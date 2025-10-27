import "./ChatBot.css";
import "/home/gillaspiecl/OVPRI_AI/Frontend/src/App.css";
import "@fontsource/inter/300.css";
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import user_icon from "/home/gillaspiecl/OVPRI_AI/Frontend/src/icons/user.jpeg"
import bot_icon from "/home/gillaspiecl/OVPRI_AI/Frontend/src/icons/bot.jpeg"
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";


function ChatBot() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<{ user: string; bot: string }[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const chatBoxRef = useRef<HTMLDivElement>(null);

  const isChatActive = chatHistory.length > 0;

  // generate per-tab session ID (resets when refreshed)
  const [sessionId] = useState(() => {
    let id = sessionStorage.getItem("session_id");
    if (!id) {
      id = crypto.randomUUID();
      sessionStorage.setItem("session_id", id);
    }
    return id;
  });

  // auto scroll
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistory, isLoading]);

  // resize chatbox
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + "px";  // grow to content
    }
    setMessage(e.target.value);
  };

  // use return to send message
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // stop newline
      if (message.trim()) {
        handleSubmit(e as unknown as React.FormEvent); // reuse your submit handler
      }
    }
  };

  // call LLM to respond to input
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    const newMessage = { user: message, bot: "" };
    setChatHistory((prev) => [...prev, newMessage]);

    setMessage("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }

    try {
      const response = await axios.post("http://localhost:5001/chat", {
        message,
        session_id: sessionId
      });
      const botMessage = response.data.response;

      setChatHistory((prev) => {
        const updated = [...prev];
        updated[updated.length - 1].bot = botMessage;
        return [...updated];
      });
    } catch (error) {
      console.error("Error communicating with the backend", error);

      setChatHistory((prev) => {
        const updated = [...prev];
        updated[updated.length - 1].bot = "We're sorry, there was an issue with your request.";
        return updated;
      });
    } finally {
      setIsLoading(false);
    }

  };

  return (
  <div className={`App ${isChatActive ? "" : "centered"}`}>
    <div className={`chat-wrapper ${isChatActive ? "active" : ""}`}>
      <h1 className="chat-header">OVPRI AI Chatbot</h1>

      <div className="chat-box" ref={chatBoxRef}>
        {chatHistory.map((chat, index) => (
          <div key={index}>
            <div className="chat-message user">
              <img src={user_icon} width="40" alt="user" />
              <p>{chat.user}</p>
            </div>

            {chat.bot ? (
              <div className="chat-message bot">
                <img src={bot_icon} width="40" alt="bot" />
                <div className="chat-bubble">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {chat.bot}
                  </ReactMarkdown>
                </div>
              </div>
            ) : isLoading && index === chatHistory.length - 1 ? (
              <div className="chat-message bot">
                <img src={bot_icon} width="40" alt="bot" />
                <div className="chat-bubble loading">
                  Thinking<span className="dots"></span>
                </div>
              </div>
            ) : null}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-border">
        <textarea
          className="chat-input"
          ref={textareaRef}
          value={message}
          rows={1}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Ask me about the IRB"
        />
        <button type="submit" className="chat-submit">Send</button>
      </form>
    </div>
  </div>
  );
}

export default ChatBot;