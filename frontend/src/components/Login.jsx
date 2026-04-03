import React from 'react';
import { motion } from 'framer-motion';
import { User, ShieldCheck, Users, LayoutDashboard } from 'lucide-react';

const users = [
  { id: 1, role: 'employee', name: 'Mithun', icon: User, color: '#3b82f6' },
  { id: 2, role: 'manager', name: 'Sushma', icon: Users, color: '#10b981' },
  { id: 3, role: 'admin', name: 'Makesh', icon: ShieldCheck, color: '#ef4444' }
];

const Login = ({ onLogin }) => {
  return (
    <div style={{ 
      height: '100vh', width: '100vw', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%)', color: 'white'
    }}>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ 
          background: 'rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(10px)',
          padding: '3rem', borderRadius: '24px', border: '1px solid rgba(255,255,255,0.2)',
          textAlign: 'center', maxWidth: '500px', width: '90%'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', marginBottom: '2rem' }}>
          <div style={{ background: 'white', padding: '0.75rem', borderRadius: '12px' }}>
            <LayoutDashboard color="#1e40af" size={32} />
          </div>
          <h1 style={{ fontSize: '2rem', fontWeight: '800' }}>SynapseHR</h1>
        </div>
        
        <p style={{ opacity: 0.8, marginBottom: '2.5rem' }}>Select your role to enter the workspace</p>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {users.map((user) => {
            const Icon = user.icon;
            return (
              <motion.button
                key={user.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onLogin(user)}
                style={{
                  display: 'flex', alignItems: 'center', gap: '1.25rem',
                  padding: '1.25rem', borderRadius: '16px', border: 'none',
                  background: 'rgba(255,255,255,0.1)', color: 'white',
                  cursor: 'pointer', textAlign: 'left', transition: 'background 0.3s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.2)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.1)'}
              >
                <div style={{ 
                  background: user.color, padding: '0.75rem', borderRadius: '12px',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                  <Icon size={24} />
                </div>
                <div>
                  <div style={{ fontWeight: '700', fontSize: '1.1rem' }}>{user.name}</div>
                  <div style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'capitalize' }}>{user.role} Access</div>
                </div>
              </motion.button>
            );
          })}
        </div>
        
        <div style={{ marginTop: '2rem', fontSize: '0.8rem', opacity: 0.5 }}>
          Secure Enterprise Authentication System v2.0
        </div>
      </motion.div>
    </div>
  );
};

export default Login;
