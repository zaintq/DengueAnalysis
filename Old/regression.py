import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import operator
import numpy as np
from thresholds import thresholds_ca as tc, thresholds_2i as t2i, thresholds_ct as tct
import MySQLdb
import datetime

class DbConn():
    def __init__(self, h="127.0.0.1", u="root", p="", db="containment"):
        self.host   = h
        self.user   = u
        self.passwd = p
        self.db     = db
        self.conn   = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)

    def getConn(self):
        if self.conn:
            return self.conn
        return None

    def getCursor(self):
        if self.conn:
            return self.conn.cursor()
        else:
            return None

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

cursor = DbConn().getCursor()

def getPhotoURLs(activities, dates, cluster):
    count = 0
    for a in activities:
        for d in dates:
            end_date = datetime.datetime.strptime(d, "%m/%d/%Y").date()
            start_date = end_date - datetime.timedelta(days=7)
            # print start_date, end_date
            # exit()
            for a in list(activities):
                sql = "SELECT `before_picture_url`, `after_picture_url`, created_at FROM `activities` WHERE `cluster` = "+str(cluster)+" AND tag='"+a+"' AND `created_at` BETWEEN '"+str(start_date)+"' AND '"+str(end_date)+"' ORDER BY created_at"
                cursor.execute(sql)
                for row in cursor.fetchall():
                    count += 1
                    print "C:",cluster,"A:",a,"Date:",row[2],"Before:", row[0]
                    print "C:",cluster,"A:", a, "Date:", row[2], "After:", row[1]
                    print
    print count
                # print sql

all_data = pd.read_csv('adjusted_con_calls2.csv', index_col=0)
activities = ["Awareness","Larviciding","Fogging","irs","Ovi_Trap","Dewatering","Tyres","FishSeed"]

# print_full( all_data.loc[all_data['cluster'] == 15])

a1, a2 = "Larviciding", "irs"

for c in range(1, 20):
    # c = 15
    try:
        a1t = t2i[c][(a1,a2)][0]
        a2t = t2i[c][(a1,a2)][1]
    except KeyError:
        try:
            a1, a2 = a2, a1
            a1t = t2i[c][(a1, a2)][0]
            a2t = t2i[c][(a1, a2)][1]
        except KeyError:
            # print "Not significant in cluster:", c
            # print "Significant activites in cluster:",c
            # for x in t2i[c].keys(): print x,
            # print "\n\n"
            continue

    d = all_data.ix[ ( all_data["confirmed"] > 1 ) & ( all_data['cluster'] == c  ) & ( all_data[a1] >= a1t ) &  ( all_data[a2] >= a2t ) ]

    print
    # print c, a1t, a2t

    # print (d['date'].iloc(0))
    # print "****"
    # print_full(d[["confirmed", a1, a2]].index.values)
    getPhotoURLs([a1, a2], d[["confirmed", a1, a2]].index.values, c)
    # print "****"
    # print_full(  d[["confirmed", a1, a2]] )
    print
    # exit()

# for c in tc.keys():
#     for a in activities:
#         try:
#             # print a, tc[c][a]
#             res = all_data.ix[(all_data[a] <= tc[c][a]) & (all_data['cluster'] == c)]
#             # print res
#             print_full( res[[a, 'confirmed']] )
#         except KeyError:
#             pass
#     exit()

# all_data.head()

# formula = "confirmed ~ Awareness + Larviciding + Fogging + irs + Ovi_Trap + Dewatering + Tyres + FishSeed"
# formula = "confirmed ~ Larviciding + Fogging + irs + Ovi_Trap + Dewatering + Tyres + FishSeed"
# result = smf.ols(formula, all_data).fit()
# print result.summary()
# print formula

# for c in tc.keys():
#     try:
#         a1 = "irs"
#         a2 = "Larviciding"
#         a3 = "Fogging"
#
#         result = smf.ols(formula, all_data.loc[all_data['cluster'] == c]).fit()
#
#         res = all_data.ix[
#             (all_data[a1] >= tc[c][a1]) &
#             (all_data[a2] >= tc[c][a2]) &
#             (all_data[a3] >= tc[c][a3]) &
#             (all_data['cluster'] == c)
#         ]
#         # print res
#         # print_full(res[[a1, a2, a3, 'confirmed', 'cluster']])
#
#
#         print result.summary()
#
#         if result.pvalues[a1] <= 0.05 and result.params [a1] < 0:
#             print c, a1, tc[c][a1]
#         if result.pvalues[a2] <= 0.05 and result.params[a2] < 0:
#             print c, a1, tc[c][a2]
#         if result.pvalues[a3] <= 0.05 and result.params[a3] < 0:
#             print c, a1, tc[c][a3]

        # print c, a1, tc[c][a1],
        # print( "*s" if round(result.pvalues[a1],2) <= 0.05 else "i" ),
        # print( "*n" if round(result.params [a1],2) <=  0    else "p" )
        #
        # print a2, tc[c][a2],
        # print( "*s" if round(result.pvalues[a2],2) <= 0.05 else "i" ),
        # print( "*n" if round(result.params [a2],2) <=  0    else "p" )
        #
        # print a3, tc[c][a3]
        # print( "*s" if round(result.pvalues[a3],2) <= 0.05 else "i" ),
        # print( "*n" if round(result.params [a3],2) <=  0    else "p" )
        #
        # print "\n"

    # except KeyError:
    #     print "**",c, "Error","**"
    # exit()