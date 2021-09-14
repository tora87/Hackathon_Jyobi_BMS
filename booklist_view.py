from databases.getbooklist import select_allbooks, select_bookdetail, select_searchbooks
from databases.mngbookdetail import update_detail as upd_d, delete_detail as dlt_d
from flask import Flask, Blueprint, render_template, redirect, session, request, url_for
import MySQLdb, databases.getbooklist
bol_view = Blueprint('booklist_view', __name__)

#! 図書一覧===============================
@bol_view.route('/booklist')
def booklist_view():
    if "user_id" not in session: #? セッションの有無
        return redirect("/")
    books_all_table = select_allbooks()
    # ajax
    session['book_list'] = books_all_table #? 図書テーブルから全図書の取得[JANcode,book_name]
    # return render_template('books_list.html', books_all_table=books_all_table)
    return render_template('books_list.html')

#! JANコードから詳細表示==================
@bol_view.route('/booklist/<int:jancord>', methods=['GET','POST'])
def detail_view(jancord):
    if "user_id" not in session: #? セッションの有無
        return redirect("/")
    books_all_table = select_allbooks() #? 図書テーブルから全図書の取得[JANcode,book_name]
    sel_book_detail = select_bookdetail(jancord) #? 図書のデータの取得[JANcode,book_name,book_author,AllAmo,remainingAmo]
    return render_template('books_list.html', books_all_table=books_all_table, sel_book_detail=sel_book_detail)


# ajaxを用いて、遷移を伴わずに登録情報を表示する
@bol_view.route('/booklist/ajax', methods=['POST'])
def get_ajax_book_list():
    if "user_id" not in session:
        return redirect("/")
    jancord = request.form.get("jan")
    sel_book_detail = select_bookdetail(jancord=jancord)
    return render_template('books_list.html', sel_book_detail=sel_book_detail)

# ajaxを用いて、遷移を伴わずに図書検索を行う
@bol_view.route('/booklist/search', methods=['POST'])
def search_book_list():
    if "user_id" not in session:  # ? セッションの有無
        return redirect("/")
    keyword = request.form.get("key")
    sel_search_books = select_searchbooks(keyword)
    return render_template("books_list.html", search_book_table=sel_search_books)

#! 詳細編集ページ表示==================
@bol_view.route('/booklist/<int:jancord>/edit')
def edit_view(jancord):
    if "user_id" not in session: #? セッションの有無
        return redirect("/")
    sel_book_detail = select_bookdetail(jancord)
    return render_template('edit.html', sel_book_detail=sel_book_detail, jancord=jancord)

#! 詳細の更新==================
@bol_view.route('/booklist/<int:jancord>/update_detail', methods=['POST'])
def update_detail(jancord):
    if "user_id" not in session: #? セッションの有無
        return redirect("/")
    title = request.form.get("name")
    author = request.form.get("author")
    stock = request.form.get("stock")
    result = upd_d(jancord,title,author,stock)
    if (result):
        return redirect(url_for('booklist_view.detail_view', jancord=jancord))
    else:
        return redirect(url_for('booklist_view.edit_view', jancord=jancord))

#! 本の削除==================
@bol_view.route('/booklist/<int:jancord>/delete_detail', methods=['POST'])
def delete_detail(jancord):
    if "user_id" not in session: #? セッションの有無
        return redirect("/")
    result = dlt_d(jancord)
    if (result):
        return redirect(url_for('booklist_view.booklist_view'))
    else:
        return redirect(url_for('booklist_view.edit_view', jancord=jancord))

