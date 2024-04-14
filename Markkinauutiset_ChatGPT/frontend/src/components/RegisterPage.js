import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import PhoneInput from 'react-phone-number-input';
import { countries as countriesList } from 'countries-list';
import FlashMessage from './FlashMessage';
import 'react-phone-number-input/style.css';
import './Forms.css';


const countryOptions = Object.entries(countriesList).map(([code, { name }]) => ({
  value: code,
  label: name,
}));

function RegisterPage() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [address, setAddress] = useState('');
  const [country, setCountry] = useState(null);
  const [phone, setPhone] = useState('');
  const [defaultCountry, setDefaultCountry] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleCountryChange = selectedOption => {
    console.log("Selected country option:", selectedOption); // Debug log
    setCountry(selectedOption);
    setDefaultCountry(selectedOption.value);
  };


  const handleSubmit = async (event) => {
    event.preventDefault();
    const user = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
      address:address,
      country: country?.label,
      phone: phone
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
          <label>First Name: *</label>
          <input
            type="text"
            className="form-control"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Last Name: *</label>
          <input
            type="text"
            className="form-control"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Email: *</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Address: (optional)</label>
          <input
            type="text"
            className="form-control"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
        </div>
        <div className="form-group">
        <label>Country: (optional)</label>
        <Select
          options={countryOptions}
          value={country}
          onChange={handleCountryChange}
        />
      </div>
      <div className="form-group">
        <label>Phone: (optional)</label>
        <PhoneInput
          international
          defaultCountry={defaultCountry}
          value={phone}
          onChange={setPhone}
        />
      </div>
        <div className="form-group">
          <label>Password: *</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary form-button">
          Register
        </button>
      </form>
    </div>
  );
}

export default RegisterPage;