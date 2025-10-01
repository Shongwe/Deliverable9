import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import '../styles/MetricsDisplay.css';

function MetricsDisplay() {
  const [metrics, setMetrics] = useState({
    totalPackets: 0,
    suspiciousEvents: 0,
    blockedIPs: 0,
    activeConnections: 0,
    ddosAlerts: 0,
  });

useEffect(() => {
  const fetchMetrics = async () => {
    try {
      const res = await fetch("http://localhost:5002/metrics");
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      console.error("Error fetching metrics:", err);
    }
  };

  fetchMetrics();
  const interval = setInterval(fetchMetrics, 5000);

  const socket = io("http://localhost:5002");

  socket.on("connect", () => {
    console.log("Connected to dashboard socket");
  });

  socket.on("new_alert", (data) => {
    console.log("Live alert received:", data);
    setMetrics(prev => ({
      ...prev,
      totalPackets: prev.totalPackets + 1,
      suspiciousEvents: data.type !== "Benign" ? prev.suspiciousEvents + 1 : prev.suspiciousEvents,
      ddosAlerts: data.type === "SYN Flood" ? prev.ddosAlerts + 1 : prev.ddosAlerts
    }));
  });

  socket.on("blocked_ip", (data) => {
    console.log("Blocked IP received:", data.ip);
    setMetrics(prev => ({
      ...prev,
      blockedIPs: prev.blockedIPs + 1
    }));
  });

  return () => {
    clearInterval(interval);
    socket.disconnect();
  };
}, []);

  return (
    <div className="metrics-grid">
      <div className="metric-card">
        <h3>Total Packets</h3>
        <p>{metrics.totalPackets.toLocaleString()}</p>
      </div>

      <div className="metric-card warning">
        <h3>Suspicious Events</h3>
        <p>{metrics.suspiciousEvents}</p>
      </div>

      <div className="metric-card danger">
        <h3>Blocked IPs</h3>
        <p>{metrics.blockedIPs}</p>
      </div>

      <div className="metric-card">
        <h3>Active Connections</h3>
        <p>{metrics.activeConnections}</p>
      </div>

      <div className="metric-card critical">
        <h3>DDoS Alerts</h3>
        <p>{metrics.ddosAlerts}</p>
      </div>
    </div>
  );
}

export default MetricsDisplay;