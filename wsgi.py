import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV') or 'development')

# create_app()
# app = Flask(__name__)
# load_dotenv()
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','my_secret_key')
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI','sqlite:///project.db')
# Bootstrap(app)
# db.init_app(app)
# from models import Book, Author, User
# Migrate(app, db)
'''''''''
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
    '''''''''