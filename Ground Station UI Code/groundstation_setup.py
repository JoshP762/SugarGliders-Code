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
        self.setWindowIcon(QIcon("SugarGliders_Logo1.png"))
        self.LED_on=False
        self.buzzer_on=False

        # Read graphs
        self.altitude_data = []
        self.altitude_time_data = []

        self.pressure_data = []
        self.pressure_time_data = []

        self.temp_data=[]
        self.temp_time_data=[]

        self.GyroR_data =[]
        self.GyroP_data =[]
        self.GyroY_data =[]

        self.packet_count=[]

        self.GPS_Latitude_data=[]
        self.GPS_Longitude_data=[]

        self.SW_State_data=[]
        self.PL_State_data=[]

        self.voltage_data = []
        self.voltage_time_data = []

        self.Acceleration_data = []
        self.Acceleration_time_data = []

        self.setup_ui()

    # Serial Setup
    # ==============================================

    def start_serial_stream(self, port="COM3", baudrate=9600):
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
            self.timer = QTimer()
            self.timer.timeout.connect(self.read_serial_data)
            self.timer.start(10)  # Poll every 10ms
            print(f"Serial stream started on {port}")
        except Exception as e:
            print(f"Serial error: {e}")

    def read_serial_data(self):
        if self.serial.in_waiting:
            line = self.serial.readline().decode('utf-8').strip()
            self.read_altitude_data(line)
            self.read_pressure_data(line)
            self.read_temperature_data(line)
            self.read_packet_data(line)
            self.read_GyroR_data(line)
            self.read_GyroP_data(line)
            self.read_GyroY_data(line)
            self.read_GPS_Latitude_data(line)
            self.read_GPS_Longitude_data(line)
            self.read_SW_State_data(line)
            self.read_PL_State_data(line)
            self.read_voltage_data(line)
            self.read_acceleration_data(line)

    # Altitude parser and plotter
    def read_altitude_data(self, line):
        match = re.search(r'Altitude = ([\d\.]+)', line)
        if match:
            altitude = float(match.group(1))
            self.Altitude.setText(f"Altitude: {altitude:.2f} m")
            self.altitude_data.append(altitude)
            self.altitude_time_data.append(len(self.altitude_data))
            self.plot1.clear()
            self.plot1.plot(self.altitude_time_data, self.altitude_data, pen='red')

    # Pressure parser and plotter
    def read_pressure_data(self, line):
        match = re.search(r'Pressure = ([\d\.]+)', line)
        if match:
            pressure = float(match.group(1))
            self.Pressure.setText(f"Pressure: {pressure:.2f} hPa")
            self.pressure_data.append(pressure)
            self.pressure_time_data.append(len(self.pressure_time_data))
            self.plot5.clear()
            self.plot5.plot(self.pressure_time_data, self.pressure_data, pen='blue')

    # Temperature parser and plotter
    def read_temperature_data(self, line):
        match = re.search(r'Temperature = ([\d\.]+)', line)
        if match:
            temperature = float(match.group(1))
            self.Temp.setText(f"Temperature: {temperature:.2f} °C")
            self.temp_data.append(temperature)
            self.temp_time_data.append(len(self.temp_time_data))
            self.plot2.clear()
            self.plot2.plot(self.temp_time_data, self.temp_data, pen='blue')

    # Packet parser and plotter
    def read_packet_data(self, line):
        match = re.search(r'Packet_Count = ([\d\.]+)', line)
        if match:
            packet = float(match.group(1))
            self.PacketCount.setText(f"Packet_Count: {packet:.2f} ")
            self.packet_count.append(packet)

    # Gyro-R parser 
    def read_GyroR_data(self, line):
        match = re.search(r'GYRO_R = ([\d\.]+)', line)
        if match:
            Gyro_R = float(match.group(1))
            self.GyroR.setText(f"GYRO_R: {Gyro_R:.2f}")
            self.GyroR_data.append(Gyro_R)

    # Gyro-P parser 
    def read_GyroP_data(self, line):
        match = re.search(r'GYRO_P = ([\d\.]+)', line)
        if match:
            Gyro_P = float(match.group(1))
            self.GyroP.setText(f"GYRO_P: {Gyro_P:.2f} ")
            self.GyroP_data.append(Gyro_P)
   
    # Gyro-Y parser 
    def read_GyroY_data(self, line):
        match = re.search(r'GYRO_Y = ([\d\.]+)', line)
        if match:
            Gyro_Y = float(match.group(1))
            self.GyroY.setText(f"GYRO_Y: {Gyro_Y:.2f} ")
            self.GyroY_data.append(Gyro_Y)
    
    #GPS_Latitude_Longitude_Graph
    def read_GPS_Latitude_data(self, line):
        match = re.search(r'Latitude = ([\d\.]+)', line)
        match = re.search(r'Longitude = ([\d\.]+)', line)
        if match:
            GPS_Latitude = float(match.group(1))
            self.GPSLat.setText(f"Latitude: {GPS_Latitude:.2f}")
            self.GPS_Latitude_data.append(GPS_Latitude)
            self.GPS_Longitude_data.append(len(self.GPS_Longitude_data))
            self.plot6.clear()
            self.plot6.plot(self.GPS_Latitude_data, self.GPS_Longitude_data, pen='blue')

    #GPS_Longitude_Data
    def read_GPS_Longitude_data(self, line):
        match = re.search(r'Longitude = ([\d\.]+)', line)
        if match:
            GPS_Longitude = float(match.group(1))
            self.GPSLong.setText(f"Longitude: {GPS_Longitude:.2f}")
            self.GPS_Longitude_data.append(GPS_Longitude)

    #SW_State_Data
    def read_SW_State_data(self, line):
        match = re.search(r'SW_State = ([\d\.]+)', line)
        if match:
            SW_State = float(match.group(1))
            self.SWState.setText(f"SW_State: {SW_State:.2f}")
            self.SW_State_data.append(SW_State)
    
    #PL_State_Data
    def read_PL_State_data(self, line):
        match = re.search(r'PL_State = ([\d\.]+)', line)
        if match:
            PL_State = float(match.group(1))
            self.PLState.setText(f"PL_State: {PL_State:.2f}")
            self.PL_State_data.append(PL_State)

    #voltage_data
    def read_voltage_data(self, line):
        match = re.search(r'Voltage = ([\d\.]+)', line)
        if match:
            voltage = float(match.group(1))
            self.Volt.setText(f"Voltage: {voltage:.2f} V")
            self.voltage_data.append(voltage)
            self.voltage_time_data.append(len(self.voltage_time_data))
            self.plot3.clear()
            self.plot3.plot(self.voltage_time_data, self.voltage_data, pen='green')

    #Acceleration_data
    def read_acceleration_data(self, line):
        match = re.search(r'Acceleration = ([\d\.]+)', line)
        if match:
            acceleration = float(match.group(1))
            self.Acc.setText(f"Acceleration: {acceleration:.2f} m/s²")
            self.Acceleration_data.append(acceleration)
            self.Acceleration_time_data.append(len(self.Acceleration_time_data))
            self.plot4.clear()
            self.plot4.plot(self.Acceleration_time_data, self.Acceleration_data, pen='orange')



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
        title.setStyleSheet("font-size: 32pt; font-weight: bold; color: #015482;")
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
        self.LED = QtWidgets.QPushButton('LED')  # LED
        self.LED.setFixedSize(QSize(150,150))
        self.LED.setStyleSheet("""
                background-color: white;
                color: #015482;
                border-radius: 75px;
                padding: 5px;
            """)
        self.LED.clicked.connect(self.LED_clicked)

        self.buzzer = QtWidgets.QPushButton('Buzzer')  # Buzzer
        self.buzzer.setFixedSize(QSize(150,150))
        self.buzzer.setStyleSheet("""
                background-color: white;
                color: #015482;
                border-radius: 75px;
                padding: 5px;
            """)
        self.buzzer.clicked.connect(self.buzzer_clicked)
        row2.addWidget(self.LED)
        row2.addWidget(self.buzzer)

        button_layout.addLayout(row1)
        button_layout.addLayout(row2)
        button_layout.addStretch()
        leftcol_layout.addWidget(button_container)  # Displays buttons

        # Data
        # ==============================================

        font = QFont("Helvetica [Cronyx]", 13)
        
        self.teamID = QLabel("Team_ID: 2")
        label_layout.addWidget(self.teamID)
        self.teamID.setStyleSheet("color : #015482;")
        self.teamID.setFont(font)
        
        self.MissionTime = QLabel("Mission_Time")
        label_layout.addWidget(self.MissionTime)
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

        self.Pressure = QLabel("Pressure")
        label_layout.addWidget(self.Pressure)
        self.Pressure.setStyleSheet("color : #015482")
        self.Pressure.setFont(font)

        logo = QLabel(self)
        pixmap = QPixmap(r"C:\Users\JoshAi\Documents\CANSAT-SG-CODE\SugarGliders-Code\Ground Station UI Code\SugarGliders_Logo1.png")
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

        self.plot4 = graphs.addPlot(row=1, col=1, title="Acceleration")
        self.plot4.setLabel('left', 'Acceleration (m/s²)')
        self.plot4.setLabel('bottom', 'Time (s)')

        self.plot5 = graphs.addPlot(row=2, col=0, title="Pressure")
        self.plot5.setLabel('left', 'Pressure (hPa)')
        self.plot5.setLabel('bottom', 'Time (s)')

        self.plot6 = graphs.addPlot(row=2, col=1, title = "Flight Path")
        self.plot6.setLabel('left', "Longitude")
        self.plot6.setLabel("bottom", "Latitude")


        main_layout.addWidget(graphs)
        self.setCentralWidget(main_widget)

    def LED_clicked(self):
        self.LED_on = not self.LED_on
        if self.LED_on:
            self.LED.setStyleSheet("""
                background-color: #EC7357;
                color: white;
                border-radius: 75px;
                padding: 5px;
            """)
        else:
            self.LED.setStyleSheet("""
                background-color: white;
                color: #015482;
                border-radius: 75px;
                padding: 5px;
            """)
    def buzzer_clicked(self):
        self.buzzer_on = not self.buzzer_on
        if self.buzzer_on:
            self.buzzer.setStyleSheet("""
                background-color: #EC7357;
                color: white;
                border-radius: 75px;
                padding: 5px;
            """)
        else:
            self.buzzer.setStyleSheet("""
                background-color: white;
                color: #015482;
                border-radius: 75px;
                padding: 5px;
            """)

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