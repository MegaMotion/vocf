
import bpy
import os
import sys
from mathutils import Matrix, Vector



#ply_filename = sys.argv[1]
ply_filename = "D:/OCF2020/canopy_2_5_center.ply"

inBody = False
min_x = 99999999
max_x = 0
min_y = 99999999
max_y = 0
min_z = 99999999
max_z = 0
line_count = 0

ply_in = open(ply_filename,"r")
line = ply_in.readline()

objectname = "Plane"
bpy.data.objects[objectname].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[objectname]


while line:
    line = ply_in.readline()
    words = line.split()
    if (len(words)==0):
        break
    if (words[0]=="end_header"):
        inBody = True
        continue
    if (inBody):
        line_count += 1
        print("reading line: " + str(line_count))
        
        bpy.context.view_layer.objects.active = None
        for obj in bpy.context.selected_objects:
            obj.select_set(False)            
        #Now select cube again
        bpy.data.objects[objectname].select_set(True)        
        bpy.context.view_layer.objects.active = bpy.data.objects[objectname]
        mw = bpy.data.objects[objectname].matrix_world.copy()
        bpy.ops.object.duplicate_move()
        posX = float(words[0])
        posY = float(words[1])
        posZ = float(words[2])
        normX = float(words[3])
        normY = float(words[4])
        normZ = float(words[5])
        
        normVec = Vector((normX,normY,normZ))        
        axis_dst = Vector((0, 0, 1))
        #matrix_rotate = matrix_rotate * normVec.rotation_difference(axis_dst).to_matrix()
        matrix_rotate = normVec.rotation_difference(axis_dst).to_matrix()
        #bpy.ops.transform.rotate(matrix_rotate)
        #print(str(matrix_rotate))
        obj = bpy.context.selected_objects[0]
        m = matrix_rotate
        matrix_4x4 = [[m[0][0],m[0][1],m[0][2],0],[m[1][0],m[1][1],m[1][2],0],[m[2][0],m[2][1],m[2][2],0],[0,0,0,1]]
        obj.matrix_world = matrix_4x4
        bpy.ops.transform.resize(value=(8.0,8.0,8.0))
        bpy.ops.transform.translate(value=(posX,posY,posZ))
        

ply_in.close()

mid_x = (max_x + min_x)/2
mid_y = (max_y + min_y)/2
mid_z = (max_z + min_z)/2
print("mid point: " + str(mid_x) + " " + str(mid_y) + " " + str(mid_z))



