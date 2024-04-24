import json
from pymongo import MongoClient
import logging
import os
import config

# Setup logging
logging.basicConfig(filename=f'update_stocks_{os.getpid()}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the path to the JSON file
data_path = os.path.join(os.getcwd(), 'aliases_output.json')
logging.info(f"Attempting to open file at: {data_path}")

try:
    # Load the JSON file with aliases
# Load the JSON file with aliases
    with open(data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # MongoDB connection
    client = MongoClient(config.MONGO_URI)
    db = client.get_database()
    stocks_collection = db['stocks']

    # Enable or disable dry run mode
    dry_run = False  # Change this to False to perform actual database updates

    # List of known markets
    known_markets = [
        "First North Sweden", "First North Finland", "First North Denmark", "First North Iceland",
        "Main Market, Copenhagen", "Main Market, Helsinki", "Main Market, Iceland", "Main Market, Stockholm"
    ]

    # Update process
    for market in known_markets:
        if market in data:
            for company_name, aliases_info in data[market].items():
                aliases = [alias['name'] for alias in aliases_info]  # Extract only the names
                query = {'name': company_name, 'market': market}
                new_values = {'$set': {'aliases': aliases}}
                if not dry_run:
                    result = stocks_collection.update_one(query, new_values)
                    if result.modified_count > 0:
                        logging.info(f"Updated {company_name} in {market} with aliases: {aliases}")
                    else:
                        logging.info(f"No update needed for {company_name} in {market}")
                else:
                    logging.info(f"Dry Run: Would update {company_name} in {market} with aliases: {aliases}")
finally:
    if 'client' in locals():
        client.close()  # Ensure the MongoDB client is closed regardless of earlier success or failure

