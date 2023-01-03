from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class StudioLightingWidget(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(StudioLightingWidget, self).__init__(parent=parent)

        self.key_light = None
        self.fill_light = None
        self.back_light = None

        self.setWindowTitle("EZ Studio")

        # Main widget
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QGridLayout(self)

        # Add Backdrop Button
        self.btn_add_backdrop = QtWidgets.QPushButton('Add Backdrop')
        self.btn_add_backdrop.clicked.connect(self.add_backdrop)
        main_layout.addWidget(self.btn_add_backdrop, 0, 0)

        # Add Lights Button
        self.btn_add_lights = QtWidgets.QPushButton('Add Lights')
        self.btn_add_lights.clicked.connect(self.generate_lights)
        main_layout.addWidget(self.btn_add_lights, 0, 1)

        # Set main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_backdrop(self):
        # Delete any existing backdrop
        if pm.objExists('studioBackdrop'):
            pm.delete('studioBackdrop')

        # Create mesh
        pm.polyPlane(n='studioBackdrop', w=20, h=20, sw=2, sh=2)
        pm.polyExtrudeEdge('studioBackdrop.e[0]', 'studioBackdrop.e[2]', kft=True, lt=(0, 5, 5))
        pm.polyExtrudeEdge('studioBackdrop.e[14]', 'studioBackdrop.e[17]', kft=True, lt=(0, 5, 5))
        pm.rotate('studioBackdrop', [0, 180, 0])
        pm.setAttr('studioBackdrop.displaySmoothMesh', 2)

        # Set pivot to center
        pm.select('studioBackdrop')
        pm.manipPivot(p=(0, 0, 0))
        pm.delete(constructionHistory=True)
        pm.select(clear=True)

    def generate_lights(self):
        # Delete any existing lights
        if pm.objExists('keyLight'):
            pm.select('keyLight')
            pm.delete()

        # Create keylight
        self.key_light = pm.shadingNode('areaLight', asLight=True)
        self.key_light.rename('keyLight')
        self.key_light.getTransform().translate.set(5, 5, 5)



def show_ui():
    ui = StudioLightingWidget()  # Create instance of widget
    ui.show(dockable=True, floating=True)
    return ui