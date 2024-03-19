import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook for redirection
import { useUser } from '../App.js'; // Add this line
import './RegisterPage.css'; // Assuming you have CSS for styling the page and flash messages

function RegisterPage() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
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
        console.log('Registration succesful:');
        navigate('/login');
      } else {
        console.error('Registration failed:', response.data.message);
      }
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  // Your form rendering code here...

  // Display flash message somewhere in your component, styled based on its type
  return (
    <div>
      <form onSubmit={handleSubmit} className="register-form">
  <div className="form-group">
    <label>
      First Name:
      <input type="text" value={firstName} onChange={e => setFirstName(e.target.value)} required className="form-control" />
    </label>
  </div>
  <div className="form-group">
    <label>
      Last Name:
      <input type="text" value={lastName} onChange={e => setLastName(e.target.value)} required className="form-control" />
    </label>
  </div>
  <div className="form-group">
    <label>
      Email:
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} required className="form-control" />
    </label>
  </div>
  <div className="form-group">
    <label>
      Password:
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} required className="form-control" />
    </label>
  </div>
  <input type="submit" value="Register" className="btn btn-primary" />
</form>
    </div>
  );
}

export default RegisterPage;

