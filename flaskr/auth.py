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
from twilio.rest import Client
from dotenv import load_dotenv
import random
import os

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

# update register function below to fetch 'mobile number' details from form. Check if 'mobile_number' set is not set.
# If 'mobile_number' is not set, set an error message
# If no error occurs, then insert 'mobile_number' alond with other details into database.
# commit the changes to the database and redirect the user to the login page.

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mobile_number = '+91' + str(request.form['mobile'])
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not mobile_number:
            error = 'Mobile number is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, mobile_number) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), mobile_number)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

# create a route for 'otpvalidation' wih methods as 'GET' and 'POST'.
# If a POST request is received then get the input 'otp' from form and check if it matches the stored 'otp'.
# return redirect(url_for('index'))
# If a GET request is received:
# write a code to generate and send OTP to user's mobile number using twilio
# Ensure that this route is registered with the 'auth' blueprint and can be accessed at '/auth/otpvalidation' for user login functionality.

@bp.route('/otpvalidation', methods=('GET', 'POST'))
def otpvalidation():
    if request.method == 'POST':

        entered_otp = int(request.form['otp'])
        if entered_otp == session['otp']:
            return redirect(url_for('index'))
        else:
            flash('Invalid OTP')

    # UNCOMMENT THE BELOW PART TO GENERATE OTP USING TWILIO SERVICE WHICH INCURS CHARGES FOR OTP GENERATION AND DISTRIBUTION
    # BELOW PART IS TESTED WITH ACTUAL VERIFICATION. BYPASSING IT FOR FURTHER DEVELOPMENT.
            
    # # Load environment variables from .env file
    # load_dotenv()

    # # Your Twilio account SID and auth token. Load the details from .env file using dotenv
    # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    # twilio_phone_number = str(os.getenv('TWILIO_PHONE_NUMBER'))

    # client = Client(account_sid, auth_token)
    # # Generate a random 4-digit OTP
    # otp = random.randint(1000, 9999)
    # # Send the OTP to the user's mobile number
    # message = client.messages.create(
    #     to=session['mobile_number'],
    #     from_=twilio_phone_number,
    #     body=f'Your OTP is {otp}'
    # )
    # print(message.sid)
    # session['otp'] = otp
            
    session['otp'] = 1234

    return render_template('auth/otpvalidation.html')

# create route for 'reset_password' with methods as as 'GET' and 'POST'.
# If get request is received then return the render template for reset_password.html
# If post request is received then get the input 'new_password' from form and update the password in database.

@bp.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        print('===============================')
        print(f'new_password = {new_password}')
        print('===============================')
        otp = int(request.form['otp'])

        # check if received otp matches the stored otp
        if otp != session['otp']:
            print(f'otp = {otp} ({type(otp)})')
            print(f"session['otp'] = {session['otp']} ({type(session['otp'])})")
            flash('Invalid OTP')
            return redirect(url_for('auth.reset_password'))

        db = get_db()
        db.execute(
            'UPDATE user SET password = ? WHERE id = ?',
            (generate_password_hash(new_password), session['user_id'])
        )
        db.commit()
        return redirect(url_for('index'))

    return render_template('auth/reset_password.html')



# create a route for forget_password with methods as 'GET' and 'POST'.
# return the render template for forget_password.html

@bp.route('/forget_password', methods=('GET', 'POST'))
def forget_password():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        else:
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            if not user:
                error = 'User {} is not registered.'.format(username)

        if error is None:
            session.clear()

            # UNCOMMENT THE BELOW PART TO GENERATE OTP USING TWILIO SERVICE WHICH INCURS CHARGES FOR OTP GENERATION AND DISTRIBUTION
            # BELOW PART IS TESTED WITH ACTUAL VERIFICATION. BYPASSING IT FOR FURTHER DEVELOPMENT.
                    
            # # Load environment variables from .env file
            # load_dotenv()

            # # Your Twilio account SID and auth token. Load the details from .env file using dotenv
            # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            # twilio_phone_number = str(os.getenv('TWILIO_PHONE_NUMBER'))

            # client = Client(account_sid, auth_token)
            # # Generate a random 4-digit OTP
            # otp = random.randint(1000, 9999)
            # # Send the OTP to the user's mobile number
            # message = client.messages.create(
            #     to=user['mobile_number'],
            #     from_=twilio_phone_number,
            #     body=f'Your OTP is {otp}'
            # )
            # print(message.sid)
            # session['otp'] = otp

            session['otp'] = 1234
            session['user_id'] = user['id']

            return redirect(url_for('auth.reset_password'))

        flash(error)

    return render_template('auth/forget_password.html')

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

# update the below login function to take 'mobile number' as input. Check if 'mobile_number' is not set.
# If 'mobile_number' is not set, set an error message
# If no error occurs, then check if the 'mobile_number' provided matches the stored 'mobile_number' for the user.
# If the 'mobile_number' matches, then clear the session, set the 'user_id' in the session to the user's ID, and redirect the user to the 'index' page.

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
            session['mobile_number'] = user['mobile_number']
            # return redirect(url_for('index'))
            return redirect(url_for('auth.otpvalidation'))
            # return render_template('auth/otpvalidation.html')

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