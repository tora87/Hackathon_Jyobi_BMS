from flask import Flask, Blueprint, render_template, session, request, redirect, url_for

from databases import lender_db

# 有原 担当
lend = Blueprint('lender', __name__, url_prefix='/lend-return')


# url http://127.0.0.1:5000/lend-borrow/
@lend.route('/')
def get_lender():
    if 'user_id' in session:
        # 最初にページを読み込むときに、すでに本の一覧を表示する
        # 本のjanコードを読み込んだ際に情報を表示するように変更するなら、下記のコードは必要ない
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
    else:
        return redirect(url_for('login_top.login_page'))


# ajaxで本を読み込んだ際、
# let jan = $("#jan").val();  # janコードを取得
# $.ajax({
#     "type": 'POST',
#     "url": '/lend-return/search',
#     "data": {'jan': jan }
# })
# みたいな書き方で、下記の処理にアクセスできる
@lend.route('/search', methods=['POST'])
def get_book():
    if 'user_id' in session:
        jan = request.form['jan']
        jan = is_integer(jan)
        if not jan:
            return redirect(url_for('lender.get_lender'))
    
        book = lender_db.select_specify_books(book_id=jan)
    
        if book is None:
            return redirect(url_for('lender.get_lender'))
    
        book_data = []
        for array in book:
            book_data.append({
                'book_id': array[0],
                'name': array[1],
                'author': array[2],
                'amount': array[3],
                'stock': array[3] - array[4] if array[4] is not None else array[3],
            })
    
        return render_template('lender.html', books_json=book_data)
    else:
        return redirect(url_for('login_top.login_page'))


# 一つの関数で貸出、返却処理することになるかも
# 一つの関数で処理する場合、input:radio等で分岐すると思われるので、
# request.form.get('radio_id') で取得して、if で分岐させる
@lend.route('/lend', methods=['POST'])
def lend_process():
    if 'user_id' in session:
        # 貸出処理
        # 受け取ったデータから、本のisbnコードを受け取る
        # 学籍番号を、sessionから取得する
        user_id = session['user_id']  # integer
        jan = request.form.get('jan')
    
        jan = is_integer(jan)
        if not jan:
            # 受け取った値がFalseの場合
            return redirect(url_for('lender.get_lender'))
    
        # 受け取ったデータをdbに登録する
        flg = lender_db.insert_specify_book(user_number=user_id, book_number=jan)
    
        if flg:
            print('ok')
        else:
            print('couldn\'t lend')
    
        return redirect(url_for('lender.get_lender'))
    else:
        return redirect(url_for('login_top.login_page'))


@lend.route('/return', methods=['POST'])
def return_process():
    if 'user_id' in session:
        # 返却処理
        # 受け取ったデータから、本のisbnコードを受け取る
        # 学籍番号を、sessionから取得する
        user_id = session['user_id']
        jan = request.form.get('jan')
    
        jan = is_integer(jan)
        if not jan:
            # 受け取った値がFalseの場合
            return redirect(url_for('lender.get_lender'))
    
        # 受け取ったデータをdbに登録する
        flg = lender_db.update_return_book(user_number=user_id, book_number=jan)
    
        if flg:
            print('ok')
        else:
            print('couldn\'t return')
    
        return redirect(url_for('lend.get_lender'))
    else:
        return redirect(url_for('login_top.login_page'))


def is_integer(s: 'str'):
    """
    引数で受け取った値が１０進数の整数値に変換可能か判定する。変換可能ならば、変換して値を返す。

    Parameters
    ---------
    s : string
        判定する文字列

    Return
    ---------
    data : False or integer
        変換不可能ならFalse, 変換可能なら返還後の整数値
    """
    try:
        int(s, 10)
    except ValueError as e:
        return False
    else:
        return int(s, 10)