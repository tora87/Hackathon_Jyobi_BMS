from flask import Flask, Blueprint, render_template, request
from flask.wrappers import Request
from databases.getbooklist import select_bookdetail
from databases.addbookdetail import adbook_detail
books = Blueprint('add_books', __name__, url_prefix='/add_books')


# url http://127.0.0.1:5000/add-books/
@books.route('/', methods=['GET' ,'POST'])
def add_books():
    # if "user" not in session: #? セッションの有無
    #     return redirect("/")
    if request.method == "GET":
        return render_template('add_books.html')
    else:
        success=0
        error=0
        jancord = request.form.get("jancord")
        if (select_bookdetail(jancord)) == None:
            title = request.form.get("book-name")
            author = request.form.get("author")
            stock = request.form.get("book-amount")
            result = adbook_detail(jancord,title,author,stock)
            if result:
                success = 1
            else:
                error = 1
        else:
            error = 2
        return render_template('add_books.html', error=error, success=success)