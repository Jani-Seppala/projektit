import os

# MongoDB Configuration
MONGO_URL = os.environ.get('MONGODB_URL')
MONGO_USER = os.environ.get('MONGODB_USER')
MONGO_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGO_STOCK_URL = os.environ.get('MONGODB_STOCK_URL')

# Flask Configuration
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

# MongoDB URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URL}/{MONGO_STOCK_URL}"

