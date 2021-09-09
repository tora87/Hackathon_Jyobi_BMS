from databases.getbooklist import select_allbooks, select_bookdetail
from databases.mngbookdetail import update_detail as upd_d, delete_detail as dlt_d
from flask import Flask, Blueprint, render_template, redirect, session, request, url_for
import MySQLdb, databases.getbooklist
bol_view = Blueprint('booklist_view', __name__)

#! 図書一覧===============================
@bol_view.route('/booklist')
def booklist_view():
    # if "user" not in session: #? セッションの有無
    #     return redirect("/")
    books_all_table = select_allbooks() #? 図書テーブルから全図書の取得[JANcode,book_name]
    return render_template('books_list.html', books_all_table=books_all_table)

#! JANコードから詳細表示==================
@bol_view.route('/booklist/<int:jancord>', methods=['GET','POST'])
def detail_view(jancord):
    # if "user" not in session: #? セッションの有無
    #     return redirect("/")
    books_all_table = select_allbooks() #? 図書テーブルから全図書の取得[JANcode,book_name]
    sel_book_detail = select_bookdetail(jancord) #? 図書のデータの取得[JANcode,book_name,book_author,AllAmo,remainingAmo]
    return render_template('books_list.html', books_all_table=books_all_table, sel_book_detail=sel_book_detail)

#! 詳細編集ページ表示==================
@bol_view.route('/booklist/<int:jancord>/edit')
def edit_view(jancord):
    # if "user" not in session: #? セッションの有無
    #     return redirect("/")
    sel_book_detail = select_bookdetail(jancord)
    return render_template('edit.html', sel_book_detail=sel_book_detail, jancord=jancord)

#! 詳細の更新==================
@bol_view.route('/booklist/<int:jancord>/update_detail', methods=['POST'])
def update_detail(jancord):
    # if "user" not in session: #? セッションの有無
    #     return redirect("/")
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
    # if "user" not in session: #? セッションの有無
    #     return redirect("/")
    result = dlt_d(jancord)
    if (result):
        return redirect(url_for('booklist_view.booklist_view'))
    else:
        return redirect(url_for('booklist_view.edit_view', jancord=jancord))

