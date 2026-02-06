import React from 'react';

const MessageList = ({ messages }) => {
  return (
    <div className="message-list">
      {messages.map((message) => (
        <div 
          key={message.id} 
          className={`message-item ${message.sender === 'user' ? 'user-message' : 'ai-message'}`}
        >
          <div className="message-content">
            <div className="message-text">{message.content}</div>
            
            {/* Show tool calls if present */}
            {message.toolCalls && message.toolCalls.length > 0 && (
              <div className="tool-calls">
                <strong>Tools Used:</strong>
                {message.toolCalls.map((toolCall, index) => (
                  <div key={index} className="tool-call">
                    <span className="tool-name">{toolCall.tool_name}</span>
                    <span className="tool-args">Args: {JSON.stringify(toolCall.arguments)}</span>
                    {toolCall.result && (
                      <span className="tool-result">Result: {toolCall.result}</span>
                    )}
                  </div>
                ))}
              </div>
            )}
            
            {/* Show confirmation if present */}
            {message.confirmation && (
              <div className="confirmation">
                <em>✓ {message.confirmation}</em>
              </div>
            )}
            
            <div className="message-timestamp">
              {message.timestamp ? new Date(message.timestamp).toLocaleTimeString() : ''}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;