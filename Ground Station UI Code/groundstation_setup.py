import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer
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
    window.setWindowTitle('Sugar Gliders test window')
    window.setWindowIcon(QIcon("Sugargliderstopicon.jpg"))
    
    main_widget = QWidget()
    layout=QVBoxLayout(main_widget)

    sub_widget=QWidget()
    sub_layout=QHBoxLayout(sub_widget)
    
    
    data = QLabel(window)
    data.setText('Data')
    data.move(10, 230)
    data.setStyleSheet("font-size: 24pt;")

    Team_ID = QLabel(window)
    Team_ID.setText('Team 2: The Sugar GLiders')
    Team_ID.move(10, 265)

    Mission_time = QLabel(window)
    Mission_time.setText('Mission time:')
    Mission_time.move(10, 280)
    
    Packet_count = QLabel(window)
    Packet_count.setText('Packet count:')
    Packet_count.move(10, 295)

    SW_state = QLabel(window)
    SW_state.setText('SW state:')
    SW_state.move(10, 310)

    PL_state = QLabel(window)
    PL_state.setText('PL state:')
    PL_state.move(10, 325)

    Altitude = QLabel(window)
    Altitude.setText('Altitude:')
    Altitude.move(10, 340)

    Temperature = QLabel(window)
    Temperature.setText('Temperature:')
    Temperature.move(10, 355)

    Voltage = QLabel(window)
    Voltage.setText('Voltage:')
    Voltage.move(10, 370)

    GPS_Latitude = QLabel(window)
    GPS_Latitude.setText('GPS_Latitude:')
    GPS_Latitude.move(10, 385)

    GPS_Longitude = QLabel(window)
    GPS_Longitude.setText('GPS_Longitude:')
    GPS_Longitude.move(10, 400)

    Gyro_R = QLabel(window)
    Gyro_R.setText('Gyro_R:')
    Gyro_R.move(10, 415)

    Gyro_P = QLabel(window)
    Gyro_P.setText('Gyro_P:')
    Gyro_P.move(10, 430)

    Gyro_Y = QLabel(window)
    Gyro_Y.setText('Gyro_Y:')
    Gyro_Y.move(10, 445)

    Velocity = QLabel(window)
    Velocity.setText('Velocity:')
    Velocity.move(10, 460)

    Acceleration = QLabel(window)
    Acceleration.setText('Acceleration:')
    Acceleration.move(10, 475)
    

    #Buttons
    Buttons = QLabel(window)
    Buttons.setText('Buttons')
    Buttons.move(10, 0)
    Buttons.setStyleSheet("font-size: 20pt;")

    manual_release = QtWidgets.QPushButton(window)
    manual_release.move(10, 30)
    manual_release.setText('Manual Release')
    manual_release.clicked.connect(manual_release_clicked)

    calibration = QtWidgets.QPushButton(window)
    calibration.move(110, 30)
    calibration.setText('Calibration')
    calibration.clicked.connect(calibration_clicked)

    LED = QtWidgets.QPushButton(window)
    LED.move(10,60)
    LED.setText('Toggle LED')
    LED.clicked.connect(LED_clicked)

    buzzer = QtWidgets.QPushButton(window)
    buzzer.move(110, 60)
    buzzer.setText('Toggle buzzer')
    buzzer.clicked.connect(buzzer_clicked)

    ping = QtWidgets.QPushButton(window)
    ping.move(10, 90)
    ping.setText('Ping')
    ping.clicked.connect(ping_clicked)

    simulation = QtWidgets.QPushButton(window)
    simulation.move(110, 90)
    simulation.setText('Simulation')
    simulation.clicked.connect(simulation_clicked)

    graphs = pg.GraphicsLayoutWidget()
    plot1 = graphs.addPlot(title="Graph1",row=1,col=0)
    x = [1,2,3,4,5]
    y = [2,4,6,8,10]
    plot1.plot(x,y,pen='r')



    
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