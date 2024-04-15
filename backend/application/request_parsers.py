from flask_restful import Api, Resource, reqparse,fields,marshal_with,marshal


user_data = reqparse.RequestParser()
user_data.add_argument('name')
user_data.add_argument('email')
user_data.add_argument('password')
user_data.add_argument('roles')

role_parser = reqparse.RequestParser()
role_parser.add_argument('name')
role_parser.add_argument('description')


book_parser = reqparse.RequestParser()
book_parser.add_argument('book_name')
book_parser.add_argument('price')
book_parser.add_argument('manufacture_date')
book_parser.add_argument('author_name')
book_parser.add_argument('quantity')
book_parser.add_argument('genre_id')




login_parser = reqparse.RequestParser()
login_parser.add_argument('email')
login_parser.add_argument('password')