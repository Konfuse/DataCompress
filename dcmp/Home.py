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
        MainWindow.resize(770, 572)
        MainWindow.setStyleSheet("background-color: rgb(32, 140, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.compress = QtWidgets.QPushButton(self.centralwidget)
        self.compress.setGeometry(QtCore.QRect(140, 170, 161, 151))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.compress.setFont(font)
        self.compress.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:100px;\n"
"\n"
"")
        self.compress.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/9.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.compress.setIcon(icon)
        self.compress.setIconSize(QtCore.QSize(200, 200))
        self.compress.setObjectName("compress")
        self.discompress = QtWidgets.QPushButton(self.centralwidget)
        self.discompress.setGeometry(QtCore.QRect(310, 170, 171, 151))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.discompress.setFont(font)
        self.discompress.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:100px;\n"
"")
        self.discompress.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.discompress.setIcon(icon1)
        self.discompress.setIconSize(QtCore.QSize(200, 200))
        self.discompress.setObjectName("discompress")
        self.evaluation = QtWidgets.QPushButton(self.centralwidget)
        self.evaluation.setGeometry(QtCore.QRect(490, 170, 161, 151))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.evaluation.setFont(font)
        self.evaluation.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:100px;\n"
"")
        self.evaluation.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/image/7.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.evaluation.setIcon(icon2)
        self.evaluation.setIconSize(QtCore.QSize(200, 200))
        self.evaluation.setObjectName("evaluation")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(180, 280, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255,255,255);")
        self.label_10.setObjectName("label_10")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(350, 280, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255,255,255);")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(530, 280, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255,255,255);")
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 770, 26))
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
        self.label_10.setText(_translate("MainWindow", "  压缩文件"))
        self.label_8.setText(_translate("MainWindow", "  解压缩文件"))
        self.label_9.setText(_translate("MainWindow", "  质量评估"))
from dcmp import picture_rc
