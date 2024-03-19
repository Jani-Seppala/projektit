
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import NewsItem from './NewsItem';

function StockPage() {
  const { stockId } = useParams(); // Extract stockId from the URL
  const [stockData, setStockData] = useState(null);
  const [newsData, setNewsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/stocks/${stockId}`);
        setStockData(response.data);
        const newsResponse = await axios.get(`http://localhost:5000/api/news-with-analysis/${stockId}`);
        setNewsData(newsResponse.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch data');
        setLoading(false);
        console.error(err);
      }
    };

    fetchStockData();
  }, [stockId]); // Re-run this effect if stockId changes

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>Stock Details</h2>
      {stockData ? (
        <div>
          <h3>{stockData.company} ({stockData.symbol})</h3>
          <p>Market: {stockData.sector}</p>
          {/* Add more stock details here as needed */}
        </div>
      ) : (
        <p>Stock information not available.</p>
      )}
          {newsData.length > 0 ? (
          newsData.map(({ news, analysis }) => {
          // Ensure you're using the $oid property if _id is an object
          const keyId = news._id.$oid || news._id;
          return <NewsItem key={keyId} news={news} analysis={analysis} />;
        })
      ) : (
        <p>This company doesn't have news/analysis.</p>
      )}
    </div>
  );
}

export default StockPage;
