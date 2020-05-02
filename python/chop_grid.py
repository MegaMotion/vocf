#!/c/Python27/python


# Take a point cloud and move it so that it is centered on the origin and lowered such
#that its lowest point is at zero. Also flip axes so that it works with Z up right handed.

import sys


ply_filename = sys.argv[1]

ply_filename_in = ply_filename + ".ply"

points = []
cols = 25
for i in range(cols):
    col = []
    points.append(col)

print(points) 


inBody = False
min_x = 99999999
max_x = 0
min_y = 99999999
max_y = 0
min_z = 99999999
max_z = 0
line_count = 0

start_x = -2000
start_y = -2000
step_x = 800
step_y = 800


#Open the input file
ply_in = open(ply_filename_in,"r")
line = ply_in.readline()
while line:
    #print("Line {}: {}".format(cnt, line.strip()))
    line = ply_in.readline()
    words = line.split()
    if (len(words)==0):
        break
    if (words[0]=="end_header"):
        inBody = True
        continue
    if (inBody):
        for x in range(5):
            for y in range(5):
                if ((float(words[0]) >= start_x + (x * step_x)) and \
                    (float(words[0]) < start_x + ((x+1) * step_x)) and \
                    (float(words[1]) >= start_y + (y * step_y)) and \
                    (float(words[1]) < start_y + ((y+1) * step_y)) ):
                     points[(y*5)+x].append(str(words[0]) + " " + str(words[1]) + " " + str(words[2]) + "\n")
        line_count += 1
        print("reading line: " + str(line_count))

ply_in.close()

mid_x = (max_x + min_x)/2
mid_y = (max_y + min_y)/2
mid_z = (max_z + min_z)/2
print("mid point: " + str(mid_x) + " " + str(mid_y) + " " + str(mid_z))


for x in range(5):
    for y in range(5):
        i = (y*5)+x
        print("Count " + str(x) + "_" + str(y) + ": " + str(len(points[i])))
        if (len(points[i])>0):
            ply_filename_out = "points_" + str(x+1) + "_" + str(y+1) + ".ply"
            ply_out = open(ply_filename_out,"w+")
            ply_out.write("ply\n")
            ply_out.write("format ascii 1.0\n")
            ply_out.write("comment Original LiDAR: USGS National Dataset\n")
            ply_out.write("comment Cropped and converted to PLY by CloudCompare v2.11 alpha (Anoia)\n")
            ply_out.write("comment Converted from original position to centered position by Chris Calef.\n")
            ply_out.write("element vertex " + str(len(points[i])) + "\n")
            ply_out.write("property float x\n")
            ply_out.write("property float y\n")
            ply_out.write("property float z\n")
            ply_out.write("end_header\n")
            for c in range(len(points[i])):
                ply_out.write(points[i][c])
            ply_out.close()
            
print ("Success!")




#print "Line count: " + str(linecount)



#

#start_elev = 0.0 # just in case you need a manual adjust, try not to.
#for row in c.execute(query):
#    if (start_elev == 0.0):
#        start_elev = row[2]
#        print "Starting elevation: " + str(start_elev)

#    colorString = material_colors[4] #temp, just picked a visible color
#    ply_out.write(str(row[1]) + " " + str(row[2] - start_elev) + " " + str(row[0]) + " " + colorString + "\n")


