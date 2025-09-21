import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Plot")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.data_x = np.arange(100)
        self.data_y = np.sin(self.data_x / 10)
        self.curve = self.plot_widget.plot(self.data_x, self.data_y, pen='y')

        self.timer = QTimer()
        self.timer.setInterval(50) # Update every 50ms
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Simulate new data
        self.data_y = np.roll(self.data_y, -1) # Shift data
        self.data_y[-1] = np.sin(self.data_x[-1] / 10 + np.random.rand() * 0.5) # Add new point

        self.curve.setData(self.data_x, self.data_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())