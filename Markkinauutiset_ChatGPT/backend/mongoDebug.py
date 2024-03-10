from app import mongo
from bson.objectid import ObjectId



# Assuming 'mongo' is your PyMongo database connection from Flask app
analysis_collection = mongo.db.analysis
news_collection = mongo.db.news
users_collection = mongo.db.users

# # Fetch all analyses from the database
# all_analyses = analysis_collection.find({})

# for analysis in all_analyses:
#     # Make sure news_id is stored as ObjectId before querying
#     news_id = analysis.get('news_id')
#     if isinstance(news_id, str):
#         news_id = ObjectId(news_id)

#     # Find the corresponding news document
#     news = news_collection.find_one({"_id": news_id})

#     if news:
#         # print(f"Analysis matched with news title: {news.get('headline')}")
#         print(f"Analysis matched with news content: {news.get('messageUrlContent')}")
#         print("------------------------------------------")
#         print(f"Analysis: {analysis.get('analysis_content')}")
#         print("----------------NEXT ITEM----------------")
#     else:
#         print(f"No matching news for analysis with ID: {analysis.get('_id')}")




# Fetch all users from the database
all_users = users_collection.find({})

for user in all_users:
    if 'favorites' in user and user['favorites']:  # Check if user has favorites
        print(f"User: {user.get('email')}")
        favorite_stocks = user.get('favorites', [])
        
        for stock_id in favorite_stocks:
            if isinstance(stock_id, str):
                stock_id = ObjectId(stock_id)
            
            # Find news related to this favorite stock
            related_news = news_collection.find({"stock_id": stock_id})
            
            for news_item in related_news:
                print(f"Related News: {news_item.get('headline')}")
                # Find analyses related to this news item
                analysis = analysis_collection.find_one({"news_id": news_item['_id']})
                if analysis:
                    print(f"\tAnalysis Content: {analysis.get('analysis_content')[:200]}...")  # Print the first 100 chars

