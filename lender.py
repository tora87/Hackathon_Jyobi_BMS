from flask import Flask, Blueprint, render_template
from databases import lender_db

# 有原 担当
lend = Blueprint('lender', __name__, url_prefix='/lend-borrow')


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

# @lend.route('/', method='POST')
# def post_lender():
