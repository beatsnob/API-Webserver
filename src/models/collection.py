from marshmallow import fields
from .user import User
from .book import Book
from db import db, ma

class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    name = db.Column(db.String)

class CollectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user id', 'book id', 'name')
        ordered = True