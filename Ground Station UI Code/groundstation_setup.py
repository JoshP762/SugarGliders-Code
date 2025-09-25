from PyQt6.QtWidgets import (                                  # PyQt6 imported libraries 
    QApplication, QWidget, QPushButton, QLabel, 
    QLineEdit, QVBoxLayout, QGridLayout, QStatusBar, 
    QToolBar, 
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys

class MainWindow(QWidget):                                     # Window setup
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("Sugargliderstopicon.jpg"))   # Icon
        self.setWindowTitle("Sugar Gliders Ground Station")    # Window Title
        layout = QGridLayout()                                 # Grid layout to propagate later 
        self.setLayout(layout)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())                                           # Ensures program aborts correctly


