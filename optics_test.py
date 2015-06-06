from optics_geo import *
from db_conn import *
from larvae_midpoint_list import *
from math import cos, sin, atan2, sqrt
import math

def midpoint(pointA, pointB):
    lonA = math.radians(pointA.longitude)
    lonB = math.radians(pointB.longitude)
    latA = math.radians(pointA.latitude)
    latB = math.radians(pointB.latitude)

    dLon = lonB - lonA

    Bx = math.cos(latB) * math.cos(dLon)
    By = math.cos(latB) * math.sin(dLon)

    latC = math.atan2(math.sin(latA) + math.sin(latB),
                  math.sqrt((math.cos(latA) + Bx) * (math.cos(latA) + Bx) + By * By))
    lonC = lonA + math.atan2(By, math.cos(latA) + Bx)
    lonC = (lonC + 3 * math.pi) % (2 * math.pi) - math.pi

    return Point(math.degrees(latC), math.degrees(lonC))

def midPointOfList(coords):
    
    if len(coords) <= 1: return False    
    
    new = coords[0]
    for coord in coords[1:]:
        new = midpoint(new, coord)
    return new

def getData(year = False, _type="p"):
    
    db     = DB()
    coords = []
    
    if year:
        date = {"start": year+"-08-01", "end": year+"-12-31"}
        sql = {
            "p": "SELECT DISTINCT lat, lng FROM irs_patients WHERE tag='irs_patient' AND district = 'Lahore' AND created_at BETWEEN '"+date["start"]+"' AND '"+date["end"]+"'",
            "l":   "SELECT DISTINCT lat, lng FROM positive_larvae WHERE district = 'Lahore' AND created_at BETWEEN '"+date["start"]+"' AND '"+date["end"]+"'"
        }
    else:
        print "** Parameter Missing: Year"
        exit()

    db.query(sql[_type])
    for row in db.fetchall():
        coords.append(Point(float(row[0]), float(row[1])))

    return coords

def larvaeNormalization(year):
    points = getData(year, "l")
    optics = Optics(points, 10, 2) # 100m radius for neighbor consideration, cluster size >= 2 points
    optics.run()                    # run the algorithm
    clusters = optics.cluster(10)   # 50m threshold for clustering
    new_list = []
    for cluster, i in zip(clusters, range(0,len(clusters))):
        print i, cluster.points
        new = midPointOfList(cluster.points)
        new_list.append(new)
    return new_list


year     = "2015"
larvae   = [Point(x[0], x[1]) for x in larvae[year]]
patients = getData(year, "p")
points   = larvae + patients

radius, csize = 100, 5
optics = Optics(points, radius, csize) # 100m radius for neighbor consideration, cluster size >= 5 patients+larvae
optics.run()                    # run the algorithm
clusters = optics.cluster(radius)   # 50m threshold for clustering
count = 0

for cluster, i in zip(clusters, range(0,len(clusters))):
    count += len(cluster.points)
    print "#", i, "S:", len(cluster.points), "P:", cluster.points

print " ==> Total Points:", len(points), "Clustered Points:", count, "Total Clusters:", len(clusters)