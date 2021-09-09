import MySQLdb

# test用localhost_access
def connect_db():
    conn = MySQLdb.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'パスワード',
        db = 'jyobi_bms',
        charset = 'utf8'
    )
    return conn

def adbook_detail(jancord,title,author,stock):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = "INSERT INTO books VALUES(%s,%s,%s,%s)"
        cur.execute(sql,(jancord,title,author,stock,))
        cur.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
    return False
