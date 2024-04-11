from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash
from flask_security import auth_required, roles_required, current_user

from flask_restful import marshal, fields
import flask_excel as excel
from celery.result import AsyncResult
from .tasks import create_resource_csv
from .models import Book, Section, User, db,BookRequest,BookAccessHistory,BookRating
from werkzeug.security import generate_password_hash
from .resources import section_marshal,book_marshal

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

#-----------------------------------------------------------------------For Librarian------------------------------------------------------------------------------------------
#to add book
@app.route('/add-book', methods=['POST'])
@auth_required("token")
@roles_required("admin")
def add_book():
    book_data = request.json
    print(book_data,"aaaa")
    if 'name' not in book_data or 'content' not in book_data or 'author' not in book_data or 'section_id' not in book_data or 'image' not in book_data:
        return jsonify({'error': 'Missing required fields'}), 400
    new_book = Book(name=book_data['name'], content=book_data['content'], author=book_data['author'],section_id=book_data['section_id'], image=book_data['image'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

#to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.filter_by(is_deleted=False).all()
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
    if 'author' in book_data:
        book.author = book_data['author']
    if 'image' in book_data:
        book.image = book_data['image']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

#to delete book by id
@app.route('/book/<int:id>', methods=['DELETE'])
@auth_required("token")
@roles_required("admin")
def delete_book(id):
    book = Book.query.get(id)
    if book:
        book.is_deleted = True
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
@auth_required("token")
def get_sections():
    sections = Section.query.filter_by(is_deleted=False).all()
    serialized_sections = []
    for section in sections:
        section_data = marshal(section, section_marshal)
        section_data['books'] = []
        for book in section.books and book.is_deleted==False:
            book_data = marshal(book, book_marshal)
            # Call the status method to get the status
            book_data['status'] = book.status(current_user.id)
            book_data['requested_date'] = book.requested_date(current_user.id)
            print(book.status,"status")
            section_data['books'].append(book_data)
        serialized_sections.append(section_data)
    print(serialized_sections)
    print("a2222222222222222222")

    return jsonify(serialized_sections)



#to get section by id
@app.route('/section/<int:id>', methods=['GET'])
def get_section(id):
    section = Section.query.get(id)
    if section:
         return marshal(section, section_marshal)
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
@app.route('/delete-section/<int:id>', methods=['DELETE'])
@auth_required("token")
@roles_required("admin")
def delete_section(id):
    section = Section.query.get(id)
    if section:
        section.is_deleted = True
        db.session.commit()
        return jsonify({'message': 'Section deleted successfully'})
    return jsonify({'error': 'Section not found'}), 404


# rent a book
@app.route('/rent-book', methods=['POST'])
@auth_required("token")
@roles_required("stud")
def rent_book():
    data = request.json
    book_id = data.get('book_id')
    user_id = current_user.id
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    book_request = BookRequest(book_id=book_id, user_id=user_id,status='requested',requested_date=db.func.current_timestamp())
    db.session.add(book_request)
    db.session.commit()
    
    return jsonify({'message': 'Book renting requested successfully'}), 201

# return a book
@app.route('/revoke-book', methods=['POST'])
@auth_required("token")
@roles_required("stud")
def revoke_book():
    data = request.json
    book_id = data.get('book_id')
    user_id = current_user.id
    book_request = BookRequest.query.filter_by(book_id=book_id, user_id=user_id).first()
    if not book_request:
        return jsonify({'error': 'Book request not found'}), 404

    # remove the book request
    db.session.delete(book_request)
    db.session.commit()
    return jsonify({'message': 'Book renting revoked successfully'})

# get all book requests
@app.route('/requests', methods=['GET'])
@auth_required("token")
@roles_required("admin")
def get_requests():
    requests = BookRequest.query.all()
    return jsonify([request.serialize() for request in requests])

@app.route('/approve-request/<int:request_id>', methods=['PUT'])
@auth_required("token")
@roles_required("admin")
def approve_request(request_id):
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({'error': 'Request not found'}), 404
    request.status = 'approved'
    db.session.commit()
    return jsonify({'message': 'Request approved successfully'})

@app.route('/reject-request/<int:request_id>', methods=['PUT'])
@auth_required("token")
@roles_required("admin")
def reject_request(request_id):
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({'error': 'Request not found'}), 404
    request.status = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Request rejected successfully'})

@app.route("/my-books", methods=['GET'])
@auth_required("token")
@roles_required("stud")
def my_books():
    books = BookRequest.query.filter_by(user_id=current_user.id).all()
    return jsonify([book.serialize() for book in books])


@app.route("/return-book", methods=['POST'])
@auth_required("token")
@roles_required("stud")
def return_book():
    data = request.json
    book_id = data.get('book_id')
    user_id = current_user.id
    book_request = BookRequest.query.filter_by(book_id=book_id, user_id=user_id).first()
    if not book_request:
        return jsonify({'error': 'Book request not found'}), 404

    book_request.status = 'returned'
    db.session.commit()
    return jsonify({'message': 'Book returned successfully'})