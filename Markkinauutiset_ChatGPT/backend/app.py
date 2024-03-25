from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from flask_cors import CORS
from bson import json_util
from datetime import timedelta
import bson.json_util
import bcrypt
import config  # Ensure you have a config.py file with your configurations

app = Flask(__name__)

# Configurations
app.config["MONGO_URI"] = config.MONGO_URI  # Your MongoDB URI
app.config["SECRET_KEY"] = config.SECRET_KEY  # Secret key for session management
jwt = JWTManager(app)

print(config.MONGO_URI)
print(config.SECRET_KEY)

# Initialize PyMongo
mongo = PyMongo(app)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/users/register', methods=['POST'])
def register_user():
    users = mongo.db.users
    existing_user = users.find_one({'email': request.json['email']})

    if existing_user is None:
        password = request.json['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({
            'first_name': request.json['first_name'],
            'last_name': request.json['last_name'],
            'email': request.json['email'],
            'password': hashed_password,
            'favorites': []
        })
        return jsonify({"success": True, "message": "User registered successfully"})
    else:
        return jsonify({"success": False, "message": "Email is already registered."})


@app.route('/api/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email': request.json['email']})

    if login_user:
        hashed_password = login_user['password']
        password_check = bcrypt.checkpw(request.json['password'].encode('utf-8'), hashed_password)
        if password_check:
            # Set the token to expire in 1 hour
            expires = timedelta(hours=1)
            access_token = create_access_token(identity=str(login_user['_id']), expires_delta=expires)
            # Convert the ObjectId to a string before returning the user data
            login_user['_id'] = str(login_user['_id'])
            # Remove the password before returning the user data
            login_user.pop('password')
            return jsonify({"success": True, "message": f"Welcome back, {login_user['first_name']}!", "token": access_token, "user": login_user})
        else:
            return jsonify({"success": False, "message": "Invalid login credentials."}), 401
    else:
        return jsonify({"success": False, "message": "Invalid login credentials."}), 401


@app.route('/api/users/<user_id>/add_favorite/<stock_id>', methods=['POST'])
@jwt_required()
def add_favorite(user_id, stock_id):
    if get_jwt_identity() != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if stock_id in user.get("favorites", []):
        return jsonify({"message": "Stock is already in favorites"}), 409
    try:
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorites": stock_id}}
        )
        return jsonify({"message": "Stock added to favorites"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()  # Get user ID from the JWT payload
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user and 'favorites' in user:
        # Convert strings in the favorites list to ObjectIds
        favorites_ids = [ObjectId(favorite) for favorite in user['favorites']]
        # Fetch the full details of each favorite stock
        favorites_info = list(mongo.db.stocks.find({"_id": {"$in": favorites_ids}}))
        # Convert ObjectIds in the favorites_info to strings
        for favorite in favorites_info:
            favorite['_id'] = str(favorite['_id'])
        print('Favorites Info:', favorites_info)  # Add this line
        return jsonify(favorites_info)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/favorites', methods=['POST'])
@jwt_required()
def update_favorites():
    user_id = get_jwt_identity()  # Get user ID from the JWT payload
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        favorites = request.json.get('favorites', [])
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"favorites": favorites}}
        )
        return jsonify({"message": "Favorites updated successfully!"})
    else:
        return jsonify({"error": "User not found"}), 404



# Logout Route
@app.route('/logout')
def logout():
    # Clear the user session
    session.clear()
    # Flash a message indicating the user has been logged out
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('index'))


# Get all stocks for search bar
@app.route('/api/stocks')
def get_stocks():
    search_query = request.args.get('query', '')  # Retrieve the search query parameter
    if search_query:
        # Perform a case-insensitive search for stocks matching the query
        stocks = mongo.db.stocks.find({"company": {"$regex": search_query, "$options": "i"}})
    else:
        # If no query is provided, return all stocks
        stocks = mongo.db.stocks.find()
    
    stocks_list = list(stocks)
    # Convert ObjectId() to string because it is not JSON serializable
    for stock in stocks_list:
        stock['_id'] = str(stock['_id'])
    return jsonify(stocks_list)


# Get a single stock by its ID
@app.route('/api/stocks/<stockId>', methods=['GET'])
def get_stock(stockId):
    try:
        # Assuming your MongoDB collection is named 'stocks' and uses default ObjectIds
        stock = mongo.db.stocks.find_one({"_id": ObjectId(stockId)})
        if stock:
            # Convert the _id from ObjectId to string for JSON serialization
            stock['_id'] = str(stock['_id'])
            return jsonify(stock), 200
        else:
            return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app.route('/api/news-with-analysis', methods=['GET'])
def get_news_with_analysis():
    # Handle GET request
    stock_id = request.args.get('stock_id')
    stock_ids = request.args.get('stock_ids')
    print('Received stock_id:', stock_id)
    print('Received stock_ids:', stock_ids)

    if stock_id:
        # If stock_id is provided, fetch news for the specified stock
        news_items = mongo.db.news.find({"stock_id": ObjectId(stock_id)})
    elif stock_ids:
        # If stock_ids is provided, fetch news for the specified stocks
        stock_ids_list = stock_ids.split(',')
        stock_object_ids = [ObjectId(stock_id) for stock_id in stock_ids_list]
        news_items = mongo.db.news.find({"stock_id": {"$in": stock_object_ids}})
        print('Fetched news items:', list(news_items))  # Log the fetched news items
        news_items = mongo.db.news.find({"stock_id": {"$in": stock_object_ids}})  # Fetch the news items again
    else:
        # If neither stock_id nor stock_ids is provided, fetch all news
        news_items = mongo.db.news.find()

    result = []
    for news_item in news_items:
        analysis = mongo.db.analysis.find_one({"news_id": news_item["_id"]})
        combined = {"news": news_item, "analysis": analysis}
        result.append(combined)

    result_json = json_util.dumps(result)
    return app.response_class(response=result_json, mimetype='application/json')


@app.route('/api/users/me', methods=['GET'])
@jwt_required()
def get_logged_in_user():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if user:
        # Convert ObjectId to string
        user['_id'] = str(user['_id'])
        # Remove the password before returning the user data
        user.pop('password')
        return jsonify({"success": True, "user": user})
    else:
        return jsonify({"success": False, "message": "User not found."}), 404
    

if __name__ == '__main__':
    app.run(debug=True)
