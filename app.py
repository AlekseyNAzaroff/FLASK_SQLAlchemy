from flask import Flask, request, render_template
from database import db, Book, Genre

API_ROOT = '/api/v1/'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
db.init_app(app)

with app.app_context():
    db.create_all()


def get_genre_id_v2(genre, book):
    res = Genre.query.filter(Genre.genre == genre).all()
    print(res)
    book.genre_id = res.id
    db.session.add(book)
    db.session.commit()


def get_genre_id(genre, book):
    genre_id = genre.id
    book.genre_id = genre_id
    db.session.add(book)
    db.session.commit()
genres = []

@app.route(API_ROOT + 'create_book/', methods=['POST', 'GET'])
def create_book():
    if request.method == 'POST':
        try:
            book = Book(title=request.form['title'],
                        author=request.form['author'])
            genre = Genre(genre=request.form['genre'])
            if genre.genre not in genres:
                db.session.add(genre)
                db.session.add(book)
                db.session.flush()
                db.session.commit()
                get_genre_id(genre, book)
                genres.append(genre.genre)
            else:
                db.session.add(book)
                db.session.flush()
                db.session.commit()
                get_genre_id_v2(genre, book)
        except:
            db.session.rollback()
            print('Ошибка добавления в базу данных')
    return render_template('create_book.html')


@app.route(API_ROOT + 'book/')
def all_books():
    books = Book.query.all()
    return render_template('all_books.html', books=books)


@app.route(API_ROOT + 'genre/<int:genre_id>/', methods=['POST', 'GET'])
def all_genre_books(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template('all_genre_books.html',
                           genre=genre.genre, books=genre.books)


if __name__ == '__main__':
    app.run(debug=True)
