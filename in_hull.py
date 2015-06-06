import numpy as np
import csv

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

cluster_file = csv.reader(open('LahoreKMEANS20cluster0.csv'))
hull_file = csv.reader(open('LahoreKMEANS20convex_hull_cluster0.csv'))

cluster_coords = np.array([[x[0], x[1]] for x in cluster_file])
hull_coords = np.array([[x[0], x[1]] for x in hull_file])

print in_hull(cluster_coords,hull_coords)