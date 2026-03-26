import os
import sys

from flann.vi.attenuator import Attenuator024, Attenuator625

from qtpy import QtCore, QtWidgets, QtGui

from configparser import ConfigParser

basedir = os.path.dirname(__file__)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, attenuator_list=[], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Demo Window")
        self.setWindowIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, ".\\icons\\FlannMicrowave.ico"))))
        self.setStyleSheet("background-color: rgb(132, 181, 141)")

        self.attenuator_list = attenuator_list
        self.chosen_attenuator = None

        self.layout_main = QtWidgets.QVBoxLayout()

        self.create_main_layout()

        self.setLayout(self.layout_main)

    def create_main_layout(self):
        parser = ConfigParser()
        parser.read(os.path.join(basedir, "settings.ini"))

        attenuator_layout = QtWidgets.QHBoxLayout()
        attenuator_layout.addWidget(QtWidgets.QLabel("Attenuator:"), stretch=1)
        self.attenuator_comboBox = QtWidgets.QComboBox()
        self.attenuator_comboBox.addItems([str(type(a)) for a in self.attenuator_list])
        self.attenuator_comboBox.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        attenuator_layout.addWidget(self.attenuator_comboBox, stretch=3)

        x_axis_layout = QtWidgets.QHBoxLayout()
        x_axis_layout.addWidget(QtWidgets.QLabel("VNA Sweep\nTime (s):"))
        self.vna_sweep_time_lineEdit  = QtWidgets.QLineEdit()
        self.vna_sweep_time_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        self.vna_sweep_time_lineEdit.setText(parser['DEMO']['vna_sTime'])
        x_axis_layout.addWidget(self.vna_sweep_time_lineEdit)
        x_axis_layout.addWidget(QtWidgets.QLabel("VNA Sweep\nPoints:"))
        self.vna_sweep_points_lineEdit  = QtWidgets.QLineEdit()
        self.vna_sweep_points_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        self.vna_sweep_points_lineEdit.setText(parser['DEMO']['vna_nPoints'])
        x_axis_layout.addWidget(self.vna_sweep_points_lineEdit)

        y_axis_layout = QtWidgets.QHBoxLayout()
        y_axis_layout.addWidget(QtWidgets.QLabel("Max (dB):"))
        self.attenuator_max_lineEdit = QtWidgets.QLineEdit()
        self.attenuator_max_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        self.attenuator_max_lineEdit.setText(parser['DEMO']['max_attenuation'])
        y_axis_layout.addWidget(self.attenuator_max_lineEdit)
        y_axis_layout.addWidget(QtWidgets.QLabel("Min (dB):"))
        self.attenuator_min_lineEdit = QtWidgets.QLineEdit()
        self.attenuator_min_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        self.attenuator_min_lineEdit.setText(parser['DEMO']['min_attenuation'])
        y_axis_layout.addWidget(self.attenuator_min_lineEdit)

        image_selector_layout = QtWidgets.QHBoxLayout()
        image_selector_button = QtWidgets.QPushButton('Import\nImage')
        image_selector_layout.addWidget(image_selector_button)
        image_selector_layout.addWidget(QtWidgets.QLabel("Mask\nValue:"))
        self.image_mask_lineEdit = QtWidgets.QLineEdit()
        self.image_mask_lineEdit.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")
        self.image_mask_lineEdit.setText(parser['DEMO']['mask'])
        image_selector_layout.addWidget(self.image_mask_lineEdit)
        image_update_buttom = QtWidgets.QPushButton('Update\nImage')
        image_selector_layout.addWidget(image_update_buttom)

        # self.target_image = 
     
        demo_button = QtWidgets.QPushButton("Run Demo")
        demo_button.setStyleSheet("""
                                  QPushButton { background-color: rgb(247, 236, 223); }
                                  QPushButton:checked { background-color: rgb(0, 140, 124); }
                                  """)

        main_widget = QtWidgets.QWidget()
        main_widget.setStyleSheet("background-color: rgb(247, 236, 223); border-radius: 5px; margin: 10px;")

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(attenuator_layout)
        main_layout.addLayout(x_axis_layout)
        main_layout.addLayout(y_axis_layout)
        main_layout.addLayout(image_selector_layout)
        main_layout.addWidget(demo_button)
        

        main_widget.setLayout(main_layout)
        self.layout_main.addWidget(main_widget)
    
    def closeEvent(self, event):
        self.update_parser()  # Save settings to INI file

    def update_parser(self):
        new_parser = ConfigParser()
        new_parser.read(os.path.join(basedir, "settings.ini"))
        update_file = open(os.path.join(basedir, "settings.ini"), 'w')
        new_parser['DEMO']['vna_npoints'] = self.vna_sweep_points_lineEdit.text()
        new_parser['DEMO']['vna_stime'] = self.vna_sweep_time_lineEdit.text()
        new_parser['DEMO']['min_attenuation'] = self.attenuator_min_lineEdit.text()
        new_parser['DEMO']['max_attenuation'] = self.attenuator_max_lineEdit.text()
        new_parser['DEMO']['mask'] = self.image_mask_lineEdit.text()
        new_parser.write(update_file)
        update_file.close()
