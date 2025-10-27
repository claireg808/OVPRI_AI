import React from "react";
import { Link } from "react-router-dom";
import "./HomePage.css";
import "/home/gillaspiecl/OVPRI_AI/Frontend/src/App.css";

const HomePage = () => {
  return (
    <div className="App">
    <div className="homepage-container">
      <h1 className="homepage-title">OVPRI AI Assistants</h1>
      <nav className="homepage-nav">
        <Link className="nav-button" to="/chatbot">Chatbot</Link>
        <Link className="nav-button" to="/redline">Document Review</Link>
      </nav>
    </div>
    </div>
  );
};

export default HomePage;