
import sys
import os
from scipy import spatial
import numpy as np


ply_filename = sys.argv[1]
ply_filename_in = ply_filename + ".ply"
ply_filename_out = ply_filename + "_trees.ply"

print("Finding tree positions...")

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

#HERE: open the file and find the extents... necessary?
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
print("mid point: " + str(mid_x) + " " + str(mid_y) + " " + str(mid_z))
print("min point: " + str(min_x) + " " + str(min_y) + " " + str(min_z))
print("max point: " + str(max_x) + " " + str(max_y) + " " + str(max_z))

array_points = np.array(points)
pointtree = spatial.KDTree(array_points)
print(str(pointtree.data))

current_point = [0,0,0]
matches = pointtree.query(current_point,10)

print(str(matches))

neighbor_pnts = []
neighbor_pnts = []
for i in matches[1]:
    print(str(i) + " " + str(points[i]) + " " + str(normals[i]))
    norm = normals[i]
    


print("")


print(str(matches[0][0]) + "   " + str(matches[1][0]))


vector_1 = [0, 1]
vector_2 = [1, 0]


unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
dot_product = np.dot(unit_vector_1, unit_vector_2)
angle = np.arccos(dot_product)

print(angle)
