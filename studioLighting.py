from Qt import QtWidgets, QtCore, QtGui
import pymel.core as pm
from functools import partial


class StudioLightingWidget(QtWidgets.QDialog):
    def __init__(self):
        super(StudioLightingWidget, self).__init__()
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QGridLayout(self)

        # Generate Button
        btn_create = QtWidgets.QPushButton('Add Lighting')
        btn_create.clicked.connect(self.add_lights)
        layout.addWidget(btn_create, 0, 0)

    def add_lights(self):
        add_area_light = partial(pm.shadingNode, 'areaLight', asLight=True)
        add_area_light()


def show_ui():
    ui = StudioLightingWidget()  # Create instance of widget
    ui.show()
    return ui
