import click
from flask.cli import with_appcontext
import sqlite3
import os

DATABASE = os.path.join(os.getcwd(), 'database.db')  # change as needed

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Example table — adjust as needed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('✅ Database initialized.')

app.cli.add_command(init_db_command)
