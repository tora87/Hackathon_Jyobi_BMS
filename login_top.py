from flask import Flask, Blueprint, render_template
# 有原 担当
log_top = Blueprint('login_top', __name__, url_prefix='/login-top')


# url http://127.0.0.1:5000/login-top/
@log_top.route('/')
def login_page():
    print('this is login page.')
    return render_template('login.html')
