from flask import Flask, Blueprint, render_template, session, request, redirect, url_for

from databases import lender_db

# 有原 担当
lend = Blueprint('lender', __name__, url_prefix='/lend-return')


# url http://127.0.0.1:5000/lend-borrow/
@lend.route('/')
def get_lender():
    if "user_id" not in session:
        return redirect("/")

    session['counter'] = 0
    return render_template('lender.html')


@lend.route('/search', methods=['POST'])
def get_book():
    if "user_id" not in session:
        return redirect("/")

    jan = request.form['jan']
    jan = is_integer(jan)

    if not jan:
        session['counter'] += 1
        error = 0
        return render_template('lender.html', error=error, count=session['counter'])

    book = lender_db.select_specify_books(book_id=jan)
    count = lender_db.select_history_lend_book(book_id=jan, user_id=session['user_id'])
    print(count)

    if book is None:
        session['counter'] += 1
        error = 0
        return render_template('lender.html', error=error, count=session['counter'])

    book_data = []
    stock = book[3] if book[4] is None else int(book[3]) - int(book[4])
    flg = False if count[0] > 0 else True
    book_data.append({
        'book_id': book[0],
        'name': book[1],
        'author': book[2],
        'amount': book[3],
        'stock': stock,
        'flg': flg,
    })

    return render_template('lender.html', books_json=book_data)

@lend.route('/lend', methods=['POST'])
def lend_process():
    if "user_id" not in session:  # ? セッションの有無
        return redirect("/")

    user_id = session['user_id']  # integer
    jan = request.form.get('jancode')

    jan = is_integer(jan)
    if not jan:
        error = 0
        session['counter'] += 1
        return render_template('lender.html', error=error, count=session['counter'])

    recode = lender_db.select_specify_books(book_id=jan)
    if recode is None:
        error = 1
        return render_template('lender.html', error=error)
    stock = recode[3] if recode[4] is None else int(recode[3]) - int(recode[4])
    if stock == 0:
        error = 2
        return render_template('lender.html', error=error)

    flg = lender_db.insert_specify_book(user_number=user_id, book_number=jan)

    if flg:
        print('ok')
    else:
        print('couldn\'t lend')
    
    operation_name = "lend"

    return render_template('lender.html', result=flg, operation_name=operation_name)


@lend.route('/return', methods=['POST'])
def return_process():
    if "user_id" not in session:  # ? セッションの有無
        return redirect("/")

    user_id = session['user_id']
    jan = request.form.get('jancode')

    jan = is_integer(jan)
    if not jan:
        session['counter'] += 1
        error = 0
        return render_template('lender.html', error=error, count=session['counter'])

    flg = lender_db.update_return_book(user_number=user_id, book_number=jan)

    if flg:
        print('ok')
    else:
        print('couldn\'t return')

    operation_name = "return"

    return render_template('lender.html', result=flg, operation_name=operation_name)


def is_integer(s: 'str'):
    try:
        int(s, 10)
    except ValueError as e:
        return False
    else:
        return int(s, 10)
