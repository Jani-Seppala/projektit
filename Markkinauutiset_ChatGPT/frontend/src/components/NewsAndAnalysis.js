import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import NewsItem from './NewsItem';
import FlashMessage from './FlashMessage';

  function NewsAndAnalysis({ favorites, token }) {
    console.log('Favorites:', favorites);
    const [newsWithAnalysis, setNewsWithAnalysis] = useState([]);
    const location = useLocation();
  
    useEffect(() => {
      if (favorites) {
        // Fetch news for favorite stocks
        const stockIdsParam = favorites.join(',');
        console.log('stockIdsParam:', stockIdsParam);
        axios.get(`http://localhost:5000/api/news-with-analysis?stock_ids=${stockIdsParam}`, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }).then(response => {
          console.log('Fetched news for favorite stocks:', response.data);
          setNewsWithAnalysis(response.data);
        }).catch(error => {
          console.error("Failed to fetch news for favorite stocks", error);
        });
      } else {
        // Fetch all news
        axios.get('http://localhost:5000/api/news-with-analysis')
          .then(response => {
            console.log('Fetched all news:', response.data);
            setNewsWithAnalysis(response.data);
          })
          .catch(error => console.error('Error fetching news with analysis:', error));
      }
    }, [favorites, token]);

  return (
    <div className="container">
      <h1 className="text-center mb-4">News and Analysis</h1>
      {/* Directly render FlashMessage if there is a message in location.state */}
      {location.state?.message && (
        <FlashMessage message={location.state.message} type={location.state.type} />
      )}
      {newsWithAnalysis.map(({ news, analysis }) => {
        // Extract the $oid property if it exists, otherwise use _id directly
        const keyId = news._id.$oid || news._id;
        return <NewsItem key={keyId} news={news} analysis={analysis} />;
      })}
    </div>
  );
}

export default NewsAndAnalysis;
