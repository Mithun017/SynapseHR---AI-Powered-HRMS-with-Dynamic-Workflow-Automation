import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Dashboard = ({ role, onAction, children }) => {
  const isEmployee = role === 'employee';
  const isManager = role === 'manager';
  const isAdmin = role === 'admin';

  return (
    <main className="main-content">
      <div style={{ gridColumn: '1 / -1', marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '800', marginBottom: '0.5rem' }}>
            {isEmployee && "My Workforce Portal"}
            {isManager && "Management Console"}
            {isAdmin && "Administrative Suite"}
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Welcome back! Here's a quick look at your {role} dashboard.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1.5rem' }}>
            <div className="card-premium" style={{ padding: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                    {isEmployee ? "Leave Balance" : "Team Headcount"}
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: '800' }}>{isEmployee ? "18 Days" : "24 members"}</div>
            </div>
            <div className="card-premium" style={{ padding: '1.25rem' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                    {isEmployee ? "Salary Status" : "Active Projects"}
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: '800', color: 'var(--success)' }}>{isEmployee ? "Paid" : "12 Active"}</div>
            </div>
            <div className="card-premium" style={{ padding: '1.25rem', borderLeft: '4px solid var(--accent)', position: 'relative', zIndex: 10 }}>
                <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                    Quick Actions
                </div>
                <div style={{ display: 'flex', gap: '0.75rem' }}>
                    {isEmployee && (
                        <motion.button 
                            whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                            className="btn-primary" 
                            style={{ fontSize: '0.75rem', padding: '0.5rem 1rem', boxShadow: '0 4px 6px -1px rgba(30, 64, 175, 0.2)' }} 
                            onClick={() => onAction("I want to raise a ticket")}
                        >
                            Raise Ticket
                        </motion.button>
                    )}
                    {isManager && (
                        <motion.button 
                            whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                            className="btn-primary" 
                            style={{ fontSize: '0.75rem', padding: '0.5rem 1rem' }} 
                            onClick={() => onAction("Show my workspace")}
                        >
                            Review Team
                        </motion.button>
                    )}
                    {isAdmin && (
                        <motion.button 
                            whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                            className="btn-primary" 
                            style={{ fontSize: '0.75rem', padding: '0.5rem 1rem' }} 
                            onClick={() => onAction("I want to add a user")}
                        >
                            Add User
                        </motion.button>
                    )}
                </div>
            </div>
        </div>
      </div>

      <AnimatePresence>
        {children.length === 0 ? (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ 
                gridColumn: '1 / -1', textAlign: 'center', marginTop: '10vh',
                color: 'var(--text-muted)'
            }}
          >
            <p>Use the chat to load more tools and tickets.</p>
          </motion.div>
        ) : (
          children.map((card, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: -20 }}
              transition={{ delay: index * 0.1, duration: 0.3 }}
            >
              {card}
            </motion.div>
          ))
        )}
      </AnimatePresence>
    </main>
  );
};

export default Dashboard;
