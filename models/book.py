from db import db, ma

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    read_by = db.Column(db.String)

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'year', 'rating', 'read_by')
        ordered = True