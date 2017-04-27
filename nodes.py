
#---------------------------------------------------
# File nodes.py
#---------------------------------------------------
import bpy, bpy.context

# define convenience variables as terminal
C = bpy.context
D = bpy.data


# switch on nodes
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

 
# clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)

#---------------------------------------------------
# set the nodes as motion traking defaults
#---------------------------------------------------


# create the movie clip input node
movClip = tree.nodes.new('CompositorNodeMovieClip')
movClip.name = 'movClip'
movClip.location = -200, 0
# load the movie into blender
movieFilePath = "D:\\workspace\\Blender\\3d_gt\\cat\\cat_video.avi"
mv = C.blend_data.movieclips.load(movieFilePath)
# set the clip for the movie clip node
movClip.clip = mv


# create the undistortion node
undis = tree.nodes.new('CompositorNodeMovieDistortion')
undis.name = 'undis'
undis.location = 0,0
undis.clip = mv
# set the link between movie clip node and the distortion node
links.new(movClip.outputs[0], undis.inputs[0])


# create the scale node
scale = tree.nodes.new('CompositorNodeScale')
scale.name = 'scale'
scale.location = 200,0
# coordiante space to scale relative to
scale.space = 'RENDER_SIZE'
# set the link between distortion node and scale node
links.new(undis.outputs[0], scale.inputs[0])


# create the render layer node
# this is based ont the assumption that there have already been a background layer
# ----------------------------------------------
# this is to be amended as to set the layer
# also, check is needed to see if there is such a layer
# --------------------------------------
rLayer1 = tree.nodes.new('CompositorNodeRLayers')
rLayer1.name = 'rLayer1'
rLayer1.location = -200, -400


# create the invert layer
invert = tree.nodes.new('CompositorNodeInvert')
invert.name = 'invert'
invert.location = 0,-400
# set the link between render layer node and the color invert node
links.new(rLayer1.outputs[1], invert.inputs[1])


# create the color add node
add1 = tree.nodes.new('CompositorNodeMixRGB')
add1.name = 'add1'
add1.location = 200, -400
# set the blend type for the color mix node: add 
add1.blend_type = 'ADD'
# set the link between invert node and the color mix node
links.new(invert.outputs[0], add1.inputs[1])
# ------------------------------------------------------
# there is another link between rlayer and add node
# but since there is something wrong to be amended with rlayer
# this is set to be done too
# ------------------------------------------------------


# create another color add node
add2 = tree.nodes.new('CompositorNodeMixRGB')
add2.name = 'add2'
add2.location = 200, -600
# set the blend type for the color mix node: add 
add2.blend_type = 'ADD'
# set the link between invert node and the color mix node
links.new(invert.outputs[0], add2.inputs[1])
# ------------------------------------------------------
# there is another link between rlayer and add node
# but since there is something wrong to be amended with rlayer
# this is set to be done too
# ------------------------------------------------------


# create the color multiply node
mul = tree.nodes.new('CompositorNodeMixRGB')
mul.name = 'mul'
mul.location = 400, -400
# set the blend type for the color mix node: multiply
mul.blend_type = 'MULTIPLY'
# set the default value for the multiply node
mul.inputs[0].default_value = 0.8
# set the link between color add nodes and the color multiply node
links.new(add1.outputs[0], mul.inputs[1])
links.new(add2.outputs[0], mul.inputs[2])


# create the second multiply node
mul2 = tree.nodes.new('CompositorNodeMixRGB')
mul2.name = 'mul2'
mul2.location = 600,-200
# set the blend type for the color mix node: multiply
mul2.blend_type = 'MULTIPLY'
# set the default value for the multiply node
mul2.inputs[0].default_value = 0.8
# set the link between the scale node and the muliply node
links.new(scale.outputs[0], mul2.inputs[1])
# set the link between the first multiply node and the second one
links.new(mul.outputs[0], mul2.inputs[2])


# create the second render layer
# this is based ont the assumption that there have already been a background layer
# ----------------------------------------------
# this is to be amended as to set the layer
# also, check is needed to see if there is such a layer
# --------------------------------------
rLayer2 = tree.nodes.new('CompositorNodeRLayers')
rLayer2.name = 'rLayer2'
rLayer2.location = -200, -800


# create the vector blur node
vecBlur = tree.nodes.new('CompositorNodeVecBlur')
vecBlur.name = 'vecBlur'
vecBlur.location = 600, -800
# set the default values for the vecotr blur node
vecBlur.factor = 0.75
# set the links between the second render layer and the vector blur node
links.new(rLayer2.outputs[0], vecBlur.inputs[0])
links.new(rLayer2.outputs[2], vecBlur.inputs[1])
# there is still something to be fixed, or all the links are to be fixed
# ----------------------------------------------------------
# need attention here
# ----------------------------------------------------------
links.new(rLayer2.outputs['Speed'], vecBlur.inputs['Speed'])


# create the alpha over node
alphaOver = tree.nodes.new('CompositorNodeAlphaOver')
alphaOver.name = 'alphaOver'
alphaOver.location = 800, -400
# set the links between the multiply node and the alpha over node
links.new(mul2.outputs[0], alphaOver.inputs[1])
# set the links between the vector blur node and the alpha over node
links.new(vecBlur.outputs[0], alphaOver.inputs[2])


# create the output node compositor
compo = tree.nodes.new('CompositorNodeComposite')
compo.name = 'compo'
compo.location = 1000, -200
# set the links between the alphaover node and the composite node
links.new(alphaOver.outputs[0], compo.inputs[0])


# create the output node viewer
viewer = tree.nodes.new('CompositorNodeViewer')
viewer.name = 'viewer'
viewer.location = 1000, -600
# set the links between the alpha over node and the viewer node
links.new(alphaOver.outputs[0], viewer.inputs[0])