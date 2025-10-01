import React from 'react';
import Sidebar from './Sidebar';
import MetricsDisplay from './MetricsDisplay';
import LivePacketChart from './LivePacketChart';
import Alerts from './Alerts';

import '../styles/Dashboard.css';

function Dashboard({ onLogout }) {
  return (
    <div className="dashboard-container">
      <Sidebar onLogout={onLogout} />

      <main className="dashboard-content">
        <header className="dashboard-header">
          <h1>Intrusion Detection Dashboard</h1>
        </header>

        <section className="metrics-section">
          <MetricsDisplay />
          <LivePacketChart />
        </section>

        <section className="alerts-section">
          <Alerts />
        </section>
      </main>
    </div>
  );
}

export default Dashboard;