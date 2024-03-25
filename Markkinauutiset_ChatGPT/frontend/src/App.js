import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import FavoritesPage from './components/FavoritesPage';
import StockPage from './components/StockPage';
import InfoPage from './components/InfoPage';
import SearchBar from './components/SearchBar';
import Logout from './components/Logout';
import NewsAndAnalysis from './components/NewsAndAnalysis';
import { useUser, UserProvider } from './components/UserContext';
import './App.css';

function App() {
  const { isLoggedIn } = useUser();
  const [logoutCount, setLogoutCount] = useState(0);

  const handleLogout = () => {
    setLogoutCount(logoutCount + 1);
  };

  return (
    <Router>
      <nav className="navbar navbar-expand-lg navbar-light bg-light fixed-navbar mb-4">
        <div className="container">
          <Link className="navbar-brand fs-2" to="/">News App</Link>
          <div className="navbar-collapse collapse">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0 fs-4">            
              {!isLoggedIn && (
                <>
                  <li className="nav-item"><Link className="nav-link" to="/login">Login</Link></li>
                  <li className="nav-item"><Link className="nav-link" to="/register">Register</Link></li>
                </>
              )}
              {isLoggedIn && (
                <>
                  <li className="nav-item"><Link className="nav-link" to="/favorites">Favorites</Link></li>
                  <li className="nav-item"><Logout onLogout={handleLogout} /></li>
                </>
              )}
              <li className="nav-item"><Link className="nav-link" to="/info">Info</Link></li>
            </ul>
            <SearchBar />
          </div>
        </div>
      </nav>
      <div className="nav-spacer"></div> {/* This line is added */}
      <div className="container">
        <Routes>
          <Route path="/" element={<NewsAndAnalysis key={logoutCount} />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          <Route path="/stocks/:stockId" element={<StockPage />} />
          <Route path="/info" element={<InfoPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default function WrappedApp() {
  return (
    <UserProvider>
      <App />
    </UserProvider>
  );
}