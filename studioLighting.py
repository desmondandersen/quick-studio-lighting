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

        # UI - Main widget
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

        # UI - Scroll Area
        scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll_area, 3, 0)

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

        self.add_backdrop_widget(backdrop=self.backdrop)

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
        self.scroll_layout.addWidget(widget)

    def add_backdrop_widget(self, backdrop):
        widget = BackdropWidget(backdrop)
        self.scroll_layout.addWidget(widget)


class LightWidget(QtWidgets.QFrame):
    """
    Control a specified light in the scene
    """
    def __init__(self, light, name):
        super(LightWidget, self).__init__()
        self.light = light
        self.name = str(name)
        self.isLinkedToBackdrop = True

        # UI
        layout = QtWidgets.QVBoxLayout(self)
        self.setStyleSheet("QFrame { border: 1px solid black; border-radius: 8px; }")

        # UI - Color and Name
        color_widget = QtWidgets.QWidget()
        color_layout = QtWidgets.QHBoxLayout(color_widget)
        color_widget.setStyleSheet("QLabel { border: none }")

        label = QtWidgets.QLabel(self.name)
        label.setStyleSheet("font-size: 16px")
        color_layout.addWidget(label)

        self.btn_color = QtWidgets.QPushButton()
        self.btn_color.clicked.connect(self.update_color)
        self.set_btn_color()
        color_layout.addWidget(self.btn_color)

        # UI - Intensity
        intensity_widget = QtWidgets.QWidget()
        intensity_layout = QtWidgets.QHBoxLayout(intensity_widget)
        intensity_widget.setStyleSheet("QLabel { border: none }")

        label = QtWidgets.QLabel('Intensity')
        intensity_layout.addWidget(label)

        slider_intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider_intensity.setMinimum(1)
        slider_intensity.setMaximum(1000)
        slider_intensity.setValue(self.light.intensity.get())
        slider_intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        intensity_layout.addWidget(slider_intensity)

        # UI - Toggle visibility
        toggles_widget = QtWidgets.QWidget()
        toggles_layout = QtWidgets.QVBoxLayout(toggles_widget)

        toggle_visibility = QtWidgets.QCheckBox('Visibility')
        toggle_visibility.setChecked(self.light.visibility.get())
        toggle_visibility.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))
        toggles_layout.addWidget(toggle_visibility)

        # UI - Toggle illuminate backdrop
        toggle_link = QtWidgets.QCheckBox('Illuminate backdrop (in render)')
        toggle_link.setChecked(self.isLinkedToBackdrop)
        toggle_link.toggled.connect(lambda val: self.update_lightlink(val))
        toggles_layout.addWidget(toggle_link)

        layout.addWidget(color_widget)
        layout.addWidget(intensity_widget)
        layout.addWidget(toggles_widget)

    def update_lightlink(self, val):
        """
        :param val: true to make lightlink; false to break lightlink
        :type val: bool
        """
        light_name = str(self.light.getTransform())

        if pm.objExists('studioBackdrop'):
            if val:
                pm.lightlink(light=light_name, object='studioBackdrop')
            else:
                pm.lightlink(b=True, light=light_name, object='studioBackdrop')

    def update_color(self):
        light_color = self.light.color.get()
        color = pm.colorEditor(rgbValue=light_color)
        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)
        self.light.color.set(color)
        self.set_btn_color(color)

    def set_btn_color(self, color=None):
        """
        :param color: tuple with RGB values
        :type color: tuple
        """
        if not color:
            color = self.light.color.get()
        if len(color) == 3:
            r, g, b = [c * 255 for c in color]
            self.btn_color.setStyleSheet('background-color: rgba({0}, {1}, {2}, 1.0)'.format(r, g, b))


class BackdropWidget(QtWidgets.QFrame):
    """
    Control backdrop in the scene
    """
    def __init__(self, backdrop):
        super(BackdropWidget, self).__init__()
        self.backdrop = backdrop

        # UI
        layout = QtWidgets.QVBoxLayout(self)
        self.setStyleSheet("QFrame { border: 1px solid black; border-radius: 8px; }")

        # UI - Color and Name
        color_widget = QtWidgets.QWidget()
        color_layout = QtWidgets.QHBoxLayout(color_widget)
        color_widget.setStyleSheet("QLabel { border: none }")

        label = QtWidgets.QLabel('Backdrop')
        label.setStyleSheet("font-size: 16px")
        color_layout.addWidget(label)

        # self.btn_color = QtWidgets.QPushButton()
        # self.btn_color.clicked.connect(self.update_color)
        # self.set_btn_color()
        # color_layout.addWidget(self.btn_color)

        layout.addWidget(color_widget)


def show_ui():
    ui = StudioLightingWidget()  # Create instance of widget
    ui.resize(300, 500)
    ui.show(dockable=True, floating=True)
