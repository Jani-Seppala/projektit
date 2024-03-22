import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import FlashMessage from './FlashMessage';
import './Forms.css';

function RegisterPage() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const user = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password
    };

    try {
      const response = await axios.post('http://localhost:5000/api/users/register', user);
      if (response.data.success) {
        console.log('Registration successful:');
        navigate('/login', { state: { message: 'Registration successful!', type: 'success' } });
      } else {
        console.error('Registration failed:', response.data.message);
        setErrorMessage(response.data.message);
      }
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  return (
    <div className="login-page">
      {errorMessage && (
        <FlashMessage message={errorMessage} type="error" />
      )}
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label>First Name:</label>
          <input
            type="text"
            className="form-control"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Last Name:</label>
          <input
            type="text"
            className="form-control"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />
        </div>
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
          Register
        </button>
      </form>
    </div>
  );
}

export default RegisterPage;