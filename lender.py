from flask import Flask, Blueprint, render_template

lend = Blueprint('lender', __name__)


@lend.route('/')
def lender():
    print('this is login page.')
    return render_template('lender.html')
