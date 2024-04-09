from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash
from flask_security import auth_required, roles_required, current_user

from flask_restful import marshal, fields
import flask_excel as excel
from celery.result import AsyncResult
from .tasks import create_resource_csv
from .models import Book, Section, User, db
from werkzeug.security import generate_password_hash

from .sec import datastore


@app.get('/')
def home():
    return {"hello":"world"}

@app.post("/register")
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    password=generate_password_hash(password)
    name= data.get('name')
    if not email:
        return jsonify({"message": "email not provided"}), 400
    if not password:
        return jsonify({"message": "password not provided"}), 400
    if not name:
        return jsonify({"message": "name not provided"}), 400
    if datastore.find_user(email=email):
        return jsonify({"message": "User Already Exists"}), 400
    user = datastore.create_user(name=name, email=email, password=password, roles=["stud"])
    db.session.commit()
    
    return jsonify({"message": "User Created"}), 201


def get_user_roles(roles):
    return [role.name for role in roles]

@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": get_user_roles(user.roles)})
    else:
        return jsonify({"message": "Wrong Password"}), 400
    
@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def admin():
    return "Hello Admin"

@app.get('/stud')
@auth_required("token")
@roles_required("stud")
def stud():
    print(current_user.email)
    return "Hello "+current_user.email

#for librarian-dashboard to add book
@app.route('/add-book', methods=['POST'])
@auth_required("token")
@roles_required("admin")
def add_book():
    book_data = request.json
    if 'name' not in book_data or 'content' not in book_data or 'author_id' not in book_data:
        return jsonify({'error': 'Missing required fields'}), 400
    new_book = Book(name=book_data['name'], content=book_data['content'], author_id=book_data['author_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

#to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

#to get book by id
@app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if book:
        return jsonify(book.serialize())
    return jsonify({'error': 'Book not found'}), 404

#to update book by id
@app.route('/book/<int:id>', methods=['PUT'])
@auth_required("token")
@roles_required("admin")
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    book_data = request.json
    if 'name' in book_data:
        book.name = book_data['name']
    if 'content' in book_data:
        book.content = book_data['content']
    if 'author_id' in book_data:
        book.author_id = book_data['author_id']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

#to delete book by id
@app.route('/book/<int:id>', methods=['DELETE'])
@auth_required("token")
@roles_required("admin")
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'error': 'Book not found'}), 404

#to add section
@app.route('/add-section', methods=['POST'])
@auth_required("token")
@roles_required("admin")
def add_section():
    section_data = request.json
    if 'name' not in section_data:
        return jsonify({'error': 'Missing required fields'}), 400
    new_section = Section(name=section_data['name'])
    db.session.add(new_section)
    db.session.commit()
    return jsonify({'message': 'Section added successfully'}), 201

#to get all sections
@app.route('/sections', methods=['GET'])
def get_sections():
    sections = Section.query.all()
    return jsonify([section.serialize() for section in sections])

#to get section by id
@app.route('/section/<int:id>', methods=['GET'])
def get_section(id):
    section = Section.query.get(id)
    if section:
        return jsonify(section.serialize())
    return jsonify({'error': 'Section not found'}), 404

#to update section by id
@app.route('/section/<int:id>', methods=['PUT'])
@auth_required("token")
@roles_required("admin")
def update_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    section_data = request.json
    if 'name' in section_data:
        section.name = section_data['name']
    db.session.commit()
    return jsonify({'message': 'Section updated successfully'})

#to delete section by id
@app.route('/section/<int:id>', methods=['DELETE'])
@auth_required("token")
@roles_required("admin")
def delete_section(id):
    section = Section.query.get(id)
    if section:
        db.session.delete(section)
        db.session.commit()
        return jsonify({'message': 'Section deleted successfully'})
    return jsonify({'error': 'Section not found'}), 404

