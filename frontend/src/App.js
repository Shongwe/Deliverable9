import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import Dashboard from './components/Dashboard';
import Alerts from './components/Alerts';
import Sensors from './components/Sensors';
import ThreatIntel from './components/LivePacketChart';
import Settings from './components/Settings';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="p-4">
        <Routes>
          <Route path="/login" element={<LoginForm onLogin={handleLogin} />} />

          <Route
            path="/"
            element={isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/login" />}
          />
          <Route
            path="/alerts"
            element={isAuthenticated ? <Alerts /> : <Navigate to="/login" />}
          />
          <Route
            path="/sensors"
            element={isAuthenticated ? <Sensors /> : <Navigate to="/login" />}
          />
          <Route
            path="/LivePacketChart"
            element={isAuthenticated ? <ThreatIntel /> : <Navigate to="/login" />}
          />
          <Route
            path="/settings"
            element={isAuthenticated ? <Settings /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
