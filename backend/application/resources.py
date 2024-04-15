from flask_restful import Resource, Api, reqparse, fields, marshal
from flask_security import auth_required, roles_required, current_user
from flask import jsonify
from sqlalchemy import or_
from .models import  db
from .instances import cache


api = Api(prefix='/api')


parser = reqparse.RequestParser()
parser.add_argument('topic', type=str,
                    help='Topic is required should be a string', required=True)
parser.add_argument('description', type=str,
                    help='Description is required and should be a string', required=True)
parser.add_argument('resource_link', type=str,
                    help='Resource Link is required and should be a string', required=True)


class Creator(fields.Raw):
    def format(self, user):
        return user.email


study_material_fields = {
    'id': fields.Integer,
    'topic':   fields.String,
    'description':  fields.String,
    'resource_link': fields.String,
    'is_approved': fields.Boolean,
    'creator': Creator
}

book_marshal={
    'id': fields.Integer,
    'name': fields.String,
    'author': fields.String,
    'section_id': fields.Integer,
    'content': fields.String,
    'image': fields.String,
    "status": fields.String,
    'is_deleted': fields.Boolean
}

section_marshal={
    'id': fields.Integer,
    'name': fields.String,
    "books": fields.List(fields.Nested(book_marshal))
}

