import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random

log = logging.getLogger(__name__)
selecttion = cmds.ls(orderedSelection=True, flatten=True)

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class ScatterToolUI(QtWidgets.QDialog):
    """Smart Class UI Class"""

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(500)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connection()


    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 19px")
        self.objectToScatter_lbl = QtWidgets.QLabel("Object To Scatter: " + selecttion[0])
        self.objectToScatterTo_lbl = QtWidgets.QLabel("Object To Scatter To: " + selecttion[1])
        self.button_lay = self._create_button_UI()
        self.density_lay = self._create_density_UI()
        self.scale_lay = self._create_scale_UI()
        self.rot_lay = self._create_rotation_UI()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addWidget(self.objectToScatter_lbl)
        self.main_lay.addWidget(self.objectToScatterTo_lbl)
        self.main_lay.addLayout(self.density_lay)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addLayout(self.rot_lay)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_button_UI(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter to whole")
        self.undo_btn = QtWidgets.QPushButton("Undo")
        self.scatterSelection_btn = QtWidgets.QPushButton("Scatter to Selection")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.undo_btn)
        layout.addWidget(self.scatterSelection_btn)
        return layout

    def _create_density_UI(self):
        self.scatterDensity_spx = QtWidgets.QSpinBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("DENSITY:"), -1)
        layout.addWidget(self.scatterDensity_spx)
        return layout

    def _create_scale_UI(self):
        self.maxScale_dspx = QtWidgets.QDoubleSpinBox()
        self.minScale_dspx = QtWidgets.QDoubleSpinBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("SCALE:"), 0)
        layout.addWidget(QtWidgets.QLabel("min:"), 0)
        layout.addWidget(self.minScale_dspx)
        layout.addWidget(QtWidgets.QLabel("max:"), 0)
        layout.addWidget(self.maxScale_dspx)
        return layout

    def _create_rotation_UI(self):
        self.maxRot_spx = QtWidgets.QSpinBox()
        self.maxRot_spx.setMaximum(365)
        self.minRot_spx = QtWidgets.QSpinBox()
        self.minRot_spx.setMaximum(365)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("ROTATION:"), 0)
        layout.addWidget(QtWidgets.QLabel("min angle:"), 0)
        layout.addWidget(self.minRot_spx)
        layout.addWidget(QtWidgets.QLabel("max angle:"), 0)
        layout.addWidget(self.maxRot_spx)
        return layout

    def create_connection(self):
        self.scatter_btn.clicked.connect(self.scatterObject)
        self.undo_btn.clicked.connect(self.UNDO)
        self.scatterSelection_btn.clicked.connect(self.scatterToVerts)

    def scatterToVerts(self):
        random.seed(1234)
        verts = cmds.ls(selection=True, flatten=True)

        for vert in verts:
            pos = cmds.xform([vert], query=True, worldSpace=True, translation=True)
            scatter_instance = cmds.instance(selecttion[0], name="scat_inst")

            xRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())
            yRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())
            zRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())

            scalingFactor = random.uniform(self.minScale_dspx.value(), self.maxScale_dspx.value())

            cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)

            cmds.rotate(xRot, yRot, zRot, scatter_instance, worldSpace=True)
            cmds.scale(scalingFactor, scalingFactor, scalingFactor, scatter_instance, worldSpace=True)

            ncos = cmds.normalConstraint([vert], scatter_instance)
            cmds.delete(ncos)


    def scatterObject(self):
        random.seed(1234)
        objectToScatterTo = str(selecttion[1])

        verts = cmds.ls(objectToScatterTo + ".vtx[*]", flatten=True)
        print(verts)
        """Index feature to help affect the density of the vertices selected """
        for idx in range(len(verts)):
            if idx % self.scatterDensity_spx.value():
                continue
            point = verts[idx]
            print(point)

            """first object selected"""
            scatter_instance = cmds.instance(selecttion[0], name="instance")

            """change instance rotation based on input"""
            xRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())
            yRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())
            zRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())

            """Change instance scale based on input"""
            scalingFactor = random.uniform(self.minScale_dspx.value(), self.maxScale_dspx.value())

            pos = cmds.pointPosition(point, world=True)
            print(pos)
            cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)
            cmds.rotate(xRot, yRot, zRot, scatter_instance, worldSpace=True)
            cmds.scale(scalingFactor, scalingFactor, scalingFactor, scatter_instance, worldSpace=True)
            """normals"""
            ncos = cmds.normalConstraint([point], scatter_instance)
            cmds.delete(ncos)







    def UNDO(self):
        cmds.undo()
"""personal addition, undo button"""
