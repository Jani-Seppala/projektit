import React from 'react';
import { useUser } from '../components/UserContext';
import { useNavigate } from 'react-router-dom';

function Logout() {
  const { logout } = useUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    console.log('You have been logged out.');
    navigate('/', { state: { message: 'You have been logged out.', type: 'success' } });
  };

  return <a className="nav-link" onClick={handleLogout}>Logout</a>;
}

export default Logout;