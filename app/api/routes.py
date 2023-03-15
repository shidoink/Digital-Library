
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yeah': 'boiiiiiiiiiiiiiiiiiiii'}

@api.route('/books', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    length = request.json['length']
    binding = request.json['binding']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, title, author, length, binding, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(contacts)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_contact_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    book = Book.query.get(id) 
    book.isbn = request.json['isbn']
    book.title = request.json['title']
    book.author = request.json['author']
    book.length = request.json['length']
    book.binding = request.json['binding']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE book ENDPOINT
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)