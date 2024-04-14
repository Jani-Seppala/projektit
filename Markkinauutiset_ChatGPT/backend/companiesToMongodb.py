# UPDATES ALL OF THE COMPANIES TO MONGO DB OVERWRITING EVERYTHING, SHOULD ONLY BE USED WHEN MAKING NEW DB!!!

# from pymongo import MongoClient
# import json
# import config
# import os

# print(os.getcwd())


# # MongoDB connection string
# mongo_uri = config.MONGO_URI

# # Connect to MongoDB
# client = MongoClient(mongo_uri)
# db = client.get_database()  # Automatically infer database name from URI

# # Specify the collection
# collection = db['stocks']  # Adjust 'stocks' to your collection name

# # Load JSON data from file
# filepath = os.path.join(os.getcwd(), 'nordicCompanies.json')
# print(f"Attempting to open file at: {filepath}")

# with open('backend/nordicCompanies.json', 'r', encoding='utf-8') as file:
#     stocks_data = json.load(file)

# # Insert data into collection
# result = collection.insert_many(stocks_data)
# print(f"Inserted {len(result.inserted_ids)} documents into the collection.")

# # Close the connection
# client.close()


# UPDATES THE STOCKS IN THE DATABASE AND ADDS NEW STOCKS IF THEY ARE NOT ALREADY IN THE DATABASE
# NOT TESTED THOROUGHLY, SHOULD ONLY USE MANUAL UPDATES WITH THE DRY RUN SET TO TRUE

from pymongo import MongoClient
import json
import config
import os
import logging

# Set up logging
logging.basicConfig(filename='update_stocks.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load JSON data from file
filepath = os.path.join(os.getcwd(), 'backend', 'nordicCompanies.json')
print(f"Attempting to open file at: {filepath}")

try:
    with open(filepath, 'r', encoding='utf-8') as file:
        stocks_data = json.load(file)
except FileNotFoundError as e:
    logging.error(f"File not found: {filepath}")
    print(f"File not found: {filepath}")
    exit()

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client.get_database()
collection = db['stocks']

# Dry run setting
dry_run = True

if dry_run:
    logging.info("Dry run mode - No changes will be made to the database")
    print("Dry run mode - No changes will be made to the database")

updates = []
for new_stock in stocks_data:
    # Use both ISIN and market for finding the existing document
    existing_stock = collection.find_one({'isin': new_stock['isin'], 'market': new_stock['market']})
    if existing_stock:
        # Check for differences, excluding 'isin' and 'market'
        differences = {key: new_stock[key] for key in new_stock if key not in ['isin', 'market'] and new_stock[key] != existing_stock.get(key)}
        if differences:
            print(f"Updating {new_stock['name']} in {new_stock['market']} with changes: {differences}")
            if not dry_run:
                collection.update_one({'isin': new_stock['isin'], 'market': new_stock['market']}, {'$set': differences})
            updates.append(new_stock)
    else:
        print(f"New stock {new_stock['name']} will be added to the database.")
        if not dry_run:
            collection.insert_one(new_stock)

if dry_run:
    print(f"Dry run complete. Detected {len(updates)} updates but no changes made.")
else:
    print(f"Applied updates to {len(updates)} stocks in the database.")

# Close the connection
client.close()

