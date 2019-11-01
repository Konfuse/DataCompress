import sys
import logging
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
from PyQt5.QtCore import QBasicTimer, QThread, pyqtSignal

from db.db_insert import insert_all
from dcmp.Home import *
from dcmp.compress import *
from dcmp.discompress import *
from db.read_data import read_data
from cleantool.evaluateAndClean import evaluateAndClean, ModifyRangeLimit, averagePolicy
from decompress.Data_de_compress import Data_compress, Data_decompress


class Compress(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.compress_ui = Ui_CompressUI()
        self.compress_ui.setupUi(self)

        self.path = ''
        self.step = 0
        self.mode = 0
        self.row_num = 0
        self.compress_thread = CompressThread()
        self.timer = QBasicTimer()
        self.compress_init()

    def compress_init(self):
        self.compress_thread.log_signal.connect(self.set_log_slot)
        self.compress_thread.progress_signal.connect(self.set_progress_slot)
        self.compress_thread.mode_signal.connect(self.set_mode_slot)
        self.compress_thread.finished_signal.connect(self.finish_slot)
        self.compress_thread.row_signal.connect(self.set_row_slot)

    def set_log_slot(self, new_log):
        self.compress_ui.log_info.append(new_log)

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
            self.compress_ui.filename.setText(file_name)
        except Exception as e:
            self.compress_ui.filename.setText("打开文件失败")

    def timerEvent(self, event):
        if self.mode == 0:
            if self.step > 30:
                self.timer.stop()
                return
            self.step = self.step + 0.2
            self.compress_ui.progressBar.setValue(self.step)
        elif self.mode == 1:
            if self.step > 100:
                self.timer.stop()
                return
            self.step = self.step + 24 / self.row_num
            self.compress_ui.progressBar.setValue(self.step)

    def confirm_compress(self):
        self.step = 0
        self.compress_ui.comfirm_compress.setEnabled(False)
        self.compress_ui.cancel_compress.setEnabled(True)
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.compress_thread.set_path(self.path)
            self.timer.start(100, self)
            self.compress_thread.start()

    def cancel_compress(self):
        self.timer.stop()


class CompressThread(QThread):
    path = None
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    mode_signal = pyqtSignal(int)
    row_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def set_path(self, path):
        self.path = path

    def run(self):
        if self.path is None:
            self.log_signal.emit("文件名为空")
        else:
            self.log_signal.emit("开始读取文件")
            data = read_data(self.path)
            self.log_signal.emit("文件读取完毕，开始清洗与评估...")
            avg_policy = averagePolicy()
            range_limit = ModifyRangeLimit()
            data, miss_rate, exceed_rate, jump_rate = evaluateAndClean(range_limit, data, avg_policy)
            self.log_signal.emit("缺失率：{0}, 跳变率: {1}, 越界率: {2}".format(miss_rate, jump_rate, exceed_rate))
            self.row_signal.emit(len(data))
            self.progress_signal.emit(30)
            self.mode_signal.emit(1)
            self.log_signal.emit("开始压缩......")
            out_path = "C:/Users/Konfuse/Desktop/" + (self.path.split('/')[-1]).split('.')[0] + ".zlib"
            Data_compress(data, out_path)
            self.log_signal.emit("压缩完成......")
            self.progress_signal.emit(100)
            self.finished_signal.emit()


class Discompress(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.discompress_ui = Ui_DiscompressUI()
        self.discompress_ui.setupUi(self)

        self.timer = QBasicTimer()
        self.path = ''
        self.step = 0

    def select_discomfile(self):  ##选择解压缩文件
        try:
            self.path, _ = QFileDialog.getOpenFileName(self, 'open file', '/', "Zlib files (*.zlib )")
            fname = self.path.split('/')[-1]
            self.discompress_ui.dis_filename.setText(fname)
        except:
            self.discompress_ui.dis_filename.setText("打开文件失败")

    def timerEvent(self, event):
        row_number = 10
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 24 / row_number
        self.discompress_ui.dis_progressBar.setValue(self.step)

    def confirm_discompress(self):  ##确定解压缩
        self.step = 0
        self.discompress_ui.comfirm_discompress.setEnabled(False)
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)
        data = Data_decompress(self.path, self.path.split('.')[0] + ".xlsx")
        self.discompress_ui.cancel_discompress.setEnabled(False)
        insert_all(data)
        self.discompress_ui.comfirm_discompress.setEnabled(True)
        self.discompress_ui.cancel_discompress.setEnabled(True)
        self.path = ''

    def cancel_discompress(self):  ##取消解压缩
        self.timer.stop()


class Home(QMainWindow):  ##主界面类
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    logging.basicConfig(filename='logger.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    ###
    homewindow = Home()
    compresswindow = Compress()
    discompresswindow = Discompress()
    btn_compress = homewindow.main_ui.compress
    btn_compress.clicked.connect(compresswindow.show)
    btn_discompress = homewindow.main_ui.discompress
    btn_discompress.clicked.connect(discompresswindow.show)
    homewindow.show()
    sys.exit(app.exec_())
