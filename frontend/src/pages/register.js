import React, { useState, useContext, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [formError, setFormError] = useState('');
  
  const { register, error, clearError, isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();
  
  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);
  
  // Set form error if there's an auth error
  useEffect(() => {
    if (error) {
      setFormError(error);
    }
  }, [error]);
  
  // Clear errors when inputs change
  useEffect(() => {
    if (formError) {
      setFormError('');
    }
    if (error) {
      clearError();
    }
  }, [username, email, password, confirmPassword, clearError, error]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!username) {
      setFormError('Username is required');
      return;
    }
    
    if (!email) {
      setFormError('Email is required');
      return;
    }
    
    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setFormError('Please enter a valid email address');
      return;
    }
    
    if (!password) {
      setFormError('Password is required');
      return;
    }
    
    if (password.length < 6) {
      setFormError('Password must be at least 6 characters');
      return;
    }
    
    if (password !== confirmPassword) {
      setFormError('Passwords do not match');
      return;
    }
    
    // Submit registration
    try {
      await register(username, email, password);
    } catch (err) {
      // Error handling is done in the AuthContext
      console.error('Registration error:', err);
    }
  };
  
  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>Create Account</h1>
          <p>Sign up to discover music in a whole new way</p>
        </div>
        
        {formError && (
          <div className="auth-error">
            {formError}
          </div>
        )}
        
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              autoComplete="username"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              autoComplete="email"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password"
              autoComplete="new-password"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              autoComplete="new-password"
            />
          </div>
          
          <button type="submit" className="auth-button">
            Create Account
          </button>
        </form>
        
        <div className="auth-footer">
          <p>
            Already have an account? <Link to="/login">Log In</Link>
          </p>
        </div>
      </div>
      
      <div className="auth-info">
        <div className="auth-info-content">
          <h2>Why Join MusicMind?</h2>
          <p>
            Create an account to unlock personalized music recommendations 
            and keep track of your favorite songs.
          </p>
          
          <div className="auth-features">
            <div className="auth-feature">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 22C10.93 22 9.86 21.83 8.83 21.48L7.41 21.01L8.83 20.54C12.78 19.31 15 15.88 15 12C15 8.12 12.78 4.69 8.83 3.47L7.41 2.99L8.83 2.52C9.86 2.17 10.93 2 12 2C17.5 2 22 6.5 22 12C22 17.5 17.5 22 12 22ZM5 12C5 13.93 5.64 15.75 6.8 17.2L8.21 14.54C7.75 13.76 7.5 12.89 7.5 12C7.5 11.11 7.75 10.24 8.21 9.46L6.8 6.8C5.64 8.25 5 10.07 5 12Z" fill="currentColor"/>
              </svg>
              <div>
                <h3>Personalized Recommendations</h3>
                <p>Get music suggestions tailored to your taste</p>
              </div>
            </div>
            
            <div className="auth-feature">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.03L12 21.35Z" fill="currentColor"/>
              </svg>
              <div>
                <h3>Save Favorites</h3>
                <p>Like songs and create playlists</p>
              </div>
            </div>
            
            <div className="auth-feature">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 5C13.66 5 15 6.34 15 8C15 9.66 13.66 11 12 11C10.34 11 9 9.66 9 8C9 6.34 10.34 5 12 5ZM12 19.2C9.5 19.2 7.29 17.92 6 15.98C6.03 13.99 10 12.9 12 12.9C13.99 12.9 17.97 13.99 18 15.98C16.71 17.92 14.5 19.2 12 19.2Z" fill="currentColor"/>
              </svg>
              <div>
                <h3>User Profile</h3>
                <p>Track your music history and preferences</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;