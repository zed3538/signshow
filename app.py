from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
from livereload import Server
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
            'img_src': 'images/icon_photovideo.png',
            'img_alt': 'Use of photos and videos to help you visualise sign language gestures',
            'title': 'Clear visuals',
            'summary': 'Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.',
        },
        {
            'img_src': 'images/icon_photovideo.png',
            'img_alt': 'smiley face',
            'title': 'ABC',
            'summary': 'Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.',
        },
        {
            'img_src': 'images/icon_photovideo.png',
            'img_alt': 'smiley face',
            'title': 'ABC',
            'summary': 'Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.',
        }
    ]
    return pages

def get_lessons():
    lessons = [
        {
            'title': 'Lesson 1',
            'terms': '',
        }
    ]
    return lessons

@app.route('/')
def index():
    pages = get_pages()
    return render_template("index.html", pages=pages)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE username = ?"
        global user
        user =  query_db(sql=sql,args=(username,),one=True)
        if user:
            if check_password_hash(user[2],password):
                session['user'] = user
                flash("Logged in successfully!")
                redirect('/learn')
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
        return redirect('/learn')
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')

@app.route('/learn')
def learn():
    terms = query_db("SELECT * FROM terms")
    return render_template("learn.html", terms=terms)

@app.route('/learn/<int:id>')
def termLearn(id):
    sql = f"SELECT * FROM terms WHERE id={id}"
    terms = query_db(sql, one=True)
    return render_template ("term.html", terms=terms)

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")

if __name__ == "__main__":
    app.run(debug=True)
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/")
    server.watch("static/")
    server.serve()