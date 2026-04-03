import React, { useState } from 'react';
import RoleSwitcher from './RoleSwitcher';
import ChatInterface from './ChatInterface';
import DynamicUI from './DynamicUI';

const Layout = ({ role, setRole, userId, setUserId }) => {
  const [dashboardCards, setDashboardCards] = useState([]);

  // This function is called by the chat when the backend returns a UI card
  const handleNewCard = (card) => {
    if (card) {
      setDashboardCards(prev => [card, ...prev]);
    }
  };

  return (
    <div className="layout-container">
      {/* Left Panel: Dashboard */}
      <div className="dashboard-panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '2rem' }}>
            SynapseHR Workspace
          </h1>
          <RoleSwitcher role={role} setRole={setRole} userId={userId} setUserId={setUserId} />
        </div>
        
        <div className="dashboard-content">
          {dashboardCards.length === 0 ? (
            <div style={{ color: 'var(--text-muted)' }}>No recent activity. Ask the agent via the chat panel.</div>
          ) : (
            dashboardCards.map((card, index) => (
              <DynamicUI key={index} uiDescriptor={card} />
            ))
          )}
        </div>
      </div>

      {/* Right Panel: Chat */}
      <div className="chat-panel">
        <div style={{ padding: '1rem', borderBottom: '1px solid var(--border-color)', fontWeight: 'bold' }}>
          Synapse Agent
        </div>
        <ChatInterface role={role} userId={userId} onNewCard={handleNewCard} />
      </div>
    </div>
  );
};

export default Layout;
