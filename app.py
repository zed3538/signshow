from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
from livereload import Server
from werkzeug.security import generate_password_hash, check_password_hash
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "SuperSecretKey"

database = 'database.db'

global user

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
            'summary': 'SignShow has clear visuals that demonstrate signs so they are easy to understand and imitate. The official NZSL website uses the same visuals.',
        },
        {
            'img_src': 'images/icon_photovideo.png',
            'img_alt': 'smiley face',
            'title': 'Repetitive testing',
            'summary': 'SignShow has a quiz section for every group of words you learn! You get to test yourself iteratively and you can see your progress towards learning a certain word.',
        },
        {
            'img_src': 'images/icon_photovideo.png',
            'img_alt': 'smiley face',
            'title': 'Simple and easy to use',
            'summary': 'It is straightforward and easy to use.'
        }
    ]
    return pages

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
        user =  query_db(sql=sql,args=(username,),one=True)
        if user:
            if check_password_hash(user[2],password):
                session['user'] = user
                return redirect("/learn")
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
        ## come back to this later to make error when duplicate user
        session['user'] = user
        flash("Sign up successful!")
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')

@app.route('/learn')
def learn():
    if not session.get('user', None):
        flash("Please log in to access!")
        return redirect('/login')
    else:
        terms = query_db("SELECT * FROM terms")
        quiz = query_db("SELECT * FROM quiz")
        terms2 = query_db("SELECT term FROM terms WHERE id > 10")
        return render_template("learn.html", terms=terms, quiz=quiz, terms2=terms2, id=id)

# random shuffle
# need list of ids of previously seen questions
@app.route('/learn/<int:id>')
def termLearn(id):
    sql = f"SELECT * FROM terms WHERE id={id}"
    terms = query_db(sql, one=True)
    return render_template("term.html", terms=terms)

@app.route('/learn/quiz-<int:id>', methods=["GET","POST"])
def quiz(id):
    sql = f"SELECT * FROM quiz WHERE id={id}"
    quiz = query_db(sql, one=True)
    questions = query_db(sql, one=True)
    answer = request.form

    # checks if the submitted answer matches the correct term in the database
    if answer == quiz[7]:
        flash("Correct!")
        sql = "INSERT OR IGNORE INTO progress (status) VALUES ('learned')"
    else:
        flash("Incorrect.")
        sql = "INSERT OR IGNORE INTO progress (status) VALUES ('not learned')"
        print(answer)
        # sql = "SELECT farm.*, farmType.type FROM farms LEFT JOIN farmType ON farms.farmtype = farmType.id" *** reference this
    status = query_db(sql, one=True)
    # redirects to next question regardless of answer
    redirect(f"/learn/quiz-{id+1}")

    return render_template("quiz.html", questions=questions, quiz=quiz, status=status, answer=answer)

@app.route("/correct/", methods=["GET","POST"])
def correct(id):
    ans_correct = "correct!! yay"
    quiz = query_db(f"SELECT * FROM quiz WHERE id={id}")
    questions = query_db(f"SELECT question, media FROM quiz WHERE id={id}")
    join = query_db("SELECT progress.*, user.id FROM progress LEFT JOIN user ON progress.user_id = user.id")

    return render_template("quiz.html", ans_correct=ans_correct, quiz=quiz, questions=questions, join=join)

## Livereload to allow automatic website refresh when saving files
if __name__ == "__main__":
    app.run(debug=True)
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/")
    server.watch("static/")
    server.serve(
        port=5000,
        debug=True
    )