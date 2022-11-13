from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
from db import db, ma

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    type = db.Column(db.String)

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'type')
        ordered = True

    title = fields.String(required=True, validate=And(
        Length(min=3, error='Title must be at least 3 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Please enter only numbers or letters')
    ))
    author = fields.String(required=True, validate=And(
        Length(min=5, error='Author must be at least 5 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Please enter only numbers or letters')
    ))