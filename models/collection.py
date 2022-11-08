from db import db, ma

class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey)
    bookID = db.Column(db.Integer, db.ForeignKey)
    name = db.Column(db.String)

class CollectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user id', 'book id', 'name')
        ordered = True