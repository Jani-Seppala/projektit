import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

function useUser() {
  return useContext(UserContext);
}

function UserProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const logout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  const value = {
    isLoggedIn,
    setIsLoggedIn,
    logout,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

export { UserContext, useUser, UserProvider };