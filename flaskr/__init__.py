# Create a Flask application named 'app' with the following characteristics:
# 1) The application should be created with instance-relative configuration enabled.
# 2) Set the 'SECRET_KEY' configuration to 'dev'.
# 3) Configure the application to use 'flaskr.sqlite' as the database located in the 'instance' folder.
# Load the instance configuration from 'config.py' if it exists, silently ignoring if not found.
# Define a route '/hello' that returns 'Hello, World!' when accessed.
# Return the Flask application instance."
from flask import Flask
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    # Import product and register the blueprint from the factory using app.register_blueprint().
    from . import product
    app.register_blueprint(product.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app


