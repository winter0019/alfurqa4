import sqlite3
import click
from flask import Flask, g

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'  # or your preferred DB path

# --- Database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- CLI command to initialize the database
@app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())
    click.echo("✅ Initialized the database.")
