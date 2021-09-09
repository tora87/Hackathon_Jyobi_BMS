from flask import Flask, Blueprint, render_template, session, request, redirect, url_for

import lender
from databases import lender_db

# 有原 担当
lend = Blueprint('lender', __name__, url_prefix='/lend-return')


# url http://127.0.0.1:5000/lend-borrow/
@lend.route('/')
def get_lender():
    # 最初にページを読み込むときに、すでに本の一覧を表示する
    book = lender_db.select_all_books()
    book_data = []
    for array in book:
        book_data.append({
            'book_id': array[0],
            'name': array[1],
            'author': array[2],
            'amount': array[3],
            'stock': array[3] - array[4] if array[4] is not None else array[3],
        })
    print(book_data)
    return render_template('lender.html', books_json=book_data)


# 一つの関数で貸出、返却処理することになるかも
@lend.route('lend', methods=['POST'])
def lend_process():
    # 貸出処理
    # 受け取ったデータから、本のisbnコードを受け取る
    # 学籍番号を、sessionから取得する
    user_id = session['user_id']
    isbn = request.form.get('isbn')

    # 受け取ったデータをdbに登録する
    flg = lender_db.insert_specify_book(user_number=user_id, book_number=isbn)

    if flg:
        print('ok')
    else:
        print('couldn\'t lend')

    return redirect(url_for('lend.get_lender'))


@lend.route('return', methods=['POST'])
def return_process():
    # 返却処理
    # 受け取ったデータから、本のisbnコードを受け取る
    # 学籍番号を、sessionから取得する
    user_id = session['user_id']
    isbn = request.form.get('isbn')
    
    # 受け取ったデータをdbに登録する
    flg = lender_db.update_return_book(user_number=user_id, book_number=isbn)
    
    if flg:
        print('ok')
    else:
        print('couldn\'t return')
        
    return redirect(url_for('lend.get_lender'))


# @lend.route('/', method='POST')
# def post_lender():
