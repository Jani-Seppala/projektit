# from pymongo import MongoClient
# import json
# import config
# import os
# import logging
# from fuzzywuzzy import process, fuzz

# # Set up logging
# logging.basicConfig(filename='update_aliases.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Load JSON data from file
# aliases_filepath = os.path.join(os.getcwd(), 'all_companies_aliases.json')
# print(f"Attempting to open file at: {aliases_filepath}")

# try:
#     with open(aliases_filepath, 'r', encoding='utf-8') as file:
#         aliases_data = json.load(file)
# except FileNotFoundError:
#     logging.error(f"File not found: {aliases_filepath}")
#     print(f"File not found: {aliases_filepath}")
#     exit()

# # MongoDB connection
# client = MongoClient(config.MONGO_URI)
# db = client.get_database()
# stocks_collection = db['stocks']

# # Fetch all stocks for matching
# all_stocks = list(stocks_collection.find({}))

# # Correct market mapping from alias file markets to database markets
# market_mapping = {
#     "Nasdaq Copenhagen": "Main Market, Copenhagen",
#     "Nasdaq Helsinki": "Main Market, Helsinki",
#     "Nasdaq Stockholm": "Main Market, Stockholm",
#     "Nasdaq Iceland": "Main Market, Iceland",
#     "First North Denmark MTF": "First North Denmark",
#     "First North Sweden MTF": "First North Sweden",
#     "First North Finland MTF": "First North Finland",
#     "First North Iceland MTF": "First North Iceland"
# }

# # Dry run setting
# dry_run = True

# if dry_run:
#     logging.info("Dry run mode - No changes will be made to the database")
#     print("Dry run mode - No changes will be made to the database")

# updates = 0
# for alias in aliases_data:
#     alias_market = alias['market'].strip()
#     normalized_market = market_mapping.get(alias_market, alias_market)  # Use mapping
#     stocks_names = [(stock['name'], stock) for stock in all_stocks if stock['market'] == normalized_market]
#     names_list = [name for name, _ in stocks_names]

#     if names_list:
#         best_match, score = process.extractOne(alias['name'], names_list, scorer=fuzz.ratio)
#         if score > 80:
#             matched_stock = next(stock for name, stock in stocks_names if name == best_match)
#             # Ensure 'aliases' field exists and is a list
#             if 'aliases' not in matched_stock:
#                 matched_stock['aliases'] = []
#             # Add the alias if it's not already in the list
#             if alias['name'] not in matched_stock['aliases']:
#                 matched_stock['aliases'].append(alias['name'])
#                 logging.info(f"Adding alias '{alias['name']}' to '{matched_stock['name']}' with match score {score}")
#                 print(f"Adding alias '{alias['name']}' to '{matched_stock['name']}' with match score {score}")
#                 # Update the stock document in the database
#                 if not dry_run:
#                     result = stocks_collection.update_one({'_id': matched_stock['_id']}, {'$set': {'aliases': matched_stock['aliases']}})
#                     if result.modified_count > 0:
#                         updates += 1
#     else:
#         logging.info(f"No stocks found in market '{normalized_market}' for alias '{alias['name']}'")
#         print(f"No stocks found in market '{normalized_market}' for alias '{alias['name']}'")

# if dry_run:
#     print(f"Dry run complete. Detected {updates} updates but no changes made.")
#     logging.info(f"Dry run complete. Detected {updates} updates but no changes made.")
# else:
#     print(f"Applied updates to {updates} stocks in the database.")
#     logging.info(f"Applied updates to {updates} stocks in the database.")

# # Close the connection
# client.close()



# from pymongo import MongoClient

from pymongo import MongoClient
import json
import config
import os
import logging
from fuzzywuzzy import process, fuzz
import re

# Set up logging
logging.basicConfig(filename='update_aliases.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the normalization function
def normalize_company_name(name):
    # Convert to lower case and remove punctuation
    name = re.sub(r'[\s.,;:\'\"()&/]+', '', name).lower()
    # Remove common corporate suffixes including 'group' using a regex
    # Ensure the regex accounts for case and proper boundary at word's end
    name = re.sub(r'(ab|oyj|plc|as|ltd|inc|llc|group|international|a/s)(ab|oyj|plc|as|ltd|inc|llc|group|international|a/s)?$', '', name, flags=re.IGNORECASE)
    # name = re.sub(r'(ab|oyj|plc|as|ltd|inc|llc|group|corporation|international|solutions|holding|a/s)(ab|oyj|plc|as|ltd|inc|llc|group|corporation|international|solutions|holding|a/s)?$', '', name, flags=re.IGNORECASE)
    return name.strip()

# Load JSON data from file
aliases_filepath = os.path.join(os.getcwd(), 'all_companies_aliases.json')
print(f"Attempting to open file at: {aliases_filepath}")

try:
    with open(aliases_filepath, 'r', encoding='utf-8') as file:
        aliases_data = json.load(file)
except FileNotFoundError:
    logging.error(f"File not found: {aliases_filepath}")
    print(f"File not found: {aliases_filepath}")
    exit()

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client.get_database()
stocks_collection = db['stocks']

# Fetch all stocks for matching
all_stocks = list(stocks_collection.find({}))

# Market mapping from alias file markets to database markets
market_mapping = {
    "Nasdaq Copenhagen": "Main Market, Copenhagen",
    "Nasdaq Helsinki": "Main Market, Helsinki",
    "Nasdaq Stockholm": "Main Market, Stockholm",
    "Nasdaq Iceland": "Main Market, Iceland",
    "First North Denmark MTF": "First North Denmark",
    "First North Sweden MTF": "First North Sweden",
    "First North Finland MTF": "First North Finland",
    "First North Iceland MTF": "First North Iceland"
}

# Dry run setting
dry_run = True

if dry_run:
    logging.info("Dry run mode - No changes will be made to the database")
    print("Dry run mode - No changes will be made to the database")


market_aliases_dict = {}
updates = 0
stock_count = 0

for stock in all_stocks:
    stock_count += 1
    print(f"Processing stock {stock_count}/{len(all_stocks)}: {stock['name']}")

    stock_market = stock['market']
    normalized_stock_name = normalize_company_name(stock['name'])
    relevant_aliases = [alias for alias in aliases_data if market_mapping.get(alias['market'].strip(), alias['market'].strip()) == stock_market]
    
    # if 'aliases' not in stock:
    #     stock['aliases'] = []
    
    # Ensure the market exists in the dictionary
    if stock_market not in market_aliases_dict:
        market_aliases_dict[stock_market] = {}
        
    # Ensure the company is initialized under the market
    if stock['name'] not in market_aliases_dict[stock_market]:
        market_aliases_dict[stock_market][stock['name']] = []

    for alias in relevant_aliases:
        normalized_alias_name = normalize_company_name(alias['name'])
        initial_score = fuzz.token_set_ratio(normalized_alias_name, normalized_stock_name)
        if initial_score > 50:
            detailed_score = fuzz.partial_ratio(normalized_alias_name, normalized_stock_name)
            if detailed_score > 80:
                # if alias['name'] not in stock['aliases']:
                    # stock['aliases'].append(alias['name'])
                    # print(f"Added alias '{alias['name']}' to '{stock['name']}' with match score {detailed_score}")
                    # logging.info(f"Added alias '{alias['name']}' to '{stock['name']}' with match score {detailed_score}")
                    
                alias_entry = {
                'name': alias['name'],
                'score': detailed_score  # Store the match score with the alias
                }
                if alias_entry not in market_aliases_dict[stock_market][stock['name']]:
                    market_aliases_dict[stock_market][stock['name']].append(alias_entry)
                    print(f"Added alias '{alias['name']}' to '{stock['name']}' in '{stock_market}' with match score {detailed_score}")
                    logging.info(f"Added alias '{alias['name']}' to '{stock['name']}' in '{stock_market}' with match score {detailed_score}")
                    
                # if alias['name'] not in market_aliases_dict[stock_market][stock['name']]:
                #     market_aliases_dict[stock_market][stock['name']].append(alias['name'])
                #     print(f"Added alias '{alias['name']}' to '{stock['name']}' in '{stock_market}' with match score {detailed_score}")
                #     logging.info(f"Added alias '{alias['name']}' to '{stock['name']}' in '{stock_market}' with match score {detailed_score}")
                
                if not dry_run:
                    pass
                    # result = stocks_collection.update_one({'_id': stock['_id']}, {'$set': {'aliases': stock['aliases']}})
                    # if result.modified_count > 0:
                        # updates += 1
            else:
                print(f"Discarded low score match for '{stock['name']}' with alias '{alias['name']}' - Score: {detailed_score}")
        else:
            print(f"Ignored '{alias['name']}' for '{stock['name']}' - Initial Score: {initial_score}")

if dry_run:
    print(f"Dry run complete. Detected {updates} updates but no changes made.")
    logging.info(f"Dry run complete. Detected {updates} updates but no changes made.")
else:
    print(f"Applied updates to {updates} stocks in the database.")
    logging.info(f"Applied updates to {updates} stocks in the database.")

# Output the JSON file for review
with open('aliases_output.json', 'w', encoding='utf-8') as json_file:
    json.dump(market_aliases_dict, json_file, ensure_ascii=False, indent=4)

# Close the connection
client.close()