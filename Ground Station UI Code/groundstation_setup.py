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
        self.setWindowIcon(QIcon("Sugargliderstopicon"))
        self.setWindowTitle("Sugar Gliders Ground Station")
        layout = QGridLayout()
        self.setLayout(layout)

        canvas = FigureCanvasQTAgg(fig)
        layout.addWidget(canvas)

x = [1, 2, 8, 3, 6]
y= [9, 3, 1, 6, 3]

fig = Figure(figsize=(4,4))
ax = fig.add_subplot()
ax.plot(x, y)

       # self.label1 = QLabel("Test1")
        # layout.addWidget(self.label1, 0, 0)

        #self.label2 = QLabel("Test2")
       # layout.addWidget(self.label2, 1, 0)

       # self.input1 = QLineEdit()
       # layout.addWidget(self.input1, 0, 1)

      #  self.input2 = QLineEdit()
       # layout.addWidget(self.input2, 1, 1)

       # button = QPushButton("Submit")
        #button.setFixedWidth(50)
        #button.clicked.connect(self.display)
       # layout.addWidget(button, 2, Qt.AlignmentFlag.AlignRight)

    # def display(self):
        # print(self.input1.text())
        # print(self.input2.text())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())