# -*- coding: utf-8 -*-

from urllib2 import urlopen
import json
import csv
import MySQLdb
import datetime

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
    
    def cursor(self):
        return self.conn.cursor()

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)     
        return cursor

    def commit(self):
        self.conn.commit()

end_date = datetime.datetime(2016, 1, 1).date()
date = datetime.datetime(2014, 8, 14).date()

db = DB()
# db.query("TRUNCATE TABLE irs_patients")


while date < end_date:

    url = 'http://tracking.punjab.gov.pk/ajax/irs_api.json?date='+date.strftime("%d-%m-%Y")+'&type=cr'

    print url

    content = urlopen(url)

    data = json.load(content)
    
    print len(data)
    
    if len(data) > 0:
    
        cols = data[0].keys()

        # isql = "CREATE TABLE irs_patients ("
        #
        # for key in cols:
        #     if key.find("date") < 0:
        #         isql += key + " VARCHAR(100), "
        #     else:
        #         isql += key + " timestamp, "
        #
        # isql = isql[0:-2]
        # isql += ");"
        #
        # print isql
        #
        # exit(0)
        
        isql = "INSERT INTO irs_patients ("

        for key in cols:
             isql += key
             isql += ", "

        isql = isql[0:-2]
        isql += ") VALUES "

        dict = {}

        # exit(0)

        for patient in data:
            sql = "( "
            for col in cols:
                try:
                    if patient[col] is None:
                        sql += "NULL, "
                    else:
                        sql += "'" + str.encode(str(MySQLdb.escape_string(patient[col])), 'utf-8') + "', "
                except TypeError:
                    sql += "'" + str(patient[col]) + "', "
                except UnicodeEncodeError:
                    print "unicode error"


            sql = sql[:-2]
            sql += "); "
            
            print isql+sql
            print "\n\n"
            
            try:
                db.query(isql+sql)
            except MySQLdb.OperationalError:
                print "op error"
                pass
        db.commit()
        # exit(0)
    date += datetime.timedelta(days=1)