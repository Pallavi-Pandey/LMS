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


    if not datastore.find_user(email="admin@email.com"):
        datastore.create_user(
           name="admin", email="admin@email.com", password=generate_password_hash("admin"), roles=["admin"])
   
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

    db.session.commit()
    print("Data seeding completed.")
