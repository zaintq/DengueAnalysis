import numpy as np
import json
import itertools
import csv
from db_conn import *
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist

from scipy.spatial import ConvexHull

import matplotlib.pyplot as plt

import webbrowser

def getData(year = False):
    db = DB()
    if year == 2012:
        sql = "SELECT lat, lng, created_at FROM irs_patients WHERE district = 'Lahore' AND created_at BETWEEN '2012-01-20' AND '2013-01-01'"
    elif year == 2013:
        sql = "SELECT lat, lng, created_at FROM irs_patients WHERE district = 'Lahore' AND created_at BETWEEN '2013-01-20' AND '2014-01-01'"
    elif year == 2014:
        sql = "SELECT lat, lng, created_at FROM irs_patients WHERE district = 'Lahore' AND created_at BETWEEN '2014-01-20' AND '2015-01-01'"
    elif year == 2015:
        sql = "SELECT lat, lng, created_at FROM irs_patients WHERE district = 'Lahore' AND created_at BETWEEN '2015-01-20' AND '2016-01-01'"
    else:
        sql = "SELECT lat, lng, created_at FROM irs_patients WHERE district = 'Lahore'"

    db.query(sql)

    coords = []
    for row in db.fetchall():
        coords.append([float(row[0]), float(row[1])])
        # print [row[0], row[1], row[2].date()]
        # exit()
    return np.array(coords)

def removeDuplicates(X):
  b = np.ascontiguousarray(X).view(np.dtype((np.void, X.dtype.itemsize * X.shape[1])))
  _, idx = np.unique(b, return_index=True)
  return X[idx]

def xWithoutDate(X):
  return [[x[0], x[1]] for x in X]

def transformData(X): 
  return StandardScaler().fit_transform(xWithoutDate(X))

def plotDBSCAN(X, epsilon, minPts):
  db = DBSCAN(eps=epsilon, min_samples=minPts).fit(X)
  labels = db.labels_

  core_samples_mask = np.zeros_like(labels, dtype=bool)
  core_samples_mask[db.core_sample_indices_] = True
  
  n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

  clusters = [X[labels == i] for i in xrange(n_clusters)]

  unique_labels = set(labels)
  colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
  for k, col in zip(unique_labels, colors):
      if k == -1: col = 'k'
      class_member_mask = (labels == k)
      xy = X[class_member_mask & core_samples_mask]
      plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
      xy = X[class_member_mask & ~core_samples_mask]
      plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

  print('Estimated number of clusters: %d' % n_clusters)
  print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
  
  plt.title('Estimated number of clusters: %d' % n_clusters)

  return clusters

def plotKMeans(X, k):
  k_means = KMeans(n_clusters=k)
  k_means.fit(X)

  labels = k_means.labels_

  core_samples_mask = np.zeros_like(labels, dtype=bool)
  
  n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

  clusters = [X[labels == i] for i in xrange(n_clusters)]

  # print "c=", n_clusters, "k=", k

  unique_labels = set(labels)
  colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
  print k, "%0.3f" % metrics.silhouette_score(X, labels)
  for k, col in zip(unique_labels, colors):
      if k == -1: col = 'k'
      class_member_mask = (labels == k)
      xy = X[class_member_mask & core_samples_mask]
      plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
      xy = X[class_member_mask & ~core_samples_mask]
      plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

  # print('Estimated number of clusters: %d' % n_clusters)
  # print "Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels)
  
  
  plt.title('Estimated number of clusters: %d' % n_clusters)

  return clusters

# algo = "-DBSCAN-"
algo = "__KMEANS__"

epsilon = 0.3
minPts = 2

k = 20

# for year in [2012]:

year = 2013

print 'Year:', year

data = getData(year)

K = range(1,50)

X = transformData(data)

  # scipy.cluster.vq.kmeans
KM = [kmeans(X,k) for k in K] # apply kmeans 1 to 10
centroids = [cent for (cent,var) in KM]   # cluster centroids

D_k = [cdist(X, cent, 'euclidean') for cent in centroids]

cIdx = [np.argmin(D,axis=1) for D in D_k]
dist = [np.min(D,axis=1) for D in D_k]
avgWithinSS = [sum(d)/X.shape[0] for d in dist]  

kIdx = 2
# plot elbow curve
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(K, avgWithinSS, 'b*-')
ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
      markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Average within-cluster sum of squares')
tt = plt.title('Elbow for K-Means clustering')  

plt.show()


exit()