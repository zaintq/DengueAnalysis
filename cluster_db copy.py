import MySQLdb, csv, numpy as np
np.set_printoptions(threshold='nan')

#################################################################################

def in_hull(p, hull):
    """
    Test if points in `p` are in `hull`

    `p` should be a `NxK` coordinates of `N` points in `K` dimensions
    `hull` is either a scipy.spatial.Delaunay object or the `MxK` array of the 
    coordinates of `M` points in `K`dimensions for which Delaunay triangulation
    will be computed
    """
    from scipy.spatial import Delaunay
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0

#################################################################################

db = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    db="containment"
)

db.autocommit(True)

c = db.cursor()

town_coords_json = csv.reader(open('town_coords_json.csv', 'r'))
town_coords_db = csv.reader(open('town_coords_db.csv', 'r'))

cluster_files = open('cluster_files.csv', 'rb').readlines()
hull_files = open('hull_files.csv', 'rb').readlines()

town_coords_db_dict, town_coords_json_dict = {}, {}
town_coords_db_list, town_coords_json_list = [], []

for row in town_coords_json:
 town_coords_json_dict[(row[0], row[1])] = row[2]
 town_coords_json_list.append([row[0], row[1]])
 
for row in town_coords_db:
 town_coords_db_dict[(row[1], row[2])] = row[0]
 town_coords_db_list.append([row[1], row[2]])

town_coords_db_list, town_coords_json_list = np.array(town_coords_db_list), np.array(town_coords_json_list)

for i in range(0,len(cluster_files)):
  
  print "cluster:", i
  
  cluster_filename = cluster_files[i]
  cluster_file = csv.reader(open(cluster_filename.replace('\r\n',''), 'r'))
  cluster_coords = np.array([[x[0], x[1]] for x in cluster_file])
  
  hull_filename = hull_files[i]
  hull_file = csv.reader(open(hull_filename.replace('\r\n',''), 'r'))
  hull_coords = np.array([[x[0], x[1]] for x in hull_file])
  
  cluster_members = in_hull(town_coords_db_list,hull_coords)
  
  for n in range(0, len(town_coords_db_list)):
    print n
    if cluster_members[n] == True:
      query = "UPDATE activities\
               SET cluster = "+ str(i+1) +"\
               WHERE ROUND(lat,4) = "+ str(town_coords_db_list[n][0]) +" AND ROUND(lng,4) = "+ town_coords_db_list[n][1]
      print "updating cluster: ", str(i+1)
      c.execute(query)
  # for row in cluster_file:
    # print row
    # query = "UPDATE activities\
    #          SET cluster = "+ str(i+1) +"\
    #          WHERE ROUND(lat,4) = "+ str(row[0]) +" AND ROUND(lng,4) = "+ str(row[1])
    #          # WHERE created_at = '"+ row[2] +"' AND ROUND(lat,4) = "+ str(row[0]) +" AND ROUND(lng,4) = "+ str(row[1])

    # query = "SELECT * from activities \
    #          WHERE created_at = '"+ row[2] +"' AND ROUND(lat,4) = "+ str(row[0]) +" AND ROUND(lng,4) = "+ str(row[1])

    # query = "SELECT created_at, district, town_name, cluster, tag, lat, lng from activities \
    #          WHERE ROUND(lat,4) = "+ str(row[0]) +" AND ROUND(lng,4) = "+ str(row[1])

    # print query

    # c.execute(query)

    # print "\nRow(s) were affected :" +  str(c.rowcount) +"\n"
    # print
    # result = c.fetchall()
    # for line in result:
    #   print line
    # print