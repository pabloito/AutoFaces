# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FaceRecognizer3000(object):
    def setupUi(self, FaceRecognizer3000):
        FaceRecognizer3000.setObjectName("FaceRecognizer3000")
        FaceRecognizer3000.resize(637, 480)
        self.centralwidget = QtWidgets.QWidget(FaceRecognizer3000)
        self.centralwidget.setObjectName("centralwidget")
        self.pcaSelector = QtWidgets.QComboBox(self.centralwidget)
        self.pcaSelector.setGeometry(QtCore.QRect(150, 360, 86, 25))
        self.pcaSelector.setObjectName("pcaSelector")
        self.pcaSelector.addItem("")
        self.pcaSelector.addItem("")
        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(250, 360, 91, 25))
        self.trainButton.setObjectName("trainButton")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(350, 360, 91, 25))
        self.testButton.setObjectName("testButton")
        self.fileInput = QtWidgets.QLineEdit(self.centralwidget)
        self.fileInput.setGeometry(QtCore.QRect(90, 310, 391, 25))
        self.fileInput.setObjectName("fileInput")
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(300, 30, 311, 221))
        self.graphWidget.setObjectName("graphWidget")
        self.personLabel = QtWidgets.QLabel(self.centralwidget)
        self.personLabel.setGeometry(QtCore.QRect(90, 270, 67, 17))
        self.personLabel.setText("")
        self.personLabel.setObjectName("personLabel")
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(490, 310, 89, 25))
        self.browseButton.setObjectName("browseButton")
        self.filename = QtWidgets.QLabel(self.centralwidget)
        self.filename.setGeometry(QtCore.QRect(20, 310, 61, 17))
        self.filename.setObjectName("filename")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 360, 91, 17))
        self.label.setObjectName("label")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(40, 20, 171, 231))
        self.imageLabel.setAutoFillBackground(False)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(490, 360, 89, 25))
        self.stopButton.setObjectName("stopButton")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(150, 390, 48, 26))
        self.spinBox.setObjectName("spinBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 390, 131, 17))
        self.label_2.setObjectName("label_2")
        FaceRecognizer3000.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FaceRecognizer3000)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 637, 22))
        self.menubar.setObjectName("menubar")
        FaceRecognizer3000.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FaceRecognizer3000)
        self.statusbar.setObjectName("statusbar")
        FaceRecognizer3000.setStatusBar(self.statusbar)

        self.retranslateUi(FaceRecognizer3000)
        QtCore.QMetaObject.connectSlotsByName(FaceRecognizer3000)

    def retranslateUi(self, FaceRecognizer3000):
        _translate = QtCore.QCoreApplication.translate
        FaceRecognizer3000.setWindowTitle(_translate("FaceRecognizer3000", "MainWindow"))
        self.pcaSelector.setItemText(0, _translate("FaceRecognizer3000", "KPCA"))
        self.pcaSelector.setItemText(1, _translate("FaceRecognizer3000", "PCA"))
        self.trainButton.setText(_translate("FaceRecognizer3000", "Train"))
        self.testButton.setText(_translate("FaceRecognizer3000", "Test"))
        self.browseButton.setText(_translate("FaceRecognizer3000", "Browse"))
        self.filename.setText(_translate("FaceRecognizer3000", "directory"))
        self.label.setText(_translate("FaceRecognizer3000", "PCA method"))
        self.stopButton.setText(_translate("FaceRecognizer3000", "stop"))
        self.label_2.setText(_translate("FaceRecognizer3000", "N° of eigenvectors"))
from pyqtgraph import PlotWidget
