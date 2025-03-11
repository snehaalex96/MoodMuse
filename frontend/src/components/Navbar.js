import React, { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useContext(AuthContext);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const handleLogout = (e) => {
    e.preventDefault();
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-brand">
          <Link to="/" className="logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="currentColor"/>
              <path d="M12.5 7H11V13L15.25 15.52L16 14.24L12.5 12.15V7Z" fill="currentColor"/>
            </svg>
            <span>MusicMind</span>
          </Link>
        </div>
        
        <div className="navbar-mobile-toggle" onClick={toggleMobileMenu}>
          <div className={`hamburger ${mobileMenuOpen ? 'active' : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        
        <div className={`navbar-menu ${mobileMenuOpen ? 'active' : ''}`}>
          <div className="navbar-start">
            <Link to="/" className="navbar-item" onClick={() => setMobileMenuOpen(false)}>
              Home
            </Link>
            <Link to="/recommendations" className="navbar-item" onClick={() => setMobileMenuOpen(false)}>
              Discover
            </Link>
          </div>
          
          <div className="navbar-end">
            {isAuthenticated ? (
              <>
                <Link to="/profile" className="navbar-item" onClick={() => setMobileMenuOpen(false)}>
                  <div className="user-avatar">
                    {user?.username?.charAt(0).toUpperCase()}
                  </div>
                  <span className="username">{user?.username}</span>
                </Link>
                <a href="#" className="navbar-item logout-btn" onClick={handleLogout}>
                  Logout
                </a>
              </>
            ) : (
              <>
                <Link to="/login" className="navbar-item" onClick={() => setMobileMenuOpen(false)}>
                  Login
                </Link>
                <Link to="/register" className="navbar-item register-btn" onClick={() => setMobileMenuOpen(false)}>
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;