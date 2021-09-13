from databases.db_connecter import connect_db


def select_specify_user(user_id: 'int'):
    """
    学籍番号を受け取り、DBから名前を取得する。

    Parameters
    ----------
    user_id : integer
        検索する学籍番号

    Returns
    -------
    data : tuple or None
        学籍番号と紐づいた名前
    """

    conn = connect_db()
    cur = conn.cursor()

    sql = 'select name from user where number = %s'

    try:
        cur.execute(sql, (user_id,))
    except Exception as e:
        print('SQL実行に失敗しました:', e)

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


if __name__ == '__main__':
    user_name = select_specify_user(user_id=0000000)
    if user_name is None:
        print('this is None type')
    else:
        print('this is not None type')
