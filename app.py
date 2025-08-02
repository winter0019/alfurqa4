import sqlite3
import click
from flask import Flask, g

print("App.py is being loaded!")  # Add this line

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

# ... rest of your code
