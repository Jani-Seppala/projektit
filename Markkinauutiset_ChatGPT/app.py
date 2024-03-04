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
    return "Welcome to the Stock News Analysis App!"

# User Registration Route
print(app.config["MONGO_URI"])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users  # Assuming your MongoDB collection for users is named 'users'
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'password': hashpass
            })
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))  # Redirect to the login page after successful registration
        
        else:
            flash('Email is already registered.', 'danger')

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user and bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
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

# Route for displaying user favorites
@app.route('/favorites')
def favorites():
    # Implement logic to fetch and display user's favorite stocks
    return render_template('favorites.html')  # Ensure you have a template for favorites

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
