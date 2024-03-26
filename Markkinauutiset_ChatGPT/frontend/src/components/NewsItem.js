import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './NewsItem.css';

const marketToFlag = {
  "Helsinki": "/flags/fi.png",
  "Copenhagen": "/flags/dk.png",
  "Stockholm": "/flags/se.png",
  "Oslo": "/flags/no.png",
  "Iceland": "/flags/is.png",
};

function getFlagForMarket(market) {
  const countryKey = Object.keys(marketToFlag).find(key => market.includes(key));
  return marketToFlag[countryKey];
}

function NewsItem({ news, analysis }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const flagSrc = getFlagForMarket(news.market);

  // This function toggles the expanded state
  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  // Prevents the link click from propagating to the parent div
  const handleLinkClick = (e) => {
    e.stopPropagation();
  };

  return (
    <div className="news-item my-3 p-3 bg-light border rounded" onClick={toggleExpand}>
      <div className="news-header mb-2">
        {flagSrc && <img src={flagSrc} alt="Country flag" style={{ width: "20px", marginRight: "5px", verticalAlign: "middle" }} />}
        {/* Wrap the company name in a span and Link component */}
        <span onClick={handleLinkClick}>
            <Link to={`/stocks/${news.stock_id.$oid || news.stock_id}`} className="company-name-link">
            {news.company}
            </Link>
        </span>
        <span className="release-time">{news.releaseTime}</span>
      </div>
      <span onClick={handleLinkClick}>
        <a href={news.messageUrl} target="_blank" rel="noopener noreferrer" className="headline-link">
          <h4 className="headline">{news.headline}</h4>
        </a>
      </span>
      {analysis && (
        <div className={`analysis-content mt-3 ${isExpanded ? 'expanded' : 'collapsed'}`}>
          <h5>Analysis</h5>
          <p>{isExpanded ? analysis.analysis_content : `${analysis.analysis_content.substring(0, 100)}...`}</p>
          {!isExpanded && <div className="click-to-enlarge">Click to enlarge</div>}
        </div>
      )}
    </div>
  );
}

export default NewsItem;
