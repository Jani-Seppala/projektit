import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './SearchBar.css';
import { useUser } from './UserContext';


function SearchBar() {
  const { darkMode } = useUser(); // Use the useUser hook to access the darkMode state
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (searchTerm) {
      axios.get(`http://localhost:5000/api/stocks?query=${searchTerm}`)
        .then(response => setSearchResults(response.data))
        .catch(error => console.error('Failed to fetch stocks:', error));
    } else {
      setSearchResults([]);
    }
  }, [searchTerm]);

  const handleSearchSelect = (stockId) => {
    navigate(`/stocks/${stockId}`);
    setSearchTerm(''); // Empty the search bar
    setSearchResults([]); // Close the results list
  };

// Conditional classes based on darkMode
const resultsClass = darkMode ? "search-results dark-mode-results" : "search-results";

  return (
    <div>
      <input
        className={`form-control me-2 ${darkMode ? 'dark-mode-input' : ''}`}
        type="search"
        placeholder="Search Stocks"
        aria-label="Search"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      {searchResults.length > 0 && (
        <div className={resultsClass}>
          {searchResults.map(stock => (
            <div
              key={stock._id}
              onClick={() => handleSearchSelect(stock._id)}
              className="search-result-item"
            >
              {stock.name} ({stock.sector})
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
