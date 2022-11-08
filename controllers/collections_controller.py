from flask import Blueprint, request
from db import db
from models.collection import Collection, CollectionSchema

collection_bp = Blueprint('collection', '__name__', url_prefix='/collection')

collection_bp.route('/')