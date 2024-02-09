# Create a Flask blueprint named 'product' for managing product-related routes and views. The blueprint should include the following components:
# Import necessary modules and functions from Flask and related libraries:
# Import 'Blueprint', 'flash', 'g', 'redirect', 'render_template', 'request', and 'url_for' from Flask.
# Import 'abort' from 'werkzeug.exceptions' for handling HTTP errors.
# Import the 'login_required' decorator from the 'flaskr.auth' module for protecting routes that require authentication.
# Import the 'get_db' function from the 'flaskr.db' module to interact with the database.
# Define the blueprint named 'product' using the 'Blueprint' class provided by Flask.
# Ensure that this blueprint can be imported and registered with a Flask application for managing product-related routes and views.

from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('product', __name__)

# You're building a Flask application with a Blueprint named bp for handling product-related routes. Write a Python function that defines a route for the root URL ("/") to display a list of products.

# Define a route for the root URL ("/") using the @bp.route() decorator.
# Inside the route function, retrieve product data from the database using the get_db() function.
# Execute an SQL query to select all columns from the "product" table.
# Fetch all rows of product data using the fetchall() method.
# Pass the fetched product data to the render_template() function along with the template name 'product/index.html' and the variable name products.
# Write Python code to implement these steps, encapsulate it within triple backticks, and include it in your response.

# Update below code to get all 'items' from 'cart' database
# pass fetched 'items' as argument to render template

@bp.route('/')
@login_required
def index():
    db = get_db()
    products = db.execute(
        'SELECT * FROM product'
    ).fetchall()

    items = db.execute(
        'SELECT * FROM cart'
    ).fetchall()

    return render_template('product/index.html', products=products, items=items)


@bp.route('/add_to_cart', methods=['POST'])
@login_required
def create():
    name = request.form['name']
    price = request.form['price']
    error = None

    db = get_db()
    db.execute(
        'INSERT INTO cart (name, price)'
        ' VALUES (?, ?)',
        (name, price)
    )
    db.commit()
    return redirect(url_for('product.index'))

# create a route for 'order_confirmation' wih methods as 'GET' and 'POST'.
# If a POST request is received then add 'pass' to it which will be implemented further
# If a GET request is received:
#     Retrieve 'upi_id', 'total_price', address, pin code from session
#     Retrive username
#     Pass 'upi_id', 'total_price', address, pin code, username as arguments to render template 'product/order_confirmation.html'

@bp.route('/order_confirmation', methods=['GET', 'POST'])
@login_required
def order_confirmation():
    upi_id = session.get('upi_id')
    total_price = session.get('total_price')
    address = session.get('address')
    pin_code = session.get('pincode')
    username = session.get('username') 
    payment_id = session.get('payment_id')

    return render_template(
        'product/order_confirmation.html', 
        upi_id=upi_id, 
        total_price=total_price, 
        address=address, 
        pin_code=pin_code, 
        username=username, 
        payment_id=payment_id)

def process_payment(upi_id, total_price):
    # implement payment processing logic here using upi_id and total_price
    # return payment_id as a string
    # for example:
    # payment_id = 'XXXXXX'
    # return payment_id
   
    payment_id = '123456'
    return payment_id

# create function to verify payment status using payment id
# user upi payment api_url, api_key, appropriate headers and payload to pass in call
# if payment status is successful, then return True, else return False
# write code to implement this function, encapsulate it within triple backticks, and include it in your response.

def verify_payment(payment_id):
    # implement payment verification logic here using payment_id
    # for example:
    # if payment_id == 'XXXXXX':
    #     return True
    # else:
    #     return False

    return True if payment_id == '123456' else False


# create a route for 'payment' wih methods as 'GET' and 'POST'.
# If a POST request is received then add 'pass' to it which will be implemented further
# If a GET request is received:
#     Retrieve total_price from session
#     Pass total_price as argument to render template 'product/payment.html'
#     Return the rendered template

@bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    total_price = session.get('total_price')

    if request.method == 'POST':
        # check if entered upi id is in the format as 'XXXX@upi'. If not, flash error
        # if entered upi id is in the format as 'XXXX@upi', then proceed to 'order_confirmation' page
        upi_id = request.form['upi_id']
        if not upi_id.endswith('@upi'):
            flash('Invalid UPI ID')
            return redirect(url_for('product.payment'))
        else:
            session['upi_id'] = upi_id

            payment_id = process_payment(upi_id, total_price)

            # write a code to verify if payment is successful using payment_id
            # if payment is successful, then redirect to 'order_confirmation' page
            # else, flash error and redirect to 'payment' page

            if verify_payment(payment_id):
                session['payment_status'] = True
                session['payment_id'] = payment_id
            else:
                flash('Payment failed')
                return redirect(url_for('product.payment'))
            

            return redirect(url_for('product.order_confirmation'))
        

    return render_template('product/payment.html', total_price=total_price)



# create a route for 'checkout' wih methods as 'GET' and 'POST'.
# If a POST request is received then add 'pass' to it which will be implemented further
# If a GET request is received:
#     Retrieve all 'items' from 'cart' database
#     Pass fetched 'items' as argument to render template 'product/checkout.html'
#     Return the rendered template

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    db = get_db()
    items = db.execute(
        'SELECT * FROM cart'
    ).fetchall()

    # calculate the total price of all items in the cart using items['price'] 
    # pass the total price to render template 'product/checkout.html'
    # return the rendered template

    total_price = 0
    for item in items:
        total_price += item['price']
    
    # Save the below details to session using gieven reference for their source.
    # total_price from above calculation
    # address and pincode from form
    # redirect the rul to 'product.payment'
    if request.method == 'POST':
        session['total_price'] = total_price
        session['address'] = request.form['address']
        session['pincode'] = request.form['pincode']
        return redirect(url_for('product.payment'))
    
    return render_template('product/checkout.html', items=items, total_price=total_price)

