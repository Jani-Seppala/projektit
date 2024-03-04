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
        # Directly check if the news item is related to 'Main Market, Helsinki'
        if item.get('market') == "Main Market, Helsinki":
            # Construct a unique identifier based on stable attributes (disclosureId is already unique)
            unique_id = item['disclosureId']
            
            # Check if the news item already exists in the database
            existing_news_item = mongo.db.news.find_one({'disclosureId': unique_id})
            
            # If it doesn't exist, fetch the text content and save the news item
            if not existing_news_item:
                # Since we're fetching new items, we always fetch the text content
                item_text = fetch_text_from_url(item['messageUrl'])
                if item_text:
                    # Add the text content to the news item object under 'messageUrlContent'
                    item['messageUrlContent'] = item_text
                
                # Save the news item to the database
                mongo.db.news.insert_one(item)
            else:
                print(f"News item {unique_id} already exists. Skipping content fetch.")


# def english_version_exists(news_item):
#     """
#     Check if an English version of the news item already exists in the database.
#     """
#     # Assuming 'company', 'categoryId', 'cnsCategory', 'releaseTime', and 'market'
#     # are sufficient to uniquely identify related news items.
#     print(f'english_version exist news_item {news_item}')
#     exists = mongo.db.news.find_one({
#         'company': news_item['company'],
#         'categoryId': news_item['categoryId'],
#         'cnsCategory': news_item['cnsCategory'],
#         'releaseTime': news_item['releaseTime'],
#         'market': news_item['market'],
#         'language': 'en'  # Looking specifically for an English version
#     })
#     return bool(exists)


def fetch_text_from_url(url):
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
