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
  const [dataPoints, setDataPoints] = useState([]);

  useEffect(() => {
    const socket = io("http://localhost:5002");

    socket.on("new_alert", (data) => {
      const timestamp = new Date().toLocaleTimeString();
      const packets = data.packet_count || 0;

      setLabels(prev => [...prev.slice(-19), timestamp]);
      setDataPoints(prev => [...prev.slice(-19), packets]);
    });

    return () => socket.disconnect();
  }, []);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Sniffed Packets per Flow',
        data: dataPoints,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Live Sniffed Packet Count' },
    },
  };

  return (
    <div style={{ maxWidth: '800px', margin: 'auto' }}>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
}

export default LivePacketChart;