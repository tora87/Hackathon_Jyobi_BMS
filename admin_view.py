from flask import Flask, Blueprint, render_template

adm_view = Blueprint('admin_view', __name__)


@adm_view.route('/')
def admin_view():
    print('this is login page.')
    return render_template('admin_view.html')