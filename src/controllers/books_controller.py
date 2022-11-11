from flask import Blueprint, request, jsonify
from db import db
from models.book import Book, BookSchema


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
    print (book)
    return json.dumps(book)


    # stmt = db.select(Book.author)
    # book = db.session.scalars(stmt)
    # return BookSchema(many=True).dump(book)