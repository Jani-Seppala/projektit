from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from flask import session
import config  # Ensure you have a config.py file with your configurations

app = Flask(__name__)

# Configurations
app.config["MONGO_URI"] = config.MONGO_URI  # Your MongoDB URI
app.config["SECRET_KEY"] = config.SECRET_KEY  # Secret key for session management

print(config.MONGO_URI)
print(config.SECRET_KEY)

# Initialize PyMongo
mongo = PyMongo(app)

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

if __name__ == '__main__':
    app.run(debug=True)
