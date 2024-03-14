from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from bson import json_util
import bcrypt
import config  # Ensure you have a config.py file with your configurations

app = Flask(__name__)

# Configurations
app.config["MONGO_URI"] = config.MONGO_URI  # Your MongoDB URI
app.config["SECRET_KEY"] = config.SECRET_KEY  # Secret key for session management

print(config.MONGO_URI)
print(config.SECRET_KEY)

# Initialize PyMongo
mongo = PyMongo(app)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect logged-in users to the index page
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        users = mongo.db.users  # Assuming your MongoDB collection for users is named 'users'
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'password': hashpass,
                'favorites': []  # Initialize an empty list for the user's favorites
            })
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))  # Redirect to the login page after successful registration
        
        else:
            flash('Email is already registered.', 'danger')

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user and bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
            session['user_id'] = str(login_user['_id'])  # Correctly store the user_id in session
            session['first_name'] = login_user['first_name']  # Store the first name in session
            flash(f'Welcome back, {session["first_name"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid login credentials.', 'danger')

    return render_template('login.html')

# Route for adding a favorite stock
@app.route('/add_favorite/<stock_id>', methods=['POST'])
def add_favorite(stock_id):
    # Implement logic to add a stock to the user's favorites
    return redirect(url_for('index'))

# Route for user to add and show favorites
@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    # Check if the user is logged in at the very beginning
    if 'user_id' not in session:
        flash('You need to be logged in to view or update favorites.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        selected_favorites = set(request.form.getlist('favorite_stocks'))
        user_id = ObjectId(session['user_id'])
        user = mongo.db.users.find_one({"_id": user_id})
        current_favorites = set(user.get('favorites', []))
        
        # Identify deselected favorites
        deselected_favorites = current_favorites - selected_favorites
        
        # Update the favorites list: remove deselected, add newly selected
        updated_favorites = (current_favorites | selected_favorites) - deselected_favorites
        
        mongo.db.users.update_one(
            {"_id": user_id},
            {"$set": {"favorites": list(updated_favorites)}}
        )
        flash('Favorites updated successfully!', 'success')
    
    # The user is guaranteed to be logged in if this part of the code is reached
    stocks = list(mongo.db.stocks.find())
    user = mongo.db.users.find_one({"_id": ObjectId(session['user_id'])})
    user_favorites = user.get('favorites', [])
    
    return render_template('favorites.html', stocks=stocks, user_favorites=user_favorites)


# Logout Route
@app.route('/logout')
def logout():
    # Clear the user session
    session.clear()
    # Flash a message indicating the user has been logged out
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('index'))


# API ENDPOINTS

@app.route('/api/stocks')
def get_stocks():
    stocks = mongo.db.stocks.find()  # Assuming you have a "stocks" collection
    stocks_list = list(stocks)
    # Convert ObjectId() to string because it is not JSON serializable
    for stock in stocks_list:
        stock['_id'] = str(stock['_id'])
    return jsonify(stocks_list)


@app.route('/api/users/register', methods=['POST'])
def register_user():
    # Assume request.json contains email, password, etc.
    user_data = request.json
    # Process registration (hash password, validate data, etc.)
    # Save the user to the database
    return jsonify({"success": True, "message": "User registered successfully"})


@app.route('/api/news-with-analysis')
def get_news_with_analysis():
    news_items = mongo.db.news.find()
    result = []

    for news_item in news_items:
        news_item_json = json_util.dumps(news_item)  # Serialize
        analysis = mongo.db.analysis.find_one({"news_id": news_item["_id"]})
        analysis_json = json_util.dumps(analysis) if analysis else None  # Serialize
        result.append({"news": json_util.loads(news_item_json), "analysis": json_util.loads(analysis_json) if analysis_json else None})

    # Serialize the entire result list and then create a Response object
    result_json = json_util.dumps(result)
    return Response(result_json, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
