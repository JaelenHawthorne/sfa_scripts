import maya.cmds as cmds
selecttion = cmds.ls(orderedSelection=True, flatten=True)


verts = cmds.ls("pSphere1.vtx[*]", flatten = True)
print(verts)

for point in verts:
    print(point)
    scatter_instance = cmds.instance(selecttion[0], name = "cube")
    pos = cmds.pointPosition(point, world = True)
    print(pos)
    cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)