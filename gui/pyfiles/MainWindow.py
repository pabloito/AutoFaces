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
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(100, 380, 86, 25))
        self.comboBox.setObjectName("comboBox")
        self.TrainButton = QtWidgets.QPushButton(self.centralwidget)
        self.TrainButton.setGeometry(QtCore.QRect(20, 310, 91, 25))
        self.TrainButton.setObjectName("TrainButton")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(120, 310, 91, 25))
        self.testButton.setObjectName("testButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 280, 191, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(300, 30, 311, 221))
        self.graphWidget.setObjectName("graphWidget")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(40, 380, 48, 26))
        self.spinBox.setObjectName("spinBox")
        self.imageWidget = QtWidgets.QWidget(self.centralwidget)
        self.imageWidget.setGeometry(QtCore.QRect(20, 20, 191, 241))
        self.imageWidget.setObjectName("imageWidget")
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
        self.TrainButton.setText(_translate("MainWindow", "Train"))
        self.testButton.setText(_translate("MainWindow", "Test"))
from pyqtgraph import PlotWidget
