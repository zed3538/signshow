from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
from livereload import server
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "SuperSecretKey"

database = 'database.db'

def query_db(sql,args=(),one=False):
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results

## routes and stuff

def get_pages():
    pages = [
        {
            'img_src': 'images/smiley.jpg',
            'img_alt': 'smiley face',
            'title': 'ABC',
            'summary': 'abcdefg',
        },
        {
            'img_src': 'images/smiley.jpg',
            'img_alt': 'smiley face',
            'title': 'ABC',
            'summary': 'abcdefg',
        },
        {
            'img_src': 'images/smiley.jpg',
            'img_alt': 'smiley face',
            'title': 'ABC',
            'summary': 'abcdefg',
        }
    ]
    return pages

@app.route('/')
def index():
    pages = get_pages()
    return render_template("index.html", pages=pages)

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE username = ?"
        user =  query_db(sql=sql,args=(username,),one=True)
        if user:
            if check_password_hash(user[2],password):
                session['user'] = user
                flash("Logged in successfully!")
            else:
                flash("Password incorrect.")
        else:
            flash("User does not exist.")
    return render_template('login.html')

@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        sql = "INSERT or IGNORE INTO user (username,password) VALUES (?,?)"
        query_db(sql,(username,hashed_password))
        flash("Sign Up Successful!")
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')

@app.route('/learn')
def learn():
    session['user'] = user
    return render_template("learn.html")

if __name__ == "__main__":
    app.run(debug=True);