from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # index here
    pass

if __name__ == "__main__":
    app.run(debug=True);