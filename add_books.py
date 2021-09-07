from flask import Flask, Blueprint, render_template

books = Blueprint('add_books', __name__, url_prefix='/add_books')


# url http://127.0.0.1:5000/add-books/
@books.route('/')
def add_books():
    print('this is login page.')
    return render_template('add_books.html')
