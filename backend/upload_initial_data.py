from app import app
from application.sec import datastore
from application.models import db, Role
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
    if not datastore.find_user(email="stud1@email.com"):
        datastore.create_user(
         name="stud1",    email="stud1@email.com", password=generate_password_hash("stud1"), roles=["stud"])
    if not datastore.find_user(email="stud2@email.com"):
        datastore.create_user(
         name="stud2",    email="stud2@email.com", password=generate_password_hash("stud2"), roles=["stud"])

    db.session.commit()
