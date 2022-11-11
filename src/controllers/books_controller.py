from flask import Blueprint, request, jsonify
from db import db
from models.book import Book, BookSchema
from models.collection import Collection, CollectionSchema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User
from datetime import timedelta


book_bp = Blueprint('books', '__name__', url_prefix='/book')

@book_bp.route('/')
def all_books():
    stmt = db.select(Book).order_by(Book.id)
    books = db.session.scalars(stmt)
    return BookSchema(many=True).dump(books)

@book_bp.route('/<int:id>/')
def one_book(id):
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        return BookSchema().dump(book)
    else:
        return{'error': f'Book not found with {id}'}, 404

@book_bp.route('/authors')
def all_authors():
    book = Book.query.with_entities(Book.author).all()
    authors = []
    for row in book:
        authors.append(row.author)
    return authors

@book_bp.route('/add', methods=['POST'])
@jwt_required()
def add():
    new_book = Book(
        title = request.json['Title'],
        author = request.json['Author'],
        type = request.json['Type']
    )

    token = create_access_token(identity=str(User.id), expires_delta=timedelta(days=1))

    db.session.add(new_book)
    db.session.commit()
    return {
        'message': f'You have added {new_book.title} by {new_book.author}',
        'token': token
    }

@book_bp.route('/change-details/<int:id>/', methods=['PUT','PATCH'])
@jwt_required()
def update_book(id):
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        book.title = request.json['title'] or book.title
        book.author = request.json['author'] or book.author
        book.type = request.json['type'] or book.type

        db.session.commit()
    return BookSchema().dump(book), 201,

@book_bp.route('/delete-book/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Your book has been deleted'}