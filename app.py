import string
import random

from login_top import log_top
from admin_view import adm_view
from student_view import std_view
from add_books import books
from lender import lend
from create_qr import qr

from flask import Flask, Blueprint, redirect, url_for

app = Flask(__name__)
app.secret_key = "".join(random.choices(string.ascii_letters, k=256))


# ログイン、トップページ
app.register_blueprint(log_top)

# 管理者の図書一覧
app.register_blueprint(adm_view)

# 生徒の図書一覧
app.register_blueprint(std_view)

# 図書追加
app.register_blueprint(books)

# 貸借
app.register_blueprint(lend)

# qrコード
app.register_blueprint(qr)


@app.route('/')
def default_transition():
    return redirect(url_for('login_top.login_page'))


if __name__ == '__main__':
    app.run(debug=True)
