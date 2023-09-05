import os

from flask import Flask, request, render_template

from database import db, Book, Genre

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add(Genre(name='Драма'))
    db.session.add(Genre(name='Эпик'))
    db.session.add(
        Book(
            name='Война и мир',
            genre_id=2
        )
    )
    db.session.add(
        Book(
            name='Идиот',
            genre_id=1
        )
    )
    db.session.add(
        Book(
            name='Му-му',
            genre_id=1
        )
    )
    db.session.commit()


@app.route('/')
def all_books():
    books = Book.query.all()
    return render_template("all_books.html", books=books)


@app.route('/genre/<int:genre_id>', methods=['POST', 'GET'])
def all_genre_books(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template("all_genre_books.html",
                           genre=genre.name, books=genre.books)


if __name__ == '__main__':
    app.run(debug=True)