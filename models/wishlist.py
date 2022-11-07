from db import db, ma

class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.Integer)
    wished_by = db.Column(db.String)

class WishlistSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'year', 'wished_by')
        ordered = True