# this script reads the existing containment-calls data
# and adjusts the number of activities performed according to the t+14 scale
# the number of activities performed for the past two weeks are added to show how they affect the number of confirmed patients
# this is done for every activity and every cluster

import csv
import datetime

existing_fname = "con_calls2.csv"
existing_fh = open(existing_fname, "rb")
existing_file = csv.reader(existing_fh)


adjusted_fname = "com_con_calls.csv"
adjusted_fh = open(adjusted_fname, "wb")
adjusted_file = csv.writer(adjusted_fh)

columns = [
    "date",
    "cases(t+14)",
    "confirmed(t)",
    "calls(t)",
    "complaint(t)",
    "Awareness",
    "Larviciding",
    "Fogging",
    "irs",
    "Ovi_Trap",
    "Dewatering",
    "Tyres",
    "water_leakage",
    "Debris",
    "FishSeed",
    "Adult_Mosquitoes",
    "irs_patient",
    "cluster"
]

existing_file.next()


data = {}

for row in existing_file:
    date = datetime.datetime.strptime(row[0], '%m/%d/%Y').date()

    if date in data.keys():
        data[date][2]  = int(float(data[date][2])  + float(row[2]))
        data[date][5]  = int(float(data[date][5])  + float(row[5]))
        data[date][6]  = int(float(data[date][6])  + float(row[6]))
        data[date][7]  = int(float(data[date][7])  + float(row[7]))
        data[date][8]  = int(float(data[date][8])  + float(row[8]))
        data[date][9]  = int(float(data[date][9])  + float(row[9]))
        data[date][10] = int(float(data[date][10]) + float(row[10]))
        data[date][11] = int(float(data[date][11]) + float(row[11]))
        data[date][12] = int(float(data[date][12]) + float(row[12]))
        data[date][13] = int(float(data[date][13]) + float(row[13]))
        data[date][14] = int(float(data[date][14]) + float(row[14]))
        data[date][15] = int(float(data[date][15]) + float(row[15]))
        data[date][16] = int(float(data[date][16]) + float(row[16]))
    else:
        data[date] = row

def sortdict(d):
    for key in sorted(d): yield d[key]

# print data
adjusted_file.writerow(columns)
for row in sortdict(data):
    adjusted_file.writerow(row)
    print row
    # print date.strftime('%m/%d/%Y')