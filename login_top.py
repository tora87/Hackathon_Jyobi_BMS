from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from databases import login_db

# 有原 担当
log_top = Blueprint('login_top', __name__, url_prefix='/login-top')


# url http://127.0.0.1:5000/login-top/
@log_top.route('/')
def login_page():
    # ログインページを表示するのに必要な処理
    return render_template('login.html')


@log_top.route('/login_result', methods=['POST'])
def login_process():
    # ログイン処理
    # 学籍番号、名前を受け取り、DBで照合する
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')

    data = login_db.select_specify_user(user_id=user_id)
    if data is None:
        # 取得した学籍番号がDBに登録されていないか、名前が未登録の場合
        return redirect(url_for('login_top.login_page'))

    for get_user_name in data:
        if get_user_name != user_name:
            # DBから取得した名前とフロントから受け取った名前が不一致の場合
            return redirect(url_for('login_top.login_page'))

    # 取得したデータをsessionに保存する
    session['user_id'] = user_id
    session['user_name'] = user_name
    return redirect(url_for('login_top.top_page'))


@log_top.route('/top_page')
def top_page():
    # トップページを表示するのに必要な処理
    return render_template('home.html')