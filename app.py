from flask import Flask, request, render_template
from database import db, Book, Genre

API_ROOT = '/api/v1/'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route(API_ROOT + 'create_book/', methods=['POST', 'GET'])
def create_book():
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            genre_name = request.form['genre']
            genre = db.session.query(Genre).filter_by(name=genre_name).first()
            if genre is None and title != '':
                genre = Genre(name=genre_name)
                db.session.add(genre)
                db.session.commit()
            genre_id = genre.id
            book = Book(title=title, author=author, genre_id=genre_id)
            db.session.add(book)
            db.session.commit()
        except:
            db.session.rollback()
            print('Ошибка добавления в базу данных')
    return render_template('create_book.html')


@app.route(API_ROOT + 'books/')
def all_books():
    books = Book.query.order_by(Book.added.desc()).limit(15)
    return render_template('all_books.html', books=books)


@app.route(API_ROOT + 'genre/<int:genre_id>/', methods=['POST', 'GET'])
def all_genre_books(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template('all_genre_books.html',
                           genre=genre.name, books=genre.books)


if __name__ == '__main__':
    app.run(debug=True)
