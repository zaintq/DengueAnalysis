import MySQLdb, csv, numpy as np
from itertools import izip as zip, count

np.set_printoptions(threshold='nan')

db = MySQLdb.connect(host="127.0.0.1", db="containment", user="root", passwd="")
c  = db.cursor()

hulls = {}

bfile = csv.reader(open("rects-coors-256.csv","rb"), delimiter=' ')

for row, block in zip(bfile,  count()):
    row = [float(x) for x in row]
    hulls[block] = np.array([[row[0], row[1]], [row[2], row[3]], [row[4], row[5]], [row[6], row[7]]])

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

def assignIrsBlocksViaHull(): # irs acts + patients
    
    sql = "SELECT lat, lng, irspat_lid FROM irs_patients WHERE district = 'Lahore' AND lat IS NOT NULL AND lng IS NOT NULL"

    c.execute(sql)
    print c.rowcount
    # exit()
    
    # raw_input()
    
    for row in c.fetchall():
        print row[2]
        print row[0], row[1]
        print "checking in:",
        for block in range(0,len(hulls)):
            print block,
            if in_hull([float(row[0]),float(row[1])],hulls[block]):
                sql = "UPDATE irs_patients SET block = "+ str(block+1) +\
                      " WHERE irspat_lid = "+ str(row[2])
                # print sql
                c.execute(sql)
                print "\nfound in:", block
                break
        print "\n"
        db.commit()
        
def assignActivitiesBlocksViaHull():
    
    sql = "SELECT lat, lng, ca_id FROM containment_activities WHERE district = 'Lahore' AND lat IS NOT NULL AND lng IS NOT NULL"
    c.execute(sql)
    print c.rowcount
    # exit()
    # 2,891,383
    
    for row, i in zip(c.fetchall(), count()):
        print i, row[2]
        print row[0], row[1]
        print "checking in:",
        for block in range(0,len(hulls)):
            print block,
            if in_hull([float(row[0]),float(row[1])],hulls[block]):
                sql = "UPDATE containment_activities SET block = "+ str(block+1) +\
                      " WHERE ca_id = "+ str(row[2])
                # print sql
                c.execute(sql)
                print "\nfound in:", block
                break
        print "\n"
        db.commit()
        
# assignIrsBlocksViaHull()
assignActivitiesBlocksViaHull()