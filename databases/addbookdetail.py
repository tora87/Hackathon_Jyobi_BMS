from databases.db_connecter import connect_db

def adbook_detail(jancord,title,author,stock):
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = "INSERT INTO books(jancord, title, author, amount) VALUES(%s,%s,%s,%s)"
        cur.execute(sql,(jancord,title,author,stock,))
        cur.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
    return False
