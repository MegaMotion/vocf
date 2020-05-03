
import sys
import os
from scipy import spatial
import numpy as np



def angle_from_up(normal):
    dotprod = np.dot(up_vector, normal)
    angle = np.arccos(dotprod)
    degrees = np.rad2deg([angle])
    return degrees

def veclen(vec):
    length = 0
    if (len(vec)==2):
        length = np.sqrt((vec[0]*vec[0]) + (vec[1]*vec[1]))
    elif (len(vec)==3):
        length = np.sqrt((vec[0]*vec[0]) + (vec[1]*vec[1]) + (vec[2]*vec[2]))
    return length

def vecadd(vec1,vec2):
    sumvec = []
    if (len(vec1)==2):
        sumvec = [vec1[0]+vec2[0],vec1[1]+vec2[1]]
    elif (len(vec1)==3):
          sumvec = [vec1[0]+vec2[0],vec1[1]+vec2[1],vec1[2]+vec2[2]]
    return sumvec

def vecsub(vec1,vec2):
    diffvec = []
    if (len(vec1)==2):
          diffvec = [vec1[0]-vec2[0],vec1[1]-vec2[1]]
    elif (len(vec1)==3):
          diffvec = [vec1[0]-vec2[0],vec1[1]-vec2[1],vec1[2]-vec2[2]]
    return diffvec

def vecscale(vec1,scale):
    scalevec = []
    if (len(vec1)==2):
          scalevec = [vec1[0]*scale,vec1[1]*scale]
    elif (len(vec1)==3):
          scalevec = [vec1[0]*scale,vec1[1]*scale,vec1[2]*scale]
    return scalevec
    
#######################################################

ply_filename = sys.argv[1]
gridsize = 32
gridpoints = 100

pointCount = ""
inBody = False
min_x = 9999999
max_x = -9999999
min_y = 9999999
max_y = -9999999
min_z = 9999999
max_z = -9999999
line_count = 0
points = []
normals = []
up_vector = [0,1,0]

######## maybe all these are obsolete now?
treetop_norm_diff = 15.0  # normal degrees off of vertical we allow for "treetops"
treetop_points = 10       # the number of "highest points" we examine in every cell, as potential treetops
treetop_neighbors = 10    # the number of neighbors that we examine for each potential treetop
min_tree_dist = 20        # if another high point is with this far of an existing treetop, don't count it.
treetop_cluster = 100     # size of cluster we grab for analysis
######## obsolete?





if (len(sys.argv) > 2):
    gridsize = int(sys.argv[2])

if (len(sys.argv) > 3):
    gridpoints = int(sys.argv[3])

    
ply_filename_in = ply_filename + ".ply"
ply_filename_out = ply_filename + "_trees.ply"

print("Finding tree positions. Filename = " + ply_filename_out + ", grid size " + str(gridsize) + ", points per cell " + str(gridpoints))

print("scaled vec: " + str(vecscale([8,8,8],2.5)))

print("vecsub: " + str(vecsub([8,8,8],[2,2,2])))

######################################
#First, open the ply file, read the points and normals, and find the extents and midpoint of the cloud.
ply_in = open(ply_filename_in,"r")
line = ply_in.readline()
while line:
    line = ply_in.readline()
    words = line.split()
    if (len(words)==0):
        break
    if (words[0]=="end_header"):
        inBody = True
        continue
    if (inBody):
        if (float(words[0]) < min_x):
            min_x = float(words[0])
        if (float(words[0]) > max_x):
            max_x = float(words[0])
        if (float(words[1]) < min_y):
            min_y = float(words[1])
        if (float(words[1]) > max_y):
            max_y = float(words[1])
        if (float(words[2]) < min_z):
            min_z = float(words[2])
        if (float(words[2]) > max_z):
            max_z = float(words[2])
        line_count += 1
        points.append([float(words[0]),float(words[1]),float(words[2])])
        normals.append([float(words[3]),float(words[4]),float(words[5])])
        #print("appending point: " + words[0] + " "  + words[1] + " " + words[2] + " normal " + words[3] + " "  + words[4] + " " + words[5])

ply_in.close()

mid_x = (max_x + min_x)/2
mid_y = (max_y + min_y)/2
mid_z = (max_z + min_z)/2

diff_x = max_x - min_x
diff_y = max_y - min_y
diff_z = max_z - min_z

print("mid point: " + str(mid_x) + " " + str(mid_y) + " " + str(mid_z))
print("min point: " + str(min_x) + " " + str(min_y) + " " + str(min_z))
print("max point: " + str(max_x) + " " + str(max_y) + " " + str(max_z))
print("max point: " + str(max_x) + " " + str(max_y) + " " + str(max_z))




######################################
#Next, turn the points into a numpy array and hand it to a KDTree.

array_points = np.array(points)
pointtree = spatial.KDTree(array_points)
print(str(pointtree.data))

x_step = diff_x / gridsize
z_step = diff_z / gridsize
start_x = min_x + x_step/2
start_z = min_z + z_step/2
current_x = start_x
current_z = start_z

pointset = []
top_points = []
#for x in range(gridsize):
#    for z in range(gridsize):
for x in range(gridsize):  # only do one square while we're testing.
    current_x = start_x + (x * x_step)
    for z in range(gridsize):
        pointset = []
        current_z = start_z + (z * z_step)
        current_point = [current_x,mid_y,current_z]
        matches = pointtree.query(current_point,gridpoints)
        #print("gridpoint: " + str(current_point))
        #print("matches: " + str(matches))
        for i in matches[1]:
            pos = points[i]
            normal = normals[i]
            #pointset.append(pos + normal)
            pointset.append(pos)
            
        #sort the pointset by height
        sorted_pointset = sorted(pointset, key=lambda x: x[1], reverse=True)
        topmost = sorted_pointset[0]
        last_topmost = [0,0,0]
        sanity_count = 0;
        while ((np.array_equal(topmost,last_topmost) == False) and (sanity_count < 5)):
            pointset = []
            sanity_count += 1
            last_topmost = topmost
            matches = pointtree.query(topmost,gridpoints)
            for i in matches[1]:
                pos = points[i]
                normal = normals[i]
                #pointset.append(pos + normal)
                pointset.append(pos)
            sorted_pointset = sorted(pointset, key=lambda x: x[1], reverse=True)
            topmost = sorted_pointset[0]
            #print("Next topmost = " + str(topmost))
        #print("TREE LOCATION: " + str(topmost))
        if topmost not in top_points:
            top_points.append(topmost)
        
        
print("\ntop points: " + str(len(top_points)) + "\n" + str(top_points))


#open the output file
ply_out = open(ply_filename_out,"w+")
ply_out.write("ply\n")
ply_out.write("format ascii 1.0\n")
ply_out.write("comment Original LiDAR: USGS National Dataset\n")
ply_out.write("comment Cropped and converted to PLY by CloudCompare v2.11 alpha (Anoia)\n")
ply_out.write("comment Treetop positions derived via algorithm by Chris Calef.\n")
ply_out.write("element vertex " + str(len(top_points)) + "\n")
ply_out.write("property float x\n")
ply_out.write("property float y\n")
ply_out.write("property float z\n")
ply_out.write("end_header\n")
for p in top_points:
    ply_out.write(str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + "\n")
