from datetime import timedelta
from flask import Blueprint, jsonify, request
from db import db
from models.collection import Collection, CollectionSchema
from models.user import User
from models.book import Book, BookSchema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

collection_bp = Blueprint('collections', '__name__', url_prefix='/collections')

def authorized():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin

@collection_bp.route('/')
@jwt_required()
def all_collections():
    if not authorized:
        return {'error': 'You must be an admin'}, 401
    stmt = db.select(Collection).order_by(Collection.id)
    collections = db.session.scalars(stmt)
    return CollectionSchema(many=True).dump(collections)

@collection_bp.route('/create', methods=['POST'])
@jwt_required()
def create():

        # user = User(
        #     username = request.json['username'],
        #     email = request.json['email'],
        #     password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        # )
        # db.session.add(user)
        # db.session.commit()
    print(request.json['book_id'])
    print(request.json['user_id'])
    print(request.json['name'])

    new_collection = Collection(
        book_id = request.json['book_id'],
        user_id = request.json['user_id'],
        name = request.json['name']
    )

    # collection_fields = CollectionSchema.load(request.json)
    token = create_access_token(identity=str(User.id), expires_delta=timedelta(days=1))

    # new_collection = Collection()
    # new_collection.name = collection_fields["Read"]
    # new_collection.book_id = collection_fields["Title"]
    

    db.session.add(new_collection)
    db.session.commit()
    return {
        'message': f'This is your {new_collection.name} collection',
        'token':token,
        'collection':CollectionSchema(many=False).dump(new_collection),
        'book':BookSchema(many=False).dump(Book.title)
    }
    
    
    
    
# @collection_bp.route('/my-collections')
# @jwt_required
# def my_collections():
#     stmt = db.select(Collection).filter_by(