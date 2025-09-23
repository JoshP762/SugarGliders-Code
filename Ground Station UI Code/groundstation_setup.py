from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, 
    QLineEdit, QVBoxLayout, QGridLayout
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("Sugargliderstopicon.jpg"))
        self.setWindowTitle("Sugar Gliders Ground Station")
        layout = QGridLayout()
        self.setLayout(layout)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())