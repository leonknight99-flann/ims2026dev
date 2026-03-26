
import os

from qtpy import QtCore, QtWidgets, QtGui

def create_button_stylesheet(icon_path):
    """Create a stylesheet for a button with the given icon path."""
    return f"""
        QPushButton {{
            border-image: url({icon_path});
            background-repeat: no-repeat;
            background-position: center;
        }}
        QPushButton:pressed {{
            border: 10px solid white;
        }}
    """

class Attenuator024Button(QtWidgets.QPushButton):
    def __init__(self, basedir):#, *args, **kwargs):
        super().__init__()#*args, **kwargs)

        self.ratio = 1024/1024
        minWidth = 240
        icon_path = os.path.join(basedir, 'icons', 'Attenuator024.png').replace('\\', '/')
        self.setStyleSheet(create_button_stylesheet(icon_path))
        self.setMinimumSize(QtCore.QSize(minWidth, int(minWidth / self.ratio)))

    def resizeEvent(self, event):
        w = self.width()
        h = int(w / self.ratio)
        self.setFixedHeight(h)
        super().resizeEvent(event)


class Attenuator625Button(QtWidgets.QPushButton):
    def __init__(self, basedir):#, *args, **kwargs):
        super().__init__()#*args, **kwargs)

        self.ratio = 1536/1024
        minWidth = 320
        icon_path = os.path.join(basedir, 'icons', 'Attenuator625.png').replace('\\', '/')
        self.setStyleSheet(create_button_stylesheet(icon_path))
        self.setMinimumSize(QtCore.QSize(minWidth, int(minWidth / self.ratio)))

    def resizeEvent(self, event):
        w = self.width()
        h = int(w / self.ratio)
        self.setFixedHeight(h)
        super().resizeEvent(event)


class Switch337Button(QtWidgets.QPushButton):
    def __init__(self, basedir):#, *args, **kwargs):
        super().__init__()#*args, **kwargs)

        self.ratio = 1024/1536
        minWidth = 160
        icon_path = os.path.join(basedir, 'icons', 'Switch337.png').replace('\\', '/')
        self.setStyleSheet(create_button_stylesheet(icon_path))
        self.setMinimumSize(QtCore.QSize(minWidth, int(minWidth / self.ratio)))

    def resizeEvent(self, event):
        w = self.width()
        h = int(w / self.ratio)
        self.setFixedHeight(h)
        super().resizeEvent(event)


class Horn240Button(QtWidgets.QPushButton):
    def __init__(self, basedir):#, *args, **kwargs):
        super().__init__()#*args, **kwargs)

        self.ratio = 1536/1024
        minWidth = 160
        icon_path = os.path.join(basedir, 'icons', 'Horn240.png').replace('\\', '/')
        self.setStyleSheet(create_button_stylesheet(icon_path))
        self.setMinimumSize(QtCore.QSize(minWidth, int(minWidth / self.ratio)))

    def resizeEvent(self, event):
        w = self.width()
        h = int(w / self.ratio)
        self.setFixedHeight(h)
        super().resizeEvent(event)


class Waveguide562PathButton(QtWidgets.QPushButton):
    def __init__(self, basedir):#, *args, **kwargs):
        super().__init__()#*args, **kwargs)

        self.setCheckable(True)

        self.ratio = 1264/842
        minWidth = 600
        icon1_path = os.path.join(basedir, 'icons', '29562-90deg-path1.png').replace('\\', '/')
        icon2_path = os.path.join(basedir, 'icons', '29562-90deg-path2.png').replace('\\', '/')
        self.setStyleSheet(f"""
                            QPushButton {{
                                border-image: url({icon1_path});
                                background-repeat: no-repeat;
                                background-position: center;
                            }}
                            QPushButton:pressed {{
                                border: 10px solid white;
                            }}
                            QPushButton:checked {{
                                border-image: url({icon2_path});
                            }}
                            """)
        self.setMinimumSize(QtCore.QSize(minWidth, int(minWidth / self.ratio)))

    def resizeEvent(self, event):
        w = self.width()
        h = int(w / self.ratio)
        self.setFixedHeight(h)
        super().resizeEvent(event)

