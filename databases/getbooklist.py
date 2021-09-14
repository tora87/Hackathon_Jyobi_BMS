from databases.db_connecter import connect_db


#? 全図書一覧取得
def select_allbooks():
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = "SELECT jancord, title from books"
        cur.execute(sql,)
        books_all_table = list(cur.fetchall())
        cur.close()
        conn.close()
        return books_all_table
    except Exception as e:
        print(e)
    return

#? JANコードから図書詳細を返す
def select_bookdetail(jancord):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = """SELECT jancord,
                title,
                author,
                amount,
                (amount - (SELECT COUNT(id) FROM rental
                    WHERE books_jancord=books.jancord AND
                    status_flg=true)) as renokamo
                from books WHERE jancord=%s"""
        cur.execute(sql, (jancord,))
        sel_book_detail = list(cur.fetchone())
        cur.close()
        conn.close()
        return sel_book_detail
    except Exception as e:
        print(e)
    return

def select_searchbooks(keyword):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = "SELECT jancord, title from books WHERE title LIKE '%s'"
        cur.execute(sql,('%'+keyword+'%',))
        sel_search_books = list(cur.fetchall())
        cur.close()
        conn.close()
        return sel_search_books
    except Exception as e:
        print(e)
    return