import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './FlashMessage.css';

function FlashMessage({ message, type, duration = 3000, onDismiss }) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      if (onDismiss) onDismiss();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onDismiss]);

  if (!isVisible) return null;

  return (
    <div className={`flash-message ${type}`}>
      {message}
    </div>
  );
}

FlashMessage.propTypes = {
  message: PropTypes.string.isRequired,
  type: PropTypes.string,
  duration: PropTypes.number,
  onDismiss: PropTypes.func
};

export default FlashMessage;
