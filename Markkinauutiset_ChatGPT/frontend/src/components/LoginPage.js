import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';
import { useUser } from '../components/UserContext';
import './LoginPage.css'; // Ensure you have CSS for styling this page similarly to your register page

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { setIsLoggedIn } = useUser(); // Add this line

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/api/users/login', { email, password });
      if (response.data.success) {
        console.log('Login successful:', response.data);
        localStorage.setItem('token', response.data.token);
        setIsLoggedIn(true);
        navigate('/');
        // console.log('Login successful:', response.data);
        // localStorage.setItem('token', response.data.token);
        // setIsLoggedIn(true);
        // navigate('/', {
        //   state: { flashMessage: 'Login successful!', flashMessageType: 'success' } // Pass flash message through state
        // });

      } else {
        console.error('Login failed:', response.data.message);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
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
        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
    </div>
  );
}

export default LoginPage;
