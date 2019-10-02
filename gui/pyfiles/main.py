from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout, QFileDialog
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from gui.pyfiles.MainWindow import Ui_MainWindow
import os
from classifier.svm_classifier import svm_classifier_pca

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        self.setupUi(self)
        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

        # Set button presses
        self.browseButton.clicked.connect(self.browsePress)
        self.trainButton.clicked.connect(self.train)
        self.testButton.clicked.connect(self.test)

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)

    def train(self):
        self.graphWidget.clear()
        self.plot([1, 2], [10, 20])

    def test(self):
        print(self.fileInput.text())

    def browsePress(self):
        self.openFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.fileInput.setText(fileName)
            self.set_image(fileName)

    def set_image(self, path_to_file):
        print(path_to_file)
        self.imageLabel.setText("")
        pixmap = QPixmap(path_to_file).scaled(self.imageLabel.width(), self.imageLabel.height())
        self.imageLabel.setPixmap(pixmap)
        svm_classifier_pca.predict_for_image()
        self.personLabel.setText(".Ito")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()