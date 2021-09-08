from flask import Flask, Blueprint, render_template

adm_view = Blueprint('admin_view', __name__, url_prefix='/admin-views')


# url http://127.0.0.1:5000/student-views/
@adm_view.route('/')
def admin_view():
    print('this is login page.')
    return render_template('books_list.html')
