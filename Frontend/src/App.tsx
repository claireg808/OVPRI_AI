import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './components/Home/HomePage';
import ChatBot from './components/Chatbot/ChatBot';
import Redline from './components/Redline/Redline';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link> | <Link to="/chatbot">Chatbot</Link> | <Link to="/redline">Document Review</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chatbot" element={<ChatBot />} />
      </Routes>
    </Router>
  );
}

export default App;