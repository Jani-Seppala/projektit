import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
// import NewsItem from './NewsItem';
import NewsAndAnalysis from './NewsAndAnalysis';

function StockPage() {
  const { stockId } = useParams();
  const [stockData, setStockData] = useState(null);
  // const [newsData, setNewsData] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const token = localStorage.getItem('token');
  console.log(token);

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/stocks/${stockId}`);
        console.log('Stock Response:', response); // Debug print
        setStockData(response.data);
  
        // const newsResponse = await axios.get(`http://localhost:5000/api/news-with-analysis?stock_id=${stockId}`);
        // console.log('News Response:', newsResponse); // Debug print
        // // console.log('News Data:', newsResponse.data);
        // console.log('News Data:', newsResponse.data.items);
        // // setNewsData(newsResponse.data);
        // setNewsData(newsResponse.data.items);
  
        if (token) {
          const favoritesResponse = await axios.get('http://localhost:5000/api/favorites', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          console.log('Favorites Response:', favoritesResponse.data);
          setFavorites(favoritesResponse.data.map(stock => stock._id));
        }
        setLoading(false);
      } catch (err) {
        console.error('Error:', err); // Debug print
        setError('Failed to fetch data');
        setLoading(false);
      }
    };
  
    fetchStockData();
  }, [stockId, token]);


  const handleAddToFavorites = (stockToAdd) => {
    const userId = localStorage.getItem('userId');
    if (!favorites.includes(stockToAdd._id)) {
      
      axios.post(`http://localhost:5000/api/users/${userId}/add_favorite/${stockToAdd._id}`, {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        const newFavorites = [...favorites, stockToAdd._id];
        setFavorites(newFavorites);
        console.log('Favorites after adding:', newFavorites);
      })
      .catch(error => console.error("Failed to add stock to favorites", error));
    }
  };

  const handleRemoveFromFavorites = () => {
    const updatedFavorites = favorites.filter(favoriteId => favoriteId !== stockId);
    setFavorites(updatedFavorites);
    console.log('Favorites after removing:', updatedFavorites);
    axios.post('http://localhost:5000/api/favorites', { favorites: updatedFavorites }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }).catch(error => console.error("Failed to update favorites", error));
  
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  console.log('Favorites:', favorites);
  console.log('Stock ID:', stockId);
  const isFavorite = favorites.includes(stockId);
  console.log('Is Favorite:', isFavorite);

//   return (
//     <div>
//       <h2>Stock Details</h2>
//       {stockData ? (
//         <div className="d-flex justify-content-between align-items-center">
//           <h3>{stockData.name} ({stockData.symbol})</h3>
//           {token && (
//             <button className={`btn ${isFavorite ? 'btn-danger' : 'btn-primary'}`} onClick={() => isFavorite ? handleRemoveFromFavorites() : handleAddToFavorites(stockData)}>
//               {isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
//             </button>
//           )}
//         </div>
//       ) : (
//         <p>Stock information not available.</p>
//       )}
//       {newsData.length > 0 ? (
//         newsData.map(({ news, analysis }) => {
//           const keyId = news._id.$oid || news._id;
//           return <NewsItem key={keyId} news={news} analysis={analysis} />;
//         })
//       ) : (
//         <p>This company doesn't have news/analysis.</p>
//       )}
//     </div>
//   );
// }

// export default StockPage;

return (
  <div>
    <h2>Stock Details</h2>
    {stockData ? (
      <div className="d-flex justify-content-between align-items-center">
        <h3>{stockData.name} ({stockData.symbol})</h3>
        {token && (
          <button className={`btn ${isFavorite ? 'btn-danger' : 'btn-primary'}`} onClick={() => isFavorite ? handleRemoveFromFavorites() : handleAddToFavorites(stockData)}>
            {isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
          </button>
        )}
      </div>
    ) : (
      <p>Stock information not available.</p>
    )}
    <NewsAndAnalysis stockIds={[stockId]} token={token} />
  </div>
);
}

export default StockPage;