import React, { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import NewsItem from './NewsItem';
import FlashMessage from './FlashMessage';

function NewsAndAnalysis({ stockIds, token }) {
    const [newsWithAnalysis, setNewsWithAnalysis] = useState([]);
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);
    const [loading, setLoading] = useState(false);
    const location = useLocation();

    const fetchNews = useCallback((currentPage, reset = false) => {
        setLoading(true);
        const baseUrl = 'http://localhost:5000/api/news-with-analysis';
        const params = new URLSearchParams({
            page: currentPage
        });

        if (stockIds) {
            params.append('stock_ids', stockIds.join(','));
        }

        axios.get(`${baseUrl}?${params.toString()}`, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        }).then(response => {
          console.log('Current state before update:', newsWithAnalysis.map(item => item.news._id));
          console.log('New items to add:', response.data.items.map(item => item.news._id));
            if (reset) {
                setNewsWithAnalysis(response.data.items);
            } else {
                setNewsWithAnalysis(prev => [...prev, ...response.data.items]);
            }

            setHasMore(response.data.has_more);
            setPage(currentPage + 1); // Increment page if there's more to load
            setLoading(false);
        }).catch(error => {
            console.error("Failed to fetch news", error);
            setLoading(false);
        });
    }, [token, stockIds]);

    useEffect(() => {
        fetchNews(1, true); // Fetch the first page and reset the news list
    }, [stockIds, token, fetchNews]);
    

    console.log('News item IDs:', newsWithAnalysis.map(({ news }) => news._id));

    return (
        <div className="container">
            <h1 className="text-center mb-4">News and Analysis</h1>
            {location.state?.message && (
                <FlashMessage message={location.state.message} type={location.state.type} />
            )}
            {loading ? (
                <p>Loading...</p>
            ) : (
                newsWithAnalysis.length === 0 ? (
                    <p>No news for this company.</p>
                ) : (
                    newsWithAnalysis.map(({ news, analysis }, index) => {
                        // Ensure the key is a string. Access the $oid property if _id is an object.
                        const keyId = news._id && news._id.$oid ? news._id.$oid : index.toString();
                        console.log(`Key for NewsItem ${index}: ${keyId}`); // Check what key is used.
                        return <NewsItem key={keyId} news={news} analysis={analysis} />;
                    })
                )
            )}
            {!loading && hasMore && (
                <button onClick={() => fetchNews(page)} className="btn btn-primary">
                    Show More
                </button>
            )}
        </div>
    );
}

export default NewsAndAnalysis;
