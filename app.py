import datetime
from flask import Flask, jsonify, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
import json
from database import db
from models import Book, Author
from forms import BookForm ,AuthorForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd2b0873fb7c652daa2ccc52b5b479edd'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project1.db"
Bootstrap(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/',endpoint="home",methods=['GET'])
def all_books():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/authors',endpoint="authors",methods=['GET'])
def all_authors():
    authors = Author.query.all()
    return render_template('authors.html', authors=authors)

@app.route('/author/<int:id>',endpoint="author_details",methods=['GET'])
def author_details(id):
    author = Author.query.get(id)
    return render_template('author_details.html', author=author)

@app.route('/<int:id>',endpoint="book_details")
def book_details(id):
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)
    return render_template('book_details.html',book=book , author=author)

@app.route('/add_author', endpoint="add_author", methods=['GET','POST'])
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name = form.name.data, birth_date = form.birth_date.data, image = form.image.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('authors'))
    return render_template('add_author_book.html', form=form ,form_title="Add Author form")

@app.route('/add_book',endpoint="add_book", methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    authors = Author.query.all()
    form.author_id.choices = [(author.id, author.name) for author in authors]  # Populate the dropdown

    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            image=form.image.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            appropriate_for=form.appropriate_for.data,
            author_id=form.author_id.data
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))  # Redirect to the homepage or another route
    return render_template('add_author_book.html', form=form , form_title="Add book form")