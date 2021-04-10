import logging
import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter Tool UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(600)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()
        self.scatterobject = ScatterObject()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        layout = self.layout_setup()
        layout.addWidget(self.title_lbl)
        layout.addLayout(self.scatter_field_lay)
        layout.addLayout(self.xrot_rand_lay)
        layout.addLayout(self.yrot_rand_lay)
        layout.addLayout(self.zrot_rand_lay)
        layout.addLayout(self.xscale_rand_lay)
        layout.addLayout(self.yscale_rand_lay)
        layout.addLayout(self.zscale_rand_lay)
        layout.addStretch()
        layout.addLayout(self.bottom_button_rand_lay)
        return layout

    def layout_setup(self):
        main_lay = QtWidgets.QVBoxLayout()
        self.layout_creation()
        self.xrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xrot_rand_lay.setRowMinimumHeight(1, 20)
        self.yrot_rand_lay.setRowMinimumHeight(0, 20)
        self.zrot_rand_lay.setRowMinimumHeight(0, 20)
        self.xscale_rand_lay.setRowMinimumHeight(0, 40)
        self.yscale_rand_lay.setRowMinimumHeight(0, 20)
        self.zscale_rand_lay.setRowMinimumHeight(0, 20)
        self.bottom_button_rand_lay.setRowMinimumHeight(0, 20)
        self.setLayout(main_lay)
        return main_lay

    def layout_creation(self):
        self.scatter_field_lay = self._create_scatter_field_ui()
        self.xrot_rand_lay = self._create_xrot_rand_field_ui()
        self.yrot_rand_lay = self._create_yrot_rand_field_ui()
        self.zrot_rand_lay = self._create_zrot_rand_field_ui()
        self.xscale_rand_lay = self._create_xscale_rand_field_ui()
        self.yscale_rand_lay = self._create_yscale_rand_field_ui()
        self.zscale_rand_lay = self._create_zscale_rand_field_ui()
        self.bottom_button_rand_lay = self._create_bottom_buttons_ui()

    def create_connections(self):
        """Connects Signals and Slots"""
        self.scatter_btn.clicked.connect(self._scatter_click)
        self.reset_btn.clicked.connect(self._reset_click)
        self.scatter_obj_pb.clicked.connect(self._select_scatter_object_click)

    @QtCore.Slot()
    def _select_scatter_object_click(self):
        """Sets scatter object to name of last selected object"""
        self._set_selected_scatter_object()

    @QtCore.Slot()
    def _scatter_click(self):
        """Scatters object with randomization specifications"""
        self._set_scatterobject_properties_from_ui()
        self.scatterobject.create_scatter_randomization()

    @QtCore.Slot()
    def _reset_click(self):
        """Reset UI values to default"""
        self._reset_scatterobject_properties_from_ui()

    def _create_scatter_field_ui(self):
        layout = self._create_scatter_field_headers()
        self.scatter_obj = QtWidgets.QLineEdit()
        self.scatter_obj.setMinimumWidth(100)
        self.scatter_obj_pb = QtWidgets.QPushButton("Select")
        self.scatter_obj_pb.setFixedWidth(50)
        self.scatter_targ = QtWidgets.QLineEdit()
        self.scatter_targ.setMinimumWidth(100)
        self.scatter_targ_pb = QtWidgets.QPushButton("Select")
        self.scatter_targ_pb.setFixedWidth(50)
        layout.addWidget(self.scatter_obj, 1, 0)
        layout.addWidget(self.scatter_obj_pb, 1, 2)
        layout.addWidget(self.scatter_targ, 1, 3)
        layout.addWidget(self.scatter_targ_pb, 1, 4)
        return layout

    def _create_xrot_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.x_min_lbl = QtWidgets.QLabel("X Rotation Variation Minimum")
        self.x_max_lbl = QtWidgets.QLabel("X Rotation Variation Maximum")
        self._set_xrot_spinbox()
        layout.addWidget(self.x_min_lbl, 1, 0)
        layout.addWidget(self.xrot_min, 2, 0)
        layout.addWidget(self.x_max_lbl, 1, 1)
        layout.addWidget(self.xrot_max, 2, 1)
        return layout

    def _set_xrot_spinbox(self):
        self.xrot_min = QtWidgets.QSpinBox()
        self.xrot_min.setMinimum(0)
        self.xrot_min.setMaximum(360)
        self.xrot_min.setMinimumWidth(100)
        self.xrot_min.setSingleStep(10)
        self.xrot_max = QtWidgets.QSpinBox()
        self.xrot_max.setMinimum(0)
        self.xrot_max.setMaximum(360)
        self.xrot_max.setValue(360)
        self.xrot_max.setMinimumWidth(100)
        self.xrot_max.setSingleStep(10)

    def _create_yrot_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.y_min_lbl = QtWidgets.QLabel("Y Rotation Variation Minimum")
        self.y_max_lbl = QtWidgets.QLabel("Y Rotation Variation Maximum")
        self._set_yrot_spinbox()
        layout.addWidget(self.y_min_lbl, 3, 0)
        layout.addWidget(self.yrot_min, 4, 0)
        layout.addWidget(self.y_max_lbl, 3, 1)
        layout.addWidget(self.yrot_max, 4, 1)
        return layout

    def _set_yrot_spinbox(self):
        self.yrot_min = QtWidgets.QSpinBox()
        self.yrot_min.setMinimum(0)
        self.yrot_min.setMaximum(360)
        self.yrot_min.setMinimumWidth(100)
        self.yrot_min.setSingleStep(10)
        self.yrot_max = QtWidgets.QSpinBox()
        self.yrot_max.setMinimum(0)
        self.yrot_max.setMaximum(360)
        self.yrot_max.setValue(360)
        self.yrot_max.setMinimumWidth(100)
        self.yrot_max.setSingleStep(10)

    def _create_zrot_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.z_min_lbl = QtWidgets.QLabel("Z Rotation Variation Minimum")
        self.z_max_lbl = QtWidgets.QLabel("Z Rotation Variation Maximum")
        self._set_zrot_spinbox()
        layout.addWidget(self.z_min_lbl, 5, 0)
        layout.addWidget(self.zrot_min, 6, 0)
        layout.addWidget(self.z_max_lbl, 5, 1)
        layout.addWidget(self.zrot_max, 6, 1)
        return layout

    def _set_zrot_spinbox(self):
        self.zrot_min = QtWidgets.QSpinBox()
        self.zrot_min.setMinimum(0)
        self.zrot_min.setMaximum(360)
        self.zrot_min.setMinimumWidth(100)
        self.zrot_min.setSingleStep(10)
        self.zrot_max = QtWidgets.QSpinBox()
        self.zrot_max.setMinimum(0)
        self.zrot_max.setMaximum(360)
        self.zrot_max.setValue(360)
        self.zrot_max.setMinimumWidth(100)
        self.zrot_max.setSingleStep(10)

    def _create_xscale_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_xmin_lbl = QtWidgets.QLabel("Scale X Variation Minimum")
        self.scale_xmax_lbl = QtWidgets.QLabel("Scale X Variation Maximum")
        self._set_xscale_spinbox()
        layout.addWidget(self.scale_xmin_lbl, 7, 0)
        layout.addWidget(self.scale_xmin, 8, 0)
        layout.addWidget(self.scale_xmax_lbl, 7, 1)
        layout.addWidget(self.scale_xmax, 8, 1)
        return layout

    def _create_yscale_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_ymin_lbl = QtWidgets.QLabel("Scale Y Variation Minimum")
        self.scale_ymax_lbl = QtWidgets.QLabel("Scale Y Variation Maximum")
        self._set_yscale_spinbox()
        layout.addWidget(self.scale_ymin_lbl, 9, 0)
        layout.addWidget(self.scale_ymin, 10, 0)
        layout.addWidget(self.scale_ymax_lbl, 9, 1)
        layout.addWidget(self.scale_ymax, 10, 1)
        return layout

    def _create_zscale_rand_field_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_zmin_lbl = QtWidgets.QLabel("Scale Z Variation Minimum")
        self.scale_zmax_lbl = QtWidgets.QLabel("Scale Z Variation Maximum")
        self._set_zscale_spinbox()
        layout.addWidget(self.scale_zmin_lbl, 11, 0)
        layout.addWidget(self.scale_zmin, 12, 0)
        layout.addWidget(self.scale_zmax_lbl, 11, 1)
        layout.addWidget(self.scale_zmax, 12, 1)
        return layout

    def _set_xscale_spinbox(self):
        self.scale_xmin = QtWidgets.QDoubleSpinBox()
        self.scale_xmin.setMinimum(0.1)
        self.scale_xmin.setValue(1.0)
        self.scale_xmin.setMaximum(10)
        self.scale_xmin.setMinimumWidth(100)
        self.scale_xmin.setSingleStep(.1)
        self.scale_xmax = QtWidgets.QDoubleSpinBox()
        self.scale_xmax.setMinimum(0.1)
        self.scale_xmax.setValue(1.0)
        self.scale_xmax.setMaximum(10)
        self.scale_xmax.setMinimumWidth(100)
        self.scale_xmax.setSingleStep(.1)

    def _set_yscale_spinbox(self):
        self.scale_ymin = QtWidgets.QDoubleSpinBox()
        self.scale_ymin.setMinimum(0.1)
        self.scale_ymin.setValue(1.0)
        self.scale_ymin.setMaximum(10)
        self.scale_ymin.setMinimumWidth(100)
        self.scale_ymin.setSingleStep(.1)
        self.scale_ymax = QtWidgets.QDoubleSpinBox()
        self.scale_ymax.setMinimum(0.1)
        self.scale_ymax.setValue(1.0)
        self.scale_ymax.setMaximum(10)
        self.scale_ymax.setMinimumWidth(100)
        self.scale_ymax.setSingleStep(.1)

    def _set_zscale_spinbox(self):
        self.scale_zmin = QtWidgets.QDoubleSpinBox()
        self.scale_zmin.setMinimum(0.1)
        self.scale_zmin.setValue(1.0)
        self.scale_zmin.setMaximum(10)
        self.scale_zmin.setMinimumWidth(100)
        self.scale_zmin.setSingleStep(.1)
        self.scale_zmax = QtWidgets.QDoubleSpinBox()
        self.scale_zmax.setMinimum(0.1)
        self.scale_zmax.setValue(1.0)
        self.scale_zmax.setMaximum(10)
        self.scale_zmax.setMinimumWidth(100)
        self.scale_zmax.setSingleStep(.1)

    def _create_bottom_buttons_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.reset_btn = QtWidgets.QPushButton("Reset")
        layout.addWidget(self.scatter_btn, 13, 0)
        layout.addWidget(self.reset_btn, 13, 1)
        return layout

    def _create_scatter_field_headers(self):
        self.scatter_targ_lbl = QtWidgets.QLabel("Object Being Scattered")
        self.scatter_targ_lbl.setStyleSheet("font: bold")
        self.scatter_obj_lbl = QtWidgets.QLabel("Scatter Destination Object")
        self.scatter_obj_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_targ_lbl, 0, 0)
        layout.addWidget(self.scatter_obj_lbl, 0, 3)
        return layout

    def _set_scatterobject_properties_from_ui(self):
        self.scatterobject.scatter_x_min = self.xrot_min.value()
        self.scatterobject.scatter_x_max = self.xrot_max.value()
        self.scatterobject.scatter_y_min = self.yrot_min.value()
        self.scatterobject.scatter_y_max = self.yrot_max.value()
        self.scatterobject.scatter_z_min = self.zrot_min.value()
        self.scatterobject.scatter_z_max = self.zrot_max.value()
        self.scatterobject.scatter_scale_xmin = self.scale_xmin.value()
        self.scatterobject.scatter_scale_xmax = self.scale_xmax.value()
        self.scatterobject.scatter_scale_ymin = self.scale_ymin.value()
        self.scatterobject.scatter_scale_ymax = self.scale_ymax.value()
        self.scatterobject.scatter_scale_zmin = self.scale_zmin.value()
        self.scatterobject.scatter_scale_zmax = self.scale_zmax.value()

    def _set_selected_scatter_object(self):
        self.scatterobject.select_scatter_object()
        self.scatterobject.scatter_object_select = self.scatter_obj.setText(
            self.scatterobject.current_object_def)

    def _reset_scatterobject_properties_from_ui(self):
        self.scatterobject.scatter_x_min = self.xrot_min.setValue(0)
        self.scatterobject.scatter_x_max = self.xrot_max.setValue(360)
        self.scatterobject.scatter_y_min = self.yrot_min.setValue(0)
        self.scatterobject.scatter_y_max = self.yrot_max.setValue(360)
        self.scatterobject.scatter_z_min = self.zrot_min.setValue(0)
        self.scatterobject.scatter_z_max = self.zrot_max.setValue(360)
        self.scatterobject.scatter_scale_xmin = self.scale_xmin.setValue(1.0)
        self.scatterobject.scatter_scale_xmax = self.scale_xmax.setValue(1.0)
        self.scatterobject.scatter_scale_ymin = self.scale_ymin.setValue(1.0)
        self.scatterobject.scatter_scale_ymax = self.scale_ymax.setValue(1.0)
        self.scatterobject.scatter_scale_zmin = self.scale_zmin.setValue(1.0)
        self.scatterobject.scatter_scale_zmax = self.scale_zmax.setValue(1.0)
        self.scatterobject.scatter_obj_def = self.scatter_obj.setText("")
        self.scatterobject.scatter_target_def = self.scatter_targ.setText("")


class ScatterObject(object):
    """Functionality to scatter UI and random rotation/scale"""

    def __init__(self):
        self.scatter_x_min = 0
        self.scatter_x_max = 0
        self.scatter_y_min = 0
        self.scatter_y_max = 0
        self.scatter_z_min = 0
        self.scatter_z_max = 0
        self.scatter_scale_xmin = 0
        self.scatter_scale_xmax = 0
        self.scatter_scale_ymin = 0
        self.scatter_scale_ymax = 0
        self.scatter_scale_zmin = 0
        self.scatter_scale_zmax = 0
        self.scatter_obj_def = None
        self.current_object_def = None
        self.scatter_target_def = None
        self.current_target_def = None

    def create_scatter_randomization(self):
        xRot = random.uniform(self.scatter_x_min, self.scatter_x_max)
        yRot = random.uniform(self.scatter_y_min, self.scatter_y_max)
        zRot = random.uniform(self.scatter_z_min, self.scatter_z_max)
        "cmds.rotate(xRot, yRot, zRot, scatterObject)"
        scaleFactorX = random.uniform(self.scatter_scale_xmin,
                                      self.scatter_scale_xmax)
        scaleFactorY = random.uniform(self.scatter_scale_ymin,
                                      self.scatter_scale_ymax)
        scaleFactorZ = random.uniform(self.scatter_scale_zmin,
                                      self.scatter_scale_zmax)
        "cmds.scale(scaleFactorX, scaleFactorY, scaleFactorZ, scatterObject)"

    def select_scatter_object(self):
        self.scatter_obj_def = cmds.ls(os=True, o=True)
        if len(self.scatter_obj_def) > 0:
            self.current_object_def = self.scatter_obj_def[-1]
        else:
            self.current_object_def = None
            log.warning("No objects are currently selected. Select one or "
                        "more objects and then try again.")
