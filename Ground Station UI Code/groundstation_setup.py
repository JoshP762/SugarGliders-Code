<<<<<<< HEAD
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
from PyQt6 import QtWidgets 
from PyQt6.QtGui import QIcon




def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(800, 300, 600, 600)
    window.setWindowTitle('Sugar Gliders test window')
    window.setWindowIcon(QIcon("Sugargliderstopicon.jpg"))
    
    
    
    text = QLabel(window)
    text.setText('Data')
    text.move(0, 250)
    
    manual_release = QtWidgets.QPushButton(window)
    manual_release.move(0, 0)
    manual_release.setText('Manual Release')
    manual_release.clicked.connect(manual_release_clicked)

    calibration = QtWidgets.QPushButton(window)
    calibration.move(100, 0)
    calibration.setText('Calibration')
    calibration.clicked.connect(calibration_clicked)

    LED = QtWidgets.QPushButton(window)
    LED.move(200,0)
    LED.setText('Toggle LED')
    LED.clicked.connect(LED_clicked)

    buzzer = QtWidgets.QPushButton(window)
    buzzer.move(300, 0)
    buzzer.setText('Toggle buzzer')
    buzzer.clicked.connect(buzzer_clicked)

    ping = QtWidgets.QPushButton(window)
    ping.move(400, 0)
    ping.setText('Ping')
    ping.clicked.connect(ping_clicked)

    simulation = QtWidgets.QPushButton(window)
    simulation.move(500, 0)
    simulation.setText('Simulation')
    simulation.clicked.connect(simulation_clicked)
    

    window.show()
    sys.exit(app.exec())


def manual_release_clicked():
    print('manual release')
    #release payload here

def calibration_clicked():
    print('calibration')
    #tell pico to tell sensors to shut up and listen

def LED_clicked():
    print('LED')
    #Turn LED on and off

def buzzer_clicked():
    print('buzzer')
    #turn buzzer on and off

def ping_clicked():
    print('ping')
    #ping

def simulation_clicked():
    print('simulation')
    #simulate
main()
=======
from PyQt5.QtWidgets import QDialog
from ui_imagedialog import Ui_ImageDialog

class ImageDialog(QDialog):
    def __init__(self):
        super(ImageDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_ImageDialog()
        self.ui.setupUi(self)

        # Make some local modifications.
        self.ui.colorDepthCombo.addItem("2 colors (1 bit per pixel)")

        # Connect up the buttons.
        self.ui.okButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
>>>>>>> 1edc99db23f750e5d4829d728dbcc2e79db042d8
