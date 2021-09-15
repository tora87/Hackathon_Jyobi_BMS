from databases.db_connecter import connect_db


def select_all_user() -> 'data':
    """
    管理者以外の登録されているユーザ情報を取得する

    Returns
    ----------
    data: tuple (tuple1, tuple2, tuple3...)
        登録件数
    data[any]: tuple (number, name, mail)
        学籍番号、 名前、 メールアドレス
    """
    conn = connect_db()
    cur = conn.cursor()

    # 管理者を表示しない
    sql = 'select * from user where number > 0999999'

    try:
        cur.execute(sql, )
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        return None

    user = cur.fetchall()

    cur.close()
    # conn.commit()
    conn.close()

    return user


def select_search_user(selectnum):
    conn = connect_db()
    cur = conn.cursor()

    sql = "SELECT * FROM user WHERE number BETWEEN %s AND %s"
    try:
        cur.execute(sql, (int(selectnum), int(selectnum)+99999))
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        return None
    user = cur.fetchall()
    cur.close()
    conn.close()

    return user


def select_number_scope():
    conn = connect_db()
    cur = conn.cursor()
    sql = "SELECT DISTINCT(number DIV 100000 * 100000) FROM user WHERE number > 1"
    try:
        cur.execute(sql,)
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        return None
    number = cur.fetchall()
    cur.close()
    conn.close()
    return number


def select_for_generation_user_data(student_id: 'int') -> 'data':
    """
    qrコード生成時に必要なデータの取得

    Returns
    ----------
    data: tuple (number, name, mail)
        学籍番号, 名前、 メールアドレス
    """
    conn = connect_db()
    cur = conn.cursor()

    # 管理者を表示しない
    sql = 'select * from user where number = %s'

    try:
        cur.execute(sql, (student_id,))
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        return None

    user_data = cur.fetchone()

    cur.close()
    # conn.commit()
    conn.close()

    return user_data


if __name__ == '__main__':
    user = select_for_generation_user_data(student_id=4204101)
    print(user)
    if user is None:
        print(user)
