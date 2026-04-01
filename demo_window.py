import os
import sys

import numpy as np
import pyqtgraph as pg
import PIL.Image as Image

from flann.vi.attenuator import Attenuator625, Attenuator024

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
        self.trace_file_path = None
        self.trace_array = None
        self.create_trace_image()

        self.timer = QtCore.QTimer(self)  # Timer for demo
        self.timer.timeout.connect(self.running_demo)

        self.layout_main = QtWidgets.QVBoxLayout()

        self.create_main_layout()

        self.setLayout(self.layout_main)

    def create_trace_image(self):
        self.trace_image = pg.PlotWidget()
        self.trace_image.setBackground((132, 181, 141))
        self.trace_image.showGrid(x=True, y=True)
        for axis in ['left', 'bottom', 'right', 'top']:
            ax = self.trace_image.getAxis(axis)
            ax.setPen('w')
            ax.setTextPen('w')

    def create_main_layout(self):
        parser = ConfigParser()
        parser.read(os.path.join(basedir, "settings.ini"))

        attenuator_layout = QtWidgets.QHBoxLayout()
        attenuator_layout.addWidget(QtWidgets.QLabel("Attenuator:"), stretch=1)
        self.attenuator_comboBox = QtWidgets.QComboBox()
        self.attenuator_comboBox.addItems([str(type(a)) for a in self.attenuator_list])
        attenuator_layout.addWidget(self.attenuator_comboBox, stretch=3)

        x_axis_layout = QtWidgets.QHBoxLayout()
        x_axis_layout.addWidget(QtWidgets.QLabel("VNA Sweep\nTime (s):"))
        self.vna_sweep_time_lineEdit  = QtWidgets.QLineEdit()
        self.vna_sweep_time_lineEdit.setStyleSheet("background-color: white;")
        self.vna_sweep_time_lineEdit.setText(parser['DEMO']['vna_sTime'])
        x_axis_layout.addWidget(self.vna_sweep_time_lineEdit)
        x_axis_layout.addWidget(QtWidgets.QLabel("VNA Sweep\nPoints:"))
        self.vna_sweep_points_lineEdit  = QtWidgets.QLineEdit()
        self.vna_sweep_points_lineEdit.setStyleSheet("background-color: white;")
        self.vna_sweep_points_lineEdit.setText(parser['DEMO']['vna_nPoints'])
        x_axis_layout.addWidget(self.vna_sweep_points_lineEdit)

        y_axis_layout = QtWidgets.QHBoxLayout()
        y_axis_layout.addWidget(QtWidgets.QLabel("Max (dB):"))
        self.attenuator_max_lineEdit = QtWidgets.QLineEdit()
        self.attenuator_max_lineEdit.setStyleSheet("background-color: white;")
        self.attenuator_max_lineEdit.setText(parser['DEMO']['max_attenuation'])
        y_axis_layout.addWidget(self.attenuator_max_lineEdit)
        y_axis_layout.addWidget(QtWidgets.QLabel("Min (dB):"))
        self.attenuator_min_lineEdit = QtWidgets.QLineEdit()
        self.attenuator_min_lineEdit.setStyleSheet("background-color: white;")
        self.attenuator_min_lineEdit.setText(parser['DEMO']['min_attenuation'])
        y_axis_layout.addWidget(self.attenuator_min_lineEdit)

        image_selector_layout = QtWidgets.QHBoxLayout()
        image_selector_button = QtWidgets.QPushButton('Import\nImage')
        image_selector_button.clicked.connect(lambda: self.open_image_dialog())
        image_selector_layout.addWidget(image_selector_button)
        image_selector_layout.addWidget(QtWidgets.QLabel("Mask\nValue:"))
        self.image_mask_lineEdit = QtWidgets.QLineEdit()
        self.image_mask_lineEdit.setStyleSheet("background-color: white;")
        self.image_mask_lineEdit.setText(parser['DEMO']['mask'])
        image_selector_layout.addWidget(self.image_mask_lineEdit)
        image_update_button = QtWidgets.QPushButton('Update\nImage')
        image_update_button.clicked.connect(lambda: self.update_image())
        image_selector_layout.addWidget(image_update_button)

        # self.target_image = 
     
        self.demo_button = QtWidgets.QPushButton("Run Demo")
        self.demo_button.setCheckable(True)
        self.demo_button.clicked.connect(lambda: self.demo())
        
        main_widget = QtWidgets.QWidget()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(attenuator_layout)
        main_layout.addLayout(x_axis_layout)
        main_layout.addLayout(y_axis_layout)
        main_layout.addLayout(image_selector_layout)
        main_layout.addWidget(self.trace_image)
        main_layout.addWidget(self.demo_button)
        

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

    def open_image_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self,
                                            "Select file","",
                                            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;" \
                                            "CSV Files (*.csv)")
        file_dialog.setWindowTitle("Open Image")
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            self.trace_file_path = file_dialog.selectedFiles()[0]
            self.update_image()

    def update_image(self):
        pen = pg.mkPen(color='w')
        self.trace_image.clear()
        self.lineImage_to_array(self.trace_file_path)
        self.trace_image.plot(self.trace_array[:, 0], self.trace_array[:, 1], pen=pen)

    def lineImage_to_array(self, image):
        self.trace_array = None
        img = Image.open(image).convert('L')
        img_array = np.array(img)
        mask = (img_array > int(self.image_mask_lineEdit.text())).astype(np.uint8)
        y, x = np.where(mask == 1)

        array = np.column_stack((x, y))
        # Remove duplicates based on first column, keeping row with max second column
        sorted_indices = np.lexsort((array[:, 1], array[:, 0]))
        array = array[sorted_indices]
        unique_mask = np.concatenate(([True], np.diff(array[:, 0]) != 0))
        array = array[unique_mask]
        array = array[np.argsort(array[:, 0])]
        
        array = np.append(array, [[array[-1, 0]+1, array[0, 1]]], axis=0)
        array = array.astype(float)

        sweep_time_range = float(self.vna_sweep_time_lineEdit.text())
        max_attenuation = float(self.attenuator_max_lineEdit.text())
        min_attenuation = float(self.attenuator_min_lineEdit.text())
        attenuation_range = max_attenuation - min_attenuation


        array[:, 0] = np.round((array[:, 0] - np.min(array[:, 0])) * sweep_time_range / np.max(array[:, 0]), 1)
        array[:, 1] = np.round(((array[:, 1] - np.min(array[:, 1])) * attenuation_range / np.ptp(array[:, 1])) + min_attenuation, 1)
        np.savetxt(image+'.csv', array, delimiter=',')

        print(array)

        self.trace_array = array

    def demo(self):
        if self.demo_button.isChecked() and isinstance(self.attenuator_list[self.attenuator_comboBox.currentIndex()], (Attenuator024, Attenuator625)):
            self.demo_button.setText("Stop")
        elif not self.demo_button.isChecked() and isinstance(self.attenuator_list[self.attenuator_comboBox.currentIndex()], (Attenuator024, Attenuator625)):
            self.demo_button.setText("Run Demo")
        else:
            print('incorrect class')
            self.demo_button.setChecked(False)
            self.demo_button.setText("Run Demo")

    def running_demo(self):
        selected_attenuator = self.attenuator_list[self.attenuator_comboBox.currentIndex()]
        print(selected_attenuator)
        return


test_atten = Attenuator625(address='10.200.1.9', timedelay=0.1, tcp_port=10001)
print(test_atten.id())
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow([test_atten, '1', '2'])
    window.show()
    app.exec_()