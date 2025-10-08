import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QPushButton
)
import pyqtgraph as pg
import numpy as np
from PyQt6.QtGui import QIcon

# Placeholder functions for button clicks
def manual_release_clicked():
    print('Manual release button clicked')

def calibration_clicked():
    print('Calibration button clicked')

def LED_clicked():
    print('LED button clicked')

def buzzer_clicked():
    print('Buzzer button clicked')

def ping_clicked():
    print('Ping button clicked')

def simulation_clicked():
    print('Simulation button clicked')

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(800, 300, 1000, 800)
    window.setWindowTitle('Sugar Gliders test window')
    window.setWindowIcon(QIcon("Sugargliderstopicon.jpg"))

    # Create a central widget and a main layout for it
    central_widget = QWidget()
    main_layout = QVBoxLayout()
    central_widget.setLayout(main_layout)
    window.setCentralWidget(central_widget)

    # --- Buttons Layout ---
    buttons_layout = QHBoxLayout()
    buttons_label = QLabel('Buttons')
    buttons_label.setStyleSheet("font-size: 20pt;")
    
    manual_release = QPushButton('Manual Release')
    manual_release.clicked.connect(manual_release_clicked)
    
    calibration = QPushButton('Calibration')
    calibration.clicked.connect(calibration_clicked)
    
    LED = QPushButton('Toggle LED')
    LED.clicked.connect(LED_clicked)
    
    buzzer = QPushButton('Toggle buzzer')
    buzzer.clicked.connect(buzzer_clicked)
    
    ping = QPushButton('Ping')
    ping.clicked.connect(ping_clicked)
    
    simulation = QPushButton('Simulation')
    simulation.clicked.connect(simulation_clicked)

    buttons_layout.addWidget(manual_release)
    buttons_layout.addWidget(calibration)
    buttons_layout.addWidget(LED)
    buttons_layout.addWidget(buzzer)
    buttons_layout.addWidget(ping)
    buttons_layout.addWidget(simulation)
    
    main_layout.addWidget(buttons_label)
    main_layout.addLayout(buttons_layout)

    # --- Data Labels ---
    data_label = QLabel('Data')
    data_label.setStyleSheet("font-size: 24pt;")
    main_layout.addWidget(data_label)

    # Add data labels
    data_labels_container = QWidget()
    data_labels_layout = QVBoxLayout()
    data_labels_container.setLayout(data_labels_layout)
    
    data_labels_layout.addWidget(QLabel('Team ID: Team 2: The Sugar Gliders'))
    data_labels_layout.addWidget(QLabel('Mission time:'))
    data_labels_layout.addWidget(QLabel('Packet count:'))
    data_labels_layout.addWidget(QLabel('SW state:'))
    data_labels_layout.addWidget(QLabel('PL state:'))
    data_labels_layout.addWidget(QLabel('Altitude:'))
    data_labels_layout.addWidget(QLabel('Temperature:'))
    data_labels_layout.addWidget(QLabel('Voltage:'))
    data_labels_layout.addWidget(QLabel('GPS_Latitude:'))
    data_labels_layout.addWidget(QLabel('GPS_Longitude:'))
    data_labels_layout.addWidget(QLabel('Gyro_R:'))
    data_labels_layout.addWidget(QLabel('Gyro_P:'))
    data_labels_layout.addWidget(QLabel('Gyro_Y:'))
    data_labels_layout.addWidget(QLabel('Velocity:'))
    data_labels_layout.addWidget(QLabel('Acceleration:'))
    
    main_layout.addWidget(data_labels_container)

    # --- Plotting Section ---
    graphics_layout_widget = pg.GraphicsLayoutWidget()
    
    # Add a title to the layout
    graphics_layout_widget.addLabel("Multiple Graphs", row=0, col=0, colspan=2)

    # Add the first plot
    plot1 = graphics_layout_widget.addPlot(title="Graph 1", row=1, col=0)
    x1 = [1, 2, 3, 4, 5]
    y1 = [2, 4, 1, 5, 3]
    plot1.plot(x1, y1, pen='r')

    # Add the second plot on a new row
    graphics_layout_widget.nextRow()
    plot2 = graphics_layout_widget.addPlot(title="Graph 2", row=2, col=0)
    x2 = [1, 2, 3, 4, 5]
    y2 = [5, 1, 3, 2, 4]
    plot2.plot(x2, y2, pen='g')
    
    main_layout.addWidget(graphics_layout_widget)
    
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()