import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.css';


const Navbar = () => (
  <nav className="bg-gray-800 p-4 text-white flex space-x-6">
    <Link to="/">Dashboard</Link>
    <Link to="/alerts">Alerts</Link>
    <Link to="/sensors">Sensors</Link>
    <Link to="/threat-intel">Threat Intel</Link>
    <Link to="/settings">Settings</Link>
  </nav>
);

export default Navbar;
