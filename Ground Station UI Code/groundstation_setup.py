import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer, QSize
import pyqtgraph as pg
import numpy as np
from PyQt6 import QtWidgets 
from PyQt6.QtGui import QIcon
import serial
import csv

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(800, 300, 1000, 800)
    window.setWindowTitle('Sugar Gliders Ground Station')
    window.setWindowIcon(QIcon("Sugargliderstopicon.jpg"))
    
    # Object Setup
    # ==============================================

    main_widget = QWidget()
    main_layout=QHBoxLayout(main_widget)

    main_widget.setStyleSheet("background-color: #black;") # HEX color bg

    leftcol_container=QWidget()
    leftcol_layout=QVBoxLayout(leftcol_container)

    button_container=QWidget()
    button_layout=QVBoxLayout(button_container)
    button_label=QLabel('Buttons')
    button_label.setStyleSheet("font-size: 20pt; color: black;")
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
    LED = QtWidgets.QPushButton('Toggle LED')  # LED
    LED.setMinimumSize(QSize(100,30))
    LED.clicked.connect(LED_clicked)
    
    buzzer = QtWidgets.QPushButton('Toggle Buzzer')  # Buzzer
    buzzer.setMinimumSize(QSize(100,30))
    buzzer.clicked.connect(buzzer_clicked)
    row2.addWidget(LED)
    row2.addWidget(buzzer)

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
    data_title.setStyleSheet("font-size: 20pt; color: black;")
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
    
    plot1 = graphs.addPlot(row=0, col=0, title="Altitude")
    plot2 = graphs.addPlot(row=0, col=1, title="Temperature")
    plot3 = graphs.addPlot(row=1, col=0, title="Voltage")
    plot4 = graphs.addPlot(row=1, col=1, title="Velocity")

    x_data = [1, 2, 3, 4, 5]
    y_data_alt = [10, 20, 15, 25, 30]
    y_data_temp = [20, 22, 21, 23, 25]
    y_data_volt = [4.5, 4.2, 4.3, 4.1, 4.0]
    y_data_vel = [5, 10, 8, 12, 15]

    # Plot the data on each plot
    plot1.plot(x_data, y_data_alt, pen=('r'))  # ('r', #) - # changes line thickness
    plot2.plot(x_data, y_data_temp, pen=('b'))
    plot3.plot(x_data, y_data_volt, pen=('g'))
    plot4.plot(x_data, y_data_vel, pen=('y'))

    main_layout.addWidget(graphs)
    
    #Buttons
    #Buttons = QLabel(window)
    #Buttons.setText('Buttons')
    #Buttons.move(10, 0)
    #Buttons.setStyleSheet("font-size: 20pt;")

    #manual_release = QtWidgets.QPushButton(window)
    #manual_release.move(10, 30)
    #manual_release.setText('Manual Release')
    #manual_release.clicked.connect(manual_release_clicked)

    #calibration = QtWidgets.QPushButton(window)
    #calibration.move(110, 30)
    #calibration.setText('Calibration')
    #calibration.clicked.connect(calibration_clicked)

    #LED = QtWidgets.QPushButton(window)
    #LED.move(10,60)
    #LED.setText('Toggle LED')
    #LED.clicked.connect(LED_clicked)

    #buzzer = QtWidgets.QPushButton(window)
    #buzzer.move(110, 60)
    #buzzer.setText('Toggle buzzer')
    #buzzer.clicked.connect(buzzer_clicked)

    #ping = QtWidgets.QPushButton(window)
    #ping.move(10, 90)
    #ping.setText('Ping')
    #ping.clicked.connect(ping_clicked)

    #simulation = QtWidgets.QPushButton(window)
    #simulation.move(110, 90)
    #simulation.setText('Simulation')
    #simulation.clicked.connect(simulation_clicked)

    #graphs = pg.GraphicsLayoutWidget()
    #plot1 = graphs.addPlot(title="Graph1",row=1,col=0)
    #x = [1,2,3,4,5]
    #y = [2,4,6,8,10]
    #plot1.plot(x,y,pen='r')

    window.setCentralWidget(main_widget)
    window.show()
    sys.exit(app.exec())

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

def LED_clicked():
    print('LED Pressed')
    #Turn LED on and off

def buzzer_clicked():
    print('Buzzer Pressed')
    #turn buzzer on and off

def ping_clicked():
    print('Ping Pressed')
    #ping

def simulation_clicked():
    print('Simulation Pressed')
    #simulate
    
main()