from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
from models.book import Book
from models.user import User
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

    name = fields.String(required=True, validate=And(
        Length(min=2, error='Collection name must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Please enter only numbers or letters')
    ))