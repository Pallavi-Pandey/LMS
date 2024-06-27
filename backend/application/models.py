from datetime import timedelta
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import validates


db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'role_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

    @validates('user_id', 'role_id')
    def validate_user_role(self, key, value):
        if key == 'role_id':
            if value == 1:
                admin_count = RolesUsers.query.filter_by(role_id=1).count()
                if admin_count > 0:
                    raise ValueError("Only one user can be admin")
        return value

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    authenticated = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    last_login_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary="role_users", backref=db.backref('users', lazy='dynamic'))

    def get_id(self):
        return str(self.id)

    @property
    def is_authorised(self):
        return self.authenticated
    
    @property
    def get_user_role(self):
        return self.roles[0].name
    
    @property
    def books_requested(self):
        return BookRequest.query.filter_by(user_id=self.id, status='requested').count()

    @property
    def user_accessible_books(self):
        accessible_books = []
        BookRequest.query.filter_by(user_id=self.id).all()
        for book_request in BookRequest.query.filter_by(user_id=self.id).all():
            accessible_books.append(book_request.book_id)
        return accessible_books
    
    @property
    def monthly_report(self):
        # books activity this month
        books= BookRequest.query.filter_by(user_id=self.id).filter(BookRequest.requested_date > datetime.datetime.now() - timedelta(days=30)).all()
        data=[]
        # book={book_id, book_title, author, section_name, requested_date, status}
        for book in books:
            data.append({
                'book_id': book.book_id,
                'book_title': book.book_title,
                'author': book.author_name,
                'section_name': book.section_name,
                'requested_date': book.requested_date,
                'status': book.status
            })  
        return data

    
    
        
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    date_created= db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    description = db.Column(db.Text)

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
    full_content = db.Column(db.Text)
    image = db.Column(db.String(100))
    author= db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    @property
    def content(self):
        return self.full_content[:500]

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
    
    # add constraint that total books requested or approved by a user should not exceed 5

    @validates('status')
    def validate_status(self, key, status):
        if status not in ['requested', 'approved', 'rejected', 'revoke','returned','access-revoked']:
            raise ValueError("Invalid status value")
        return status
    
    @validates('user_id', 'book_id')
    def validate_user_book(self, key, value):
        if key == 'user_id':
            user_requests_count = BookRequest.query.filter_by(user_id=value).filter(BookRequest.status.in_(['requested', 'approved'])).count()
            if user_requests_count >= 5:
                raise ValueError("User has already requested/approved 5 books")
        return value


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

