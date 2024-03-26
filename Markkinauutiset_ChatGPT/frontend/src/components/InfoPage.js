import React from 'react';

function InfoPage() {
  return (
    <div className="info-page container mt-4">
      <h1 className="mb-4">About</h1>
      <p className="mb-4">Welcome to <strong>Stock News and Analysis App</strong>, a comprehensive platform designed to simplify stock market news and analysis. Our platform allows users to effortlessly follow the latest developments and insights into their favorite stocks. Here's how to get started and make the most of our features:</p>
      
      <h4 className="mb-3">Registration and Login:</h4>
      <p className="mb-4">Users have the option to register an account to personalize their experience. Registered users can select and save their favorite stocks to track news and analysis specifically tailored to their interests. Registration is not mandatory; visitors can browse the platform and access general stock market news without an account.</p>
      
      <h4 className="mb-3">Navigating the Homepage:</h4>
      <p className="mb-4">The homepage showcases the latest news and analyses across a wide range of stocks. Each news block includes the company's name, the market it belongs to, the time of the news release, and a headline. Click on the headline to access the full news article. An analysis section accompanies each news item, providing AI insights into its implications. Click on the news block to expand and read the detailed analysis.</p>
      
      <h4 className="mb-3">Searching for Stocks:</h4>
      <p className="mb-4">Use the search feature located in the right side of the navbar to find specific stocks. Simply enter the name of the stock you're interested in. Clicking on a stock from the search results will redirect you to a dedicated page for that stock, where you can find specific news, analysis, and other relevant information.</p>
      
      <h4 className="mb-3">Stock Page:</h4>
      <p className="mb-4">The stock page is a dedicated space for each company, featuring news, expert analyses, and key information about the stock. Registered users can add the stock to their favorites for quick access and personalized updates. Whether you're a seasoned investor or new to the stock market, <strong>Stock News and Analysis App</strong> is designed to provide you with easy access to essential information, helping you make informed decisions.</p>
      
      <h2 className="mb-3">Disclaimer</h2>
      <p className="mb-4">Please note that the analyses provided on <strong>Stock News and Analysis App</strong> are generated with the assistance of artificial intelligence (AI). While we strive for accuracy and relevance, AI-generated analyses may sometimes contain inaccuracies or fail to capture the nuances of human analysis. Consequently, they should not be the sole basis for any investment decision.</p>
      <p className="mb-4">We strongly advise all our users to cross-reference the information presented here with official sources and conduct thorough research before making any investment. <strong>Stock News and Analysis App</strong> does not assume liability for any financial loss or discrepancy arising from reliance on AI-generated analyses. Investment in the stock market involves risks, and it's crucial to make informed decisions.</p>
      <p>By using <strong>Stock News and Analysis App</strong>, you acknowledge and accept that the responsibility for investment decisions lies solely with you, the investor. Always consult with a qualified financial advisor or conduct your own comprehensive research before making investment decisions.</p>
    </div>
  );
}

export default InfoPage;
