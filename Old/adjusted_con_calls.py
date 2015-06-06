# this script reads the existing containment-calls data
# and adjusts the number of activities performed according to the t+14 scale
# the number of activities performed for the past two weeks are added to show how they affect the number of confirmed patients
# this is done for every activity and every cluster

import csv
import linecache
from operator import add

existing_fname = "con_calls.csv"

adjusted_fname = "adjusted_con_calls.csv"
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

line_number = 1

while True:
    row  = linecache.getline(existing_fname, line_number).split(',')
    if len(row) <= 1: break
    if line_number > 1:
        activities = map(int, row[5:-2])
        for i in range(1,7):
            if line_number - i > 1:
                _row = linecache.getline(existing_fname, line_number - i).split(',')
                activities = map(add, activities, map(int, _row[5:-2]))
        row[5:-2] = activities
    row[-1] = row[-1].replace('\n',"")
    print row
    adjusted_file.writerow(row)
    line_number += 1