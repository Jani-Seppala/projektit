import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';
import { useUser } from '../components/UserContext';
import FlashMessage from './FlashMessage';
import './Forms.css';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { setIsLoggedIn } = useUser();
  

  const handleSubmit = async (e) => {
    e.preventDefault();

  try {
    const response = await axios.post('http://localhost:5000/api/users/login', { email, password });
    if (response.data.success) {
      console.log('Login successful:', response.data);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('userId', response.data.user._id);
      setIsLoggedIn(true);
      navigate('/', { state: { message: 'Logged in!', type: 'success' } });
    }
  } catch (error) {
    console.error('Login error:', error);
    if (error.response && error.response.status === 401) {
      setErrorMessage(error.response.data.message);
    } else {
      setErrorMessage('An unexpected error occurred.');
    }
  }
};

  return (
    <div className="login-page">
      {errorMessage && (
      <FlashMessage message={errorMessage} type="error" />
      )}
      {/* Check for location.state and render FlashMessage if present */}
      {location.state?.message && (
      <FlashMessage message={location.state.message} type={location.state.type} />
      )}
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary form-button">
          Login
        </button>
      </form>
    </div>
  );
}

export default LoginPage;
