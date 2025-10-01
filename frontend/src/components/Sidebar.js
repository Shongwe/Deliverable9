import React from 'react';
import '../styles/Sidebar.css';

function Sidebar({ onLogout }) {
  return (
    <aside className="sidebar">
      <h2>IDS Menu</h2>
      <ul>
        <li>Overview</li>
        <li>Alerts</li>
        <li>Logs</li>
      </ul>
      <button onClick={onLogout}>Logout</button>
    </aside>
  );
}

export default Sidebar;
