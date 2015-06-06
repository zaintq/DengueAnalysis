import csv
from db_conn import *

db = DB()

sql = "SELECT irspat_lid, created_at, lat, lng FROM irs_patients WHERE tag = 'irs_patient' AND district = 'Lahore' ORDER BY created_at"

db.query(sql)

_file = csv.writer(open("irs_patients.csv", "wb"))
_file.writerow(["id", "created_at", "lat", "lng"])

for row in db.fetchall():
    line = [int(row[0]), str(row[1]).split(' ')[0], float(row[2]), float(row[3])]
    print list(line)
    _file.writerow(line)