import datetime
from database import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False) 
    image = db.Column(db.String(100), nullable = False)
    books = db.relationship("Book", backref='author',lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  
    image = db.Column(db.String(100), nullable = False)
    publish_date = db.Column(db.Date, nullable=False) 
    add_to_site_at = db.Column(db.DateTime, default=datetime.datetime.now()) 
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)  
    price = db.Column(db.Float, nullable=False) 
    appropriate_for = db.Column(db.String(20), nullable=False)  