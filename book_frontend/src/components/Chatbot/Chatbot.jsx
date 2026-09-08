import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! I\'m your documentation assistant. How can I help you today?', sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputValue }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        text: data.answer || 'I couldn\'t process your request. Please try again.',
        sender: 'bot'
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please check if the backend server is running.');

      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I\'m having trouble connecting. Please make sure the backend server is running.',
        sender: 'bot'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      { id: 1, text: 'Hello! I\'m your documentation assistant. How can I help you today?', sender: 'bot' }
    ]);
    setError(null);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <>
      {/* Floating chat button */}
      <button
        className="chatbot-toggle-button"
        onClick={toggleChat}
        aria-label="Open chat"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.5L14.06 19.44C13.28 20.22 12.19 20.22 11.42 19.44C10.64 18.66 10.64 17.57 11.42 16.8L13 15.25H12C10.343 15.25 9 13.907 9 12.25V5.75C9 4.093 10.343 2.75 12 2.75H18C19.657 2.75 21 4.093 21 5.75V15Z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M11 7.75H13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M11 11.25H16" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {/* Chatbot popup */}
      {isOpen && (
        <div className="chatbot-popup-overlay" onClick={closeChat}>
          <div
            className="chatbot-popup"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="chatbot-header">
              <h3>Documentation Assistant</h3>
              <button
                onClick={closeChat}
                className="close-chat-btn"
                aria-label="Close chat"
              >
                ×
              </button>
            </div>

            <div className="chatbot-messages">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}-message`}
                >
                  <div className="message-text">{message.text}</div>
                  <div className="message-sender">{message.sender === 'bot' ? 'Assistant' : 'You'}</div>
                </div>
              ))}

              {isLoading && (
                <div className="message bot-message">
                  <div className="message-text">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                  <div className="message-sender">Assistant</div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {error && (
              <div className="chatbot-error">
                {error}
              </div>
            )}

            <div className="chatbot-input-area">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about the documentation..."
                disabled={isLoading}
                rows={2}
              />
              <button
                onClick={sendMessage}
                disabled={!inputValue.trim() || isLoading}
                className="send-button"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;