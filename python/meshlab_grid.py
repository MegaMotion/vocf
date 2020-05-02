#!/c/Python27/python


# Take a point cloud and move it so that it is centered on the origin and lowered such
#that its lowest point is at zero. Also flip axes so that it works with Z up right handed.

import sys
import os


#cmdString = "meshlabserver.exe -i D:\OCF2020\canopy\off-ground-points_1_1.ply"
#cmdString += " -o D:\OCF2020\canopy\canopy_test_1_1.ply -m sa"
#os.system(cmdString)

#gridfiles = ["off-ground-points_1_3"]

gridfiles = ["off-ground-points_1_1","off-ground-points_1_2","off-ground-points_1_3","off-ground-points_1_4","off-ground-points_1_5","off-ground-points_2_1","off-ground-points_2_2","off-ground-points_2_3","off-ground-points_2_4","off-ground-points_2_5","off-ground-points_3_1","off-ground-points_3_2","off-ground-points_3_3","off-ground-points_3_4","off-ground-points_3_5","off-ground-points_4_2","off-ground-points_4_3","off-ground-points_4_4","off-ground-points_4_5","off-ground-points_5_3","off-ground-points_5_4","off-ground-points_5_5"]

for n in gridfiles:
    fullname = n + "_center.ply"
    outputname = n + ".obj"
    print(fullname)
    cmdString = "meshlabserver -i " + fullname + " -o " + outputname + " -m sa -s sampling.mlx"
    os.system(cmdString)


