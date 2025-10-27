import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './components/Home/HomePage';
import ChatBot from './components/Chatbot/ChatBot';
import RedLine from './components/Redline/Redline';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chatbot" element={<ChatBot />} />
          <Route path="/redline" element={<RedLine />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;