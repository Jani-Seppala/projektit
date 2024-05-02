import yfinance as yf
# import pandas as pd
# import logging
from datetime import datetime, timedelta
import pytz
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


timezone = pytz.timezone('Europe/Stockholm')
class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND * 10)),
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache")
)

# Clear the cache at the start of the script to ensure fresh API calls
session.cache.clear()

# last_fetched_times = {}

def append_market_suffix(ticker, market):
    if "Helsinki" in market or "Finland" in market:
        return ticker + '.HE'
    elif "Stockholm" in market or "Sweden" in market:
        return ticker + '.ST'
    elif "Copenhagen" in market or "Denmark" in market:
        return ticker + '.CO'
    elif "Reykjavik" in market or "Iceland" in market:
        return ticker + '.IC'
    elif "Tallinn" in market or "Estonia" in market:
        return ticker + '.TL'
    elif "Riga" in market or "Latvia" in market:
        return ticker + '.RG'
    elif "Vilnius" in market or "Lithuania" in market:
        return ticker + '.VS'

    return ticker


# def fetch_and_process_intraday_data(ticker, news_time):
#     stock = yf.Ticker(ticker, session=session)
#     try:
#         # Attempt to fetch intraday data on the news date
#         intraday_data = stock.history(period='1d', interval='1m', start=news_time.strftime('%Y-%m-%d'), end=(news_time + timedelta(days=1)).strftime('%Y-%m-%d'))
#         time_before_news = news_time - timedelta(minutes=1)
#         # Search for price data just before the news release
#         found_data = False
#         for date, data in reversed(list(intraday_data.iterrows())):
#             if date <= time_before_news:
#                 print(f"Data found for {ticker} at {date}: {data['Close']}")
#                 found_data = True
#                 return data['Close'], date  # Return the found price and its timestamp
#         if not found_data:
#             print(f"No data found for {ticker} before news time {time_before_news}. Checking for previous close.")
#     except Exception as e:
#         print(f"Exception occurred fetching intraday data for {ticker} at {news_time}: {e}")
#         if 'intraday_data' in locals():
#             print(f"Intraday data was partially fetched: {intraday_data.describe()}")
#         else:
#             print("Intraday data could not be fetched at all.")

#     # Fallback to the last available close price if no intraday data is available
#     try:
#         previous_close = stock.info.get('previousClose')
#         previous_close_date = news_time - timedelta(days=1)  # Assume the previous close date is the day before
#         print(f"Using previous close for {ticker} as fallback: {previous_close} from {previous_close_date}")
#         return previous_close, previous_close_date
#     except Exception as e:
#         print(f"Failed to fetch previous close for {ticker}: {e}")
#         return None, None  # Return None if all attempts fail


# def process_historical_data(ticker, news_time):
#     stock = yf.Ticker(ticker, session=session)
#     # Ensure the coverage of a year's data based on the news time
#     start_date = (news_time - timedelta(days=365)).strftime('%Y-%m-%d')
#     end_date = news_time.strftime('%Y-%m-%d')
#     hist = stock.history(start=start_date, end=end_date, interval='1d')

#     target_dates = {
#         'yesterday': news_time - timedelta(days=1),
#         '1_week_ago': news_time - timedelta(weeks=1),
#         '1_month_ago': news_time - timedelta(days=30),
#         '1_year_ago': news_time - timedelta(days=365)
#     }
#     close_prices = {}

#     for label, target_date in target_dates.items():
#         # Normalize the target date for comparison
#         target_date_norm = pd.to_datetime(target_date).normalize()
#         # print(f"Checking for {label} on {target_date_norm}")

#         # Filtering the dataframe for the target date
#         filtered_data = hist[hist.index.normalize() == target_date_norm]
#         if not filtered_data.empty:
#             close_price = filtered_data['Close'].iloc[0]
#             close_prices[label] = close_price
#             # print(f"Matched {label}: {close_price} on {filtered_data.index[0]}")
#         else:
#             # print(f"No match found for {label}. Looking for closest date before {target_date_norm}")
#             # Find the closest date before the target date
#             prior_dates = hist[hist.index < target_date_norm]
#             if not prior_dates.empty:
#                 closest_date = prior_dates.index.max()
#                 closest_price = prior_dates.loc[closest_date, 'Close']
#                 close_prices[label] = closest_price
#                 # print(f"Closest match for {label}: {closest_price} on {closest_date}")
#             else:
#                 close_prices[label] = None
#                 # print(f"No historical data available before {target_date_norm} for {label}")

#     return close_prices


# def main(news_item):
#     try:
#         ticker = news_item.get('stock_symbol', '').replace(' ', '-')
#         market = news_item.get('market')
#         ticker = append_market_suffix(ticker, market)
#         news_time_str = news_item['releaseTime']
#         news_time = datetime.strptime(news_time_str, '%Y-%m-%d %H:%M:%S')
#         news_time = timezone.localize(news_time)

#         price_before_news, time_of_price = fetch_and_process_intraday_data(ticker, news_time)
#         close_prices = process_historical_data(ticker, news_time)  # Fetch historical data
#         print(f"Data fetched for {ticker}: Price before news {price_before_news} at {time_of_price}, Historical prices: {close_prices}")

#         return price_before_news, close_prices
#     except Exception as e:
#         error_details = {
#             "ticker": ticker,
#             "news_time": news_time.strftime('%Y-%m-%d %H:%M:%S'),
#             "market": market,
#             "error_message": str(e)
#         }
#         print(f"An error occurred in main function of yahoofinanceapicall.py: {error_details}")
#         return None, None


def fetch_price_before_news(ticker, news_time):
    stock = yf.Ticker(ticker)
    try:
        intraday_data = stock.history(period='1d', interval='1m', start=news_time.strftime('%Y-%m-%d'), end=(news_time + timedelta(days=1)).strftime('%Y-%m-%d'))
        time_before_news = news_time - timedelta(minutes=1)
        found_data = intraday_data[intraday_data.index <= time_before_news]
        
        if not found_data.empty:
            last_data = found_data.iloc[-1]
            stock_info = stock.info
            stock_info['price_before_news'] = last_data['Close']
            return stock_info
        else:
            print("No intraday data found, fetching previous close.")
            stock_info = stock.info
            # stock_info['price_before_news'] = stock.info.get('previousClose')
            stock_info['price_before_news'] = stock.info.get('currentPrice')
            return stock_info
    except Exception as e:
        print(f"Failed to fetch data for {ticker} at {news_time}: {e}")
        return None

def main(news_item):
    try:
        ticker = news_item.get('stock_symbol', '').replace(' ', '-')
        market = news_item.get('market')
        ticker = append_market_suffix(ticker, market)
        news_time_str = news_item['releaseTime']
        news_time = datetime.strptime(news_time_str, '%Y-%m-%d %H:%M:%S')
        news_time = pytz.timezone('Europe/Stockholm').localize(news_time)
        
        stock_info = fetch_price_before_news(ticker, news_time)
        print(f"Stock data for {ticker}: {stock_info}")
        
        return stock_info
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
