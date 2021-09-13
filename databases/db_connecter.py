import MySQLdb

def connect_db():
    conn = MySQLdb.connect(
        host = '127.0.0.1',      #localhostでもOK
        user = 'hackathon-2',
        passwd = 'hackathon',
        db = 'jyobi_bms',
        charset = 'utf8'
	)
    return conn