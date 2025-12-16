import React from 'react';
import '../App.css';

function SearchBar({ value, onChange, placeholder = "Rechercher..." }) {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="search-input"
      />
      <span className="search-icon">🔍</span>
    </div>
  );
}

export default SearchBar;

