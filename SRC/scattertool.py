import maya.cmds as cmds

selecttion = cmds.ls(orderedSelection=True, flatten=True)
vertex_names = cmds.filterExpand(selecttion, selectionMask=31, expand=True)

"""Object to instantiate is the first object selected"""
object_to_instance = selecttion[0]

"""Instantiate objects on vertexes or else there are no objects selected"""
if cmds.objectType(object_to_instance) == 'transform':
    for vertex in vertex_names:
        new_instance = cmds.instance(object_to_instance)
        position = cmds.pointPosition(vertex, world=True)
        cmds.move(position[0], position[1], position[2],  new_instance, absolute=True, worldSpace=True)
else:
    print("Please ensure the first object you select is a transform.")