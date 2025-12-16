import React from 'react';
import '../App.css';

function Modal({ show, onClose, title, children }) {
  if (!show) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button onClick={onClose} className="modal-close">&times;</button>
        </div>
        <div className="modal-content">
          {children}
        </div>
      </div>
    </div>
  );
}

export default Modal;

