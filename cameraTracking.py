# ------------------------------------------
# this is the file dealing with the imports of the camera tracking
# ------------------------------------------

import bpy
from mathutils import Vector, Quaternion

C = bpy.context
D = bpy.data


camPosFilePath = "D:\\workspace\\Blender\\3d_gt\\cat\\camera_test.txt"
file = open(camPosFilePath, "r")

for line in file:
    i, x, y, z, rx, ry, rz = line.strip("\n").split(" ")
    print(i, x, y, z, rx, ry, rz)


file.close()