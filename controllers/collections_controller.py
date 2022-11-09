from flask import Blueprint, request
from db import db
from models.collection import Collection, CollectionSchema

collection_bp = Blueprint('collections', '__name__', url_prefix='/collections')

@collection_bp.route('/')
def all_collections():
    stmt = db.select(Collection).order_by
    collections = db.session.scalars(stmt)
    return CollectionSchema(many=True).dump(collections)