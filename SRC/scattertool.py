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
        self.objectToScatter_lbl = QtWidgets.QLabel("Object To Scatter: " + selecttion[-1])
        self.objectToScatterTo_lbl = QtWidgets.QLabel("Object To Scatter To: " + selecttion[0])
        self.button_lay = self._create_button_UI()
        self.scale_lay = self._create_scale_UI()
        self.rot_lay = self._create_rotation_UI()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addWidget(self.objectToScatter_lbl)
        self.main_lay.addWidget(self.objectToScatterTo_lbl)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addLayout(self.rot_lay)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_button_UI(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.undo_btn = QtWidgets.QPushButton("Undo")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.undo_btn)
        return layout

    def _create_scale_UI(self):
        self.maxScale_dspx = QtWidgets.QDoubleSpinBox()
        self.minScale_dspx = QtWidgets.QDoubleSpinBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("SCALE"), 1, 0)
        layout.addWidget(QtWidgets.QLabel("min"), 1, 2)
        layout.addWidget(self.minScale_dspx)
        layout.addWidget(QtWidgets.QLabel("max"), 1, 3)
        layout.addWidget(self.maxScale_dspx)
        return layout

    def _create_rotation_UI(self):
        self.maxRot_spx = QtWidgets.QSpinBox()
        self.minRot_spx = QtWidgets.QSpinBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("ROTATION"), 1, 0)
        layout.addWidget(QtWidgets.QLabel("min angle"), 1, 2)
        layout.addWidget(self.minRot_spx)
        layout.addWidget(QtWidgets.QLabel("max angle"), 1, 3)
        layout.addWidget(self.maxRot_spx)
        return layout

    def create_connection(self):
        self.scatter_btn.clicked.connect(self.scatterObject)
        self.undo_btn.clicked.connect(self.UNDO)

    def scatterObject(self):
        random.seed(1234)


        objectToScatterTo = str(selecttion[1])

        verts = cmds.ls(objectToScatterTo + ".vtx[*]", flatten=True)
        print(verts)

        for idx in range(len(verts)):
            if idx % 3:
                continue
            point = verts[idx]
            print(point)
            scatter_instance = cmds.instance(selecttion[0], name="instance")

            xRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())
            yRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())
            zRot = random.uniform(self.minRot_spx.value(), self.maxRot_spx.value())

            scalingFactor = random.uniform(self.minScale_dspx.value(), self.maxScale_dspx.value())

            pos = cmds.pointPosition(point, world=True)
            print(pos)
            cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)
            cmds.rotate(xRot, yRot, zRot, scatter_instance, worldSpace=True)
            cmds.scale(scalingFactor, scalingFactor, scalingFactor, scatter_instance, worldSpace=True)





    def UNDO(self):
        cmds.undo()
"""special button for next assignment, undo button"""
