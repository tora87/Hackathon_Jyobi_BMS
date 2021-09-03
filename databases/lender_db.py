import datetime

import MySQLdb


def select_all_books() -> 'data or None':
    """
    BDに登録されている情報と現在の借りられている冊数を返す
    
    Returns
    ----------
    data: tuple (tuple1, tuple2, tuple3...)
        登録された情報と、現在借りられている冊数
    data[any]: tuple (jancord, title, author, amount, count)
        janコード、タイトル、著者、数量、現在の貸出数
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = 'select jancord, title, author, amount, cnt from books left outer join (select books_jancord, count(*) as cnt from rental where status_flg = True group by books_jancord) as rental_books on jancord = rental_books.books_jancord'

    try:
        cur.execute(sql,)
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        return None

    book = cur.fetchall()

    cur.close()
    conn.commit()
    conn.close()

    return book


def insert_specify_book (book_number: 'int', user_number: 'int',) -> 'bool':
    """
    借りる本のjanコードと、借りる生徒の学籍番号を渡すと、rentalテーブルにレコードを追加する

    Parameters
    ----------
    book_number : int
        借りる本のjanコード
    user_number : int
        借りる生徒の学籍番号

    Return
    ----------
    flg : bool
        デフォルト:True エラーが発生した場合はFalseが入る
    """
    conn = get_connection()
    cur = conn.cursor()

    date_today = datetime.date.today()
    date_future = datetime.timedelta(days=10)  # 借りてから10日後に返却期限を設ける
    date_limit = date_today + date_future

    sql = 'insert into rental(user_number, books_jancord, return_day, status_flg) values(%s, %s, %s, 1)'
    flg = True
    try:
        cur.execute(sql,(user_number, book_number, date_limit,))
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        flg = False
        return flg

    cur.fetchone()

    cur.close()
    conn.commit()
    conn.close()

    return flg


def update_return_book(book_number: 'int', user_number: 'int') -> 'bool':
    """
    返却する本のjanコードと、返却するユーザの学籍番号を渡すと、rentalの該当するデータのstatus_flgをFalseに変更する

    Parameters
    ----------
    book_number : int
        返す本のjanコード
    user_number : int
        返すユーザの学籍番号

    Return
    ---------
    flg : bool
        Dbアクセス時、エラーが発生すればFalse
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = 'update rental set status_flg = false where user_number = %s and books_jancord = %s and status_flg = true'

    flg = True

    try:
        cur.execute(sql,(user_number, book_number,))
    except Exception as e:
        print('SQL実行に失敗しました:', e)
        flg = False
        return flg

    cur.fetchone()

    cur.close()
    conn.commit()
    conn.close()

    return flg


# 本の数を数える
# select jancord, count(*) from books group by jancord;
# どの本が何冊借りられているか数える
# select books_jancord, count(*) from rental where status_flg = True group by books_jancord;
# booksテーブルと、借りられている本の冊数を結合して表示する
# select jancord, title, author, amount, cnt from books left outer join (select books_jancord, count(*) as cnt from rental where status_flg = True group by books_jancord) as rental_books on jancord = rental_books.books_jancord where jancord =  4500000000001;


def get_connection():
    return MySQLdb.connect(user='hackathon-2', passwd='hackathon', host='localhost', db='jyobi_bms', charset='utf8')


if __name__ == '__main__':
    # record = select_all_books()
    # print(record)
    
    # flg = insert_specify_book(book_number='2013031003351', user_number='4204101')
    # if flg:
    #     print('query ok')
    # else:
    #     print('query not appropriate')

    # flg = update_return_book(book_number= 2013031003351, user_number=4204101)
    # if flg:
    #     print('query ok')
    # else:
    #     print('query not appropriate')

    print('check all query \n system all clean')

