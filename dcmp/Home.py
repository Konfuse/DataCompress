# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Home.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(592, 515)
        MainWindow.setStyleSheet("background-color: rgb(32, 140, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.compress = QtWidgets.QPushButton(self.centralwidget)
        self.compress.setGeometry(QtCore.QRect(130, 150, 161, 151))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.compress.setFont(font)
        self.compress.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "background-image: url(:/image/1.jpg);\n"
                                    "")
        self.compress.setText("")
        self.compress.setObjectName("compress")
        self.discompress = QtWidgets.QPushButton(self.centralwidget)
        self.discompress.setGeometry(QtCore.QRect(300, 150, 171, 151))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.discompress.setFont(font)
        self.discompress.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "background-image: url(:/image/2.jpg);")
        self.discompress.setText("")
        self.discompress.setObjectName("discompress")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 592, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "主界面"))


from .picture_rc import *
