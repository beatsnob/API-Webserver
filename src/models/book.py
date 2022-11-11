from marshmallow import fields
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