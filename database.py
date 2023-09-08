from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    genre_id = db.Column(db.Integer,
                         db.ForeignKey('genre.id', ondelete='SET NULL'))
    genre = relationship('Genre', back_populates='books')
    is_read = db.Column(db.Boolean, nullable=True, default=False)

    def __repr__(self):
        return f'Book(name={self.title})'


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    books = relationship('Book', back_populates='genre')

    def __repr__(self):
        return self.name
