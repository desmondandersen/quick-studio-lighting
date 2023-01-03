from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class StudioLightingWidget(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(StudioLightingWidget, self).__init__(parent=parent)

        self.backdrop = None
        self.camera = None
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
        self.btn_add_lights.clicked.connect(self.add_lights)
        main_layout.addWidget(self.btn_add_lights, 1, 0)

        # Add Lights Button
        self.btn_add_cam = QtWidgets.QPushButton('Add Camera')
        self.btn_add_cam.clicked.connect(self.add_camera)
        main_layout.addWidget(self.btn_add_cam, 2, 0)


        # Set main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_backdrop(self):
        # Delete any existing backdrop
        if pm.objExists('studioBackdrop'):
            pm.delete('studioBackdrop')

        # Create mesh
        self.backdrop = pm.polyPlane(n='studioBackdrop', w=20, h=20, sw=2, sh=2)
        pm.polyExtrudeEdge('studioBackdrop.e[0]', 'studioBackdrop.e[2]', kft=True, lt=(0, 5, 5))
        pm.polyExtrudeEdge('studioBackdrop.e[14]', 'studioBackdrop.e[17]', kft=True, lt=(0, 5, 5))
        pm.rotate('studioBackdrop', [0, 180, 0])
        pm.setAttr('studioBackdrop.displaySmoothMesh', 2)

        # Set pivot to center
        self.backdrop.manipPivot(p=(0, 0, 0))
        self.backdrop.delete(constructionHistory=True)
        pm.select(clear=True)

    def add_camera(self):
        self.camera = pm.camera(position=(0, 4, 8), aspectRatio=0.66)

    def add_lights(self):
        # Delete any existing lights
        if pm.objExists('keyLight'):
            pm.select('keyLight')
            pm.delete()

        if pm.objExists('fillLight'):
            pm.select('fillLight')
            pm.delete()

        if pm.objExists('backLight'):
            pm.select('backLight')
            pm.delete()

        # Create key light
        self.key_light = pm.shadingNode('areaLight', asLight=True)
        self.key_light.rename('keyLight')
        self.key_light.getTransform().translate.set(5, 5, 5)
        self.key_light.getTransform().rotateX.set(-20)
        self.key_light.getTransform().rotateY.set(45)

        # Create fill light
        self.fill_light = pm.shadingNode('areaLight', asLight=True)
        self.fill_light.rename('fillLight')
        self.fill_light.getTransform().translate.set(-5, 5, 5)
        self.fill_light.getTransform().rotateX.set(-20)
        self.fill_light.getTransform().rotateY.set(-45)

        # Create back light
        self.back_light = pm.shadingNode('areaLight', asLight=True)
        self.back_light.rename('backLight')
        self.back_light.getTransform().translate.set(-8, 1, -5)
        self.back_light.getTransform().rotateX.set(160)
        self.back_light.getTransform().rotateY.set(45)

        # Break link to backdrop
        if pm.objExists('backLight'):
            pm.lightlink(b=True, light='backLight', object='studioBackdrop')


ui = StudioLightingWidget()  # Create instance of widget
ui.resize(500, 500)
ui.show(dockable=True, floating=True)
