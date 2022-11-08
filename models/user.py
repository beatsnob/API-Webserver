from db import db, ma

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')
        ordered = True