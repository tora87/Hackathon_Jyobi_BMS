import string
import random

from login_top import log_top
from booklist_view import bol_view
from add_books import books
from lender import lend
from create_qr import qr
from history_view import hist

from flask import Flask, Blueprint, redirect, url_for, render_template

from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.secret_key = "".join(random.choices(string.ascii_letters, k=256))

bp = Blueprint('exception', __name__)
bp.errorhandler(NotFound)

# ログイン、トップページ
app.register_blueprint(log_top)

# 図書一覧
app.register_blueprint(bol_view)

# 図書追加
app.register_blueprint(books)

# 貸借
app.register_blueprint(lend)

# qrコード
app.register_blueprint(qr)

# 貸出履歴一覧
app.register_blueprint(hist)

@app.route('/')
def default_transition():
    return redirect(url_for('login_top.login_page'))


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("images/favicon/favicon.ico")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("page_not_found.html")


@app.errorhandler(404)
def bp_not_found(e):
    return render_template("exception.html")


@app.errorhandler(Exception)
def exception(e):
    return render_template("internal.html")


if __name__ == '__main__':
    app.run(debug=True)
