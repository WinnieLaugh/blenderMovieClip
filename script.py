#---------------------------------------------------
# File nodes.py
#---------------------------------------------------
import bpy
 
# switch on nodes
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links
 
# clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)
 
# create input render layer  node
rl = tree.nodes.new('CompositorNodeRLayers')
rl.location = 0, 200
 
# create SEP_RGBA node
sep = tree.nodes.new('CompositorNodeSepRGBA')
sep.name = "Split"
sep.location = 200, 200
links.new(rl.outputs[0], sep.inputs[0])  # image-image
 
# create VIEWER node
viewer = tree.nodes.new('CompositorNodeViewer')
viewer.label = "Alpha"
viewer.location = 400, 400
links.new(sep.outputs[3], viewer.inputs[0])  # A-image
 
# create COMBRGBA node
comb = tree.nodes.new('CompositorNodeCombRGBA')
comb.label = "Cyan"
comb.location = 400, 200
links.new(sep.outputs[1], comb.inputs[2])  # G - B
links.new(sep.outputs[2], comb.inputs[1])  # B - G
 
# create HUE_SAT node
hs = tree.nodes.new('CompositorNodeHueSat')
hs.label = "Violet"
hs.location = 600, 200
hs.color_hue = 0.75
hs.color_saturation = 1.5
links.new(comb.outputs[0], hs.inputs[1])  # image-image
 
# create output node
comp = tree.nodes.new('CompositorNodeComposite')
comp.location = 600, 400
links.new(hs.outputs[0], comp.inputs[0])  # image-image