from flask import Flask, Blueprint, render_template
from .databases import lender_db
# 有原 担当
lend = Blueprint('lender', __name__, url_prefix='/lend-borrow')


# url http://127.0.0.1:5000/lend-borrow/
@lend.route('/', method='GET')
def lender():
    return render_template('lender.html')
