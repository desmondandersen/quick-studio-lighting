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

        self.setWindowTitle("Quick Studio")

        # Main widget
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout(self)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Add Backdrop Button
        self.btn_add_backdrop = QtWidgets.QPushButton('Add Backdrop')
        self.btn_add_backdrop.clicked.connect(self.add_backdrop)
        self.main_layout.addWidget(self.btn_add_backdrop, 0, 0)

        # Add Lights Button
        self.btn_add_lights = QtWidgets.QPushButton('Add Lights')
        self.btn_add_lights.clicked.connect(self.add_lights)
        self.main_layout.addWidget(self.btn_add_lights, 1, 0)

        # Add Lights Button
        self.btn_add_cam = QtWidgets.QPushButton('Add Camera')
        self.btn_add_cam.clicked.connect(self.add_camera)
        self.main_layout.addWidget(self.btn_add_cam, 2, 0)

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
        pm.select('studioBackdrop')
        pm.manipPivot(p=(0, 0, 0))
        pm.delete(constructionHistory=True)
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
        self.add_light_widget(light=self.key_light, name="Key Light")

        # Create fill light
        self.fill_light = pm.shadingNode('areaLight', asLight=True)
        self.fill_light.rename('fillLight')
        self.fill_light.getTransform().translate.set(-5, 5, 5)
        self.fill_light.getTransform().rotateX.set(-20)
        self.fill_light.getTransform().rotateY.set(-45)
        self.add_light_widget(light=self.fill_light, name="Fill Light")

        # Create back light
        self.back_light = pm.shadingNode('areaLight', asLight=True)
        self.back_light.rename('backLight')
        self.back_light.getTransform().translate.set(-8, 1, -5)
        self.back_light.getTransform().rotateX.set(160)
        self.back_light.getTransform().rotateY.set(45)
        self.add_light_widget(light=self.back_light, name="Back Light")

    def add_light_widget(self, light, name):
        widget = LightWidget(light, name)
        self.main_layout.addWidget(widget)


class LightWidget(QtWidgets.QWidget):
    """
    Light Widget: Control a specified light in the scene
    """
    def __init__(self, light, name):
        super(LightWidget, self).__init__()
        self.light = light
        self.name = str(name)
        self.isLinkedToBackdrop = True

        # UI
        layout = QtWidgets.QGridLayout(self)

        label = QtWidgets.QLabel(self.name)
        label.setStyleSheet("font-size: 16px")
        layout.addWidget(label, 0, 0)

        # UI - Intensity
        intensity_widget = QtWidgets.QWidget()
        intensity_layout = QtWidgets.QHBoxLayout(intensity_widget)
        layout.addWidget(intensity_widget, 1, 0)

        label = QtWidgets.QLabel('Intensity')
        intensity_layout.addWidget(label, 0)
        slider_intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider_intensity.setMinimum(1)
        slider_intensity.setMaximum(1000)
        slider_intensity.setValue(self.light.intensity.get())
        slider_intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        intensity_layout.addWidget(slider_intensity, 1)

        # UI - Toggle visibility
        toggle_visibility = QtWidgets.QCheckBox('Visibility')
        toggle_visibility.setChecked(self.light.visibility.get())
        toggle_visibility.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))
        layout.addWidget(toggle_visibility, 2, 0)

        # UI - Toggle illuminate backdrop
        toggle_link = QtWidgets.QCheckBox('Illuminate backdrop (in render)')
        toggle_link.setChecked(self.isLinkedToBackdrop)
        toggle_link.toggled.connect(lambda val: self.link_to_backdrop(val))
        layout.addWidget(toggle_link, 3, 0)

    def link_to_backdrop(self, val):
        """
        :param val: true to make link; false to break link
        :type val: bool
        """
        light_name = str(self.light.getTransform())

        if pm.objExists('studioBackdrop'):
            if val:
                pm.lightlink(light=light_name, object='studioBackdrop')
            else:
                pm.lightlink(b=True, light=light_name, object='studioBackdrop')


def show_ui():
    ui = StudioLightingWidget()  # Create instance of widget
    ui.resize(500, 500)
    ui.show(dockable=True, floating=True)
