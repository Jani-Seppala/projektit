import requests
import datetime
import pytz
import time
from uuid import uuid4
from bs4 import BeautifulSoup
from app import mongo
from fuzzywuzzy import process
import re
import schedule
from YahooFinanceApiCall import main as fetch_stock_data
from openAiApiCall import analyze_news

print('fsfs')


def fetch_news(url):
    """ Fetch news from a given URL and process it if successful. """
    response = requests.get(url)
    if response.status_code == 200:
        print(f"News fetched successfully.at {datetime.datetime.now(pytz.timezone('Europe/Stockholm')).strftime('%Y-%m-%d %H:%M:%S')} from {url}")
        news_data = response.json().get('results', {}).get('item', [])
        # preprocess_news_items(news_data[:3])  # Process only the first 2 news item
        preprocess_news_items(news_data)
        # exit(0)  # Exit after processing the first item
        return
    else:
        print(f"Failed to fetch news: {response.status_code}")


def extract_manager_name(headline):
    """Return an empty string if the headline ends with specified phrases, indicating no manager name."""
    # Check if the headline ends with the specified phrases.
    if headline.strip().endswith("- Managers' Transactions") or headline.strip().endswith("- Johdon liiketoimet"):
        return ""
    
    """Attempt to extract manager's name from the headline using regex."""
    patterns = [r'[-:]\s*([A-Za-zäöüßÄÖÜẞ\s]+)$', r'\(([A-Za-zäöüßÄÖÜẞ\s]+)\)']
    for pattern in patterns:
        match = re.search(pattern, headline)
        if match:
            return match.group(1).strip()
    return ""


def preprocess_news_items(news_items):
    """Group news items by company and timestamp, modifying the disclosureId to include the language."""
    processed_items = []

    for item in news_items:
        languages = item.get('languages', [item.get('language')])  # Default to the current item's language if 'languages' is not set

        # Process each language for the news item
        for lang in languages:
            new_item = item.copy()  # Create a shallow copy of the item

            # Generate a new, modified disclosureId for the item including the language
            new_item['disclosureId'] = f"{item['disclosureId']}_{lang}"

            # If there's more than one language, update the messageUrl to reflect the correct language
            if len(languages) > 1:
                new_item['messageUrl'] = item['messageUrl'].replace(item['language'], lang)
            new_item['language'] = lang  # Update the language of the news item

            processed_items.append(new_item)

    # Group the processed items
    grouped_news = {}
    for item in processed_items:
        key = (item['company'], item['releaseTime'])
        if key not in grouped_news:
            grouped_news[key] = []
        grouped_news[key].append(item)

    link_related_news(grouped_news)


def link_related_news(grouped_news):
    linked_news = {}
    for key, items in grouped_news.items():
        if len(items) <= 2:
            # print('LINK RELATED NEWS ENSIMMÄINEN IF', items)
            print('LINK RELATED NEWS ENSIMMÄINEN IF')
            # Directly link items if there are 2 or fewer in the group.
            # direct_link_key = key + ('DirectLink',)
            # linked_news[direct_link_key] = {'relatedId': str(uuid4()), 'items': items}
            linked_news[key] = {'relatedId': str(uuid4()), 'items': items}
        else:
            # ei toimi vielä
            continue
            # Attempt to group by manager names for items with more than 2 in the group.
            manager_groups = {}
            items_without_manager_name = []
            
            for item in items:
                manager_name = extract_manager_name(item['headline'])
                if manager_name:
                    print('LINK RELATED NEWS ENSIMMÄISEN IFIN ENSIMMÄINEN IF', items)
                    manager_key = (manager_name,)
                    if manager_key not in manager_groups:
                        manager_groups[manager_key] = []
                    manager_groups[manager_key].append(item)
                else:
                    print('LINK RELATED NEWS ENSIMMÄISEN IFIN TOINEN ELSE', items)
                    print(item)
                    items_without_manager_name.append(item)

            for manager_key, manager_items in manager_groups.items():
                languages = set(item['language'] for item in manager_items)
                if len(languages) == 1:
                    # If all items are of the same language, assign each a unique group ID.
                    for item in manager_items:
                        unique_key = key + manager_key + (str(uuid4()),)  # Generate unique key for each item.
                        linked_news[unique_key] = {'relatedId': str(uuid4()), 'items': [item]}
                elif len(manager_items) <= 2:
                    # If there are 2 or fewer items, link them without further analysis.
                    linked_manager_key = key + manager_key + ('LinkedByManager',)
                    linked_news[linked_manager_key] = {'relatedId': str(uuid4()), 'items': manager_items}
                else:
                    # If items vary by language and there are more than 2, consider deeper analysis or alternative handling.
                    for item in manager_items:
                        print('Multiple languages or items for manager, consider deeper analysis:', manager_key)
                        # Placeholder for deeper analysis or other logic.

            # Handle items without a manager name.
            for item in items_without_manager_name:
                print('LINK RELATED NEWS ENSIMMÄISEN ELSEN KOLMAS FOR LOOPPI', items_without_manager_name)
                # Assign a unique group ID to each ungroupable item.
                unique_key = key + ('NoManagerName', str(uuid4()))
                linked_news[unique_key] = {'relatedId': str(uuid4()), 'items': [item]}
    
    process_and_save_news(linked_news)


def normalize_company_name(name):
    name = re.sub(r'[\s.,;:\'\"()&/]+', '', name).lower()
    for suffix in ['ab', 'oyj', 'plc', 'as', 'ltd']:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    return name


def find_best_stock_match(company_name, market, stocks_collection):
    normalized_company_name = normalize_company_name(company_name)
    # Filter stocks by market
    stocks_in_same_market = [stock for stock in stocks_collection if stock.get('market') == market]
    stock_names = {stock['_id']: (normalize_company_name(stock['name']), stock.get('symbol', 'N/A')) for stock in stocks_in_same_market}
    # best_match, score = process.extractOne(normalized_company_name, {k: v[0] for k, v in stock_names.items()}.values())
    result = process.extractOne(normalized_company_name, {k: v[0] for k, v in stock_names.items()}.values())
    
    # best_match, score = process.extractOne(normalized_company_name, {k: v[0] for k, v in stock_names.items()}.values(), default=(None, 0))
    
    # Check if result is None
    if result is None:
        print(f"Could not find a good match for news item company name '{company_name}' in market '{market}'.")
        return None, None
    else:
        best_match, score = result


    if score > 85:  # You may adjust this threshold based on your observation
        stock_id = list(stock_names.keys())[list({k: v[0] for k, v in stock_names.items()}.values()).index(best_match)]
        stock_symbol = stock_names[stock_id][1]  # Get the symbol for the matched stock
        return stock_id, stock_symbol
    else:
        return None, None


def fetch_stock_price_and_analyze(news_item):
    # Create a unique cache key based on company name and release time
    cache_key = (news_item['company'], news_item['releaseTime'])

    # Check if data is in cache
    if cache_key in price_cache:
        price_before_news, close_prices = price_cache[cache_key]
        print("Using cached price data.")
        print(f"{price_cache=}")
    else:
    # try:
        # Fetch stock price from YahooFinanceApicall.py
        price_before_news, close_prices = fetch_stock_data(news_item)
        # Store in cache
        price_cache[cache_key] = (price_before_news, close_prices)
        print("Fetched new price data and cached it.")
    # except Exception as e:
    #     print(f"Error fetching stock price data: {e} for {news_item.get('stock_symbol')}, price_before_news: {price_before_news}, close_prices: {close_prices}")
    #     return
            
    
    
    news_item['price_before_news'] = price_before_news
    mongo.db.news.insert_one(news_item)
    
    # Get analysis from the news with the stock price from openAiApiCall.py
    # analysis_content, prompt = analyze_news(news_item, price_before_news, close_prices)
    # analysis_document = {
    #     "news_id": news_item["_id"],
    #     "analysis_content": analysis_content,
    #     "created_at": datetime.datetime.now(pytz.timezone('Europe/Stockholm')).strftime('%Y-%m-%d %H:%M:%S'),
    #     "prompt": prompt
    # }
    
    # Use static content for analysis
    analysis_content = "This is static analysis content for testing."
    prompt = "Static prompt for testing."

    analysis_document = {
        "news_id": news_item["_id"],
        "analysis_content": analysis_content,
        "created_at": datetime.datetime.now(pytz.timezone('Europe/Stockholm')).strftime('%Y-%m-%d %H:%M:%S'),
        "prompt": prompt
    }
    
    
    mongo.db.analysis.insert_one(analysis_document)
    # print(analysis_document)
    # print(news_item)
    print(f"Saved news and analysis for {news_item.get('stock_symbol')}")
    print('-----------------------------NEXT NEWS ITEM----------------------------------------')


def process_and_save_news(linked_news):
    stocks_collection = list(mongo.db.stocks.find({}))  # Fetch all stocks once to improve efficiency

    for key, value in linked_news.items():
        related_id = value['relatedId']
        for item in value['items']:
            item['relatedId'] = related_id
            unique_id = item['disclosureId']
            existing_news_item = mongo.db.news.find_one({'disclosureId': unique_id})
            print(f"Checking for existing item with ID {unique_id}: Found - {existing_news_item is not None}")

            if not existing_news_item:
                item_text = fetch_text_from_url(item['messageUrl'])
                if item_text:
                    item['messageUrlContent'] = item_text

                # Attempt to find the best matching stock, including the stock symbol
                stock_id, stock_symbol = find_best_stock_match(item.get('company'), item.get('market'), stocks_collection)
                if stock_id:
                    item['stock_id'] = stock_id
                    item['stock_symbol'] = stock_symbol  # Add the stock symbol to the news item

                    matched_stock_name = next((stock['name'] for stock in stocks_collection if stock['_id'] == stock_id), None)
                    print(f"Matched '{item.get('company')}' with stock '{matched_stock_name}'")
                    
                    fetch_stock_price_and_analyze(item)

                else:
                    print(f"Could not find a good match for news item company name '{item.get('company')}' in market '{item.get('market')}'.")
            
            elif existing_news_item:
                print(f"News item with disclosureId '{unique_id}' already exists in the database. Company '{item.get('company')}'")



def fetch_text_from_url(url):
    # Sends a GET request to the news URL and return the text content as one big string
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_elements = soup.find_all('p')
            all_text = " ".join(element.get_text(strip=True) for element in text_elements)
            return all_text
        else:
            print("Failed to retrieve the webpage")
            return None
    except Exception as e:
        print(f"Error fetching page content: {e}")
        return None


# def scheduled_job():
#     global price_cache
#     price_cache = {}  # Reset the cache at the start of each job

#     CET = pytz.timezone('Europe/Stockholm')
#     now = datetime.datetime.now(CET)
    
    
    
    
#     print(f"Scheduled job attempted at {now.strftime('%Y-%m-%d %H:%M:%S')}")

#     # Fetch news from Main Market
#     fetch_news("https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicMainMarkets&displayLanguage=en&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC")
    
#     # Fetch news from First North
#     fetch_news("https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicFirstNorth&displayLanguage=en&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC")

# schedule.every().minute.at(":05").do(scheduled_job)

# try:
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Stopped by user.")


def market_hours_job():
    global price_cache
    price_cache = {}  # Reset the cache at the start of each job
    print(f"Scheduled job during market hours at {datetime.datetime.now(pytz.timezone('Europe/Stockholm')).strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_news(main_market_url)
    fetch_news(first_north_url)
    check_and_reschedule()

def off_market_hours_job():
    global price_cache
    price_cache = {}  # Reset the cache at the start of each job
    print(f"Scheduled job outside market hours at {datetime.datetime.now(pytz.timezone('Europe/Stockholm')).strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_news(main_market_url)
    fetch_news(first_north_url)
    check_and_reschedule()

def check_and_reschedule():
    CET = pytz.timezone('Europe/Stockholm')
    now = datetime.datetime.now(CET)
    hour = now.hour
    weekday = now.weekday()
    
    # Clear any existing schedules regardless of the time or day
    schedule.clear()

    if weekday < 5 and 7 <= hour < 19:
        schedule.every().minute.at(":05").do(market_hours_job)
        # schedule.every(10).minutes.at(":05").do(market_hours_job)
    else:
        # schedule.clear()  # Clears all scheduled jobs
        schedule.every(15).minutes.do(off_market_hours_job)

main_market_url = "https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicMainMarkets&displayLanguage=en&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC"
first_north_url = "https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicFirstNorth&displayLanguage=en&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC"

check_and_reschedule()

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped by user.")
