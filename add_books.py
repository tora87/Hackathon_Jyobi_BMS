from flask import Flask, Blueprint, render_template

books = Blueprint('add_books', __name__)


@books.route('/')
def add_books():
    print('this is login page.')
    return render_template('add_books.html')
