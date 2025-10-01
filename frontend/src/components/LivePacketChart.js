import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { io } from 'socket.io-client';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

function LivePacketChart() {
  const [labels, setLabels] = useState([]);
  const [benignPoints, setBenignPoints] = useState([]);
  const [maliciousPoints, setMaliciousPoints] = useState([]);

  useEffect(() => {
    const socket = io("http://localhost:5002");

    socket.on("new_alert", (data) => {
      const timestamp = new Date().toLocaleTimeString();
      const packets = data.packet_count || 0;

      setLabels(prev => [...prev.slice(-19), timestamp]);

      if (data.type === "Benign") {
        setBenignPoints(prev => [...prev.slice(-19), packets]);
        setMaliciousPoints(prev => [...prev.slice(-19), 0]);
      } else {
        setBenignPoints(prev => [...prev.slice(-19), 0]);
        setMaliciousPoints(prev => [...prev.slice(-19), packets]);
      }
    });

    return () => socket.disconnect();
  }, []);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Benign Packets',
        data: benignPoints,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.3,
      },
      {
        label: 'Malicious Packets',
        data: maliciousPoints,
        fill: false,
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Live Traffic Classification' },
    },
  };

  return (
    <div style={{ maxWidth: '800px', margin: 'auto' }}>
      {labels.length === 0 ? (
        <p style={{ textAlign: 'center', fontStyle: 'italic', marginTop: '2rem' }}>
          Waiting for live traffic...
        </p>
      ) : (
        <Line data={chartData} options={chartOptions} />
      )}
    </div>
  );
}

export default LivePacketChart;