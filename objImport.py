# --------------------------------------------
# this file is to import the cat or bunny obj into blender
# --------------------------------------------

import bpy
from 

objFilePath = "D:\\workspace\\Blender\\3d_gt\\cat\\cat.obj"
imported_obj = bpy.ops.import_scene.obj(filepath = objFilePath)

obj_bunny = bpy.context.selected_objects[0]
obj_bunny.scale = (0.7, 0.7, 0.7)

