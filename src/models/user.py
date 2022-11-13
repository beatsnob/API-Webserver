from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
from db import db, ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin')
        ordered = True
    
    username = fields.String(required=True, validate=And(
        Length(min=5, error='Username must be at least 5 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Please enter only numbers or letters')
    ))
    email = fields.String(required=True, validate=And(
        Length(min=5, error='Username must be at least 5 characters long')
    ))
