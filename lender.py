from flask import Flask, Blueprint, render_template
# 有原 担当
lend = Blueprint('lender', __name__)


@lend.route('/')
def lender():
    print('this is login page.')
    return render_template('lender.html')
