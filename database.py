from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, validates

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    added = db.Column(db.DateTime, nullable=False, default=datetime.now)
    genre_id = db.Column(db.Integer,
                         db.ForeignKey('genre.id', ondelete='SET NULL'))
    genre = relationship('Genre', back_populates='books')
    is_read = db.Column(db.Boolean, default=False)

    @validates('title')
    def validate_title(self, key, title):
        if title == '':
            raise ValueError("поле title не заполнено")
        return title

    def __repr__(self):
        return f'Book(name={self.title})'


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    books = relationship('Book', back_populates='genre')


    def __repr__(self):
        return self.name
