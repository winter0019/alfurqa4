import sqlite3
from flask import Flask, g

app = Flask(__name__)
app.config.from_mapping(
    DATABASE="database.db"  # Adjust if your DB file has another name
)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())

import click

@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('✅ Initialized the database.')
