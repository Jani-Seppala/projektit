// // This is the main component of the frontend. It fetches news with analysis from the backend and displays them.

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import LoginPage from './components/LoginPage'; // Placeholder, replace with actual component
import RegisterPage from './components/RegisterPage'; // Placeholder, replace with actual component
import FavoritesPage from './components/FavoritesPage'; // Placeholder, replace with actual component


// Mapping of market names to flag image paths
const marketToFlag = {
  "Helsinki": "/flags/fi.png",
  "Copenhagen": "/flags/dk.png",
  "Stockholm": "/flags/se.png",
  "Oslo": "/flags/no.png",
  "Iceland": "/flags/is.png",
};

function getFlagForMarket(market) {
  // Find the first key (country) that matches part of the market string
  const countryKey = Object.keys(marketToFlag).find(key => market.includes(key));
  return marketToFlag[countryKey]; // Returns undefined if no match is found
}

// function NewsItem({ news, analysis }) {
//   const [isExpanded, setIsExpanded] = useState(false);
//   const toggleExpand = () => setIsExpanded(!isExpanded);
//   const flagSrc = getFlagForMarket(news.market); // Get the flag source based on the market

//   return (
//     <div className="my-3 p-3 bg-light border rounded" onClick={toggleExpand}>
//       <div className="mb-2">
//         {flagSrc && (
//           <img
//             src={flagSrc}
//             alt="Country flag"
//             style={{ width: "20px", marginRight: "5px", verticalAlign: "middle" }}
//           />
//         )}
//         {/* <h3 className="d-inline me-2">{news.company}</h3> */}
//         <span className="company-name">{news.company}</span>
//         <span className="text-muted">{news.releaseTime}</span>
//       </div>
//       {/* <h4>{news.headline}</h4> */}
//       <h4 className="headline">{news.headline}</h4>
//       <a href={news.messageUrl} target="_blank" rel="noopener noreferrer" className="btn btn-primary">Read more</a>
//       {analysis && (
//         <div className="mt-3">
//           <h5>Analysis</h5>
//           <p>{isExpanded ? analysis.analysis_content : `${analysis.analysis_content.substring(0, 100)}...`}</p>
//         </div>
//       )}
//     </div>
//   );
// }

function NewsItem({ news, analysis }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const toggleExpand = () => setIsExpanded(!isExpanded);
  const flagSrc = getFlagForMarket(news.market); // Get the flag source based on the market

  return (
    <div className="my-3 p-3 bg-light border rounded" onClick={toggleExpand}>
      <div className="mb-2">
        {flagSrc && (
          <img
            src={flagSrc}
            alt="Country flag"
            style={{ width: "20px", marginRight: "5px", verticalAlign: "middle" }}
          />
        )}
        <span className="company-name">{news.company}</span>
        <span className="text-muted">{news.releaseTime}</span>
      </div>
      {/* Wrap the headline with an <a> tag and remove the "Read more" button */}
      <a href={news.messageUrl} target="_blank" rel="noopener noreferrer" className="headline-link">
        <h4 className="headline">{news.headline}</h4>
      </a>
      {analysis && (
        <div className="mt-3">
          <h5>Analysis</h5>
          <p>{isExpanded ? analysis.analysis_content : `${analysis.analysis_content.substring(0, 100)}...`}</p>
        </div>
      )}
    </div>
  );
}



function NewsAndAnalysis() {
  const [newsWithAnalysis, setNewsWithAnalysis] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/news-with-analysis')
      .then(response => response.json())
      .then(data => setNewsWithAnalysis(data))
      .catch(error => console.error('Error fetching news with analysis:', error));
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">News and Analysis</h1>
      {newsWithAnalysis.map(({ news, analysis }) => (
        <NewsItem key={news._id} news={news} analysis={analysis} />
      ))}
    </div>
  );
}


function App() {
  return (
    <Router>
      {/* This keeps the navbar full width but you can change it to "container" if needed */}
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container">
          <Link className="navbar-brand fs-2" to="/">News App</Link>
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0 fs-4">
              <li className="nav-item"><Link className="nav-link" to="/login">Login</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/register">Register</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/favorites">Favorites</Link></li>
              {/* Add Logout link and conditionally render it based on user authentication status */}
            </ul>
          </div>
        </div>
      </nav>
      {/* Wrap Routes in a "container" for alignment with NewsAndAnalysis content */}
      <div className="container">
        <Routes>
          <Route path="/" element={<NewsAndAnalysis />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          {/* Add more routes as needed */}
        </Routes>
      </div>
    </Router>
  );
}



export default App;

