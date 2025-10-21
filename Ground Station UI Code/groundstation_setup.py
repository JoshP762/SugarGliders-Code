import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer, QSize
import pyqtgraph as pg
import numpy as np
from PyQt6 import QtWidgets 
from PyQt6.QtGui import QIcon, QPixmap, QFont
import re
import serial
from serial.tools import list_ports
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

    # Serial Setup
    # ==============================================

    def start_serial_stream(self, port="COM18", baudrate=9600):
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
            self.altitude_data = []
            self.time_data = []
            self.timer = QTimer()
            self.timer.timeout.connect(self.read_serial_data)
            self.timer.start(1000)  # Poll every 100ms
            print("Serial stream started.")
        except Exception as e:
            print(f"Serial error: {e}")

    def read_serial_data(self):
        if self.serial.in_waiting:
            line = self.serial.readline().decode('utf-8').strip()
            match = re.search(r'Approx\. Altitude = ([\d\.]+)', line)
            if match:
                altitude = float(match.group(1))
                self.Altitude.setText(f"Altitude: {altitude:.2f} m")
                self.altitude_data.append(altitude)
                self.time_data.append(len(self.altitude_data))  # simple time index
                self.plot1.clear()
                self.plot1.plot(self.time_data, self.altitude_data, pen='red')


    # Object Setup
    # ==============================================

    def setup_ui(self):
        main_widget = QWidget()
        main_layout=QHBoxLayout(main_widget)

        main_widget.setStyleSheet("background-color: #ABDAFC;") # HEX color bg

        leftcol_container=QWidget()
        leftcol_layout=QVBoxLayout(leftcol_container)

        button_container=QWidget()
        button_layout=QVBoxLayout(button_container)

        label_container=QWidget()
        label_layout=QVBoxLayout(label_container)


        # TEAM TITLE
        # ==============================================
        title = QLabel('SUGAR GLIDERS')
        title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #015482;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        leftcol_layout.addWidget(title)


        # Dropdown COM port
        # ==============================================
        comport=QWidget()
        com_layout= QVBoxLayout(comport)

        self.com_dropdown=QtWidgets.QComboBox()
        self.com_dropdown.setStyleSheet("color: #015482; background-color: white;")
        self.com_dropdown
        self.portrefresh()
        com_layout.addWidget(self.com_dropdown)
        XBee_button = QtWidgets.QPushButton("Connect to XBee")
        XBee_button.setStyleSheet("color: #015482")
        XBee_button.setMinimumSize(QSize(100, 30))
        XBee_button.setStyleSheet("color: #000000; background-color: white;")
        XBee_button.clicked.connect(self.connect_xbee)
        com_layout.addWidget(XBee_button)
        
        leftcol_layout.addWidget(comport)

        # Buttons
        # ==============================================
        
        # Row 1 buttons
        row1=QHBoxLayout()
        manual_release = QtWidgets.QPushButton('Manual Release')  # Manual Release
        manual_release.setFixedSize(QSize(200,65))
        manual_release.setStyleSheet("color: #015482; background-color: white;")
        manual_release.clicked.connect(manual_release_clicked)
        
        calibration = QtWidgets.QPushButton('Calibration') # Calibration
        calibration.setFixedSize(QSize(200,65))
        calibration.setStyleSheet("color: #015482; background-color: white;")
        calibration.clicked.connect(calibration_clicked)
       
        row1.addWidget(manual_release)
        row1.addWidget(calibration)

        # Row 2 buttons 
        row2 = QHBoxLayout()
        self.LED = QtWidgets.QPushButton('LED OFF')  # LED
        self.LED.setFixedSize(QSize(200,65))
        self.LED.setStyleSheet("color: #015482; background-color: lightgray;")
        self.LED.clicked.connect(self.LED_clicked)

        self.buzzer = QtWidgets.QPushButton('Buzzer OFF')  # Buzzer
        self.buzzer.setFixedSize(QSize(200,65))
        self.buzzer.setStyleSheet("color: #015482; background-color: lightgray;")
        self.buzzer.clicked.connect(self.buzzer_clicked)
        row2.addWidget(self.LED)
        row2.addWidget(self.buzzer)


        button_layout.addLayout(row1)
        button_layout.addLayout(row2)
        button_layout.addStretch()
        leftcol_layout.addWidget(button_container)  # Displays buttons


        # Data
        # ==============================================

        font = QFont("Arial", 15)
        
        self.teamID = QLabel("Team ID")
        label_layout.addWidget(self.teamID)
        self.teamID.setStyleSheet("color : #015482")
        self.teamID.setFont(font)
        
        self.MissionTime = QLabel("Mission_Time")
        label_layout.addWidget(self.MissionTime)
        self.MissionTime.setStyleSheet("color : #015482")
        self.MissionTime.setStyleSheet("color : #015482")
        self.MissionTime.setFont(font)

        self.PacketCount = QLabel("Packet_Count")
        label_layout.addWidget(self.PacketCount)
        self.PacketCount.setStyleSheet("color : #015482")
        self.PacketCount.setFont(font)
        
        self.SWState = QLabel("SW_State")
        label_layout.addWidget(self.SWState)
        self.SWState.setStyleSheet("color : #015482")
        self.SWState.setFont(font)

        self.PLState = QLabel("PL_State")
        label_layout.addWidget(self.PLState)
        self.PLState.setStyleSheet("color : #015482")
        self.PLState.setFont(font)
        
        self.Altitude = QLabel("Altitude")
        label_layout.addWidget(self.Altitude)
        self.Altitude.setStyleSheet("color : #015482")
        self.Altitude.setFont(font)
        
        self.Temp = QLabel("Temperture")
        label_layout.addWidget(self.Temp)
        self.Temp.setStyleSheet("color : #015482")
        self.Temp.setFont(font)
        
        self.Volt = QLabel("Voltage")
        label_layout.addWidget(self.Volt)
        self.Volt.setStyleSheet("color : #015482")
        self.Volt.setFont(font)
        
        self.GPSLat = QLabel("GPS_Latitude")
        label_layout.addWidget(self.GPSLat)
        self.GPSLat.setStyleSheet("color : #015482")
        self.GPSLat.setFont(font)
        
        self.GPSLong = QLabel("GPS_Longitude")
        label_layout.addWidget(self.GPSLong)
        self.GPSLong.setStyleSheet("color : #015482")
        self.GPSLong.setFont(font)
        
        self.GyroR = QLabel("GYRO_R")
        label_layout.addWidget(self.GyroR)
        self.GyroR.setStyleSheet("color : #015482")
        self.GyroR.setFont(font)
        
        self.GyroP = QLabel("GYRO_P")
        label_layout.addWidget(self.GyroP)
        self.GyroP.setStyleSheet("color : #015482")
        self.GyroP.setFont(font)

        
        self.GyroY = QLabel("GYRO_Y")
        label_layout.addWidget(self.GyroY)
        self.GyroY.setStyleSheet("color : #015482")
        self.GyroY.setFont(font)

        self.Vel = QLabel("Velocity")
        label_layout.addWidget(self.Vel)
        self.Vel.setStyleSheet("color : #015482")
        self.Vel.setFont(font)

        
        self.Acc = QLabel("Acceleration")
        label_layout.addWidget(self.Acc)
        self.Acc.setStyleSheet("color : #015482")
        self.Acc.setFont(font)


        logo = QLabel(self)
        pixmap = QPixmap(r"C:\Users\cosmo\OneDrive\Documents\GitHub\SugarGliders-Code\Ground Station UI Code\Sugargliderstopicon.jpg")
        scaled_logo = pixmap.scaled(50,50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(scaled_logo)
        logo.setScaledContents(False)
        label_layout.addWidget(logo)
    
        leftcol_layout.addWidget(label_container)
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
        pen_style = pg.mkPen(color='#EC7357', width=5)  # Change color and line width
        #self.plot1.plot(x_data, y_data_alt, pen=pen_style)
        self.plot2.plot(x_data, y_data_temp, pen=pen_style)
        self.plot3.plot(x_data, y_data_volt, pen=pen_style)
        self.plot4.plot(x_data, y_data_vel, pen=pen_style)

        main_layout.addWidget(graphs)
        self.setCentralWidget(main_widget)

    def LED_clicked(self):
        self.LED_on = not self.LED_on
        if self.LED_on:
            self.LED.setStyleSheet("background-color : red")
        else:
            self.LED.setStyleSheet("background-color : lightgray")

    def buzzer_clicked(self):
        self.buzzer_on = not self.buzzer_on
        if self.buzzer_on:
            self.buzzer.setStyleSheet("background-color : red")
        else:
            self.buzzer.setStyleSheet("background-color : lightgray")

    def portrefresh(self):
        ports=list_ports.comports()
        self.com_dropdown.clear()
        for port in ports:
            self.com_dropdown.addItem(port.device)

    def connect_xbee(self):
        XBeeport = self.com_dropdown.currentText()
        if XBeeport:
            try:
                self.start_serial_stream(port=XBeeport)
            except serial.SerialException as e:
                print("Failed to connect: " + str(e))
        else:
            print("No COM port selected.")

   
def manual_release_clicked():
    print('Manual Release Pressed')
    #release payload here

def calibration_clicked():
    print('Calibration Pressed')
    #tell pico to tell sensors to shut up and listen


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SugarGlidersGS()
    window.show()
    sys.exit(app.exec())