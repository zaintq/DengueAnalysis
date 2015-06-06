# -*- coding: utf-8 -*-

from urllib2 import urlopen
import json
import csv
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

# url = 'http://202.125.133.156/patients/api/get_patients_info.php?start_date=2013-01-01&end_date=2014-01-01&type=confirmed'
# url = 'http://tracking.punjab.gov.pk/ajax/get_satscan_patients.js?start_date=2013-01-01&end_date=2014-01-01&type=confirmed'

# content = urlopen(url)

content = open("get_satscan_patients_2015.js", "rb")

data = json.load(content)
patients = data['list_patients']
cols = patients[0].keys()

isql = "INSERT INTO confirmed_patients ("

for key in cols:
     isql += key
     isql += ", "

isql = isql[0:-2]
isql += ") VALUES "

dict = {}

db = DB()
# db.query("TRUNCATE TABLE confirmed_patients")
# exit(0)

print "size:", len(patients)

count = 0

for patient in patients:
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
            continue


    sql = sql[:-2]
    sql += "); "
    # print isql+sql
    try:
        db.query(isql+sql)
        count += 1
        print count# , isql+sql
        db.commit()
        print
    except MySQLdb.OperationalError:
        print "op error"
        # print "************ Operational Error ************"
        # print sql
        # print "************ Operational Error ************"
        
        pass
    # print "---------------------------"
    # exit(0)
db.commit()