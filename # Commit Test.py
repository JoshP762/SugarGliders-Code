import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg


class GroundStation(QWidget):
    def __init__(self):     #constructor
        super().__init__() #subclass calls the parent class

        #creation of the window
        self.setWindowTitle("Sugar Gliders Ground Station")
        self.setGeometry(100, 100, 300, 200)
        mainLayout = QVBoxLayout()
    
        # Creating Lables 
        labelLayout = QVBoxLayout()

        self.TeamID = QLabel("Team_ID")
        labelLayout.addWidget(self.TeamID)

        self.MissionTime = QLabel("Mission_Time")
        labelLayout.addWidget(self.MissionTime)

        self.PacketCount = QLabel("Packet_Count")
        labelLayout.addWidget(self.PacketCount)

        self.SWState = QLabel("SW_State")
        labelLayout.addWidget(self.SWState)

        self.PLState = QLabel("PL_State")
        labelLayout.addWidget(self.PLState)

        self.Altitude = QLabel("Altitude")
        labelLayout.addWidget(self.Altitude)

        self.Temp = QLabel("Temperture")
        labelLayout.addWidget(self.Temp)

        self.Volt = QLabel("Voltage")
        labelLayout.addWidget(self.Volt)

        self.GPSLat = QLabel("GPS_Latitude")
        labelLayout.addWidget(self.GPSLat)
        
        self.GPSLong = QLabel("GPS_Longitude")
        labelLayout.addWidget(self.GPSLong)

        self.GyroR = QLabel("GYRO_R")
        labelLayout.addWidget(self.GyroR)

        self.GyroP = QLabel("GYRO_P")
        labelLayout.addWidget(self.GyroP)

        self.GyroY = QLabel("GYRO_Y")
        labelLayout.addWidget(self.GyroY)

        self.Vel = QLabel("Velocity")
        labelLayout.addWidget(self.Vel)

        self.Acc = QLabel("Acceleration")
        labelLayout.addWidget(self.Acc)

        mainLayout.addLayout(labelLayout)
        self.setLayout(mainLayout)
        mainLayout.addStretch(1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTelemetry)
        self.timer.start(1000)

                        #Making Graphs
        self.speedGraph = pg.PlotWidget(title = "Speed vs Time")
        self.speedGraph.plotItem.setLabel('left', 'Speed', units='m/s')
        self.speedGraph.plotItem.setLabel('bottom', 'Time', units='s')

        self.tempGraph = pg.PlotWidget(title = "Temperture vs Time")
        self.tempGraph.plotItem.setLabel('left', 'Temperture', units='C')
        self.tempGraph.plotItem.setLabel('bottom', 'Time', units='s')

        self.altitudeGraph = pg.PlotWidget(title = "Altitude vs Time")
        self.altitudeGraph.plotItem.setLabel('left', 'Altitude', units='m')
        self.altitudeGraph.plotItem.setLabel('bottom', 'Time', units='s')

        self.voltGraph = pg.PlotWidget(title = "Voltage vs Time")
        self.voltGraph.plotItem.setLabel('left', 'Volts', units='v')
        self.voltGraph.plotItem.setLabel('bottom', 'Time', units='s')

        self.LocGraph = pg.PlotWidget(title = "Lantitude Vs Longitude")
        self.LocGraph.plotItem.setLabel('left', 'Lantitude', units='DD')
        self.LocGraph.plotItem.setLabel('bottom', 'Longitude', units='DD')

        graphLayout = QVBoxLayout()
        topGraphs = QHBoxLayout()
        topGraphs.addWidget(self.speedGraph)
        topGraphs.addWidget(self.tempGraph)
        graphLayout.addLayout(topGraphs)
        bottomgraphs = QHBoxLayout()
        bottomgraphs.addWidget(self.altitudeGraph)
        bottomgraphs.addWidget(self.voltGraph)
        bottomgraphs.addWidget(self.LocGraph)
        graphLayout.addLayout(bottomgraphs)
        mainLayout.addLayout(graphLayout)
        self.setLayout(mainLayout)

        #making buttons
        buttonLayout = QHBoxLayout()
        
        self.manualRelease = QPushButton("Manual Release")
        self.manualRelease.clicked.connect(self.manualReleaseActive)
        buttonLayout.addWidget(self.manualRelease)

        self.Calibration = QPushButton("Calibration")
        self.Calibration.clicked.connect(self.calibrationActive)
        buttonLayout.addWidget(self.Calibration)

        self.simulation = QPushButton("Simulation")
        self.simulation.clicked.connect(self.simulationActive)
        buttonLayout.addWidget(self.simulation) 

        self.LED = QPushButton("LED")
        self.LED.setCheckable(True)
        self.LED.clicked.connect(self.LEDactive)
        buttonLayout.addWidget(self.LED)

        self.buzzer = QPushButton("Buzzer")
        self.buzzer.setCheckable(True)
        self.buzzer.clicked.connect(self.buzzerActive)
        buttonLayout.addWidget(self.buzzer)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    #functions for buttons 
    def manualReleaseActive(self):
        print("Payload Relased")

    def calibrationActive(self):
        print("Senors Calibrated")

    def simulationActive(self):
        print("Simulation Completed")

    def LEDactive(self):
        if self.LED.isChecked():
            self.LED.setStyleSheet("background-color : red")
        else:
            self.LED.setStyleSheet("background-color : lightgray")

    def buzzerActive(self):
        if self.buzzer.isChecked():
            self.buzzer.setStyleSheet("background-color : red")
        else:
            self.buzzer.setStyleSheet("background-color : lightgray")

    # fuction to import data (work in progress) (going to have to make get function to obtain data from CSV and than floow the format to replace the label)
    def updateTelemetry(self):
        self.TeamID.setText('Team_ID: 2')

# closing the window 
if __name__ == "__main__": #can only be run if from the right window (not if imported)
    app = QApplication(sys.argv)
    window = GroundStation()
    window.show()
    sys.exit(app.exec_())