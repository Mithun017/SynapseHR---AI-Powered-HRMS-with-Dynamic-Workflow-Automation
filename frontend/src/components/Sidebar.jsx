import React from 'react';
import { motion } from 'framer-motion';
import { LayoutGrid, CheckSquare, Users, FileText, Settings, BarChart } from 'lucide-react';

const Sidebar = ({ onAction }) => {
  return (
    <aside className="sidebar">
      <motion.div 
        whileHover={{ scale: 1.1 }} 
        className="nav-icon active"
        onClick={() => onAction("Show my workspace")}
      >
        <LayoutGrid size={24} />
      </motion.div>
      <motion.div 
        whileHover={{ scale: 1.1 }} 
        className="nav-icon"
        onClick={() => onAction("List my tickets")}
      >
        <CheckSquare size={24} />
      </motion.div>
      <motion.div 
        whileHover={{ scale: 1.1 }} 
        className="nav-icon"
        onClick={() => onAction("Show employee directory")}
      >
        <Users size={24} />
      </motion.div>
      <motion.div 
        whileHover={{ scale: 1.1 }} 
        className="nav-icon"
        onClick={() => onAction("Show analytics")}
      >
        <BarChart size={24} />
      </motion.div>
      <motion.div 
        whileHover={{ scale: 1.1 }} 
        className="nav-icon"
        onClick={() => onAction("Show reports")}
      >
        <FileText size={24} />
      </motion.div>
      
      <div style={{ marginTop: 'auto' }}>
        <motion.div whileHover={{ scale: 1.1 }} className="nav-icon">
            <Settings size={24} />
        </motion.div>
      </div>
    </aside>
  );
};

export default Sidebar;
