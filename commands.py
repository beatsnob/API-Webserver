# from directory.file import Whatever 
from main import Flask
from models.book import Book
from models.user import User
from models.collection import Collection
from db import db
from flask import Blueprint
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db_commands = Blueprint('db', __name__)
bcrypt = Bcrypt(app)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():

    users = [
        User(
            username = 'admin_user',
            email = 'admin_user@library.com',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin = True
        ),
        User(
            username = 'SammyNandez',
            email = 'samanthafernandez@library.com',
            password = bcrypt.generate_password_hash('user123').decode('utf-8'),
            is_admin = False
        )
    ]
    books = [
        Book(
            title = 'The Earthsea Quartet',
            author = 'Ursula Le Guin',
            type = 'Fiction',
        ),
        Book(
            title = 'One Hundred Years of Solitude',
            author = 'Gabriel Garcia Marquez',
            type = 'Fiction',
        ),
        Book(
            title = 'Rooftops in Karachi',
            author = 'Misbah Khokhar',
            type = 'Fiction',
        ),
        Book(
            title = 'Dune',
            author = 'Frank Herbert',
            type = 'Fiction',
        ),
        Book(
            title = 'Brave New World',
            author = 'Aldous Huxley',
            type = 'Fiction',
        ),
        Book(
            title = 'There Will Be Rainbows: A Biography of Rufus Wainwright',
            author = 'Kirk Lake',
            type = 'Non-Fiction',
        ),
        Book(
            title = 'Slaughterhouse 5',
            author = 'Kurt Vonnegut',
            type = 'Fiction',
        ),
        Book(
            title = 'Kafka on the Shore',
            author = 'Haruki Murakami',
            type = 'Fiction',
        ),
        Book(
            title = 'The Wheel of Time',
            author = 'Robert Jordan',
            type = 'Fiction',
        ),
        Book(
            title = 'The World According to Garp',
            author = 'John Irving',
            type = 'Fiction',
        ),
        Book(
            title = 'Half of a Yellow Sun',
            author = 'Chimamanda Ngozi Adiche',
            type = 'Fiction',
        ),
        Book(
            title = 'A Little Life',
            author = 'Hanya Yanagihara',
            type = 'Fiction',
        ),
        Book(
            title = "Why You Don't Need Shoes",
            author = 'Xian',
            type = 'Non-Fiction',
        ),
        Book(
            title = 'Squirrel Seeks Chipmunk',
            author = 'David Sedaris',
            type = 'Fiction'
        ),
        Book(
            title = 'Lapvona',
            author = 'Ottessa Moshfegh',
            type = 'Fiction'
        )
    ]

    db.session.add_all(users)
    db.session.add_all(books)

    # someBook = db.Book.findByName("Harry Potter")
    one_book = db.select(Book).filter_by(id=4)
    # someUser = db.User.findByName("Mostafa")
    one_user = db.select(User).filter_by(id=2)

    #Collection(book_id=one_book.id, user_id=one_user.id, name="Wishlist")


    collections = [
        Collection(
            book_id = one_book.id,
            user_id = one_user.id,
            name = 'Wishlist'
        )
    ]

    db.session.add_all(collections)
    db.session.commit()
    print('Tables seeded')