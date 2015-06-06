import MySQLdb

class DB:
    
    def __init__(self):
        self.connect()
    
    def connect(self):
        self.conn = MySQLdb.connect(
            host="127.0.0.1",
            user="root",
            passwd="",
            db="containment"
        )
        self.conn.charset="utf8"
        self.cursor = self.conn.cursor()
    
    def cursor(self):
        return self.cursor

    def query(self, sql):
        try:
            self.cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.cursor.execute(sql)     
        return self.cursor

    def commit(self):
        self.conn.commit()
    
    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()
    
    def count(self):
        return self.cursor.rowcount