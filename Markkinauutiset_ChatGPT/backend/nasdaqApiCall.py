import requests
from openai import OpenAI
from bs4 import BeautifulSoup


# # The API endpoint URL, modified to remove the callback parameter
# mainMarketUrl = "https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicMainMarkets&displayLanguage=fi&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC"
# firstNorthUrl = "https://api.news.eu.nasdaq.com/news/query.action?type=json&showAttachments=true&showCnsSpecific=true&showCompany=true&countResults=false&freeText=&market=&cnscategory=&company=&fromDate=&toDate=&globalGroup=exchangeNotice&globalName=NordicFirstNorth&displayLanguage=fi&language=&timeZone=CET&dateMask=yyyy-MM-dd%20HH%3Amm%3Ass&limit=20&start=0&dir=DESC"

# # Make the GET request
# response = requests.get(mainMarketUrl)
# data = response.json()

# if response.status_code == 200:

#     # Iterate through each news item and extract information
#     for item in data['results']['item']:
#         time = item['releaseTime']
#         headline = item['headline']
#         company = item['company']
#         category = item['cnsCategory']
#         link = item['messageUrl']
#         language = item['language']
        
#         print(f"Time: {time}")
#         print(f"Headline: {headline}")
#         print(f"Language: {language}")
#         print(f"Company: {company}")
#         print(f"Category: {category}")
#         print(f"Link: {link}\n")
# else:
#     print(f"Failed to retrieve data: {response.status_code}")




# URL of the page to scrape
# url = 'https://view.news.eu.nasdaq.com/view?id=b54af6ed4e88ae01203159a2092cf26a5&lang=en&src=listed'
url = 'https://view.news.eu.nasdaq.com/view?id=b2f761b817d8504cbfbe95aa31f35d6c3&lang=fi&src=listed'

# Send a GET request to the URL
response = requests.get(url)

# Initialize an empty string to hold all the text
all_text = ""

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Assuming the text you're interested in is within <p> tags
    # This is a simplification; you may need to adjust the selector based on the actual HTML structure
    text_elements = soup.find_all('p')
    
    # Concatenate the text from each element into one large string
    for element in text_elements:
        all_text += element.get_text(strip=True) + " "  # Adding a space for readability

    print(all_text)
else:
    print("Failed to retrieve the webpage")

