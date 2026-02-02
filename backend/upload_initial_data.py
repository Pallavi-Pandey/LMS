from app import app
from application.sec import datastore
from application.models import db, Role, Section, Book, BookRequest
from flask_security import hash_password
from werkzeug.security import generate_password_hash
import datetime

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="User is an Admin")
    datastore.find_or_create_role(name="stud", description="User is a Student")
    db.session.commit()


    if not datastore.find_user(email="admin@gmail.com"):
        datastore.create_user(
           name="admin", email="admin@gmail.com", password=generate_password_hash("admin"), roles=["admin"])
    
    realistic_data = {
        "Fiction": [
            {
                "name": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A novel set in the Roaring Twenties that examines the American Dream.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg"
            },
            {
                "name": "1984",
                "author": "George Orwell",
                "description": "A dystopian social science fiction novel and cautionary tale about future.",
                "image": "https://upload.wikimedia.org/wikipedia/en/5/51/1984_first_edition_cover.jpg"
            },
            {
                "name": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "description": "A novel about the serious issues of rape and racial inequality.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg"
            },
            {
                "name": "Pride and Prejudice",
                "author": "Jane Austen",
                "description": "A romantic novel of manners written by Jane Austen in 1813.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/1/17/PrideAndPrejudiceTitlePage.jpg"
            },
            {
                "name": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "description": "A story about teenage angst and alienation.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/8/89/The_Catcher_in_the_Rye_%281951%2C_first_edition_cover%29.jpg"
            }
        ],
        "Science": [
            {
                "name": "A Brief History of Time",
                "author": "Stephen Hawking",
                "description": "A book on cosmology that explains complex concepts to non-specialists.",
                "image": "https://upload.wikimedia.org/wikipedia/en/a/a3/BriefHistoryTime.jpg"
            },
            {
                "name": "The Selfish Gene",
                "author": "Richard Dawkins",
                "description": "A book on evolution that introduces the concept of the meme.",
                "image": "https://upload.wikimedia.org/wikipedia/en/f/fc/TheSelfishGene.jpg"
            },
            {
                "name": "Cosmos",
                "author": "Carl Sagan",
                "description": "A popular science book exploring the universe and our place in it.",
                "image": "https://upload.wikimedia.org/wikipedia/en/archive/7/7b/20210603001851%21Cosmos-1stEd.jpg"
            },
            {
                "name": "Silent Spring",
                "author": "Rachel Carson",
                "description": "Highlighed the dangers of pesticide use and kickstarted the environmental movement.",
                "image": "https://upload.wikimedia.org/wikipedia/en/5/5f/SilentSpring.jpg"
            }
        ],
        "History": [
            {
                "name": "Sapiens",
                "author": "Yuval Noah Harari",
                "description": "A brief history of humankind from the Stone Age to the twenty-first century.",
                "image": "https://upload.wikimedia.org/wikipedia/en/0/06/%E1%B8%B2itsur_toldot_ha-enoshut.jpg"
            },
            {
                "name": "Guns, Germs, and Steel",
                "author": "Jared Diamond",
                "description": "A transdisciplinary non-fiction book explaining why Eurasian civilizations survived and conquered others.",
                "image": "https://upload.wikimedia.org/wikipedia/en/0/01/GunsGermsAndSteel.jpg"
            },
            {
                "name": "The Diary of a Young Girl",
                "author": "Anne Frank",
                "description": "The writings from the Dutch-language diary kept by Anne Frank while she was in hiding.",
                "image": "https://upload.wikimedia.org/wikipedia/en/4/46/Diary_of_a_Young_Girl.jpg"
            }
        ],
        "Technology": [
            {
                "name": "The Pragmatic Programmer",
                "author": "Andrew Hunt",
                "description": "A guide to software engineering best practices.",
                "image": "https://upload.wikimedia.org/wikipedia/en/8/8f/The_pragmatic_programmer.jpg"
            },
            {
                "name": "Clean Code",
                "author": "Robert C. Martin",
                "description": "A handbook of agile software craftsmanship.",
                "image": "https://images-na.ssl-images-amazon.com/images/I/41jEbK-jG+L._SX258_BO1,204,203,200_.jpg"
            },
            {
                "name": "Design Patterns",
                "author": "Erich Gamma et al.",
                "description": "Elements of Reusable Object-Oriented Software.",
                "image": "https://upload.wikimedia.org/wikipedia/en/9/95/Design_Patterns_-_Elements_of_Reusable_Object-Oriented_Software.jpg"
            },
            {
                "name": "Introduction to Algorithms",
                "author": "Thomas H. Cormen",
                "description": "A comprehensive textbook on algorithms.",
                "image": "https://upload.wikimedia.org/wikipedia/en/4/41/Clrs3.jpeg"
            }
        ],
        "Philosophy": [
            {
                "name": "The Republic",
                "author": "Plato",
                "description": "A Socratic dialogue concerning justice and the order and character of the just city-state.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Plato_Republic.jpg/300px-Plato_Republic.jpg"
            },
            {
                "name": "Meditations",
                "author": "Marcus Aurelius",
                "description": "A series of personal writings by Marcus Aurelius recording his private notes to himself.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Marc_Aur%C3%A8le_-_Pens%C3%A9es_pour_moi-m%C3%AAme_-_Manuscrit_Vaticanus_Graecus_1950.jpg"
            }
        ],
        "Horror": [
            {
                "name": "It",
                "author": "Stephen King",
                "description": "The story follows the experiences of seven children as they are terrorized by an evil entity.",
                "image": "https://upload.wikimedia.org/wikipedia/en/5/5a/It_cover.jpg"
            },
            {
                "name": "Dracula",
                "author": "Bram Stoker",
                "description": "The novel tells the story of Dracula's attempt to move from Transylvania to England.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Dracula_1st_ed_cover_repro.jpg/330px-Dracula_1st_ed_cover_repro.jpg"
            },
            {
                "name": "Frankenstein",
                "author": "Mary Shelley",
                "description": "The story of Victor Frankenstein, a young scientist who creates a sapient creature in an unorthodox scientific experiment.",
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Frankenstein_1818_edition_title_page.jpg/330px-Frankenstein_1818_edition_title_page.jpg"
            },
             {
                "name": "The Shining",
                "author": "Stephen King",
                "description": "The story centers on the life of Jack Torrance, an aspiring writer and recovering alcoholic who accepts a position as the off-season caretaker of the historic Overlook Hotel.",
                "image": "https://upload.wikimedia.org/wikipedia/en/4/4c/Shiningnovel.jpg"
            }
        ]
    }

    print("Seeding realistic data...")
    for section_name, books in realistic_data.items():
        section = Section.query.filter_by(name=section_name).first()
        if not section:
            section = Section(name=section_name, description=f"Books about {section_name}")
            db.session.add(section)
            db.session.commit()
            print(f"Created Section: {section_name}")
        
        for book_data in books:
            existing_book = Book.query.filter_by(name=book_data['name']).first()
            if not existing_book:
                book = Book(
                    name=book_data['name'],
                    author=book_data['author'],
                    full_content=f"Full content of {book_data['name']}...\n\n{book_data['description'] * 10}", # Dummy full content
                    image=book_data['image'],
                    section_id=section.id
                )
                db.session.add(book)
                print(f"  Added Book: {book.name}")
            else:
                # Update image if it exists but might be old/broken
                existing_book.image = book_data['image']
                existing_book.author = book_data['author'] 
                print(f"  Updated Book: {existing_book.name}")

    if not datastore.find_user(email="student@gmail.com"):
        datastore.create_user(
           name="student", email="student@gmail.com", password=generate_password_hash("student"), roles=["stud"])
        print("Created Student: student@gmail.com")

    # Add sample requests if student exists
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

