import MySQLdb, csv, numpy as np
from itertools import izip as zip, count

np.set_printoptions(threshold='nan')

db = MySQLdb.connect(host="127.0.0.1", db="containment", user="root", passwd="")
c  = db.cursor()

prefix    = "__KMEANS__19"
prefix_ch = prefix + "convex_hull_"

hulls = {}
for cluster in range(0,19):
    file = csv.reader(open(prefix_ch+"cluster"+str(cluster)+".csv","rb"))
    hulls[cluster] = np.array([[x[0], x[1]] for x in file])

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
    
def assignIrsPatientClusters():
    for cluster in range(0,19):
        file = csv.reader(open(prefix+"cluster"+str(cluster)+".csv","rb"))
        for row in file:
            # print row, cluster+1
            sql = "UPDATE irs_patients SET cluster = "+ str(cluster+1) +\
                  " WHERE tag='irs_patient' AND cluster = 0 AND lat = "+ str(row[0]) +" AND lng = "+str(row[1])+ " AND DATE(created_at) = '"+str(row[2])+"'"
            # print sql
            c.execute(sql)
        print cluster
        db.commit()
        
def assignIrsActivitiesClustersViaHull():
    
    sql = "SELECT lat, lng, irspat_lid FROM irs_patients WHERE tag = 'irs' AND district = 'Lahore' AND cluster = 0 AND lat IS NOT NULL AND lng IS NOT NULL"
    
    c.execute(sql)
    print c.rowcount
    
    # raw_input()
    
    for row in c.fetchall():
        print row[2]
        # print row[0], row[1]
        # print "checking in:",
        for cluster in range(0,19):
            # print cluster,
            if in_hull([float(row[0]),float(row[1])],hulls[cluster]):
                sql = "UPDATE irs_patients SET cluster = "+ str(cluster+1) +\
                      " WHERE tag = 'irs' AND irspat_lid = "+ str(row[2])
                # print sql
                c.execute(sql)
                print "\nfound in:", cluster
                break
        print "\n"
        db.commit()
def assignPatientsClustersViaHull():
    
    sql = "SELECT lat, lng, irspat_lid FROM irs_patients WHERE district = 'Lahore' AND cluster = 0 AND tag = 'irs_patient' AND lat IS NOT NULL AND lng IS NOT NULL"
    # sql = "SELECT lat, lng, ca_id FROM containment_activities WHERE ca_id in (SELECT irspat_lid FROM irs_patients WHERE district = 'Lahore' AND tag = 'irs_patient')"
    c.execute(sql)
    
    for row in c.fetchall():
        print row[2]
        print row[0], row[1]
        print "checking in:",
        for cluster in range(0,19):
            print cluster,
            if in_hull([float(row[0]),float(row[1])],hulls[cluster]):
                sql = "UPDATE irs_patients SET cluster = "+ str(cluster+1) +\
                      " WHERE irspat_lid = "+ str(row[2])
                # print sql
                c.execute(sql)
                print "\nfound in:", cluster
                break
        print "\n"
        db.commit()
    

def assignActivitiesClustersViaHull():
    
    sql = "SELECT lat, lng, ca_id FROM containment_activities WHERE district = 'Lahore' AND cluster = 0 AND lat IS NOT NULL AND lng IS NOT NULL"
    c.execute(sql)
    
    for row in c.fetchall():
        print row[2]
        # print row[0], row[1]
        # print "checking in:",
        for cluster in range(0,19):
            # print cluster,
            if in_hull([float(row[0]),float(row[1])],hulls[cluster]):
                sql = "UPDATE containment_activities SET cluster = "+ str(cluster+1) +\
                      " WHERE ca_id = "+ str(row[2])
                # print sql
                c.execute(sql)
                print "found in:", cluster
                break
        # print "\n"
        db.commit()
        
        # exit()
    
def assignIrsActivitiesTownClustersViaHull():
    
    sql = "SELECT lat, lng, irspat_lid FROM irs_patients WHERE tag = 'irs' AND district IS NULL AND lat IS NOT NULL AND lng IS NOT NULL"
    
    c.execute(sql)
    print c.rowcount
    
    # raw_input()
    
    for row in c.fetchall():
        print row[2]
        # print row[0], row[1]
        # print "checking in:",
        for cluster in range(0,19):
            # print cluster,
            if in_hull([float(row[0]),float(row[1])],hulls[cluster]):
                sql = "UPDATE irs_patients SET cluster = "+ str(cluster+1) +\
                      " WHERE tag = 'irs' AND irspat_lid = "+ str(row[2])
                # print sql
                c.execute(sql)
                print "\nfound in:", cluster
                break
        print "\n"
        db.commit()
def assignIrsPatientsTownClustersViaHull():
    
    sql = "SELECT lat, lng, irspat_lid FROM irs_patients WHERE tag = 'irs_patient' AND district IS NULL AND lat IS NOT NULL AND lng IS NOT NULL"
    
    c.execute(sql)
    print c.rowcount
    
    # raw_input()
    
    for row in c.fetchall():
        print row[2]
        # print row[0], row[1]
        # print "checking in:",
        for cluster in range(0,19):
            # print cluster,
            if in_hull([float(row[0]),float(row[1])],hulls[cluster]):
                sql = "UPDATE irs_patients SET district = 'Lahore' AND cluster = "+ str(cluster+1) +\
                      " WHERE tag = 'irs_patient' AND irspat_lid = "+ str(row[2])
                # print sql
                c.execute(sql)
                print "\nfound in:", cluster
                break
        print "\n"
        db.commit()
        
def assignActivitiesTownClustersViaHull():
    
    sql = "SELECT lat, lng, ca_id FROM containment_activities WHERE district IS NULL AND lat IS NOT NULL AND lng IS NOT NULL"
    
    c.execute(sql)
    print c.rowcount
    
    # raw_input()
    
    for row in c.fetchall():
        # print row[2]
        # print row[0], row[1]
        # print "checking in:",
        for cluster in range(0,19):
            # print cluster,
            if in_hull([float(row[0]),float(row[1])],hulls[cluster]):
                sql = "UPDATE containment_activities SET district = 'Lahore' AND cluster = "+ str(cluster+1) +\
                      " WHERE ca_id = "+ str(row[2])
                # print sql
                c.execute(sql)
                print row[2],"found in:", cluster+1
                break
        # print "\n"
        db.commit()
# assignIrsPatientClusters()
assignActivitiesClustersViaHull()
# assignPatientsClustersViaHull()
# assignIrsActivitiesClustersViaHull()
# assignIrsActivitiesTownClustersViaHull()
# assignIrsPatientsTownClustersViaHull()
# assignActivitiesTownClustersViaHull()