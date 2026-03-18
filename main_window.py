
import os

from flann_widgets import Attenuator024Button, Attenuator625Button, Switch337Button

from attenuator_window import MainWindow as AttenuatorWindow
from switch_window import MainWindow as SwitchWindow

from qtpy import QtCore, QtWidgets, QtGui

basedir = os.path.dirname(__file__)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._version = '1.0.0'

        self.setWindowTitle("Flann IMS 2026")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, ".\\Icons\\FlannMicrowave.ico"))))

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setStyleSheet("background-color: rgb(132, 181, 141)")
    
        self.create_menu_bar()
        self.create_control_panel()

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
        switch1 = Switch337Button()
        switch1.clicked.connect(SwitchWindow(None, basedir).show)
        switch2 = Switch337Button()
        switch2.clicked.connect(SwitchWindow(None, basedir).show)
        attenuator1 = Attenuator024Button()
        attenuator1.clicked.connect(AttenuatorWindow(None, basedir).show)
        attenuator2 = Attenuator625Button()
        attenuator2.clicked.connect(AttenuatorWindow(None, basedir).show)
        
        grid_layout = QtWidgets.QGridLayout()
        
        grid_layout.addWidget(switch1, 1, 0)
        grid_layout.addWidget(switch2, 1, 3)
        grid_layout.addWidget(attenuator1, 2, 1)
        grid_layout.addWidget(attenuator2, 2, 2)
        
        # Set row and column stretch to fill available space
        grid_layout.setRowStretch(1, 1)
        grid_layout.setRowStretch(2, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)
        grid_layout.setColumnStretch(3, 1)

        main_widget = QtWidgets.QWidget()
        main_widget.setStyleSheet("background-color: white; border-radius: 5px; margin: 10px;")
        main_widget.setLayout(grid_layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(main_widget)

        self.centralWidget.setLayout(main_layout)

    def about_message(self):
        QtWidgets.QMessageBox.about(self, "About Flann IMS 2026", f"Flann Microwave's IMS 2026 Control Software\nVersion {self._version}\n\nDeveloped by LKNI")

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    window = ApplicationWindow()
    window.show()
    app.exec_()