import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, MessageSquare, X, Minus, Maximize2 } from 'lucide-react';

const ChatInterface = ({ role, userId, onNewCard }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(true);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/agent/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMsg.content,
          user_id: userId,
          role: role,
          session_id: "test-session"
        })
      });
      
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `Server error: ${response.status}`);
      }
      
      const agentMsg = {
        role: 'agent',
        content: data.reasoning || (data.intent ? `Intent: ${data.intent}` : "I'm not sure how to respond.")
      };
      
      setMessages(prev => [...prev, agentMsg]);
      
      if (data.ui) {
        onNewCard(data.ui);
      }
      
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { 
        role: 'agent', 
        content: `Error: ${error.message}. Please check if the backend is running and configured correctly.` 
      }]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) {
    return (
        <motion.div 
            style={{ 
                position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 100,
                width: '64px', height: '64px', borderRadius: '50%',
                background: 'var(--primary)', color: 'white',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: 'var(--shadow-lg)', cursor: 'pointer'
            }}
            whileHover={{ scale: 1.1 }}
            onClick={() => setIsOpen(true)}
        >
            <MessageSquare size={24} />
        </motion.div>
    )
  }

  return (
    <motion.div 
        initial={{ opacity: 0, y: 50, scale: 0.9 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 50, scale: 0.9 }}
        className="chat-widget"
    >
      <div className="chat-header">
        <MessageSquare size={20} />
        <span style={{ fontWeight: '600', flex: 1 }}>AI Chat Assistant</span>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
            <Minus size={18} style={{ cursor: 'pointer', opacity: 0.7 }} onClick={() => setIsOpen(false)} />
            <X size={18} style={{ cursor: 'pointer', opacity: 0.7 }} onClick={() => setIsOpen(false)} />
        </div>
      </div>

      <div className="chat-messages" ref={scrollRef}>
        <div className="chat-bubble agent">
            Hi! I am your HR assistant. How can I help you today?
        </div>
        {messages.map((m, i) => (
          <motion.div 
            key={i} 
            initial={{ opacity: 0, x: m.role === 'user' ? 20 : -20 }}
            animate={{ opacity: 1, x: 0 }}
            className={`chat-bubble ${m.role}`}
          >
            {m.content}
          </motion.div>
        ))}
        {loading && (
            <motion.div 
                initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className="chat-bubble agent" style={{ fontStyle: 'italic', opacity: 0.6 }}
            >
                Processing...
            </motion.div>
        )}
      </div>

      <div className="chat-footer">
        <input 
          className="chat-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Ask something..."
        />
        <button className="btn-primary" onClick={sendMessage} disabled={loading} style={{ width: '42px', padding: '0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Send size={18} />
        </button>
      </div>
    </motion.div>
  );
};

export default ChatInterface;
