from flask import Flask, Blueprint, render_template
# 有原 担当
qr = Blueprint('create_qr', __name__)


@qr.route('/')
def lender():
    print('this is login page.')
    return render_template('qr.html')
