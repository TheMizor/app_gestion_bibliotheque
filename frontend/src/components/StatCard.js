import React from 'react';
import '../App.css';

function StatCard({ title, value, type = 'default' }) {
  return (
    <div className={`stat-card stat-${type}`}>
      <h3>{title}</h3>
      <p className="stat-number">{value}</p>
    </div>
  );
}

export default StatCard;

