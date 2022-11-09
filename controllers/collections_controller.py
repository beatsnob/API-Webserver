from flask import Blueprint, request
from db import db
from models.collection import Collection, CollectionSchema

collection_bp = Blueprint('collection', '__name__', url_prefix='/collection')

collection_bp.route('/')
def all_collections():
    stmt = db.select(Collection)
    collections = db.session.scalars(stmt)
    return CollectionSchema(many=True).dump(collections)