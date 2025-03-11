import React, { useState, useContext, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');
  
  const { login, error, clearError, isAuthenticated } = useContext(AuthContext);
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
  }, [username, password, clearError, error]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!username) {
      setFormError('Username is required');
      return;
    }
    
    if (!password) {
      setFormError('Password is required');
      return;
    }
    
    // Submit login
    try {
      await login(username, password);
    } catch (err) {
      // Error handling is done in the AuthContext
      console.error('Login error:', err);
    }
  };
  
  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>Welcome Back</h1>
          <p>Log in to your account to continue</p>
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
              placeholder="Enter your username"
              autoComplete="username"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              autoComplete="current-password"
            />
          </div>
          
          <button type="submit" className="auth-button">
            Log In
          </button>
        </form>
        
        <div className="auth-footer">
          <p>
            Don't have an account? <Link to="/register">Register</Link>
          </p>
        </div>
      </div>
      
      <div className="auth-info">
        <div className="auth-info-content">
          <h2>Discover Music in a New Way</h2>
          <p>
            Our multimodal AI analyzes audio, visuals, and lyrics to find your perfect music match. 
            Upload an image, select a mood, or let us recommend songs based on your taste.
          </p>
          
          <div className="auth-features">
            <div className="auth-feature">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 3V13.55C11.41 13.21 10.73 13 10 13C7.79 13 6 14.79 6 17C6 19.21 7.79 21 10 21C12.21 21 14 19.21 14 17V7H18V3H12ZM10 19C8.9 19 8 18.1 8 17C8 15.9 8.9 15 10 15C11.1 15 12 15.9 12 17C12 18.1 11.1 19 10 19Z" fill="currentColor"/>
              </svg>
              <div>
                <h3>Audio Analysis</h3>
                <p>We analyze rhythm, melody, and audio features</p>
              </div>
            </div>
            
            <div className="auth-feature">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 19V5C21 3.9 20.1 3 19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19ZM8.5 13.5L11 16.51L14.5 12L19 18H5L8.5 13.5Z" fill="currentColor"/>
              </svg>
              <div>
                <h3>Visual Understanding</h3>
                <p>Find music that matches any image</p>
              </div>
            </div>
            
            <div className="auth-feature">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H5.17L4 17.17V4H20V16Z" fill="currentColor"/>
              </svg>
              <div>
                <h3>Lyrical Analysis</h3>
                <p>Understand themes and sentiment in lyrics</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;