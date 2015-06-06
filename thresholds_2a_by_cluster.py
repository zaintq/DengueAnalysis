import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import operator
import numpy as np

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

all_data = pd.read_csv('adjusted_con_calls2.csv', index_col=0)
activities = ["Awareness","Larviciding","Fogging","irs","Ovi_Trap","Dewatering","Tyres","FishSeed"]

significant_activities, count_interaction_activities, thresholds = {}, {}, {}

gen_dummy = lambda a, t, cluster_data: [1 if x >= t else 0 for x in cluster_data[a].tolist()]
gen_dummy_int = lambda a, cluster_data: [a*b for a,b in zip(cluster_data[a].tolist(),cluster_data["dummy_" + a].tolist())]

class activity:

    def __init__(self, a, result=None):

        self.name = a
        self.dummy = "dummy_" + self.name
        self.dummy_int = self.dummy + "_int"

        if result:
            self.pvalue = float(result.pvalues[self.name])
            self.coef   = float(result.params[self.name])
            self.pvalue_d = float(result.pvalues[self.dummy])
            self.coef_d = float(result.params[self.dummy])
            self.pvalue_di = float(result.pvalues[self.dummy_int])
            self.coef_di = float(result.params[self.dummy_int])

    def setFormula(self, f):
        self.formula = f

    def isValid(self, type=None):
        if type == "d":
            return self.pvalue_d <= 0.05 and self.coef_d < 0
        elif type == "di":
            return self.pvalue_di <= 0.05 and self.coef_di < 0
        return self.pvalue <= 0.05 and self.coef < 0

    def isSig(self, type=None):
        if type == "d":
            return self.pvalue_d <= 0.05
        elif type == "di":
            return self.pvalue_di <= 0.05
        return self.pvalue <= 0.05

    def isNeg(self, type=None):
        if type == "d":
            return self.coef_d < 0
        elif type == "di":
            return self.coef_di < 0
        return self.coef < 0

    def details(self):
        print "Activity:",self.name
        print "pvalue:", round(self.pvalue,2), "coef:", round(self.coef,2)
        print "pvalue_d:", round(self.pvalue_d,2), "coef_d:", round(self.coef_d,2)
        print "pvalue_di:", round(self.pvalue_di,2), "coef_di:", round(self.coef_di,2)

x = 10

for cluster in range(x, x+1):
    print "Cluster", cluster
    cluster_data = all_data.loc[all_data['cluster'] == cluster]
    significant_activities[cluster] = []
    thresholds[cluster] = {}

    cluster_data.head()

    for i in range(0, len(activities)):

        for j in range(i+1, len(activities)):

            max_a1 = max(cluster_data[activities[i]].tolist())
            max_a2 = max(cluster_data[activities[j]].tolist())

            t1 = t2 = 1

            while(True):

                cluster_data["dummy_" + activities[i]] = pd.Series(gen_dummy(activities[i], t1, cluster_data), index=cluster_data.index)
                cluster_data["dummy_" + activities[i] + "_int"] = pd.Series(gen_dummy_int(activities[i], cluster_data), index=cluster_data.index)

                cluster_data["dummy_" + activities[j]] = pd.Series(gen_dummy(activities[j], t2, cluster_data), index=cluster_data.index)
                cluster_data["dummy_" + activities[j] + "_int"] = pd.Series(gen_dummy_int(activities[j], cluster_data), index=cluster_data.index)

                formula = "confirmed ~ "

                try:

                    rhs = activities[i] + " + " + activities[j] + " + " + \
                          "dummy_" + activities[i] + " + " + "dummy_" + activities[j] + " + " + \
                          "dummy_" + activities[i] + "_int" + " + " + "dummy_" + activities[j] + "_int"

                    formula += rhs
                    result   = smf.ols(formula, cluster_data).fit()
                    a1 = activity(activities[i], result)
                    a2 = activity(activities[j], result)
                    a1.setFormula(formula)
                    a2.setFormula(formula)

                    # print result.summary()
                    # continue

                    if t1 > max_a1 or t2 > max_a2:
                        print activities[i], activities[j], "No Consensus"
                        thresholds[(activities[i], activities[j])] = (0, 0)
                        break

                    if a1.isValid("di") and a2.isValid("di"):
                        print activities[i], t1, activities[j], t2
                        thresholds[cluster][(activities[i], activities[j])] = (t1,t2)
                        break
                    else:
                        if a1.isValid("di"):
                            pass
                        else:
                            pass
                            t1 += 1

                        if a2.isValid("di"):
                            pass
                        else:
                            t2 += 1

                    pass
                except IndexError:
                    pass
    # for a in activities:
    #     pvalue = round(float(result.pvalues[a]),2)
    #     coef = round(float(result.params[a]),2)
    #     # print a, "is", # pvalue,
    #     if pvalue <= 0.05 and coef < 0:
    #         significant_activities[cluster].append(a)
    #     else:
    #         print a, "p =",pvalue, "c =",coef

    # print "break for cluster", cluster
    # exit()
    # break

# for c in significant_activities.keys():
#     print c, significant_activities[c]
# print
# print sorted(count_interaction_activities.items(), key=operator.itemgetter(1))

print thresholds