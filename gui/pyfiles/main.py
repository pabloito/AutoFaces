from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from gui.pyfiles.MainWindow import Ui_MainWindow
import os

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        self.setupUi(self)
        self.TrainButton.clicked.connect(self.train)
        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

        self.im = QPixmap("../../att_faces/Fotos/fran/1.pgm")
        self.label = QLabel()
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.imageWidget.setLayout(self.grid)

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)

    def train(self):
        self.graphWidget.clear()
        self.plot([1, 2], [10, 20])

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
    main()