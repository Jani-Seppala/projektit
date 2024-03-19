import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import NewsItem from './NewsItem'; // Import from NewsItem.js
// import './NewsAndAnalysis.css';

function NewsAndAnalysis() {
  const [newsWithAnalysis, setNewsWithAnalysis] = useState([]);
  const location = useLocation(); 
  const [flashMessage, setFlashMessage] = useState(location.state?.message);
  const [flashMessageType, setFlashMessageType] = useState(location.state?.type);

  useEffect(() => {
    fetch('http://localhost:5000/api/news-with-analysis')
      .then(response => response.json())
        .then(data => {
        setNewsWithAnalysis(data);
        console.log("tämän jälkeen newswithanalysis 2 printti");
        console.log("ennen tätä newswithanalysis printti");
      })
      .catch(error => console.error('Error fetching news with analysis:', error));
  }, []);


  useEffect(() => {
    console.log("tämän jälkeen newswithanalysis 2 printti");
    console.log("ennen tätä newswithanalysis 2 printti");
  }, [newsWithAnalysis]);

  // Add this useEffect hook
  useEffect(() => {
    if (flashMessage) {
      const timer = setTimeout(() => {
        setFlashMessage(null);
        setFlashMessageType(null);
      }, 3000); // 3 seconds

      // Clean up the timer when the component is unmounted
      return () => clearTimeout(timer);
    }
  }, [flashMessage]);

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">News and Analysis</h1>
      {flashMessage && (
        <div className={`flash-message ${flashMessageType}`}>
          {flashMessage}
        </div>
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
