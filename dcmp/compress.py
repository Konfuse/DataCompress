# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compress.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompressUI(object):
    def setupUi(self, CompressUI):
        CompressUI.setObjectName("CompressUI")
        CompressUI.resize(658, 605)
        CompressUI.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.progressBar = QtWidgets.QProgressBar(CompressUI)
        self.progressBar.setGeometry(QtCore.QRect(90, 380, 471, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar::chunk { background-color: rgb(32, 140, 255) }\n"
"QProgressBar { text-align: right }")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(CompressUI)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(340, 450, 241, 101))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.comfirm_compress = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comfirm_compress.setFont(font)
        self.comfirm_compress.setStyleSheet("background-color: rgb(32, 140, 255);\n"
"color: rgb(255, 255, 255);")
        self.comfirm_compress.setObjectName("comfirm_compress")
        self.horizontalLayout_7.addWidget(self.comfirm_compress)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.cancel_compress = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cancel_compress.setFont(font)
        self.cancel_compress.setStyleSheet("background-color: rgb(32, 140, 255);\n"
"color: rgb(255, 255, 255);")
        self.cancel_compress.setObjectName("cancel_compress")
        self.horizontalLayout_7.addWidget(self.cancel_compress)
        self.scan_filename = QtWidgets.QPushButton(CompressUI)
        self.scan_filename.setGeometry(QtCore.QRect(90, 80, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.scan_filename.setFont(font)
        self.scan_filename.setStyleSheet("background-color: rgb(32, 140, 255);\n"
"color: rgb(255, 255, 255);")
        self.scan_filename.setObjectName("scan_filename")
        self.filename = QtWidgets.QLabel(CompressUI)
        self.filename.setGeometry(QtCore.QRect(330, 80, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.filename.setFont(font)
        self.filename.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.filename.setText("")
        self.filename.setAlignment(QtCore.Qt.AlignCenter)
        self.filename.setObjectName("filename")
        self.log_info = QtWidgets.QTextBrowser(CompressUI)
        self.log_info.setGeometry(QtCore.QRect(90, 170, 471, 151))
        self.log_info.setObjectName("log_info")

        self.retranslateUi(CompressUI)
        self.scan_filename.clicked.connect(CompressUI.select_compress)
        self.comfirm_compress.clicked.connect(CompressUI.confirm_compress)
        self.cancel_compress.clicked.connect(CompressUI.cancel_compress)
        QtCore.QMetaObject.connectSlotsByName(CompressUI)

    def retranslateUi(self, CompressUI):
        _translate = QtCore.QCoreApplication.translate
        CompressUI.setWindowTitle(_translate("CompressUI", "压缩界面"))
        self.comfirm_compress.setText(_translate("CompressUI", "压缩"))
        self.cancel_compress.setText(_translate("CompressUI", "取消"))
        self.scan_filename.setText(_translate("CompressUI", "浏览文件"))
