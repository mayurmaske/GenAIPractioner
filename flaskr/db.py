# Create a Python module that interacts with an SQLite database within a Flask application. The module should include the following functions:

# Define a function named 'get_db' to obtain a connection to the SQLite database. Check if the database connection exists in the 'g' object, which represents the global context for the Flask application.
# If the connection does not exist then establish a connection to the database specified in the Flask application's configuration. Then set the connection's row factory to 'sqlite3.Row' to access rows as dictionaries.
# Return the database connection.

# Define a function named 'close_db' to close the database connection. Retrieve the database connection from the 'g' object. If the connection exists:
# Close the database connection.

# Import the necessary libraries
import sqlite3

from flask import g


def get_db():
    """
    Get a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection to the SQLite database.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            'database.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db
    

def close_db(e=None):
    """
    Close the SQLite database connection.

    Args:
        e (Exception, optional): The exception that triggered the close. Defaults to None.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


# create the function named init_db() to initialize the database.
# Within that function open a connection to the database
# Open 'schema.sql' file using open_resource feature of current_app
# Execute the SQL commands from the file. Decode the details before executing.
      
from flask import current_app
from flask import g


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# create the function named 'init_db_command()'
# Add 'click' decorator with command including input as 'init-db'
# within that function call the init_db() function.
# and send output to console "Initialized the database." using Click.echo

from flask import current_app
from flask import g
import click

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# Create a function named 'init_app' that configures a Flask application instance. 
# This function should accept a single parameter named 'app', which represents the Flask application instance. Within the 'init_app' function:
    
def init_app(app):
    """
    Initialize the Flask application instance.

    Args:
        app (flask.Flask): The Flask application instance.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    