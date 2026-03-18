
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
            border: 5px solid white;
        }}
    """

class Attenuator024Button(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet(create_button_stylesheet("./Icons/Attenuator024.png"))
        self.setIconSize(QtCore.QSize(80, 80))
        self.setMinimumSize(QtCore.QSize(120, 120))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    
    def hasHeightForWidth(self):
        return True
    
    def heightForWidth(self, width):
        return width  # Maintain square aspect ratio

class Attenuator625Button(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet(create_button_stylesheet("./Icons/Attenuator625.png"))
        self.setIconSize(QtCore.QSize(80, 80))
        self.setMinimumSize(QtCore.QSize(120, 120))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    
    def hasHeightForWidth(self):
        return True
    
    def heightForWidth(self, width):
        return width  # Maintain square aspect ratio


class Switch337Button(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet(create_button_stylesheet("./Icons/Switch337.png"))
        self.setIconSize(QtCore.QSize(80, 80))
        self.setMinimumSize(QtCore.QSize(100, 120))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    
    def hasHeightForWidth(self):
        return True
    
    def heightForWidth(self, width):
        return int(width * 1.2)  # Maintain 1.2 aspect ratio