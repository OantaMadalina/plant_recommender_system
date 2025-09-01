import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';
import hangingPlants from './hanging-plants.jpeg'; // Ensure this path is correct

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    if (username === 'admin' && password === 'admin') {
      navigate('/admin-home');
    } else if (username === 'user' && password === 'user') {
      navigate('/user-home');
    } else {
      alert('Invalid credentials');
    }
  };

  return (
    <div className="login-container">
      <img src={hangingPlants} alt="Hanging Plants" className="background-image" />
      <div className="plant-animation">
        <div className="plant plant-one">
          <div className="stem"></div>
          <div className="petals">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div className="plant plant-two">
          <div className="stem"></div>
          <div className="petals">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div className="plant plant-three">
          <div className="stem"></div>
          <div className="petals">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div className="pot">
          <span className="top"></span>
          <span className="shape">
            <div className="pattern">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </span>
          <span className="base"></span>
        </div>
        <div className="shadow"></div>
      </div>
      <div className="login-box">
        <h2>Login</h2>
        <div className="login-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
