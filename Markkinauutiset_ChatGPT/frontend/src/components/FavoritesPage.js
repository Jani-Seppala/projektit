import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './FavoritesPage.css'; // Assuming you have a CSS file for styling

function FavoritesPage() {
  const [stocks, setStocks] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const token = localStorage.getItem('token'); // Assuming JWT token is stored in localStorage

  // useEffect(() => {
  //   axios.get('http://localhost:5000/api/stocks', {
  //     headers: {
  //       Authorization: `Bearer ${token}`
  //     }
  //   })
  //   .then(response => setStocks(response.data))
  //   .catch(error => console.error("Failed to fetch stocks", error));

  //   // Also fetch the user's current favorites
  //   axios.get('http://localhost:5000/api/favorites', {
  //     headers: {
  //       Authorization: `Bearer ${token}`
  //     }
  //   })
  //   .then(response => setFavorites(response.data))
  //   .catch(error => console.error("Failed to fetch favorites", error));
  // }, [token]);

  useEffect(() => {
    // Fetch the user's current favorites directly with detailed information
    axios.get('http://localhost:5000/api/favorites', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(response => setFavorites(response.data))
    .catch(error => console.error("Failed to fetch favorites", error));
  }, [token]);
  

  // Filter stocks based on search term
  const filteredStocks = stocks.filter(stock => stock.company.toLowerCase().includes(searchTerm.toLowerCase()));

  // const handleAddToFavorites = (stockToAdd) => {
  //   if (!favorites.some(stock => stock._id === stockToAdd._id)) {
  //     const updatedFavorites = [...favorites, stockToAdd];
  //     setFavorites(updatedFavorites);
  //     // Update favorites in the backend
  //     axios.post('http://localhost:5000/api/favorites', updatedFavorites, {
  //       headers: {
  //         Authorization: `Bearer ${token}`
  //       }
  //     }).catch(error => console.error("Failed to update favorites", error));
  //   }
  const handleAddToFavorites = (stockToAdd) => {
    if (!favorites.some(stock => stock._id === stockToAdd._id)) {
        const updatedFavorites = [...favorites.map(stock => stock._id), stockToAdd._id];
        // Update the local state with full stock objects for rendering
        setFavorites([...favorites, stockToAdd]);
        // Update favorites in the backend with stock IDs
        axios.post('http://localhost:5000/api/favorites', { favorites: updatedFavorites }, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        }).catch(error => console.error("Failed to update favorites", error));
    }

  };


  const handleRemoveFromFavorites = (stockToRemove) => {
    const updatedFavoritesIds = favorites.filter(stock => stock._id !== stockToRemove._id).map(stock => stock._id);
    // Update the local state with remaining full stock objects for rendering
    setFavorites(favorites.filter(stock => stock._id !== stockToRemove._id));
    // Update favorites in the backend with remaining stock IDs
    axios.post('http://localhost:5000/api/favorites', { favorites: updatedFavoritesIds }, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    }).catch(error => console.error("Failed to update favorites", error));
};
  // const handleRemoveFromFavorites = (stockToRemove) => {
  //   const updatedFavorites = favorites.filter(stock => stock._id !== stockToRemove._id);
  //   setFavorites(updatedFavorites);
  //   // Update favorites in the backend
  //   axios.post('http://localhost:5000/api/favorites', updatedFavorites, {
  //     headers: {
  //       Authorization: `Bearer ${token}`
  //     }
  //   }).catch(error => console.error("Failed to update favorites", error));
  // };

  return (
    <div className="favorites-page">
      <h2>Your Favorite Stocks</h2>
      <div className="favorite-stocks">
        {favorites.map(stock => (
          <div key={stock._id} className="favorite-stock">
            {stock.company}
            <button onClick={() => handleRemoveFromFavorites(stock)}>X</button>
          </div>
        ))}
      </div>
      <h2>Select your favorite stocks</h2>
      <input
        type="text"
        placeholder="Search for a stock..."
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        className="form-control search-box"
      />
      {searchTerm.length >= 1 && filteredStocks.map(stock => (
        <div key={stock._id} className="search-result" onClick={() => handleAddToFavorites(stock)}>
          {stock.company}
        </div>
      ))}
    </div>
  );
}

export default FavoritesPage;

