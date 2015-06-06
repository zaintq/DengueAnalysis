"""
===================================
Demo of OPTICS clustering algorithm
===================================

Finds core samples of high density and expands clusters from them.
"""
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
#from sklearn.cluster import optics as op
from optics import *
import numpy as np
import json
from sklearn import metrics
##############################################################################
# Original data

file = open("irs_patient_2013_tag_specific_activities.json")

json_data = json.load(file)

coords = []

for json_datum in json_data:
    if json_datum['district'] == 'Lahore':# or json_datum['district'] == 'Rawalpindi':
        coords.append([json_datum['lat'], json_datum['lng']])

X = np.array(coords)

b = np.ascontiguousarray(X).view(np.dtype((np.void, X.dtype.itemsize * X.shape[1])))
_, idx = np.unique(b, return_index=True)

X = X[idx]

#np.savetxt("unfiltered.csv", X, delimiter=",")

X = StandardScaler().fit_transform(X)

#np.savetxt("fitted_coords.csv", X, delimiter=",")

#std_dev = np.std(X)


##############################################################################

##############################################################################
# Compute OPTICS

testtree = setOfObjects(X)

# Run the top-level optics algorithm

epsilon, MinPts = 0.2, 10

# Note: build_optics should process using the same parameters as prep optics #

prep_optics(testtree,epsilon,MinPts)
build_optics(testtree,epsilon,MinPts,'./list.txt')

# Extract clustering structure. This can be run for any clustering distance, 
# and can be run mulitiple times without rerunning OPTICS
# OPTICS does need to be re-run to change the min-pts parameter
ExtractDBSCAN(testtree,0.3)

##############################################################################
# Plot result

import pylab as pl

# Core samples and labels #
core_samples = testtree._index[testtree._is_core[:] > 0]
labels = testtree._cluster_id[:]
#len(testtree._index[testtree._is_core[:] > 0])

print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

n_clusters_ = max(testtree._cluster_id) # gives number of clusters

# Black removed and is used for noise instead.
unique_labels = set(testtree._cluster_id[:]) # modifed from orginal #
colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
        markersize = 6
    class_members = [index[0] for index in np.argwhere(labels == k)]
    cluster_core_samples = [index for index in core_samples
                            if labels[index] == k]
    for index in class_members:
        x = X[index]
        if index in core_samples and k != -1:
            markersize = 14
        else:
            markersize = 6
        pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=markersize)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()

##############################################################################
# Change epsilon, and plot results

ExtractDBSCAN(testtree,0.115)

# Core samples and labels #
core_samples = testtree._index[testtree._is_core[:] > 0]
labels = testtree._cluster_id[:]
#len(testtree._index[testtree._is_core[:] > 0])

print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

n_clusters_ = max(testtree._cluster_id) # gives number of clusters
n_clusters_

n_clusters_ = max(testtree._cluster_id) # gives number of clusters
n_clusters_

# Plot results #
pl.figure()

# Black removed and is used for noise instead.
unique_labels = set(testtree._cluster_id[:]) # modifed from orginal #
colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
        markersize = 6
    class_members = [index[0] for index in np.argwhere(labels == k)]
    cluster_core_samples = [index for index in core_samples
                            if labels[index] == k]
    for index in class_members:
        x = X[index]
        if index in core_samples and k != -1:
            markersize = 14
        else:
            markersize = 6
        pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=markersize)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()
