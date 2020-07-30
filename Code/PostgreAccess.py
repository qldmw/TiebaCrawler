# -*- coding: utf-8 -*-
import psycopg2
from datetime import datetime

# postgre数据库连接属性
PostgreDic = {"database":"xxxxxxx", "user":"xxxxxxx", "password":"xxxxxxx.", "host":"localhost", "port":5432}

class PostgreAccess:
    def __init__(self): 
        try:
            self._conn = psycopg2.connect(database=PostgreDic["database"], user=PostgreDic["user"], password=PostgreDic["password"], host=PostgreDic["host"], port=PostgreDic["port"])
        except Exception as e:
            print(e)
        self._cur = self._conn.cursor()

    def InsertContent(self, floor, content, acctName, date):
        self._cur.execute("INSERT INTO contenttable (floor, content, accountname, posttime, backuptime)\
            VALUES (%s, %s, %s, %s, %s)", (floor, content, acctName, date, datetime.now()))        

    def InsertComment(self, floor, comment, acctName, date):
        self._cur.execute("INSERT INTO commenttable (floor, comment, accountname, posttime, backuptime)\
            VALUES (%s, %s, %s, %s, %s)", (floor, comment, acctName, date, datetime.now()))        

    def CommitAndDispose(self):
        print("CommitAndDispose")
        self._conn.commit()
        self._cur.close()
        self._conn.close()