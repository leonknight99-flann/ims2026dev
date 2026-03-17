import sys
import os

from configparser import ConfigParser

from qtpy import QtCore, QtWidgets, QtGui

from flann.vi.attenuator import Attenuator024, Attenuator625
        

class MainWindow(QtWidgets.QWidget):
    '''Main attenuator control window insprired by the Flann 625'''
    def __init__(self, attenuator=None, basedir=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._version = '2.0.0'

        self.setWindowTitle(f"Attenuator {self._version}")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, ".\\Icons\\FlannMicrowave.ico"))))
        self.setFixedSize(QtCore.QSize(260, 300))
        self.setStyleSheet("background-color: rgb(132, 181, 141)")

        self.attenuator = attenuator

        self.layoutMain = QtWidgets.QVBoxLayout()

        self.disableButtonGroup = QtWidgets.QButtonGroup()

        '''User Interface'''

        # Layout 1
        self.layout1 = QtWidgets.QHBoxLayout()

        # Layout 1a
        self.layout1a = QtWidgets.QGridLayout()

        self.layout1a.addWidget(QtWidgets.QLabel("Actual:"), 0,0)
        self.attenReadLineEdit = QtWidgets.QLineEdit()
        self.attenReadLineEdit.setReadOnly(True)    # Read-only
        # self.attenReadLineEdit.setFixedWidth(120)
        self.attenReadLineEdit.setStyleSheet("background-color: white")
        self.layout1a.addWidget(self.attenReadLineEdit, 0,1)
        self.layout1a.addWidget(QtWidgets.QLabel("dB"), 0,2)

        self.layout1a.addWidget(QtWidgets.QLabel("Entry:"), 1,0)
        self.attenEnterLineEdit = QtWidgets.QLineEdit()
        self.attenEnterLineEdit.returnPressed.connect(lambda: self.go_to_attenuation())
        # self.attenEnterLineEdit.setFixedWidth(120)
        self.attenEnterLineEdit.setStyleSheet("background-color: white")
        self.layout1a.addWidget(self.attenEnterLineEdit, 1,1)
        self.layout1a.addWidget(QtWidgets.QLabel("dB"), 1,2)

        self.positionToggle = QtWidgets.QPushButton("Set\nPosition")
        self.positionToggle.setCheckable(True)
        self.positionToggle.setStyleSheet("""
            QPushButton { background-color: rgb(247, 236, 223); }
            QPushButton:checked { background-color: rgb(0, 140, 124); }
        """)        
        
        # Layout 2
        self.layout2 = QtWidgets.QHBoxLayout()
        
        # Layout 2a
        self.layout2a = QtWidgets.QGridLayout()
        self.keyboardButtonMap = {}
        keyboard = [['7', '8', '9'],
                    ['4', '5', '6'],
                    ['1', '2', '3'],
                    ['C', '0', '.']]
        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                self.keyboardButtonMap[key] = QtWidgets.QPushButton(key)
                self.keyboardButtonMap[key].setFixedSize(QtCore.QSize(50, 50))
                self.keyboardButtonMap[key].setStyleSheet("background-color: lightgray")
                if key == 'C':
                    self.keyboardButtonMap[key].clicked.connect(self.clear_attenuation_entry)
                else:
                    self.keyboardButtonMap[key].clicked.connect(lambda _, key=key: self.append_attenuation_entry(key))
                self.layout2a.addWidget(self.keyboardButtonMap[key], row, col)

        # Layout 2b
        self.layout2b = QtWidgets.QVBoxLayout()

        self.incrementButton = QtWidgets.QPushButton("Inc +")
        self.incrementButton.setStyleSheet("background-color: rgb(191, 215, 195)")
        self.incrementButton.clicked.connect(lambda: self.increment_attenuation())
        self.disableButtonGroup.addButton(self.incrementButton)
        self.incrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.incrementButton)
        self.decrementButton = QtWidgets.QPushButton("Dec -")
        self.decrementButton.setStyleSheet("background-color: rgb(191, 215, 195)")
        self.decrementButton.clicked.connect(lambda: self.decrement_attenuation())
        self.disableButtonGroup.addButton(self.decrementButton)
        self.decrementButton.setFixedHeight(76)
        self.layout2b.addWidget(self.decrementButton)
        self.enterButton = QtWidgets.QPushButton("Goto")
        self.enterButton.setStyleSheet("background-color: rgb(191, 215, 195)")
        self.enterButton.clicked.connect(lambda: self.go_to_attenuation())
        self.disableButtonGroup.addButton(self.enterButton)
        self.enterButton.setFixedHeight(50)
        self.layout2b.addWidget(self.enterButton)

        '''Layout'''

        self.layout1.addLayout(self.layout1a)
        self.layout1.addWidget(self.positionToggle)

        self.layout2.addLayout(self.layout2a)
        self.layout2.addLayout(self.layout2b)   

        self.layoutMain.addLayout(self.layout1)
        self.layoutMain.addLayout(self.layout2)

        self.setLayout(self.layoutMain)

    def append_attenuation_entry(self, text):
        self.attenEnterLineEdit.setText(self.read_attenuation_entry() + text)
        self.attenEnterLineEdit.setFocus()

    def read_attenuation_entry(self):
        return self.attenEnterLineEdit.text()
    
    def clear_attenuation_entry(self):
        self.attenEnterLineEdit.clear()

    def get_current_attenuation(self):
        try:
            current_val = self.attenuator.attenuation()  # get the current attenuation value
            print(current_val)
        except ValueError:
            current_val = '-1'
            print("Error reading current attenuation value")
        
        return current_val
    
    def go_to_attenuation(self):
        newAttenuation = float(self.read_attenuation_entry())
        print(f"New attenuation: {newAttenuation}")
        self.clear_attenuation_entry()

        if self.attenuator == None:
            self.attenReadLineEdit.setText('Connection Error')
            print("No attenuator connected")
            return
        if self.positionToggle.isChecked():
            try:
                self.attenuator.position = int(newAttenuation)  # set the position in steps
                self.attenReadLineEdit.setText(f'Position {newAttenuation}')
            except:
                print("Error setting position")
                self.attenReadLineEdit.setText('Position Error')
        else:
            try:
                self.attenuator.attenuation = newAttenuation  # set the attenuation value
                self.attenReadLineEdit.setText(str(self.get_current_attenuation()))
            except:
                print("Error setting attenuation")
                self.attenReadLineEdit.setText('dB Error')

    def increment_attenuation(self):
        increment = float(self.read_attenuation_entry())
        print(f"Increment: {increment}")
        try:
            self.attenuator.increment_store = increment  # set the increment value
            self.attenuator.increment_store()
            self.attenuator.increment()  # increment the attenuation
            self.attenReadLineEdit.setText(str(self.get_current_attenuation()))
        except:
            print("Error incrementing attenuation")
            self.attenReadLineEdit.setText('dB Error')

    def decrement_attenuation(self):
        decrement = float(self.read_attenuation_entry())
        print(f"Decrement: {decrement}")
        try:
            self.attenuator.increment_store = decrement
            self.attenuator.increment_store()
            self.attenuator.decrement()  # decrement the attenuation
            self.attenReadLineEdit.setText(str(self.get_current_attenuation()))
        except:
            print("Error decrementing attenuation")
            self.attenReadLineEdit.setText('dB Error')
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(None, os.path.dirname(__file__))
    window.setWindowFlag(QtCore.Qt.CustomizeWindowHint, True)
    window.show()

    app.exec()
