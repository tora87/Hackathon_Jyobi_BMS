import MySQLdb

def connect_db():
    conn = MySQLdb.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'パスワード',
        db = 'jyobi_bms',
        charset = 'utf8'
    )
    return conn

def update_detail(jancord,title,author,total):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = "UPDATE books SET title=%s, author=%s, amount=%s WHERE jancord=%s"
        cur.execute(sql,(title,author,total,jancord,))
        cur.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
    return False

def delete_detail(jancord):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = "DELETE FROM books WHERE jancord=%s"
        cur.execute(sql,(jancord,))
        cur.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
    return False