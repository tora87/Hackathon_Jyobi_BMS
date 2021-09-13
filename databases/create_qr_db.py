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
    sql = 'select * from user where number > 0000001'

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
        cur.execute(sql, (student_id, ))
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        return None

    user_data = cur.fetchone()

    cur.close()
    # conn.commit()
    conn.close()

    return user_data


if __name__ == '__main__':
    user = select_all_user()
    print(user)