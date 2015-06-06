from urllib2 import urlopen
import json
import csv
import MySQLdb

# url = 'http://202.125.133.156/patients/api/get_patients_info.php?start_date=2013-01-01&end_date=2014-01-01&type=confirmed'
# url = 'http://tracking.punjab.gov.pk/ajax/get_satscan_patients.js?start_date=2013-01-01&end_date=2014-01-01&type=confirmed'

# content = urlopen(url)

content = open("confirmed_patients.json", "rb")

data = json.load(content)

sql = "INSERT INTO patients ("

for key in data['list_patients'][0].keys():
     sql += key
     sql += ", "

sql = sql[0:-2]
sql += ") VALUES "

print sql
print
print 
exit(0)

dict = {}

db = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    db="containment"
)

c = db.cursor()

bad_items = ['', 'Other then lahore', 'M', 'Others']

for datum in data:
    district = datum['data']['district']
    if district == 'LAHORE' or district == 'RAWALPINDI':
        uc = datum['data']['uc_no']

        if uc not in bad_items:
            query = "SELECT DISTINCT cluster FROM activities WHERE uc_no = %d" % int(uc)
            c.execute(query)

            clusters = c.fetchall()
            date = datum['data']['date_of_confirmation'].split(' ')[0]
            
            for cluster in clusters:
                print cluster, date
                cluster = int(cluster[0])      
                if cluster in dict.keys():
                    if date in dict[cluster].keys():
                        dict[cluster][date] += 1
                    else:
                        dict[cluster][date] = 1
                else:
                        dict[cluster] = {date : 1}
#  add date as well!
for cluster in dict.keys():
    for uc in dict[cluster].keys():
        file.writerow([cluster, uc, dict[cluster][uc]])
print dict

sql += " );"