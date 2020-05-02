#!/c/Python27/python


# Take a point cloud and move it so that it is centered on the origin and lowered such
#that its lowest point is at zero. Also flip axes so that it works with Z up right handed.

import sys
import os

ply_filename = sys.argv[1]

ply_filename_in = ply_filename + ".ply"
ply_filename_out = ply_filename + "_center.ply"

print ("Converting ply file '" + ply_filename_in + "' to '" + ply_filename_out + "'...")



pointCount = ""
inBody = False
min_x = 9999999
max_x = -9999999
min_y = 9999999
max_y = -9999999
min_z = 9999999
max_z = -9999999
line_count = 0

#Open the input file
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
        #print("reading line: " + str(line_count))

ply_in.close()

line_count = 0
mid_x = (max_x + min_x)/2
mid_y = (max_y + min_y)/2
mid_z = (max_z + min_z)/2
print("mid point: " + str(mid_x) + " " + str(mid_y) + " " + str(mid_z))
print("min point: " + str(min_x) + " " + str(min_y) + " " + str(min_z))
print("max point: " + str(max_x) + " " + str(max_y) + " " + str(max_z))

      
#open the output file
ply_out = open(ply_filename_out,"w+")
ply_out.write("ply\n")
ply_out.write("format ascii 1.0\n")
ply_out.write("comment Original LiDAR: USGS National Dataset\n")
ply_out.write("comment Cropped and converted to PLY by CloudCompare v2.11 alpha (Anoia)\n")
ply_out.write("comment Converted from original position to centered position by Chris Calef.\n")

inBody = False
ply_in = open(ply_filename_in,"r")
line = ply_in.readline()
while line:
    line = ply_in.readline()
    words = line.split()
    if (len(words)==0):
        break
    if (words[0]=="element" and words[1]=="vertex"):
        print ("Point count: " + words[2])
        pointCount = words[2]
        ply_out.write("element vertex " + str(pointCount) + "\n") 
        ply_out.write("property float x\n")
        ply_out.write("property float y\n")
        ply_out.write("property float z\n")
        ply_out.write("end_header\n")
        
    if (words[0]=="end_header"):
        inBody = True
        continue

    #Now, finally, print the values. Have to flip sign on the X axis and trade Y for Z. #OR NOT
    if (inBody == True):
        ply_out.write(str(round((float(words[0])-mid_x),2)) + " " + str(round((float(words[2]) - min_z),2)) + " " + str(-1 * round((float(words[1])-mid_y),2)) + "\n")
        #ply_out.write(str(round((float(words[0])-mid_x),2)) + " " + str(round((float(words[1]) - mid_y),2)) + " " + str(round((float(words[2])-min_z),2)) + " " + str(-1 * float(words[3])) + " " + str(words[4]) + " " + str(words[5]) + "\n")
        line_count += 1
        print("writing line: " + str(line_count))

print ("Success!")

ply_in.close()
ply_out.close()

print("mid point: " + str(mid_x) + " " + str(mid_y) + " " + str(mid_z))
print("min point: " + str(min_x) + " " + str(min_y) + " " + str(min_z))
print("max point: " + str(max_x) + " " + str(max_y) + " " + str(max_z))



#

#start_elev = 0.0 # just in case you need a manual adjust, try not to.
#for row in c.execute(query):
#    if (start_elev == 0.0):
#        start_elev = row[2]
#        print "Starting elevation: " + str(start_elev)

#    colorString = material_colors[4] #temp, just picked a visible color
#    ply_out.write(str(row[1]) + " " + str(row[2] - start_elev) + " " + str(row[0]) + " " + colorString + "\n")


