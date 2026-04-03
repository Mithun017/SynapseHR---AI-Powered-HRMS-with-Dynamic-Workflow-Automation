import React from 'react';

const users = {
  1: { role: 'employee', name: 'Mithun' },
  2: { role: 'manager', name: 'Sushma' },
  3: { role: 'admin', name: 'Makesh' }
};

const RoleSwitcher = ({ role, setRole, userId, setUserId }) => {
  const handleChange = (e) => {
    const id = parseInt(e.target.value);
    setUserId(id);
    setRole(users[id].role);
  };

  return (
    <div className="role-switcher" style={{ margin: 0 }}>
      <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Simulate User:</span>
      <select className="role-select" value={userId} onChange={handleChange}>
        {Object.entries(users).map(([id, user]) => (
          <option key={id} value={id}>
            {user.name} ({user.role})
          </option>
        ))}
      </select>
    </div>
  );
};

export default RoleSwitcher;
