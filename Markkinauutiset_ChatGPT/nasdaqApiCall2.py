import requests
from bs4 import BeautifulSoup
from app import mongo

print('fsfs')

def fetch_news():
    mainMarketUrl = "https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicMainMarkets&displayLanguage=fi&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC"
    # firstNorthUrl = "https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicFirstNorth&displayLanguage=fi&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC"
    response = requests.get(mainMarketUrl)
    if response.status_code == 200:
        news_data = response.json()
        process_and_save_news(news_data)
    else:
        print(f"Failed to fetch news: {response.status_code}")


def process_and_save_news(news_data):
    for item in news_data['results']['item']:
        if item.get('market') == "Main Market, Helsinki":
            # Checks if the news item already exists in the database
            unique_id = item['disclosureId']
            existing_news_item = mongo.db.news.find_one({'disclosureId': unique_id})
            
            if not existing_news_item:
                # If the news item does not exist, fetch the content from the URL
                item_text = fetch_text_from_url(item['messageUrl'])
                if item_text:
                    item['messageUrlContent'] = item_text

                # Check if the stock exists in the database
                stock = mongo.db.stocks.find_one({"company": item.get('company')})
                if stock:
                    # Add the stock `_id` to the news item
                    item['stock_id'] = stock['_id']
                
                # Save the modified news item with the stock `_id` included
                mongo.db.news.insert_one(item)
            else:
                print(f"News item {unique_id} already exists. Skipping content fetch.")


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


fetch_news()
