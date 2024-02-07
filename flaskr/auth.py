# Create a Flask blueprint for authentication-related routes and views. The blueprint should include the following components:

# Import necessary modules and functions:

# Import 'functools' for working with higher-order functions.
# Import various components from 'flask' for web development functionalities:
# 'Blueprint', 'flash', 'g', 'redirect', 'render_template', 'request', 'session', and 'url_for'.
# Import 'check_password_hash' and 'generate_password_hash' functions from 'werkzeug.security' for password hashing.
# Define a blueprint named 'auth' using the 'Blueprint' class. Set the blueprint's URL prefix to '/auth' to differentiate authentication-related routes.

# Ensure that this blueprint is encapsulated within a module and can be imported into a Flask application for authentication functionality.

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Create a route named '/register' within the 'auth' blueprint for handling user registration. This route should support both GET and POST HTTP methods. The route should include the following functionality:

# When a POST request is received:

# Retrieve the username and password from the form data submitted in the request.
# Obtain a connection to the database using the 'get_db' function.
# Check if both username and password are provided; if not, set an error message accordingly.
# If no error occurs, attempt to insert the user's information (username and hashed password) into the 'user' table in the database.
# Handle any potential IntegrityError (e.g., if the username is already registered) and set an appropriate error message if necessary.
# If registration is successful, redirect the user to the login page.
# If a GET request is received or registration fails:

# Render the 'auth/register.html' template, passing any error message to be displayed using the 'flash' function.

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

# Create a route named '/login' within the 'auth' blueprint for handling user login functionality. This route should support both GET and POST HTTP methods. The route should include the following functionality:

# When a POST request is received:

# Retrieve the username and password from the form data submitted in the request.
# Obtain a connection to the database using the 'get_db' function.
# Query the database to fetch the user's information based on the provided username.
# If the user does not exist, set an error message indicating an incorrect username.
# If the user exists, but the password provided does not match the stored hashed password, set an error message indicating an incorrect password.
# If no error occurs, clear the session, set the 'user_id' in the session to the user's ID, and redirect the user to the 'index' page.
# If a GET request is received or login fails:

# Render the 'auth/login.html' template, passing any error message to be displayed using the 'flash' function.
# Ensure that this route is registered with the 'auth' blueprint and can be accessed at '/auth/login' for user login functionality.

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# Create a function named 'load_logged_in_user' that runs before each request within the 'auth' blueprint. 
# This function should load the currently logged-in user's information into the global context 'g'. The function should include the following functionality:

# Access the 'user_id' stored in the session to determine if a user is logged in.
# If no 'user_id' is found in the session, set the 'g.user' attribute to None.
# If a 'user_id' is found in the session, query the database to fetch the user's information based on the user ID.
# Assign the fetched user information to the 'g.user' attribute.
# Ensure that this function is registered as a before-request callback using the '@bp.before_app_request' decorator and is associated with the 'auth' blueprint. 
# This function should run before each request to ensure that the global 'g' object contains the currently logged-in user's information, if available.

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# write a function to logout user by clearing the session

@bp.route('/logout')
def logout():
    session.clear()

    # write code to connect to database and delete everything from 'cart' table
    db = get_db()
    db.execute('DELETE FROM cart')
    db.commit()
    db.close()    
    
    return redirect(url_for('index'))

# write a function to check if user is logged in

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view