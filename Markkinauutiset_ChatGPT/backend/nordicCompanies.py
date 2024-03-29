from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import json
import os


def determine_market(url, currency, isin):
    market = "Unknown Market"  # Default assignment

    # Direct assignments for main markets based on URL
    if "copenhagen" in url:
        market = "Main Market, Copenhagen"
    elif "helsinki" in url:
        market = "Main Market, Helsinki"
    elif "iceland" in url:
        market = "Main Market, Iceland"
    elif "stockholm" in url:
        market = "Main Market, Stockholm"
    elif "baltic" in url:
        market = "Main Market, Baltic"
    elif "first-north" in url:
        # Initialize market based on ISIN code
        isin_to_market = {
            "SE": "First North Sweden",
            "FI": "First North Finland",
            "DK": "First North Denmark",
            "IS": "First North Iceland",
        }
        country_code = isin[:2]  # Extract country code from ISIN
        market = isin_to_market.get(country_code, None)  # Attempt to assign market based on ISIN

        # If market couldn't be determined by ISIN, use currency as a fallback
        if not market:
            currency_to_market = {
                "SEK": "First North Sweden",
                "EUR": "First North Finland", 
                "DKK": "First North Denmark",
                "ISK": "First North Iceland",
            }
            market = currency_to_market.get(currency, "Check Manually")  # Fallback for manual checking

    return market

def scrape_stocks(url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    # tbody = driver.find_element(By.XPATH, '/html/body/section/div/div/div/section/article[2]/div/div/table/tbody')
    tbody = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/section/div/div/div/section/article[2]/div/div/table/tbody')))
    rows = tbody.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) >= 6:
            name_link = cells[0].find_element(By.TAG_NAME, 'a')
            name = name_link.text
            href = name_link.get_attribute('href')
            symbol = cells[1].text
            currency = cells[2].text
            isin = cells[3].text
            sector = cells[4].text
            icb = cells[5].text

            market = determine_market(url, currency, isin)
            # Add the market information to your stocks_data dictionary
            stocks_data.append({
                "name": name,
                "href": href,
                "symbol": symbol,
                "currency": currency,
                "isin": isin,
                "sector": sector,
                "icb": icb,
                "market": market  # Added market field
            })
            
        
    time.sleep(5)
    
    

# URLs to scrape
urls = [
    "https://www.nasdaqomxnordic.com/shares/listed-companies/first-north",
    "https://www.nasdaqomxnordic.com/shares/listed-companies/copenhagen",
    "https://www.nasdaqomxnordic.com/shares/listed-companies/helsinki",
    "https://www.nasdaqomxnordic.com/shares/listed-companies/iceland",
    "https://www.nasdaqomxnordic.com/shares/listed-companies/stockholm",
    "https://www.nasdaqomxnordic.com/shares/listed-companies/baltic"
]

# Initialize WebDriver
driver_path = r'C:\Chromedriver\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

stocks_data = []

# Iterate over each URL and scrape the stock data
for url in urls:
    scrape_stocks(url)
    print(len(stocks_data))

driver.quit()

filename = 'stocks_data.json'
print(f"Current working directory: {os.getcwd()}")
print(f"Attempting to write to file: {filename}")
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(stocks_data, f, ensure_ascii=False, indent=4)
print(f"Data written to file: {filename}")
