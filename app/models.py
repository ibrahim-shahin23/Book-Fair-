import datetime
from . import db
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from app import login_manager

class ModelMixin:
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        

class Author(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False) 
    image = db.Column(db.String(100), nullable = False)
    books = db.relationship("Book", backref='author',lazy=True)

class Book(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  
    image = db.Column(db.String(100), nullable = False)
    publish_date = db.Column(db.Date, nullable=False) 
    added_to_site = db.Column(db.DateTime, default=datetime.datetime.now()) 
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)  
    price = db.Column(db.Float, nullable=False) 
    appropriate_for = db.Column(db.String(20), nullable=False)  

class User(db.Model, UserMixin, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)