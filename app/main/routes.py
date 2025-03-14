from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.models import Author, Book
from forms import AuthorForm, BookForm

main_blueprint = Blueprint('main', __name__, url_prefix='/')

@main_blueprint.route('',endpoint="home",methods=['GET'])
@login_required
def all_books():
    books = Book.query.all()
    return render_template('main/index.html', books=books)

@main_blueprint.route('/authors',endpoint="authors",methods=['GET'])
@login_required
def all_authors():
    authors = Author.query.all()
    return render_template('main/authors.html', authors=authors)

@main_blueprint.route('/author/<int:id>',endpoint="author_details",methods=['GET'])
@login_required
def author_details(id):
    author = Author.query.get(id)
    return render_template('main/author_details.html', author=author)

@main_blueprint.route('/<int:id>',endpoint="book_details")
@login_required
def book_details(id):
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)
    return render_template('main/book_details.html',book=book , author=author)

@main_blueprint.route('/add_author', endpoint="add_author", methods=['GET','POST'])
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        new_author = Author(name = form.name.data, birth_date = form.birth_date.data, image = form.image.data)
        new_author.save_to_db()
        flash(f"{new_author.name} added successfully")
        return redirect(url_for('main.authors'))
    return render_template('form.html', form=form ,form_title="Add Author form")

@main_blueprint.route('/add_book',endpoint="add_book", methods=['GET', 'POST'])
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
        new_book.save_to_db()
        flash(f"{new_book.title} added successfully")
        return redirect(url_for('main.home'))  # Redirect to the homepage or another route
    return render_template('form.html', form=form , form_title="Add book form")

@main_blueprint.route('/edit_book/<int:id>',endpoint="edit_book", methods=['GET', 'POST'])
def edit_book(id):
    form = BookForm()
    authors = Author.query.all()
    form.author_id.choices = [(author.id, author.name) for author in authors]
    book = Book.query.get(id)
    if form.validate_on_submit():
        book.title = form.title.data
        book.image = form.image.data
        book.publish_date = form.publish_date.data
        book.price = form.price.data
        book.appropriate_for = form.appropriate_for.data
        book.author_id = form.author_id.data
        book.save_to_db()
        flash(f"{book.title} updated successfully")
        return redirect(url_for('main.home'))
    form.title.data = book.title
    form.price.data = book.price
    form.appropriate_for.data = book.appropriate_for
    form.author_id.data = book.author
    form.image.data = book.image
    form.publish_date.data = book.publish_date
    return render_template('form.html', form=form , form_title="Edit book form")

@main_blueprint.route('/delete_book/<int:id>',endpoint="delete_book", methods=['GET', 'POST'])
def delete_book(id):
    # form = BookDeleteForm()
    book = Book.query.get(id)
    book.delete_from_db()
    flash(f"{book.title} deleted successfully")
    return redirect(url_for('main.home'))
    # if form.validate_on_submit():
    #     return redirect(url_for('main.home'))
    # return render_template('form.html', form_title=f"Are you sure you want to delete {book.title} ?", form=form)
