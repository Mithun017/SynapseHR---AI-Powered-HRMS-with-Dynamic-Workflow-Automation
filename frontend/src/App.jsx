import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import Login from './components/Login';

// Card Renderer logic
import { LeaveCard, PayrollCard, OnboardingCard, ErrorCard, FormCard, ChartCard, TableCard, TicketCard } from './components/Cards';

const cardMap = {
  'TICKET_CARD': TicketCard,
  'LEAVE_CARD': LeaveCard,
  'PAYROLL_CARD': PayrollCard,
  'ONBOARDING_CARD': OnboardingCard,
  'ERROR_CARD': ErrorCard,
  'FORM_CARD': FormCard,
  'CHART_CARD': ChartCard,
  'TABLE_CARD': TableCard
};

function App() {
  const [role, setRole] = useState('employee');
  const [userId, setUserId] = useState(1);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [cards, setCards] = useState([]);

  const handleLogin = (user) => {
    setUserId(user.id);
    setRole(user.role);
    setIsLoggedIn(true);
    handleAction("Show my workspace", user.id, user.role);
  };

  const handleAction = async (actionCommand, overrideId, overrideRole) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/agent/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: actionCommand,
          user_id: overrideId || userId,
          role: overrideRole || role,
          session_id: "test-session"
        })
      });
      const data = await response.json();
      if (data.ui) addCard(data.ui);
    } catch (error) {
      console.error("Action failed", error);
    }
  };

  const addCard = (uiDescriptor) => {
    const Component = cardMap[uiDescriptor.type] || ErrorCard;
    const newCard = (
      <Component 
        key={Date.now() + Math.random()} 
        title={uiDescriptor.title} 
        data={uiDescriptor.data} 
        onAction={handleAction}
      />
    );
    setCards(prev => [newCard, ...prev]);
  };

  if (!isLoggedIn) {
     return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app-container">
      <Header 
         role={role} 
         userId={userId} 
         onLogout={() => setIsLoggedIn(false)}
         onAction={handleAction}
      />
      
      <Sidebar onAction={handleAction} />
      
      <Dashboard role={role} onAction={handleAction}>
        {cards}
      </Dashboard>

      <ChatInterface 
        role={role} 
        userId={userId} 
        onNewCard={addCard} 
      />
    </div>
  );
}

export default App;
