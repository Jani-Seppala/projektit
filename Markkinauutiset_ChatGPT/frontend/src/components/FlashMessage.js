import React from 'react';
import './FlashMessage.css'; // Assuming you have a CSS file for styles

const FlashMessage = ({ type, message }) => {
  return (
    <div className={`flash-message ${type}`}>
      {message}
    </div>
  );
};

export default FlashMessage;
