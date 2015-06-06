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

significant_activities = {}
count_interaction_activities = {}

activities = ["Awareness","Larviciding","Fogging","irs","Ovi_Trap","Dewatering","Debris","Tyres","FishSeed"]

gen_dummy = lambda a, t, cluster_data: [1 if x >= t else 0 for x in cluster_data[a].tolist()]

for cluster in range(1, 20):

    cluster_data = all_data.loc[all_data['cluster'] == cluster]
    significant_activities[cluster] = []

    x = cluster_data[activities]
    y = cluster_data['confirmed']

    # print print_full(x)

    cluster_data.head()

    # x = sm.add_constant(x)
    # result = sm.OLS(y, x).fit()

    # formula = "confirmed ~ Awareness * Larviciding * irs"
    # result = smf.ols(formula, cluster_data).fit()

    # print result.summary()
    # exit()
    # print dir(result)

    for i in range(0, len(activities)):
        cluster_data["dummy_" + activities[i]] = pd.Series(gen_dummy(activities[i], 50), index=cluster_data.index)
        for j in range(i+1, len(activities)):
            formula = "confirmed ~ "
            try:
                formula += activities[i]
                formula += " * "
                formula += activities[j]
                # print formula
                result = smf.ols(formula, cluster_data).fit()
                interaction = activities[i]+":"+activities[j]
                pvalue = float(result.pvalues[interaction])
                coef = float(result.params[interaction])
                if pvalue <= 0.05 and coef < 0:
                    significant_activities[cluster].append(interaction)
                    if interaction in count_interaction_activities.keys():
                        count_interaction_activities[interaction] += 1
                    else:
                        count_interaction_activities[interaction] = 1
                    # print interaction
                    # print pvalue, coef

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

for c in significant_activities.keys():
    print c, significant_activities[c]
print
print sorted(count_interaction_activities.items(), key=operator.itemgetter(1))