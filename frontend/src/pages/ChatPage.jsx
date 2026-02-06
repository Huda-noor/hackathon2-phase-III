import React, { useState, useEffect } from 'react';
import ChatInterface from '../components/ChatInterface';

const ChatPage = () => {
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // In a real app, you would get the user ID from authentication context
    // For now, we'll use a mock user ID
    const mockUserId = '123e4567-e89b-12d3-a456-426614174000'; // Example UUID
    setUserId(mockUserId);
    setLoading(false);
  }, []);

  if (loading) {
    return <div>Loading chat...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!userId) {
    return <div>Please log in to access the chat.</div>;
  }

  return (
    <div className="chat-page">
      <header className="chat-header">
        <h1>Chat Interface</h1>
      </header>
      
      <main className="chat-main">
        <ChatInterface userId={userId} />
      </main>
      
      <footer className="chat-footer">
        <p>Secure Chat Interface - All communications are encrypted</p>
        <p>Developed by: HUDA NOOR</p>
        <p>Description: Advanced chat API & frontend integration with AI agent and MCP tools</p>
      </footer>
    </div>
  );
};

export default ChatPage;