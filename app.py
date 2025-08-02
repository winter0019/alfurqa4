from flask import Flask
import sqlite3
import os
import click
from flask.cli import with_appcontext

app = Flask(__name__)

# Define your DB path
DATABASE = os.path.join(os.getcwd(), 'database.db')

# Your init_db logic
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# CLI command
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('✅ Database initialized.')

# Register the command
app.cli.add_command(init_db_command)
