import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NewsAndAnalysis from './NewsAndAnalysis';
import './FavoritesPage.css';

function FavoritesPage() {
  const [favorites, setFavorites] = useState([]);
  const token = localStorage.getItem('token');
  
  useEffect(() => {
    // Fetch the user's current favorites directly with detailed information
    axios.get('http://localhost:5000/api/favorites', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(response => {
      console.log('Fetched favorites:', response.data);
      setFavorites(response.data);
    })
    .catch(error => {
      console.error("Failed to fetch favorites", error);
      
    });
  }, [token]);

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

  return (
    <div className="favorites-page">
      <h2>Your Favorite Stocks</h2>
      <div className="favorite-stocks">
      {favorites.map(stock => (
        <div key={stock._id} className="alert alert-info favorite-stock-box">
          <div className="favorite-stock">
            <h3>{stock.name}</h3>
            <button onClick={() => handleRemoveFromFavorites(stock)} className="btn btn-outline-dark remove-button">X</button>
          </div>
        </div>
      ))}
      </div>
      {favorites.length > 0 ? (
        // <NewsAndAnalysis favorites={favorites.map(stock => stock._id)} token={token} />
        <NewsAndAnalysis stockIds={favorites.map(stock => stock._id)} token={token} />
      ) : (
        <p>Add stocks to favorites to see news.</p>
      )}
    </div>
  );
}

export default FavoritesPage;