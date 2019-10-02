import time

from PyQt5 import QtWidgets, uic, QtTest
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QFileDialog
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from gui.pyfiles.MainWindow import Ui_FaceRecognizer3000

import os

from classifier.svm_classifier import svm_classifier_pca
from gui.pyfiles.plotting import PlotCanvas


class FaceRecognizer3000(QtWidgets.QMainWindow, Ui_FaceRecognizer3000):

    def __init__(self, *args, **kwargs):
        super(FaceRecognizer3000, self).__init__(*args, **kwargs)

        #Load the UI Page
        self.setupUi(self)
        self.setWindowIcon(QIcon('../images/icon.jpeg'))
        # Set button presses
        self.browseButton.clicked.connect(self.browsePress)
        self.trainButton.clicked.connect(self.train)
        self.testButton.clicked.connect(self.test)
        self.stopButton.clicked.connect(self.stopAction)

        # Images picked up
        self.files = None

        # Flag to stop execution
        self.should_stop = False
        self.is_stopped = False

        # Classified counts for each category
        self.categories = []
        self.category_counts = []
        self.plot = None

        # Plot initial graph
        self.plot = PlotCanvas(self, width=3.2, height=2.7, labels=self.categories, counts=self.category_counts)
        self.plot.move(300, 0)

        # Add frame to photo
        self.imageLabel.setLineWidth(3)

    def plot_graph(self):
        self.plot.do_update(self.categories, self.category_counts)

    def train(self):
        svm_classifier_pca.train()

    def test(self):
        self.test_files()

    def stopAction(self):
        if self.stopButton.text == 'stop':
            self.should_stop = True
        elif self.stopButton.text == 'clear':
            self.clear_data()
            self.stopButton.setText('stop')

    def clear_data(self):
        pass

    def browsePress(self):
        self.openFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        dir_name = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_name:
            self.files = dir_name
            self.fileInput.setText(dir_name)

    def test_files(self):
        for root, dirs, files in os.walk(self.files, topdown=True):
            for file in files:
                full_path = os.path.join(root, file)
                print(full_path)
                self.set_image(full_path)
                prediction = svm_classifier_pca.predict_for_image(full_path)
                predicted_category = svm_classifier_pca.map_person(prediction[0])
                self.personLabel.setText(predicted_category)
                self.update_categories(predicted_category)
                self.plot_graph()

                if self.should_stop:
                    break
                QtTest.QTest.qWait(1000)

            if self.should_stop:
                self.should_stop = False
                self.stopButton.setText("clear")
                break

    def set_image(self, path_to_file):
        self.imageLabel.setText("")
        pixmap = QPixmap(path_to_file).scaled(self.imageLabel.width(), self.imageLabel.height())
        self.imageLabel.setPixmap(pixmap)

    def update_categories(self, predicted_category):
        try:
            index = self.categories.index(predicted_category)
            self.category_counts[index] += 1
        except ValueError:
            self.categories.append(predicted_category)
            self.category_counts.append(1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = FaceRecognizer3000()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()