from flask import Flask, Blueprint, render_template
# 有原 担当
lend = Blueprint('lender', __name__, url_prefix='/lend-borrow')


# url http://127.0.0.1:5000/lend-borrow/
@lend.route('/')
def lender():
    print('this is login page.')
    return render_template('lender.html')
