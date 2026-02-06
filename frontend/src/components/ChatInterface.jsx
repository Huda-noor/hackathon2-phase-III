import React, { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';

const ChatInterface = ({ userId }) => {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  // For demo purposes, we'll maintain messages in state
  // In a real app, you'd fetch these from your API
  const [messages, setMessages] = useState([
    { id: 1, sender: 'ai', content: 'Hello! How can I assist you today?', timestamp: new Date() }
  ]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message to the chat immediately
      const userMessage = {
        id: Date.now(),
        sender: 'user',
        content: inputValue,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, userMessage]);
      const newInputValue = inputValue;
      setInputValue('');

      // Call the API to process the message
      const response = await import('../services/api').then(api => 
        api.default.sendMessage(userId, newInputValue, conversationId)
      );

      // Update conversation ID if this is the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add AI response to the chat
      const aiMessage = {
        id: response.message_id,
        sender: 'ai',
        content: response.response,
        toolCalls: response.tool_calls,
        confirmation: response.confirmation,
        timestamp: new Date(response.timestamp)
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(err.message);
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>Chat Assistant</h2>
      </div>

      <MessageList messages={messages} />

      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message here..."
            disabled={isLoading}
            className="chat-input"
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputValue.trim()}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
        
        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}
      </form>
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatInterface;