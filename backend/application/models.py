from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'role_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    authenticated = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary="role_users", backref=db.backref('users', lazy='dynamic'))

    def get_id(self):
        return str(self.id)

    @property
    def is_authorised(self):
        return self.authenticated
    
    @property
    def get_user_role(self):
        return self.roles[0].name

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    books= db.relationship('Book', backref=db.backref('section', lazy=True))
    is_deleted = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            "books": [book.serialize() for book in self.books]
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    image = db.Column(db.String(100))
    author= db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'section_id': self.section_id,
            'content': self.content,
            'image': self.image
        }
    
    def status(self,user_id):
        book_request = BookRequest.query.filter_by(book_id=self.id,user_id=user_id).first()
        if book_request:
            return book_request.status
        return "available"
    
    def requested_date(self,user_id):
        book_request = BookRequest.query.filter_by(book_id=self.id,user_id=user_id).first()
        if book_request:
            return book_request.requested_date
        return None
        

class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    requested_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(100), nullable=False)# pending, approved, rejected //revoke
    return_date = db.Column(db.TIMESTAMP)

    @property
    def book_title(self):
        return Book.query.get(self.book_id).name
    
    @property
    def user_name(self):
        return User.query.get(self.user_id).name
    
    @property
    def author_name(self):
        return Book.query.get(self.book_id).author
    
    @property
    def section_name(self):
        return Section.query.get(Book.query.get(self.book_id).section_id).name
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'requested_date': self.requested_date,
            'status': self.status,
            'return_date': self.return_date,
            'book_title': self.book_title,
            'user_name': self.user_name,
            'author_name': self.author_name,
            'section_name': self.section_name
        }


class BookAccessHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookrequest_id = db.Column(db.Integer, db.ForeignKey('book_request.id'), nullable=False)
    from_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    to_date = db.Column(db.TIMESTAMP)# 7 days 14 days, etc..

class BookRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)

