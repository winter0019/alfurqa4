# main.py

import os
import sqlite3
from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
bcrypt = Bcrypt()
csrf = CSRFProtect()

def get_db():
    """Connects to the SQLite database, stores in `g`."""
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Closes the database connection on teardown."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database with schema.sql."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def create_app(test_config=None):
    """Flask application factory pattern."""
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.path.join(app.instance_path, "alfurqa_academy.db"),
        WTF_CSRF_ENABLED=True
    )

    # Override with testing config if provided
    if test_config:
        app.config.from_mapping(test_config)
    else:
        # Load instance config if available
        app.config.from_pyfile("config.py", silent=True)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Register database teardown
    app.teardown_appcontext(close_db)

    # Initialize extensions
    bcrypt.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
