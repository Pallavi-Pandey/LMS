from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash
from flask_restful import marshal, fields
import flask_excel as excel
from celery.result import AsyncResult
from .tasks import create_resource_csv
from .models import User, db
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