
import os

from qtpy import QtCore, QtWidgets, QtGui

class Attenuator024Button(QtWidgets.QPushButton):
    def __init__(self, device_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(f"{device_id}")
        self.setStyleSheet("border-image: url(./Icons/Attenuator024.png) 0 0 0 0 stretch stretch; background-repeat: no-repeat; background-position: center;")
        self.setIconSize(QtCore.QSize(80, 80))
        self.setFixedSize(QtCore.QSize(120, 120))

class Attenuator625Button(QtWidgets.QPushButton):
    def __init__(self, device_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(f"{device_id}")
        self.setStyleSheet("border-image: url(./Icons/Attenuator625.png) 0 0 0 0 stretch stretch; background-repeat: no-repeat; background-position: center;")
        self.setIconSize(QtCore.QSize(80, 80))
        self.setFixedSize(QtCore.QSize(120, 120))


class Switch337Button(QtWidgets.QPushButton):
    def __init__(self, device_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(f"{device_id}")
        self.setStyleSheet("border-image: url(./Icons/Switch337.png) 0 0 0 0 stretch stretch; background-repeat: no-repeat; background-position: center;")
        self.setIconSize(QtCore.QSize(80, 80))
        self.setFixedSize(QtCore.QSize(100, 120))