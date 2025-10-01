import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const socket = io("http://localhost:5002");

    socket.on("new_alert", (data) => {
      const formatted = {
        time: data.timestamp,
        source: data.device.replace("flow-", ""),
        dest: "N/A", 
        type: data.type,
        status: data.type === "SYN Flood" ? "Blocked" : "Investigating"
      };
      setAlerts(prev => [formatted, ...prev.slice(0, 19)]); 
    });

    return () => socket.disconnect();
  }, []);

  return (
    <div>
      <h2 className="text-xl mb-3">Intrusion Alerts</h2>
      <table className="w-full table-auto border">
        <thead className="bg-gray-200">
          <tr>
            <th>Timestamp</th>
            <th>Source IP</th>
            <th>Destination IP</th>
            <th>Type</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert, index) => (
            <tr key={index} className="text-center">
              <td>{alert.time}</td>
              <td>{alert.source}</td>
              <td>{alert.dest}</td>
              <td>{alert.type}</td>
              <td>{alert.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Alerts;