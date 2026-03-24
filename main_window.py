
import os
import sys

from flann_widgets import Attenuator024Button, Attenuator625Button, Switch337Button, Horn240Button, Waveguide562Button
from attenuator_window import MainWindow as AttenuatorWindow
from switch_window import MainWindow as SwitchWindow

from flann.vi.attenuator import Attenuator024, Attenuator625
from flann.vi.switch import Switch337

from qtpy import QtCore, QtWidgets, QtGui

from serial.tools import list_ports
from configparser import ConfigParser

basedir = os.path.dirname(__file__)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._version = '1.0.0'

        self.setWindowTitle("Flann IMS 2026")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, ".\\icons\\FlannMicrowave.ico"))))

        self.attenuator625 = None
        self.attenuator024 = None
        self.switch = None

        self.create_sub_windows(self.attenuator024, self.attenuator625, self.switch)

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setStyleSheet("background-color: rgb(0, 58, 34)")
    
        self.create_menu_bar()
        self.create_main_layout()

        self.setCentralWidget(self.centralWidget)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Run Demo")
        file_menu.addAction("Exit", self.close)

        connect_menu = menu_bar.addMenu("Connections")
        self.device_connect = connect_menu.addAction("Connect")
        self.device_connect.setCheckable(True)
        self.device_connect.triggered.connect(self.connect_to_instrument)
        connect_menu.addAction("Manage Connections", lambda: self.toggle_child_window(self.connection_manager))

        view_menu = menu_bar.addMenu("View")
        view_menu.addAction("024", lambda: self.toggle_child_window(self.attenuator024_window))
        view_menu.addAction("625", lambda: self.toggle_child_window(self.attenuator625_window))
        view_menu.addAction("Switch", lambda: self.toggle_child_window(self.switch_window))

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About", self.about_message)

    def create_sub_windows(self, atten024=None, atten625=None, switch=None):
        self.attenuator024_window = AttenuatorWindow(atten024, basedir)
        self.attenuator625_window = AttenuatorWindow(atten625, basedir)
        self.switch_window = SwitchWindow(switch, basedir)
        self.connection_manager = ConnectionManager()

    def create_main_layout(self):      
        switch1 = Switch337Button(basedir)
        switch1.clicked.connect(lambda: self.toggle_child_window(self.switch_window))
        switch2 = Switch337Button(basedir)
        switch2.clicked.connect(lambda: self.toggle_child_window(self.switch_window))
        attenuator1 = Attenuator024Button(basedir)
        attenuator1.clicked.connect(lambda: self.toggle_child_window(self.attenuator024_window))
        attenuator2 = Attenuator625Button(basedir)
        attenuator2.clicked.connect(lambda: self.toggle_child_window(self.attenuator625_window))
        horn1 = Horn240Button(basedir)
        horn2 = Horn240Button(basedir)
        
        grid_layout = QtWidgets.QGridLayout()
        
        grid_layout.addWidget(horn1, 0, 1)
        grid_layout.addWidget(horn2, 0, 2)
        grid_layout.addWidget(switch1, 1, 0)
        grid_layout.addWidget(switch2, 1, 3)
        grid_layout.addWidget(attenuator1, 2, 1)
        grid_layout.addWidget(attenuator2, 2, 2)

        main_widget = QtWidgets.QWidget()
        main_widget.setStyleSheet("background-color: white; border-radius: 5px; margin: 10px;")
        main_widget.setLayout(grid_layout)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(main_widget)

        self.centralWidget.setLayout(main_layout)

    def open_connection_manager(self):
        self.connection_manager.show()

    def toggle_child_window(self, window):
        if window.isVisible():
            window.hide()
        else:
            window.show()

    def about_message(self):
        QtWidgets.QMessageBox.about(self, "About Flann IMS 2026", f"Flann Microwave's IMS 2026 Control Software\nVersion {self._version}\n\nDeveloped by LKNI")

    def closeEvent(self, event):
        self.update_parser()  # Save settings to INI file
        QtWidgets.QApplication.closeAllWindows()

    def update_parser(self):
        new_parser = ConfigParser()
        new_parser.read(os.path.join(basedir, "settings.ini"))
        update_file = open(os.path.join(basedir, "settings.ini"), 'w')
        new_parser['GENERAL']['baudrate'] = self.connection_manager.baudrate_lineEdit.text()
        new_parser['GENERAL']['timeout'] = self.connection_manager.timeout_lineEdit.text()
        new_parser['GENERAL']['tcp_port'] = self.connection_manager.tcp_port_lineEdit.text()
        new_parser['GENERAL']['sleep'] = self.connection_manager.sleep_lineEdit.text()
        new_parser['INSTRUMENT1']['address'] = self.connection_manager.instrument_comboBox[0].currentText()
        new_parser['INSTRUMENT2']['address'] = self.connection_manager.instrument_comboBox[1].currentText()
        new_parser['INSTRUMENT3']['address'] = self.connection_manager.instrument_comboBox[2].currentText()
        new_parser.write(update_file)
        update_file.close()

    def connect_to_instrument(self):
        # Placeholder for connection logic
        baudrate = int(self.connection_manager.baudrate_lineEdit.text())
        timeout = float(self.connection_manager.timeout_lineEdit.text())
        tcp_port = int(self.connection_manager.tcp_port_lineEdit.text())
        sleep = float(self.connection_manager.sleep_lineEdit.text())

        if self.device_connect.isChecked():
            address_list = [self.connection_manager.instrument_comboBox[i].currentText().upper() for i in range(len(self.connection_manager.instrument_comboBox))]
            print(f"Connecting to instruments at: {address_list}")
            port_dictionary = {port.name: port.description.lower() for port in list_ports.comports()}
            for address in address_list:
                if address.startswith("COM") and 'silicon labs' in port_dictionary.get(address):
                    print(f"Found {address} at {port_dictionary.get(address)}")
                    print(f"Attempting to connect to 024 {address} via serial...")
                    self.attenuator024 = Attenuator024(address, baudrate, timeout, sleep)
                elif address.startswith("COM") and 'silicon labs' not in port_dictionary.get(address):
                    print(f"Attempting to connect to 337 {address} via serial...")
                else:
                    print(f"Attempting to connect to {address} via TCP/IP...")
                    self.attenuator625 = Attenuator625(address, tcp_port, sleep)
        elif not self.device_connect.isChecked():
            print("Disconnecting from instrument...")
            if self.attenuator024:
                self.attenuator024.close()
            if self.attenuator625:
                self.attenuator625.close()
            if self.switch:
                self.switch.close()
            self.attenuator024 = None
            self.attenuator625 = None
            self.switch = None

        self.create_sub_windows(self.attenuator024, self.attenuator625, self.switch)  # Recreate sub-windows with updated instrument connections


class ConnectionManager(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.instrument_comboBox = [None, None, None]  # Placeholder for 3 combo boxes for the 3 instruments

        self.setWindowTitle("Connection Manager")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, ".\\icons\\FlannMicrowave.ico"))))
        # self.setFixedSize(QtCore.QSize(400, 300))
        self.setStyleSheet("background-color: rgb(132, 181, 141)")

        self.layout_main = QtWidgets.QVBoxLayout()

        self.create_main_layout()

        self.setLayout(self.layout_main)

    def create_main_layout(self):
        parser = ConfigParser()
        parser.read(os.path.join(basedir, "settings.ini"))
        
        baudrate_layout = QtWidgets.QHBoxLayout()
        baudrate_layout.addWidget(QtWidgets.QLabel("Baudrate:"))
        self.baudrate_lineEdit = QtWidgets.QLineEdit()
        self.baudrate_lineEdit.setValidator(QtGui.QIntValidator())
        self.baudrate_lineEdit.setText(parser['GENERAL']['baudrate'])
        self.baudrate_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        baudrate_layout.addWidget(self.baudrate_lineEdit)

        timeout_layout = QtWidgets.QHBoxLayout()
        timeout_layout.addWidget(QtWidgets.QLabel("Timeout (ms):"))
        self.timeout_lineEdit = QtWidgets.QLineEdit()
        self.timeout_lineEdit.setValidator(QtGui.QIntValidator())
        self.timeout_lineEdit.setText(parser['GENERAL']['timeout'])
        self.timeout_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        timeout_layout.addWidget(self.timeout_lineEdit)

        tcp_layout = QtWidgets.QHBoxLayout()
        tcp_layout.addWidget(QtWidgets.QLabel("TCP Port:"))
        self.tcp_port_lineEdit = QtWidgets.QLineEdit()
        self.tcp_port_lineEdit.setValidator(QtGui.QIntValidator())
        self.tcp_port_lineEdit.setText(parser['GENERAL']['tcp_port'])
        self.tcp_port_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        tcp_layout.addWidget(self.tcp_port_lineEdit)

        sleep_layout = QtWidgets.QHBoxLayout()
        sleep_layout.addWidget(QtWidgets.QLabel("App Delay (s):"))
        self.sleep_lineEdit = QtWidgets.QLineEdit()
        self.sleep_lineEdit.setValidator(QtGui.QIntValidator())
        self.sleep_lineEdit.setText(parser['GENERAL']['sleep'])
        self.sleep_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        sleep_layout.addWidget(self.sleep_lineEdit)

        instrument_layout = QtWidgets.QVBoxLayout()
        for i in range(len(self.instrument_comboBox)):
            self.instrument_comboBox[i] = QtWidgets.QComboBox()
            self.instrument_comboBox[i].addItems(self.refresh_instrument_list(parser))
            self.instrument_comboBox[i].setCurrentText(parser[f'INSTRUMENT{i+1}']['address'])
            self.instrument_comboBox[i].setEditable(True)
            self.instrument_comboBox[i].setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
            instrument_layout.addWidget(self.instrument_comboBox[i])

        main_widget = QtWidgets.QWidget()
        main_widget.setStyleSheet("background-color: rgb(247, 236, 223); border-radius: 5px; margin: 10px;")

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(baudrate_layout)
        main_layout.addLayout(timeout_layout)
        main_layout.addLayout(tcp_layout)
        main_layout.addLayout(sleep_layout)
        main_layout.addLayout(instrument_layout)

        main_widget.setLayout(main_layout)
        self.layout_main.addWidget(main_widget)

    def refresh_instrument_list(self, parser):
        ports = list_ports.comports()
        port_names = [port.device.upper() for port in ports]
        port_names.append(parser['INSTRUMENT1']['address'])  # Add previously instruments to the list
        port_names.append(parser['INSTRUMENT2']['address'])
        port_names.append(parser['INSTRUMENT3']['address'])

        return list(set(port_names))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ApplicationWindow()
    window.show()
    app.exec_()
