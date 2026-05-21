from flask import Flask, render_template
from livereload import server

app = Flask(__name__)

def get_pages():
    pages = [
        {
            'link_href': 'abcdef',
            'img_src': 'images/smiley.jpg',
            'img_alt': 'smiley face',
            'title': 'ABC',
            'summary': 'abcdefg',
        },
        {
            'link_href': 'abcdef',
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

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True);