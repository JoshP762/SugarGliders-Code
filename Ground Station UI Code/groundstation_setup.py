import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer, QSize
import pyqtgraph as pg
import numpy as np
from PyQt6 import QtWidgets 
from PyQt6.QtGui import QIcon
import serial
import csv

class SugarGlidersGS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(800, 300, 1000, 800)
        self.setWindowTitle('Sugar Gliders Ground Station')
        self.setWindowIcon(QIcon("Sugargliderstopicon.jpg"))
        self.LED_on=False
        self.buzzer_on=False

        self.setup_ui()

    # Object Setup
    # ==============================================

    def setup_ui(self):
        main_widget = QWidget()
        main_layout=QHBoxLayout(main_widget)

        main_widget.setStyleSheet("background-color: #black;") # HEX color bg

        leftcol_container=QWidget()
        leftcol_layout=QVBoxLayout(leftcol_container)

        button_container=QWidget()
        button_layout=QVBoxLayout(button_container)
        button_label=QLabel('Buttons')
        button_label.setStyleSheet("font-size: 20pt; color: white;")
        button_layout.addWidget(button_label)

        # Buttons
        # ==============================================
        
        # Row 1 buttons
        row1=QHBoxLayout()
        manual_release=QtWidgets.QPushButton('Manual Release')  # Manual Release
        manual_release.setMinimumSize(QSize(100,30))
        manual_release.clicked.connect(manual_release_clicked)
        
        calibration = QtWidgets.QPushButton('Calibration')  # Calibration
        calibration.setMinimumSize(QSize(100,30))
        calibration.clicked.connect(calibration_clicked)
        row1.addWidget(manual_release)
        row1.addWidget(calibration)

        # Row 2 buttons 
        row2 = QHBoxLayout()
        self.LED = QtWidgets.QPushButton('LED OFF')  # LED
        self.LED.setMinimumSize(QSize(100, 30))
        self.LED.clicked.connect(self.LED_clicked)

        self.buzzer = QtWidgets.QPushButton('Buzzer OFF')  # Buzzer
        self.buzzer.setMinimumSize(QSize(100, 30))
        self.buzzer.clicked.connect(self.buzzer_clicked)
        row2.addWidget(self.LED)
        row2.addWidget(self.buzzer)

        # Row 3 buttons 
        row3 = QHBoxLayout()
        ping = QtWidgets.QPushButton('Ping')  # Ping
        ping.setMinimumSize(QSize(100,30))
        ping.clicked.connect(ping_clicked)
        
        simulation = QtWidgets.QPushButton('Simulation')  # Simulation
        simulation.setMinimumSize(QSize(100,30))
        simulation.clicked.connect(simulation_clicked)
        row3.addWidget(ping)
        row3.addWidget(simulation)

        button_layout.addLayout(row1)
        button_layout.addLayout(row2)
        button_layout.addLayout(row3)
        button_layout.addStretch()
        leftcol_layout.addWidget(button_container)  # Displays buttons

        # Data objects

        label_container=QWidget()
        label_layout=QVBoxLayout(label_container)

        data_title=QLabel('Data')
        data_title.setStyleSheet("font-size: 20pt; color: white;")
        label_layout.addWidget(data_title)

        # Data
        # ==============================================

        label_layout.addWidget(QLabel('Team 2: The Sugar Gliders'))
        label_layout.addWidget(QLabel('Mission time:'))
        label_layout.addWidget(QLabel('Packet count:'))
        label_layout.addWidget(QLabel('SW state:'))
        label_layout.addWidget(QLabel('PL state:'))
        label_layout.addWidget(QLabel('Altitude:'))
        label_layout.addWidget(QLabel('Temperature:'))
        label_layout.addWidget(QLabel('Voltage:'))
        label_layout.addWidget(QLabel('GPS_Latitude:'))
        label_layout.addWidget(QLabel('GPS_Longitude:'))
        label_layout.addWidget(QLabel('Gyro_R:'))
        label_layout.addWidget(QLabel('Gyro_P:'))
        label_layout.addWidget(QLabel('Gyro_Y:'))
        label_layout.addWidget(QLabel('Velocity:'))
        label_layout.addWidget(QLabel('Acceleration:'))

        leftcol_layout.addWidget(label_container)
        leftcol_layout.addStretch() 

        main_layout.addWidget(leftcol_container)

        # Graphs (ALL TEST)
        # ==============================================

        pg.setConfigOption('background', '#ffffff')  # white
        pg.setConfigOption('foreground', 'k')  # black

        graphs = pg.GraphicsLayoutWidget()
        graphs.setStyleSheet("background-color: #f0f0f0;")

        self.plot1 = graphs.addPlot(row=0, col=0, title="Altitude")
        self.plot1.setLabel('left', 'Altitude (m)')
        self.plot1.setLabel('bottom', 'Time (s)')

        self.plot2 = graphs.addPlot(row=0, col=1, title="Temperature")
        self.plot2.setLabel('left', 'Temperature (°C)')
        self.plot2.setLabel('bottom', 'Time (s)')

        self.plot3 = graphs.addPlot(row=1, col=0, title="Voltage")
        self.plot3.setLabel('left', 'Voltage (V)')
        self.plot3.setLabel('bottom', 'Time (s)')

        self.plot4 = graphs.addPlot(row=1, col=1, title="Speed")
        self.plot4.setLabel('left', 'Velocity (m/s)')
        self.plot4.setLabel('bottom', 'Time (s)')

        x_data = [1, 2, 3, 4, 5]
        y_data_alt = [10, 20, 15, 25, 30]
        y_data_temp = [20, 22, 21, 23, 25]
        y_data_volt = [4.5, 4.2, 4.3, 4.1, 4.0]
        y_data_vel = [5, 10, 8, 12, 15]
        y_data_acc = [2, 4, 6, 8, 10]

        # Plot the data on each plot
        self.plot1.plot(x_data, y_data_alt, pen='red')
        self.plot2.plot(x_data, y_data_temp, pen='blue')
        self.plot3.plot(x_data, y_data_volt, pen='green')
        self.plot4.plot(x_data, y_data_vel, pen='yellow')


        main_layout.addWidget(graphs)
        self.setCentralWidget(main_widget)

    def LED_clicked(self):
        self.LED_on = not self.LED_on
        self.LED.setText("LED ON" if self.LED_on else "LED OFF")
        if self.LED_on:
            self.LED.setStyleSheet("background-color: red; color: white;")
        else:
            self.LED.setStyleSheet("background-color: none; color: white;")
        print("LED turned ON" if self.LED_on else "LED turned OFF")

    def buzzer_clicked(self):
        self.buzzer_on = not self.buzzer_on
        self.buzzer.setText("Buzzer ON" if self.buzzer_on else "Buzzer OFF")
        if self.buzzer_on:
            self.buzzer.setStyleSheet("background-color: red; color: white;")
        else:
            self.buzzer.setStyleSheet("background-color: none; color: white;")
        print("Buzzer turned ON" if self.buzzer_on else "Buzzer turned OFF")


def create_color_label(text):
    label=QLabel(text)
    label.setStyleSheet("color: black;")
    return label
   
def manual_release_clicked():
    print('Manual Release Pressed')
    #release payload here

def calibration_clicked():
    print('Calibration Pressed')
    #tell pico to tell sensors to shut up and listen


def ping_clicked():
    print('Ping Pressed')
    #ping

def simulation_clicked():
    print('Simulation Pressed')
    #simulate

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SugarGlidersGS()
    window.show()
    sys.exit(app.exec())