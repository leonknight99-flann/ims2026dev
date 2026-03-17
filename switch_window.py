from operator import index
import sys
import os

from configparser import ConfigParser
from time import sleep

from qtpy import QtCore, QtWidgets, QtGui

from flann.vi.switch import Switch337
from flann.vi.attenuator import Attenuator024, Attenuator625


class MainWindow(QtWidgets.QWidget):
    '''Switch Counter Main Window'''
    def __init__(self, switches=None, basedir=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._version = '1.0.0'

        self.setWindowTitle(f"Switch {self._version}")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, ".\\Icons\\FlannMicrowave.ico"))))
        self.setFixedWidth(400)
        self.setStyleSheet("background-color: rgb(132, 181, 141)")

        self.switches = switches

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.disableButtonGroup = QtWidgets.QButtonGroup()

        '''User Interface'''

        # Layout 1
        self.layout1 = QtWidgets.QHBoxLayout()
        
        self.toggleAllSwitchesButton = QtWidgets.QPushButton("Toggle\nAll")
        self.toggleAllSwitchesButton.setFixedSize(QtCore.QSize(75, 50))
        self.toggleAllSwitchesButton.setStyleSheet("QPushButton {background-color:rgb(218,233,221); color:black;}")
        self.disableButtonGroup.addButton(self.toggleAllSwitchesButton)
        self.toggleAllSwitchesButton.clicked.connect(lambda: self.toggle_all_switches())

        self.whereIsSwitchesButton = QtWidgets.QPushButton("Position?")
        self.whereIsSwitchesButton.setFixedSize(QtCore.QSize(75, 50))
        self.whereIsSwitchesButton.setStyleSheet("QPushButton {background-color:rgb(218,233,221); color:black;}")
        self.whereIsSwitchesButton.clicked.connect(lambda: self.where_are_switches())

        ## Layout 2
        self.layout2 = QtWidgets.QGridLayout()
        self.switchButtonMap = {}

        # Layout 3
        self.layout3 = QtWidgets.QHBoxLayout()
        
        self.layout3.addWidget(QtWidgets.QLabel("Messages:"))
        self.messageLineEdit = QtWidgets.QTextEdit()
        self.messageLineEdit.setStyleSheet("QTextEdit {background-color:white; color:black; border: 0px;}")
        self.messageLineEdit.setFixedHeight(25)
        self.messageLineEdit.setReadOnly(True)  # Read-only

        '''Layout'''

        self.layout1.addWidget(self.toggleAllSwitchesButton)
        self.layout1.addWidget(self.whereIsSwitchesButton)

        self.layout3.addWidget(self.messageLineEdit)

        self.layoutMain.addLayout(self.layout1)
        self.layoutMain.addLayout(self.layout2)
        self.layoutMain.addLayout(self.layout3)

        self.setLayout(self.layoutMain)
    
    def generate_window(self):

        switchButtonLabels = [['Toggle\n1', 'Toggle\n2', 'Toggle\nBoth'],] * len(self.switches)

        for s in range(len(self.switches)):
            switchLabel = QtWidgets.QTextEdit(f'{self.switches_names[s]}')
            switchLabel.setReadOnly(True)  # Read-only
            switchLabel.setStyleSheet("QTextEdit {background-color:white; color:black; border: 0px; border-radius:2px}")
            switchLabel.setFixedSize(QtCore.QSize(100, 40))
            switchLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.layout2.addWidget(switchLabel, s, 0)

        for row, keys in enumerate(switchButtonLabels):
            for col, key in enumerate(keys):
                self.switchButtonMap[f'{row}'+key] = QtWidgets.QPushButton(key)
                self.switchButtonMap[f'{row}'+key].setFixedSize(QtCore.QSize(75, 50))
                self.switchButtonMap[f'{row}'+key].setStyleSheet("QPushButton {background-color:lightgray; color:black;}")
                if key == 'Toggle\n1':
                    self.switchButtonMap[f'{row}'+key].clicked.connect(lambda _, row=row: self.toggle_selected_switch(row, 1))
                elif key == 'Toggle\n2':
                    self.switchButtonMap[f'{row}'+key].clicked.connect(lambda _, row=row: self.toggle_selected_switch(row, 2))
                elif key == 'Toggle\nBoth':
                    self.switchButtonMap[f'{row}'+key].clicked.connect(lambda _, row=row: self.switches[row].toggle_all())
                    self.switchButtonMap[f'{row}'+key].clicked.connect(lambda _, row=row: self.messageLineEdit.setText(f'Toggling {self.switches_names[row]} Switch 1 and 2'))
                self.layout2.addWidget(self.switchButtonMap[f'{row}'+key], row, col+1)


    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()

    def toggle_selected_switch(self, switch_driver_number, switch_number):
        if self.switches:
            selected_switch = self.switches[switch_driver_number]
            selected_switch.switch = switch_number
            selected_switch.toggle()
            self.messageLineEdit.setText(f'Toggling {self.switches_names[switch_driver_number]} Switch {switch_number}')
        else:
            self.messageLineEdit.setText('No switches connected.')

    def toggle_all_switches(self):
        if self.switches:
            self.messageLineEdit.setText('Toggling all switches')
            for switch in self.switches:
                switch.toggle_all()
        else:
            self.messageLineEdit.setText('No switches connected.')

    def where_are_switches(self):
        positionList = []
        if self.switches:
            for switch in self.switches:
                switch.switch = 1
                positionList.append(switch.position)
                switch.switch = 2
                positionList.append(switch.position)
            print(positionList)
            pop_up = QtWidgets.QMessageBox(self)
            pop_up.setWindowTitle("Switch Position")
            pop_up.setText(f'Switches positions:\n{'\n'.join(positionList)}')
            pop_up.setStandardButtons(QtWidgets.QMessageBox.Ok)
            pop_up.setIcon(QtWidgets.QMessageBox.Information)
            pop_up.setStyleSheet("QMessageBox {background-color: rgb(132,181,141); color:black;}")
            pop_up.exec()
        else:
            self.messageLineEdit.setText('No switches connected.')

    def remove_switch_buttons(self):
        while self.layout2.count():
            item = self.layout2.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def connect_to_attenuator(self):
        if self.connectToAttenuatorButton.isChecked():
            try:
                if self.attenuator024 is None:
                    self.attenuator024 = Attenuator024(address=self.demoConfig['DEMO024']['address'], 
                                                    timeout=float(self.demoConfig['DEMO024']['timeout']), 
                                                    baudrate=int(self.demoConfig['DEMO024']['baudrate']), 
                                                    timedelay=float(self.demoConfig['DEMO024']['sleep']))
                    print('Attenuator 024 connected')
                if self.attenuator625 is None:
                    self.attenuator625 = Attenuator625(address=self.demoConfig['DEMO625']['address'], 
                                                    tcp_port=int(self.demoConfig['DEMO625']['tcp_port']), 
                                                    timedelay=float(self.demoConfig['DEMO625']['sleep']))
                    print('Attenuator 625 connected')
            except:
                print('Connection Error')
                self.messageLineEdit.setText(f'Connection Error {self.attenuator024} {self.attenuator625} {self.switches}')
                self.connectToAttenuatorButton.setChecked(False)
                return
            self.messageLineEdit.setText('Attenuators connected')
        
        else:
            if self.attenuator024 is not None:
                self.attenuator024.close()
                self.attenuator024 = None
                print('Attenuator 024 disconnected')
            if self.attenuator625 is not None:
                self.attenuator625.close()
                self.attenuator625 = None
                print('Attenuator 625 disconnected')
            self.messageLineEdit.setText('Attenuators disconnected')

    def demo(self):
        if self.demoButton.isChecked():
            self.demoButton.setText("Stop")
            self.start_demo()
        else:
            self.stop_demo()
            self.demoButton.setText("Demo")

    def start_demo(self):
        self.messageLineEdit.setText('Starting demo')

        if any([self.attenuator024 is None, self.attenuator625 is None, not self.switches]):
            self.messageLineEdit.setText(f'Connection Error {self.attenuator024} {self.attenuator625} {self.switches}')
            self.demoButton.setChecked(False)
            self.demoButton.setText("Demo")
            return
        
        self.timer.start(int(self.demoConfig['DEMO']['sleep']))  # Set the timer interval to the sleep time in milliseconds

    def stop_demo(self):
        self.messageLineEdit.setText('Stopping demo')
        self.timer.stop()
        self.messageLineEdit.setText('Demo stopped')

    def running_demo(self):
        print(self.demoSwitchBool)
        self.demoSwitchBool = not self.demoSwitchBool
        if self.demoSwitchBool:
            self.messageLineEdit.setText('Toggling demo switches')
            self.switches[int(self.demoConfig['DEMO']['attenuator_switch_index'])].toggle_all()
        else:
            index = self.demoAttenuationIndex % len(self.demoAttenuationList)
            attenuation = self.demoAttenuationList[index]
            self.messageLineEdit.setText(f'Setting attenuation to {attenuation} dB')
            self.attenuator024.attenuation = attenuation
            self.attenuator625.attenuation = attenuation
            self.demoAttenuationIndex += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(switches=None, basedir=os.path.dirname(__file__))
    window.show()

    app.exec()