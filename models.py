from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager


favorite_books = db.Table(
    "favorite_books",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True),
)


read_books = db.Table(
    "read_books",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    favorites = db.relationship(
        "Book",
        secondary=favorite_books,
        back_populates="favorited_by",
    )
    read = db.relationship(
        "Book",
        secondary=read_books,
        back_populates="read_by",
    )


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    books = db.relationship("Book", back_populates="genre")


class Book(db.Model):
    __tablename__ = "books"  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    genre = db.relationship("Genre", back_populates="books")

    favorited_by = db.relationship(
        "User",
        secondary=favorite_books,
        back_populates="favorites",
    )
    read_by = db.relationship(
        "User",
        secondary=read_books,
        back_populates="read",
    )


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))