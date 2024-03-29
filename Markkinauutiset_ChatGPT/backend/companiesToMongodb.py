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
db = client.get_database()  # Automatically infer database name from URI
collection = db['stocks']

# Dry run setting
dry_run = True

if dry_run:
    logging.info("Dry run mode - No changes will be made to the database")
    print("Dry run mode - No changes will be made to the database")

updates = []
for stock in stocks_data:
    existing_stock = collection.find_one({'isin': stock['isin']})
    if existing_stock:
        # Check for differences in all fields except 'isin'
        differences = {key: stock[key] for key in stock if key != 'isin' and stock[key] != existing_stock.get(key)}
        if differences:
            print(f"Updating {stock['name']} with changes: {differences}")
            update = {
                'isin': stock['isin'],
                'update': {'$set': differences}
            }
            updates.append(update)
    else:
        print(f"New stock {stock['name']} will be added to the database.")

# Apply updates
if not dry_run:
    for update in updates:
        collection.update_one({'isin': update['isin']}, update['update'])
    print(f"Applied {len(updates)} updates to the database.")
else:
    print("Dry run mode - No changes were made to the database.")

# Close the connection
client.close()
