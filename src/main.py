import os
from flask import Flask
from db import db, ma
from commands import db_commands
from controllers.collections_controller import collection_bp
from controllers.users_controller import user_bp
from controllers.books_controller import book_bp
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    jwt = JWTManager(app)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = 'my secret key'

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(collection_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(book_bp)

    return app
