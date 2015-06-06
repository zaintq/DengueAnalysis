import csv

rfname = "containment_sheet_date_all.csv"
wfname = "delay_sheet_date_all.csv"

rfile = csv.reader(open(rfname, "rb"))
wfile = csv.writer(open(wfname, "rb"))


for row in rfile:
