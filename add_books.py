from flask import Flask, Blueprint, render_template, request, session, redirect
from flask.wrappers import Request
from databases.getbooklist import select_bookdetail
from databases.addbookdetail import adbook_detail, reregist_book
books = Blueprint('add_books', __name__, url_prefix='/add_books')


# url http://127.0.0.1:5000/add-books/
@books.route('/', methods=['GET' ,'POST'])
def add_books():
    if "user_id" not in session: #? セッションの有無
        return redirect("/")
    if session["user_id"][0] != '0': #? 管理者アカウントかの確認
        return redirect("/login-top/top_page")
    if request.method == "GET":
        return render_template('add_books.html')
    else:
        success=0
        error=0
        jancord = request.form.get("jancord")
        title = request.form.get("book-name")
        author = request.form.get("author")
        stock = request.form.get("book-amount")
        detail = select_bookdetail(jancord) # 重複図書の確認
        if (detail) == None:
            result = adbook_detail(jancord,title,author,stock)
            if result:
                success = 1
            else:
                error = 1
        else:
            if (detail[5] == 1): # 削除されている場合は内容変更し一覧再表示
                result = reregist_book(jancord,title,author,stock)
                if result:
                    success = 1
                else:
                    error = 1
            else:
                error = 2
        return render_template('add_books.html', error=error, success=success)