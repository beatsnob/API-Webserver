from datetime import timedelta
from flask import Blueprint, request, Flask
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from db import db
from models.user import User, UserSchema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
bcrypt = Bcrypt(app)
user_bp = Blueprint('user', '__name__', url_prefix='/user')

@user_bp.route('/')
def all_users():
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