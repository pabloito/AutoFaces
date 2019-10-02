# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pcaSelector = QtWidgets.QComboBox(self.centralwidget)
        self.pcaSelector.setGeometry(QtCore.QRect(270, 360, 86, 25))
        self.pcaSelector.setObjectName("pcaSelector")
        self.pcaSelector.addItem("")
        self.pcaSelector.addItem("")
        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(390, 360, 91, 25))
        self.trainButton.setObjectName("trainButton")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(390, 390, 91, 25))
        self.testButton.setObjectName("testButton")
        self.fileInput = QtWidgets.QLineEdit(self.centralwidget)
        self.fileInput.setGeometry(QtCore.QRect(60, 310, 421, 25))
        self.fileInput.setObjectName("fileInput")
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(300, 30, 311, 221))
        self.graphWidget.setObjectName("graphWidget")
        self.eigenSelector = QtWidgets.QSpinBox(self.centralwidget)
        self.eigenSelector.setGeometry(QtCore.QRect(270, 390, 48, 26))
        self.eigenSelector.setObjectName("eigenSelector")
        self.personLabel = QtWidgets.QLabel(self.centralwidget)
        self.personLabel.setGeometry(QtCore.QRect(90, 270, 67, 17))
        self.personLabel.setText("0")
        self.personLabel.setObjectName("personLabel")
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(490, 310, 89, 25))
        self.browseButton.setObjectName("browseButton")
        self.filename = QtWidgets.QLabel(self.centralwidget)
        self.filename.setGeometry(QtCore.QRect(20, 310, 31, 17))
        self.filename.setObjectName("filename")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 360, 91, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 390, 141, 20))
        self.label_2.setObjectName("label_2")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(40, 20, 171, 231))
        self.imageLabel.setAutoFillBackground(False)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pcaSelector.setItemText(0, _translate("MainWindow", "KPCA"))
        self.pcaSelector.setItemText(1, _translate("MainWindow", "PCA"))
        self.trainButton.setText(_translate("MainWindow", "Train"))
        self.testButton.setText(_translate("MainWindow", "Test"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.filename.setText(_translate("MainWindow", "path"))
        self.label.setText(_translate("MainWindow", "PCA method"))
        self.label_2.setText(_translate("MainWindow", "N° of Eigenvectors"))
from pyqtgraph import PlotWidget
