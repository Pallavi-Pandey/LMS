from app import app
from application.sec import datastore
from application.models import db, Role, Section, Book
from flask_security import hash_password
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="User is an Admin")
    datastore.find_or_create_role(name="stud", description="User is a Student")
    db.session.commit()


    if not datastore.find_user(email="admin@gmail.com"):
        datastore.create_user(
           name="admin", email="admin@gmail.com", password=generate_password_hash("admin"), roles=["admin"])
   
    # Create Sections and Books
    sections_data = [
        {"name": "Fiction", "description": "Imaginative storytelling."},
        {"name": "Science", "description": "Books about the natural world."},
        {"name": "History", "description": "Accounts of past events."},
        {"name": "Technology", "description": "Computers, AI, and engineering."},
        {"name": "Philosophy", "description": "Fundamental questions about existence."}
    ]

    for sec in sections_data:
        section = Section.query.filter_by(name=sec["name"]).first()
        if not section:
            section = Section(name=sec["name"], description=sec["description"])
            db.session.add(section)
            db.session.commit()
            print(f"Created Section: {section.name}")

            # Add 5 books per section
            for i in range(1, 6):
                book = Book(
                    section_id=section.id,
                    name=f"{sec['name']} Book {i}",
                    author=f"Author {i}",
                    full_content=f"This is the content for {sec['name']} Book {i}. It is a very interesting book.",
                    image="https://via.placeholder.com/150"
                )
                db.session.add(book)
                print(f"  Added Book: {book.name}")

    if not datastore.find_user(email="student@gmail.com"):
        datastore.create_user(
           name="student", email="student@gmail.com", password=generate_password_hash("student"), roles=["stud"])
        print("Created Student: student@gmail.com")

    # Add sample requests if student exists
    from application.models import BookRequest
    import datetime
    
    student = datastore.find_user(email="student@gmail.com")
    # Get some books
    books = Book.query.limit(3).all()
    
    if student and books and len(books) >= 3:
        # 1. Pending Request
        if not BookRequest.query.filter_by(user_id=student.id, book_id=books[0].id).first():
            req1 = BookRequest(
                user_id=student.id, 
                book_id=books[0].id, 
                status='requested',
                requested_date=datetime.datetime.now()
            )
            db.session.add(req1)
            print(f"  Created Request: {books[0].name} (Requested)")

        # 2. Approved (Borrowed)
        if not BookRequest.query.filter_by(user_id=student.id, book_id=books[1].id).first():
            req2 = BookRequest(
                user_id=student.id, 
                book_id=books[1].id, 
                status='approved',
                requested_date=datetime.datetime.now() - datetime.timedelta(days=2)
            )
            db.session.add(req2)
            print(f"  Created Request: {books[1].name} (Approved)")

        # 3. Returned
        if not BookRequest.query.filter_by(user_id=student.id, book_id=books[2].id).first():
            req3 = BookRequest(
                user_id=student.id, 
                book_id=books[2].id, 
                status='returned',
                requested_date=datetime.datetime.now() - datetime.timedelta(days=10),
                return_date=datetime.datetime.now() - datetime.timedelta(days=1)
            )
            db.session.add(req3)
            print(f"  Created Request: {books[2].name} (Returned)")

    db.session.commit()
    print("Data seeding completed.")
