import csv, json

def removeDuplicates(X):
  b = np.ascontiguousarray(X).view(np.dtype((np.void, X.dtype.itemsize * X.shape[1])))
  _, idx = np.unique(b, return_index=True)
  return X[idx]

file = open("irs_patient_2013_tag_specific_activities.json")

json_data = json.load(file)

coords = []

for json_datum in json_data:
	if json_datum['district'] == "Lahore":
		coords.append((json_datum['lat'], json_datum['lng'], json_datum['town_name']))

writer = csv.writer(open('town_coords_json.csv', 'wb'))

print len(coords)

coords = list(set(coords))
print len(coords)

for row in coords:
    if row[0] != None:
        writer.writerow(list(row))