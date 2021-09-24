from databases.db_connecter import connect_db

def select_history(id="default_id"):
    conn = connect_db()
    cur = conn.cursor()
    if id == 'default_id':
        sql = """SELECT title,return_day,status_flg,user_number,name FROM rental
				INNER JOIN books ON books_jancord=jancord
				INNER JOIN user ON number=user_number
			GROUP BY id DESC"""
        try:
            cur.execute(sql,)
            history = cur.fetchall()
        except Exception as e:
            print('SQL実行に失敗しました:', e)
            return None
    else:
        sql = """SELECT title,return_day,status_flg,user_number,name FROM rental
				INNER JOIN books ON books_jancord=jancord
				INNER JOIN user ON number=user_number
			WHERE user_number=%s
			GROUP BY id DESC"""
        try:
            cur.execute(sql,(id,))
            history = cur.fetchall()
        except Exception as e:
            print('SQL実行に失敗しました:', e)
            return None
    cur.close()
    conn.close()
    return history