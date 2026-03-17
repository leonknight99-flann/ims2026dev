
import os

from flann_widgets import Attenuator024Button, Attenuator625Button, Switch337Button

from qtpy import QtCore, QtWidgets, QtGui

basedir = os.path.dirname(__file__)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._version = '1.0.0'

        self.setWindowTitle("Flann IMS 2026")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, ".\\Icons\\FlannMicrowave.ico"))))

        self.create_menu_bar()

        self.layout = QtWidgets.QGridLayout()

        self.create_control_panel()

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setStyleSheet("background-color: rgb(132, 181, 141)")
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
    
    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Run Demo")
        file_menu.addAction("Exit", self.close)

        connect_menu = menu_bar.addMenu("Connect")
        connect_menu.addAction("Manage Connections")

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About", self.about_message)

    def create_control_panel(self):
        switch1 = Switch337Button("Switch 1")
        switch2 = Switch337Button("Switch 2")
        attenuator1 = Attenuator024Button("Attenuator 1")
        attenuator2 = Attenuator625Button("Attenuator 2")

        self.layout.addWidget(switch1, 1, 0)
        self.layout.addWidget(switch2, 1, 3)
        self.layout.addWidget(attenuator1, 2, 1)
        self.layout.addWidget(attenuator2, 2, 2)

    def about_message(self):
        QtWidgets.QMessageBox.about(self, "About Flann IMS 2026", f"Flann Microwave's IMS 2026 Control Software\nVersion {self._version}\n\nDeveloped by LKNI")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    window = ApplicationWindow()
    window.show()
    app.exec_()