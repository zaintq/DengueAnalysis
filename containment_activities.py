# -*- coding: utf-8 -*-

from urllib2 import urlopen
import json
import csv
import MySQLdb
import datetime
from db_conn import *

end_date = datetime.datetime(2012, 12, 31).date()
date = datetime.datetime(2012, 10, 20).date()

db = DB()
# db.query("TRUNCATE TABLE irs_patients")


while date < end_date:
    
    exists = {}
    
    csql = "SELECT id, lat, lng FROM containment_activities WHERE DATE(created_at) = '"+str(date)+"'"
    db.query(csql)
    for row in db.fetchall():
        key = (str(row[0]), str(row[1]), str(row[2]))
        # print key
        exists[key] = True
    
    print "Existing", len(exists)

    url = 'http://tracking.punjab.gov.pk/ajax/irs_api.json?date='+date.strftime("%d-%m-%Y")+'&type=con'

    print url

    content = urlopen(url)

    data = json.load(content)
    
    print len(data)
    
    result = {"added": 0, "exists": 0}
    
    if len(data) > 0:
    
        cols = data[0].keys()

        # isql = "CREATE TABLE containment_activities ("
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
        
        isql = "INSERT INTO containment_activities ("

        for key in cols:
             isql += key
             isql += ", "

        isql = isql[0:-2]
        isql += ") VALUES "

        dict = {}

        # exit(0)

        for patient in data:
            key = (str(patient['id']), str(patient['lat']), str(patient['lng']))
            # print key
            if key in exists.keys():
                result["exists"] += 1
                # print "exists"
                continue
            
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
            
            # print isql+sql
            # print "\n\n"
            
            try:
                db.query(isql+sql)
                result["added"] += 1
                # print "added"
            except MySQLdb.OperationalError:
                print "op error"
                pass
        print result
        db.commit()
        # exit(0)
    date += datetime.timedelta(days=1)