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

# x = 10

for cluster in range(1, 20):
    print "Cluster", cluster
    cluster_data = all_data.loc[all_data['cluster'] == cluster]
    significant_activities[cluster] = []
    thresholds[cluster] = {}

    cluster_data.head()

    for i in range(0, len(activities)):

        max_a1 = max(cluster_data[activities[i]].tolist())

        t1 =  1

        while(True):

            cluster_data["dummy_" + activities[i]] = pd.Series(gen_dummy(activities[i], t1, cluster_data), index=cluster_data.index)
            cluster_data["dummy_" + activities[i] + "_int"] = pd.Series(gen_dummy_int(activities[i], cluster_data), index=cluster_data.index)

            formula = "confirmed ~ "

            try:

                rhs = activities[i] + " + " + \
                      "dummy_" + activities[i] + " + " + \
                      "dummy_" + activities[i] + "_int"

                formula += rhs
                # print formula
                # exit()

                result   = smf.ols(formula, cluster_data).fit()

                a1 = activity(activities[i], result)
                a1.setFormula(formula)

                # print result.summary()
                # continue

                if t1 > max_a1:
                    print activities[i], "No Consensus"
                    # thresholds[activities[i]] = 0
                    break

                if a1.isValid("di"):
                    print activities[i], t1
                    thresholds[cluster][activities[i]] = t1
                    break
                else:
                    if a1.isValid("di"):
                        pass
                    else:
                        pass
                        t1 += 1


                pass
            except IndexError:
                pass

print thresholds