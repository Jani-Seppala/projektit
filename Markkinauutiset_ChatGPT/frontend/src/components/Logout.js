import React from 'react';
import { useUser } from '../components/UserContext';
import { useNavigate } from 'react-router-dom';

function Logout({ onLogout }) {
  const { logout } = useUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    console.log('You have been logged out.');
    navigate('/', { state: { message: 'You have been logged out.', type: 'success' } });
    onLogout();
  };

  // return <a className="nav-link" onClick={handleLogout}>Logout</a>;
  return <button className="nav-link btn btn-link" onClick={handleLogout} style={{ border: 'none', backgroundColor: 'transparent', textDecoration: 'underline', color: 'blue' }}>Logout</button>;

}

export default Logout;