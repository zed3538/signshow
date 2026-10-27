from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
from livereload import Server
from werkzeug.security import generate_password_hash, check_password_hash
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = "SuperSecretKey"

database = 'database.db'

# Function allows interaction with the database. 
def query_db(sql,args=(),one=False):
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute(sql, args)
    results = cursor.fetchall()
    db.commit()
    db.close()
    return (results[0] if results else None) if one else results

# Routes
# A dictionary to populate the cards on the main landing page.
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

# Main page. It calls the get_pages dictionary to populate the cards.
@app.route('/')
def index():
    pages = get_pages()
    return render_template("index.html", pages=pages)

# About page.
@app.route('/about')
def about():
    return render_template("about.html")

# Login page. Uses a form for the user to submit, then checks against the database to verify if the username and password match. If only the user exists in the database, 
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
                flash("Password incorrect.", "error")
        else:
            flash("User does not exist.")
    return render_template('login.html')

# Signup page. A form is used for the user to submit their username and password. The password is hashed for the user's security before being inserted into the database.
@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        sql = "INSERT or IGNORE INTO user (username,password) VALUES (?,?)"
        user = query_db(sql,(username,hashed_password))
        ## come back to this later to make error when user is invalid (symbols)
        session['user'] = user
        flash("Sign up successful!")
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')

# Learn page. It first checks if the user is logged in. If not, they are redirected to the login page. Otherwise, it shows all the learning terms and questions for the user to choose from.
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

@app.route('/learn/<int:id>')
def termLearn(id):
    sql = f"SELECT * FROM terms WHERE id={id}"
    terms = query_db(sql, one=True)
    return render_template("term.html", terms=terms)

@app.route('/learn/quiz-<int:id>')
def quiz(id):
    sql = f"SELECT * FROM terms WHERE id={id}"
    quiz = query_db(sql, one=True)

    term_ids = []
    option_terms = []
    term_ids.append(id)

    # Loops generating an id and checking that it is not a duplicate word until there are 4 unique options.
    max_terms = query_db(f"SELECT COUNT(term) FROM terms", one=True)
    max_terms = max_terms[0]

    while len(term_ids) < 4:
        term_id = random.randint(1, (max_terms))
        while term_id in term_ids:
            term_id = random.randint(1, (max_terms))
        term_ids.append(term_id)
    
    # Grabs the associated terms from the database according to the ids then puts it into a separate list.
    for term_id in term_ids:
        grabbed_term = query_db(f"SELECT term FROM terms WHERE id={term_id}", one=True)
        grabbed_term = grabbed_term[0]
        option_terms.append(grabbed_term)

    random.shuffle(option_terms)

    session['currentQuestion'] = id

    return render_template("quiz.html", quiz=quiz, options=option_terms, option=quiz[1], id=id)

# New question route is not presented as a page but is a "helper" of sorts to redirect the user after they interact with the buttons.
@app.route('/learn/new-question')
def newQuestion():
    # This block runs the first time the user goes on this route and makes a list of ids
    if not session.get('question_ids', None):
        session['question_ids'] = []
        grabbed_ids = query_db(f"SELECT id FROM terms WHERE NOT id={1}", one=True)
        session['question_ids'].append(grabbed_ids)
        id = grabbed_ids[0]
        session['currentQuestion'] = id
        return redirect(f'/learn/quiz-{id}')
    # This block runs the next time the user is on this route and 
    else:
        session.get('currentQuestion', None)
        session['currentQuestion'] = session['currentQuestion']+1
        id = session['currentQuestion']
        return redirect(f'/learn/quiz-{id}')
    # sql = "SELECT * FROM terms"
    # quiz = query_db(sql, one=True)
    # # "SELECT user.id, terms.id FROM users INNER JOIN terms ON progress.user_id"
    # # term_status = query_db(sql, one=True)

    # question_ids = []
    # current_question = 1
    # # This runs the first time that newQuestion is called and makes a list of 10 questions for the user to be redirected to later.
    # if not session.get(question_ids, None):
    #     grabbed_id = query_db(f"SELECT id FROM terms WHERE NOT id={1}")
    #     question_ids.append(grabbed_id)
    #     print(question_ids)
    #     id = question_ids[0]
    #     print(id)
    #     return redirect(f'/learn/quiz-{id}+1')
    # else:
    #     session.get(current_question, None)
    #     current_question = current_question + 1
    #     session.get(question_ids, None)
    #     print(question_ids)
    #     redirect(f'/learn/quiz-{id}')
    return render_template("quiz.html", quiz=quiz)

# Livereload to allow automatic website refresh when saving files.
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