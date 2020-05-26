import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal
from PyQt5.QtCore import Qt

from dcmp.Home import *
from dcmp.compress import *
from dcmp.discompress import *
from dcmp.evaluate import *
from db.read_data import read_data
from cleantool.evaluateAndClean import evaluateAndClean, ModifyRangeLimit, averagePolicy
from decompress.data_de_compress import Data_compress, Data_decompress

import os
import time
import datetime

class Compress(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.compress_ui = Ui_CompressUI()
        self.compress_ui.setupUi(self)
        QtWidgets.QApplication.processEvents()
        self.path = ''
        self.step = 0
        self.mode = 0
        self.row_num = 0
        self.timer = QBasicTimer()
        self.compress_init()

    def compress_init(self):
        self.compress_ui.file_info.setColumnWidth(0,100)
        self.compress_ui.file_info.setColumnWidth(1, 90)
        self.compress_ui.file_info.setColumnWidth(2, 280)
        self.compress_ui.file_info.setColumnWidth(3, 130)


    def set_progress_slot(self, value):
        self.compress_ui.progressBar.setValue(value)

    def set_mode_slot(self, value):
        self.mode = value
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def set_row_slot(self, value):
        self.row_num = value

    def finish_slot(self):
        self.path = ''
        self.mode = 0
        self.compress_ui.comfirm_compress.setEnabled(True)
        self.compress_ui.cancel_compress.setEnabled(False)

    def select_compress(self):
        try:
            self.path, _ = QFileDialog.getOpenFileName(self, 'open file', '/', "Excel files (*.xlsx )")
            file_name = self.path.split('/')[-1]
            fSize=os.path.getsize(self.path)/float(1024)   ##文件大小为...KB
            file_size=round(fSize,2)          ##保留两位小数
            mTime=os.path.getmtime(self.path)    ##获取文件的修改时间
            timeStruct=time.localtime(mTime)
            modify_time=time.strftime('%Y-%m-%d',timeStruct)
            self.compress_ui.file_info.insertRow(0)
            Item_name=QTableWidgetItem(file_name)
            Item_name.setTextAlignment(Qt.AlignCenter|Qt.AlignCenter)
            self.compress_ui.file_info.setItem(0, 0, QTableWidgetItem(Item_name))
            Item_size=QTableWidgetItem(str(file_size)+"KB")
            Item_size.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.compress_ui.file_info.setItem(0, 1, Item_size)
            Item_path=QTableWidgetItem(self.path)
            Item_path.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.compress_ui.file_info.setItem(0, 2, Item_path)
            Item_mtime=QTableWidgetItem(modify_time)
            Item_mtime.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.compress_ui.file_info.setItem(0, 3, Item_mtime)
        except Exception as e:
            self.compress_ui.file_info.setItem(0, 0, QTableWidgetItem('打开文件失败'))

    def delete_file(self):
        self.compress_ui.file_info.removeRow(0)

    def timerEvent(self, event):
        row_number = 10
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 200 / row_number
        self.compress_ui.progressBar.setValue(self.step)

    def confirm_compress(self):
        data = read_data(self.path)
        # out_path = "/Users/mac/Desktop/" + (self.path.split('/')[-1]).split('.')[0] + ".zlib"
        out_path = (self.path.split('/')[-1]).split('.')[0] + ".zlib"
        Data_compress(data, out_path)
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)


    def cancel_compress(self):
        self.timer.stop()

    def to_decomUI(self):
        self.close()
        decompresswindow=Discompress()
        decompresswindow.exec_()

    def to_evaUI(self):
        self.close()
        evaluatewindow=Evaluate()
        evaluatewindow.exec_()


class Discompress(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.discompress_ui = Ui_DiscompressUI()
        self.discompress_ui.setupUi(self)
        self.discompress_init()
        self.timer = QBasicTimer()
        self.step = 0

    def discompress_init(self):
        self.discompress_ui.file_info.setColumnWidth(0, 100)
        self.discompress_ui.file_info.setColumnWidth(1, 90)
        self.discompress_ui.file_info.setColumnWidth(2, 280)
        self.discompress_ui.file_info.setColumnWidth(3, 130)


    def select_decomfile(self):  ##选择解压缩文件
        try:
            self.path, _ = QFileDialog.getOpenFileName(self, 'open file', '/', "Zlib files (*.zlib )")
            file_name = self.path.split('/')[-1]
            fSize = os.path.getsize(self.path) / float(1024)  ##文件大小为...KB
            file_size = round(fSize, 2)  ##保留两位小数
            mTime = os.path.getmtime(self.path)  ##获取文件的修改时间
            timeStruct = time.localtime(mTime)
            modify_time = time.strftime('%Y-%m-%d', timeStruct)
            self.discompress_ui.file_info.insertRow(0)
            Item_name = QTableWidgetItem(file_name)
            Item_name.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.discompress_ui.file_info.setItem(0, 0, QTableWidgetItem(Item_name))
            Item_size = QTableWidgetItem(str(file_size) + "KB")
            Item_size.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.discompress_ui.file_info.setItem(0, 1, Item_size)
            Item_path = QTableWidgetItem(self.path)
            Item_path.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.discompress_ui.file_info.setItem(0, 2, Item_path)
            Item_mtime = QTableWidgetItem(modify_time)
            Item_mtime.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.discompress_ui.file_info.setItem(0, 3, Item_mtime)
        except:
            self.discompress_ui.file_info.setItem(0, 0, QTableWidgetItem("打开文件失败"))

    def delete_decomfile(self):
        self.discompress_ui.file_info.removeRow(0)

    def timerEvent(self, event):
        row_number = 10
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 24 / row_number
        self.discompress_ui.dis_progressBar.setValue(self.step)

    def confirm_decompress(self):  ##确定解压缩
        Data_decompress(self.path, self.path.split('.')[0] + ".xlsx")
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def cancel_decompress(self):  ##取消解压缩
        self.timer.stop()

    def to_comUI(self):
        self.close()
        compresswindow = Compress()
        compresswindow.exec_()

    def to_evaUI(self):
        self.close()
        evaluatewindow = Evaluate()
        evaluatewindow.exec_()


class Evaluate(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.evaluate_ui = Ui_EvaluateUI()
        self.evaluate_ui.setupUi(self)
        self.timer = QBasicTimer()
        self.evaluate_ui.file_info.setColumnWidth(0, 100)
        self.evaluate_ui.file_info.setColumnWidth(1, 90)
        self.evaluate_ui.file_info.setColumnWidth(2, 280)
        self.evaluate_ui.file_info.setColumnWidth(3, 130)

    def select_evafile(self):  ##选择待评估文件
        try:
            self.path, _ = QFileDialog.getOpenFileName(self, 'open file', '/', "Excel files (*.xlsx )")
            file_name = self.path.split('/')[-1]
            fSize = os.path.getsize(self.path) / float(1024)  ##文件大小为...KB
            file_size = round(fSize, 2)  ##保留两位小数
            mTime = os.path.getmtime(self.path)  ##获取文件的修改时间
            timeStruct = time.localtime(mTime)
            modify_time = time.strftime('%Y-%m-%d', timeStruct)
            self.evaluate_ui.file_info.insertRow(0)
            Item_name = QTableWidgetItem(file_name)
            Item_name.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.evaluate_ui.file_info.setItem(0, 0, QTableWidgetItem(Item_name))
            Item_size = QTableWidgetItem(str(file_size) + "KB")
            Item_size.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.evaluate_ui.file_info.setItem(0, 1, Item_size)
            Item_path = QTableWidgetItem(self.path)
            Item_path.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.evaluate_ui.file_info.setItem(0, 2, Item_path)
            Item_mtime = QTableWidgetItem(modify_time)
            Item_mtime.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
            self.evaluate_ui.file_info.setItem(0, 3, Item_mtime)
        except:
            self.evaluate_ui.file_info.setItem(0, 0, QTableWidgetItem("打开文件失败"))

    def delete_evafile(self): ##删除评估文件
        self.evaluate_ui.file_info.removeRow(0)

    def handle_type(self):
        if self.evaluate_ui.radio_pre.isChecked():
            self.type = "压强.png"
        if self.evaluate_ui.radio_tem.isChecked():
            self.type = "温度.png"
        if self.evaluate_ui.radio_moi.isChecked():
            self.type = "湿度.png"
        if self.evaluate_ui.radio_TEC.isChecked():
            self.type = "TEC.png"
        if self.evaluate_ui.radio_fli.isChecked():
            self.type = "闪烁指数.png"
        print(self.type)
        self.pixmap = QtGui.QPixmap(self.type)
        self.evaluate_ui.dis_picture.setPixmap(self.pixmap)
        self.evaluate_ui.dis_picture.setScaledContents(True)  ##图片自适应

    def comfirm_evaluate(self):  ##质量评估
        data = read_data(self.path)
        avg_policy = averagePolicy()
        range_limit = ModifyRangeLimit()
        # data, element_missing_rate, recording_missing_rate, time_illegal_rate, \
        # exceed_rate, outlier_rate, spike_rate, levelshift_rate = evaluateAndClean(range_limit, data, avg_policy)
        data, qualities = evaluateAndClean(range_limit, data, avg_policy)
        ##在表格里添加指标数据
        newItem = QTableWidgetItem(qualities[0])
        self.evaluate_ui.index_tab.setItem(0, 0, newItem)
        newItem = QTableWidgetItem(qualities[1])
        self.evaluate_ui.index_tab.setItem(0, 1, newItem)
        newItem = QTableWidgetItem(qualities[2])
        self.evaluate_ui.index_tab.setItem(0, 2, newItem)
        newItem = QTableWidgetItem(qualities[3])
        self.evaluate_ui.index_tab.setItem(0, 3, newItem)
        newItem = QTableWidgetItem(qualities[4])
        self.evaluate_ui.index_tab.setItem(0, 4, newItem)
        newItem = QTableWidgetItem(qualities[5])
        self.evaluate_ui.index_tab.setItem(0, 5, newItem)
        newItem = QTableWidgetItem(qualities[6])
        self.evaluate_ui.index_tab.setItem(0, 6, newItem)

    def cancel_evaluate(self):  ##取消评估
        self.timer.stop()

    def to_comUI(self):
        self.close()
        compresswindow=Compress()
        compresswindow.exec_()

    def to_decomUI(self):
        self.close()
        decompresswindow=Discompress()
        decompresswindow.exec_()


class Home(QMainWindow):  ##主界面类
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    homewindow = Home()
    compresswindow=Compress()
    decompresswindow=Discompress()
    evaluatewindow=Evaluate()
    btn_compress = homewindow.main_ui.compress
    btn_discompress = homewindow.main_ui.discompress
    btn_evaluate = homewindow.main_ui.evaluation
    btn_compress.clicked.connect(compresswindow.show)
    #btn_compress.clicked.connect(homewindow.close)
    btn_discompress.clicked.connect(decompresswindow.show)
    #btn_discompress.clicked.connect(homewindow.close)
    btn_evaluate.clicked.connect(evaluatewindow.show)
    #btn_evaluate.clicked.connect(homewindow.close)
    homewindow.show()
    sys.exit(app.exec_())

