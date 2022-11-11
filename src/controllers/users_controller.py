from datetime import timedelta
from flask import Blueprint, request, Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db
from models.user import User, UserSchema

app = Flask(__name__)
bcrypt = Bcrypt(app)
user_bp = Blueprint('user', '__name__', url_prefix='/user')

def authorized():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin

@user_bp.route('/')
@jwt_required()
def all_users():
    if not authorized:
        return {'error': 'You must be an admin'}, 401
    else:
        stmt = db.select(User)
        users = db.session.scalars(stmt)
        return UserSchema(many=True).dump(users)

@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        user = User(
            username = request.json['username'],
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address is already registered to an existing user, please enter a different email address.'}, 409

@user_bp.route('/login', methods=['POST'])
def login_user():
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    if user and token and bcrypt.check_password_hash(user.password, request.json['password']):
        return {'message': f'Welcome {user.username}', 'token': token}
    else:
        return {'error': 'Invalid email or password'}, 401

@user_bp.route('/change-user-details', methods=['PUT','PATCH'])
@jwt_required()
def update_user():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    if user:
        user.username = request.json['username']
        user.email = request.json['email']
        user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')

        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201

@user_bp.route('/delete-user', methods=['DELETE'])
@jwt_required()
def delete_user():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Your account has been deleted'}
