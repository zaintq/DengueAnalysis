import numpy as np
import json
import itertools

from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

from scipy.spatial import ConvexHull

import matplotlib.pyplot as plt

import webbrowser

def getData(city):
  file = open("irs_patient_2013_tag_specific_activities.json")
  json_data = json.load(file)
  coords = []
  for json_datum in json_data:
  	if json_datum['district'] == city:
  		coords.append([json_datum['lat'], json_datum['lng'], json_datum['created_at'].split(':')[0]])
  return np.array(coords)

def removeDuplicates(X):
  b = np.ascontiguousarray(X).view(np.dtype((np.void, X.dtype.itemsize * X.shape[1])))
  _, idx = np.unique(b, return_index=True)
  return X[idx]

def transformData(X): 
  new = [[x[0], x[1]] for x in X]
  new = StandardScaler().fit_transform(new)
  return new

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

  print "c=", n_clusters, "k=", k

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

#############################################################

city = "Lahore"
#city = "Rawalpindi"

#algo = "DBSCAN"
algo = "KMEANS-test-"

epsilon = 0.2
minPts = 10
k = 5

data = getData(city)
X = transformData(data)

data_dict = {}
for datum, x in itertools.izip_longest(data,X):
    data_dict[tuple(x)] = list(datum)

#clusters = plotDBSCAN(removeDuplicates(X), epsilon, minPts)
clusters = plotKMeans(removeDuplicates(X), k)

prefix = city+algo+str(k)

for cluster, i in zip(clusters, range(len(clusters))):
  cluster_coords = []
  if len(cluster) > 2:
    for coords in cluster:
      print data_dict[tuple(coords)]
      exit()
      cluster_coords.append(float(data_dict[tuple(coords)]))
    print prefix, i
    print cluster_coords
    np.savetxt("%scluster%d.csv"%(prefix,i), cluster_coords, delimiter=",")
    hull = ConvexHull(cluster_coords)
    hull_vertices = []
    for vertex in hull.vertices:
      hull_vertices.append(cluster_coords[vertex])
    hull_vertices.append(hull_vertices[0])
    np.savetxt("%sconvex_hull_cluster%d.csv"%(prefix,i), hull_vertices, delimiter=",")

url = "http://localhost/Dengue/%s.php?prefix=%s&c="+str(len(clusters))
webbrowser.open_new(url%("polygons", prefix))
webbrowser.open_new_tab(url%("polygons_with_markers", prefix))
plt.show()
