import maya.cmds as cmds
import random

random.seed(1234)
selecttion = cmds.ls(orderedSelection=True, flatten=True)

verts = cmds.ls("pSphere1.vtx[*]", flatten=True)
print(verts)

for idx in range(len(verts)):
    if idx % 3:
        continue
    point = verts[idx]
    print(point)
    scatter_instance = cmds.instance(selecttion[0], name="cube")

    xRot = random.uniform(0, 360)
    yRot = random.uniform(0, 360)
    zRot = random.uniform(0, 360)

    scalingFactor = random.uniform(.5, 3)

    pos = cmds.pointPosition(point, world=True)
    print(pos)
    """move instance to vertices"""
    cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)
    """rotate instance in random direction"""
    cmds.rotate(xRot, yRot, zRot, scatter_instance, worldSpace=True)