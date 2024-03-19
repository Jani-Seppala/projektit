import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import FavoritesPage from './components/FavoritesPage';
import StockPage from './components/StockPage';
import SearchBar from './components/SearchBar';
import Logout from './components/Logout';
import NewsAndAnalysis from './components/NewsAndAnalysis';
import { useUser, UserProvider } from './components/UserContext';
import FlashMessage from './components/FlashMessage';


function App() {
  const { isLoggedIn } = useUser();
  // const location = useLocation(); // Added
  // // Extract flash message from location state
  // const flashMessage = location.state?.flashMessage; // Added
  // const flashMessageType = location.state?.flashMessageType; // Added

  return (
    <Router>
      {/* {flashMessage && <FlashMessage message={flashMessage} type={flashMessageType} />} // Added */}
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
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
                  <li className="nav-item"><Logout /></li>
                </>
              )}
            </ul>
            <SearchBar />
          </div>
        </div>
      </nav>
      <div className="container">
        <Routes>
          <Route path="/" element={<NewsAndAnalysis />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          <Route path="/stocks/:stockId" element={<StockPage />} />
        </Routes>
      </div>
    </Router>
  );
}

// // This function needs to be inside App or another component to use the useLocation hook
// function WrappedApp() {
//   return (
//     <UserProvider>
//       <App /> {/* This now includes the useLocation hook for flash messages */}
//     </UserProvider>
//   );
// }

// export default WrappedApp; // Modified


export default function WrappedApp() {
  return (
    <UserProvider>
      <App />
    </UserProvider>
  );
}

