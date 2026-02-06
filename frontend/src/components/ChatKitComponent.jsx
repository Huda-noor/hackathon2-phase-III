import React, { useState, useEffect, useRef } from 'react';
import OpenAI from 'openai';

const ChatKitComponent = ({ userId }) => {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([
    { id: 1, role: 'assistant', content: 'Hello! How can I assist you today?' }
  ]);
  const messagesEndRef = useRef(null);

  // Initialize OpenAI client with the domain key
  const openai = new OpenAI({
    apiKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY, // This should be your domain key
    dangerouslyAllowBrowser: true // Only for development - not recommended for production
  });

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
        role: 'user',
        content: inputValue,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMessage]);
      const newInputValue = inputValue;
      setInputValue('');

      // Prepare messages for the OpenAI API
      const formattedMessages = messages
        .filter(msg => msg.role !== 'error') // Exclude error messages
        .map(({ role, content }) => ({ role, content }));

      // Add the new user message
      formattedMessages.push({ role: 'user', content: newInputValue });

      // Call OpenAI API to get response
      const response = await openai.chat.completions.create({
        model: 'gpt-3.5-turbo', // or 'gpt-4' if you have access
        messages: formattedMessages,
        temperature: 0.7,
      });

      // Extract the AI response
      const aiResponse = response.choices[0]?.message?.content || "Sorry, I couldn't process that.";

      // Add AI response to the chat
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(err.message);
      console.error('Error sending message:', err);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now(),
        role: 'error',
        content: `Error: ${err.message}`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatkit-container">
      <div className="chatkit-header">
        <h2>AI Assistant</h2>
      </div>

      <div className="chatkit-messages">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`chatkit-message chatkit-message-${message.role}`}
          >
            <div className="chatkit-message-content">
              {message.content}
            </div>
            <div className="chatkit-message-timestamp">
              {message.timestamp ? new Date(message.timestamp).toLocaleTimeString() : ''}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="chatkit-message chatkit-message-assistant">
            <div className="chatkit-message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chatkit-input-form">
        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message here..."
            disabled={isLoading}
            className="chatkit-input"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="chatkit-send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>

        {error && (
          <div className="chatkit-error-message">
            {error}
          </div>
        )}
      </form>

      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatKitComponent;