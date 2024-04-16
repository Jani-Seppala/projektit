from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import json
import os


def determine_market(url, stock_href):
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
        # Additional logic for Baltic markets based on stock_href
        if "TAL" in stock_href:
            market = "Main Market, Tallinn"
        elif "RIS" in stock_href:
            market = "Main Market, Riga"
        elif "VSE" in stock_href:
            market = "Main Market, Vilnius"
    elif "first-north" in url:
        # Mapping of First North markets based on instrument code prefix
        market_map = {
            "SSE": "First North Sweden",
            "HEX": "First North Finland",
            "CSE": "First North Denmark",
            "ICEX": "First North Iceland",
            # Add more mappings as necessary
        }

        # Check if any known instrument code prefix is present in the URL
        for code_prefix, market_name in market_map.items():
            if f"Instrument={code_prefix}" in stock_href:
                market = market_name
                break  # Stop searching once a match is found

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
            stock_href = name_link.get_attribute('href')
            symbol = cells[1].text
            currency = cells[2].text
            isin = cells[3].text
            sector = cells[4].text
            icb = cells[5].text

            market = determine_market(url,stock_href)
            # Add the market information to your stocks_data dictionary
            stocks_data.append({
                "name": name,
                "link": stock_href,
                "symbol": symbol,
                "currency": currency,
                "isin": isin,
                "sector": sector,
                "icb": icb,
                "market": market  # Added market field
            })
            
        
    # time.sleep(5)
    
    

# URLs to scrape
urls = [
    # "https://www.nasdaqomxnordic.com/shares/listed-companies/first-north",
    # "https://www.nasdaqomxnordic.com/shares/listed-companies/copenhagen",
    # "https://www.nasdaqomxnordic.com/shares/listed-companies/helsinki",
    # "https://www.nasdaqomxnordic.com/shares/listed-companies/iceland",
    # "https://www.nasdaqomxnordic.com/shares/listed-companies/stockholm",
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

filename = 'stocks_data2.json'
print(f"Current working directory: {os.getcwd()}")
print(f"Attempting to write to file: {filename}")
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(stocks_data, f, ensure_ascii=False, indent=4)
print(f"Data written to file: {filename}")
