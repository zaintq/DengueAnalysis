import numpy as np
from sklearn.neighbors import NearestNeighbors
import polygon as py

def getData(city):
  file = open("irs_patient_2013_tag_specific_activities.json")
  json_data = json.load(file)
  coords = []
  for json_datum in json_data:
  	if json_datum['district'] == city:
  		coords.append([json_datum['lat'], json_datum['lng']])
  return np.array(coords)

city = "Lahore"
data = py.getData(city)
X = py.transformData(data)

#X = [[0], [3], [1]]

neigh = NearestNeighbors(radius=1.5)
neigh.fit(X) 

A = neigh.radius_neighbors_graph(X)
A = A.toarray()

print len(A)

for a in A:
	print a