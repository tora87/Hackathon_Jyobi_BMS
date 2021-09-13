from databases.db_connecter import connect_db

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