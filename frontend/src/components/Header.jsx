import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LayoutDashboard, LogOut, ChevronDown, Bell, User } from 'lucide-react';

const users = {
  1: { role: 'employee', name: 'Mithun' },
  2: { role: 'manager', name: 'Sushma' },
  3: { role: 'admin', name: 'Makesh' }
};

const Header = ({ role, userId, onLogout, onAction }) => {
  const currentUser = users[userId];

  return (
    <header className="header">
      <div style={{ display: 'flex', alignItems: 'center', gap: '3rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ 
            width: '32px', height: '32px', background: 'white', borderRadius: '8px',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
             <LayoutDashboard size={20} color="#1e40af" />
          </div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: '700', letterSpacing: '-0.025em' }}>SynapseHR</h1>
        </div>

        <nav style={{ display: 'flex', gap: '0.75rem', fontSize: '0.9rem', fontWeight: '600', position: 'relative', zIndex: 1000 }}>
            <motion.button 
              whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              onClick={() => onAction("Show my workspace")}
              style={{ 
                  background: 'rgba(255,255,255,0.1)', color: 'white', border: 'none', 
                  padding: '0.5rem 1.25rem', borderRadius: '12px', cursor: 'pointer',
                  borderBottom: '2px solid white'
              }}
            >
              Dashboard
            </motion.button>
            <motion.button 
              whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              onClick={() => onAction("List my tickets")}
              style={{ 
                  background: 'transparent', color: 'white', border: 'none', 
                  padding: '0.5rem 1.25rem', borderRadius: '12px', cursor: 'pointer',
                  opacity: 0.8
              }}
            >
              My Tickets
            </motion.button>
            <motion.button 
              whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              onClick={() => onAction("Show my payroll")}
              style={{ 
                  background: 'transparent', color: 'white', border: 'none', 
                  padding: '0.5rem 1.25rem', borderRadius: '12px', cursor: 'pointer',
                  opacity: 0.8
              }}
            >
              My Payroll
            </motion.button>
            {role === 'admin' && (
              <motion.button 
                whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                onClick={() => onAction("Show employee directory")}
                style={{ 
                    background: 'transparent', color: 'white', border: 'none', 
                    padding: '0.5rem 1.25rem', borderRadius: '12px', cursor: 'pointer',
                    opacity: 0.8
                }}
              >
                Users
              </motion.button>
            )}
        </nav>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
        <Bell size={20} style={{ opacity: 0.8, cursor: 'pointer' }} />
        
        <div 
          onClick={onLogout}
          style={{ 
            display: 'flex', alignItems: 'center', gap: '0.75rem', paddingLeft: '1.5rem', 
            borderLeft: '1px solid rgba(255,255,255,0.2)', cursor: 'pointer' 
          }}
        >
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: '600' }}>{currentUser.name}</div>
            <div style={{ fontSize: '0.7rem', opacity: 0.7, textTransform: 'capitalize' }}>{currentUser.role}</div>
          </div>
          
          <div style={{ 
            width: '40px', height: '40px', borderRadius: '12px', background: 'rgba(255,255,255,0.1)',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <User size={20} />
          </div>
          <LogOut size={16} style={{ opacity: 0.6 }} />
        </div>
      </div>
    </header>
  );
};

export default Header;
