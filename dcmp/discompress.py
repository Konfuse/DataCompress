# -*- coding: utf-8 -*-

# Form implementation generated from reading dcmp file 'discompress.dcmp'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DiscompressUI(object):
    def setupUi(self, DiscompressUI):
        DiscompressUI.setObjectName("DiscompressUI")
        DiscompressUI.resize(658, 603)
        DiscompressUI.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.dis_progressBar = QtWidgets.QProgressBar(DiscompressUI)
        self.dis_progressBar.setGeometry(QtCore.QRect(70, 270, 481, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dis_progressBar.setFont(font)
        self.dis_progressBar.setStyleSheet("QProgressBar::chunk { background-color: rgb(32, 140, 255) }\n"
"QProgressBar { text-align: right }")
        self.dis_progressBar.setProperty("value", 0)
        self.dis_progressBar.setObjectName("dis_progressBar")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(DiscompressUI)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(335, 360, 261, 89))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.comfirm_discompress = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comfirm_discompress.setFont(font)
        self.comfirm_discompress.setStyleSheet("background-color: rgb(32, 140, 255);\n"
"color: rgb(255, 255, 255);")
        self.comfirm_discompress.setObjectName("comfirm_discompress")
        self.horizontalLayout_7.addWidget(self.comfirm_discompress)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.cancel_discompress = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_discompress.setFont(font)
        self.cancel_discompress.setStyleSheet("background-color: rgb(32, 140, 255);\n"
"color: rgb(255, 255, 255);")
        self.cancel_discompress.setObjectName("cancel_discompress")
        self.horizontalLayout_7.addWidget(self.cancel_discompress)
        self.scan_discomfile = QtWidgets.QPushButton(DiscompressUI)
        self.scan_discomfile.setGeometry(QtCore.QRect(70, 150, 141, 61))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.scan_discomfile.setFont(font)
        self.scan_discomfile.setStyleSheet("background-color: rgb(32, 140, 255);\n"
"color: rgb(255, 255, 255);")
        self.scan_discomfile.setObjectName("scan_discomfile")
        self.dis_filename = QtWidgets.QLabel(DiscompressUI)
        self.dis_filename.setGeometry(QtCore.QRect(320, 160, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.dis_filename.setFont(font)
        self.dis_filename.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.dis_filename.setAlignment(QtCore.Qt.AlignCenter)
        self.dis_filename.setObjectName("dis_filename")

        self.retranslateUi(DiscompressUI)
        self.scan_discomfile.clicked.connect(DiscompressUI.select_discomfile)
        self.comfirm_discompress.clicked.connect(DiscompressUI.confirm_discompress)
        self.cancel_discompress.clicked.connect(DiscompressUI.cancel_discompress)
        QtCore.QMetaObject.connectSlotsByName(DiscompressUI)

    def retranslateUi(self, DiscompressUI):
        _translate = QtCore.QCoreApplication.translate
        DiscompressUI.setWindowTitle(_translate("DiscompressUI", "解压缩界面"))
        self.comfirm_discompress.setText(_translate("DiscompressUI", "解压缩"))
        self.cancel_discompress.setText(_translate("DiscompressUI", "取消"))
        self.scan_discomfile.setText(_translate("DiscompressUI", "浏览文件"))
        self.dis_filename.setText(_translate("DiscompressUI", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
