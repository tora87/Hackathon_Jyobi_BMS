import string
import random

from login_top import log_top
from booklist_view import bol_view
from add_books import books
from lender import lend
from create_qr import qr

from flask import Flask, Blueprint

app = Flask(__name__)
app.secret_key = "".join(random.choices(string.ascii_letters, k=256))


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


if __name__ == '__main__':
    app.run(debug=True)
