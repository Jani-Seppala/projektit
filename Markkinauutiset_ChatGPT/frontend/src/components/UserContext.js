import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

function useUser() {
  return useContext(UserContext);
}

function UserProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

    // Initialize darkMode state based on localStorage or default to false
    const [darkMode, setDarkMode] = useState(() => {
      const storedDarkModePref = localStorage.getItem('darkMode');
      return storedDarkModePref === 'true' ? true : false;
    });

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  useEffect(() => {
    // Store the dark mode preference in localStorage
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]); // This effect runs when darkMode state changes

  const logout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const value = {
    isLoggedIn,
    setIsLoggedIn,
    logout,
    darkMode,
    toggleDarkMode,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

export { UserContext, useUser, UserProvider };