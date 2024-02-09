# Create a Flask blueprint named 'product' for managing product-related routes and views. The blueprint should include the following components:
# Import necessary modules and functions from Flask and related libraries:
# Import 'Blueprint', 'flash', 'g', 'redirect', 'render_template', 'request', and 'url_for' from Flask.
# Import 'abort' from 'werkzeug.exceptions' for handling HTTP errors.
# Import the 'login_required' decorator from the 'flaskr.auth' module for protecting routes that require authentication.
# Import the 'get_db' function from the 'flaskr.db' module to interact with the database.
# Define the blueprint named 'product' using the 'Blueprint' class provided by Flask.
# Ensure that this blueprint can be imported and registered with a Flask application for managing product-related routes and views.

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
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
    

    if request.method == 'POST':
        pass
    return render_template('product/checkout.html', items=items, total_price=total_price)

