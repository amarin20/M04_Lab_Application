from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db' #url and database
db = SQLAlchemy(app) 

#route says when you go to this url, this function will be performed. 
@app.route('/')
def index():
    return 'Hello!'
    
#model - database table (through classes)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(80), unique = True, nullable=False) #maximum 80 characters, has to be unqiue, and can not be left empty
    author = db.Column(db.String(40), nullable =False) #max 40 for author name, can not be left blank
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}" #sends name and description to user to see. (sums it up)
    
@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'name': book.book_name, 'author': book.author, 'publisher': book.publisher}

@app.route('/books', methods = ['POST'])
def add_book():
    book = Book(book_name=request.json['name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

@app.route('/books/<id>', methods = ['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return{"message":"wow"}