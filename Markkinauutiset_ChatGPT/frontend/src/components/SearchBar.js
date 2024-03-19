import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './SearchBar.css'; // Make sure you have this CSS file

function SearchBar() {
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

  return (
    <div>
      <input
        className="form-control me-2"
        type="search"
        placeholder="Search Stocks"
        aria-label="Search"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      {searchResults.length > 0 && (
        <div className="search-results">
          {searchResults.map(stock => (
            <div
              key={stock._id}
              onClick={() => handleSearchSelect(stock._id)}
              className="search-result-item"
            >
              {stock.company} ({stock.sector})
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchBar;
