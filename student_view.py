from flask import Flask, Blueprint, render_template

std_view = Blueprint('student_view', __name__, url_prefix='/student-views')


@std_view.route('/')
def student_view():
    print('this is login page.')
    return render_template('student_view.html')