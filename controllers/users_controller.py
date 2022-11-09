from flask import Blueprint, request
from db import db
from models.user import User, UserSchema

user_bp = Blueprint('user', '__name__', url_prefix='/user')

user_bp.route('/')
def all_collections():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True).dump(users)