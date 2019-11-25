from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from desktop_ui.main import Ui_MainWindow_OCR
from desktop_ui.about_ui import AboutUI
from controllers.ocr_controller import OCRController
import sys
import cv2
import threading

MAIN_WINDOW_WIDTH = 786
MAIN_WINDOW_HEIGHT = 379
MAIN_WINDOW_WIDTH_WEBCAM = 366
MAIN_WINDOW_HEIGHT_WEBCAM = 379
TIMER_INTERVAL = 100


class MainUI(QtWidgets.QMainWindow, Ui_MainWindow_OCR):
    __results = []
    __webcam = None
    __timer_webcam = None
    __current_image = None

    def __init__(self):
        super(MainUI, self).__init__()
        self.setupUi(self)
        self.__controller = OCRController()
        self._init_ui_events()

    def _init_ui_events(self):
        self.pbtn_open.clicked.connect(self._on_open_file)
        self.pbtn_read.clicked.connect(self._on_read)
        self.pbtn_recognize.clicked.connect(self._on_recognize)
        self.action_about.triggered.connect(self._on_show_about_window)
        self.tabWidget.currentChanged.connect(self._on_tab_change)

    def _init_webcam(self):
        if self.__webcam == None:
            self.__webcam = cv2.VideoCapture(0)
            self.__webcam.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # turn the autofocus off
            # self.__webcam.set(3, 1280)  # set the Horizontal resolution
            # self.__webcam.set(4, 720)  # Set the Vertical resolution

    def _release_webcam(self):
        self.__webcam.release()
        self.__webcam = None

    def _on_tab_change(self, i):
        def init_webcam():
            # init webcam when webcam tab is selected
            self._init_webcam()
            self.__timer_webcam = QTimer()
            self.__timer_webcam.timeout.connect(self._on_next_frame_webcam)
            self.__timer_webcam.start(TIMER_INTERVAL)

        def init_document():
            # init webcam when document tab is selected
            self.__timer_webcam.stop()
            self._release_webcam()

        def switch(x):
            return {
                '0': lambda x: init_document(),
                '1': lambda x: init_webcam(),
            }[str(x)](x)
        switch(i)

    def _on_show_about_window(self):
        my_dialog = AboutUI()
        my_dialog.exec_()

    def _on_open_file(self):
        openfile = QFileDialog.getOpenFileName(self, 'Choose File', '', 'Images(*.jpg)')
        self.le_file.setText(openfile[0])
        self._open_image(openfile[0])

    def _open_image(self, filename):
        image = cv2.imread(filename)
        image_resized = cv2.resize(image, (MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT), None, 0, 0, cv2.COLOR_BGR2RGB)
        height, width, byte_value = image_resized.shape
        byte_value = byte_value * width
        qt_image = QtGui.QImage(cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB), width, height, byte_value, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(qt_image)
        self.l_image.setPixmap(pix)

    def _on_read(self):
        filename = self.le_file.text()
        print(filename)
        self.__document_reader = DocumentReader(filename, self.__controller)
        self.__document_reader.sinOut.connect(self._add_textline_to_textedit)
        self.__document_reader.start()

    def _add_textline_to_textedit(self, textline):
        try:
            self.__results.append(textline)
            self.te_result.setText('\n'.join(self.__results))
        except Exception as ex:
            print(ex)

    def _on_next_frame_webcam(self):
        try:
            ret, img = self.__webcam.read()
            if ret:
                height, width, byteValue = img.shape
                img_new = cv2.resize(img, (width, height), None, 0, 0, cv2.COLOR_BGR2RGB)
                self.__current_image = img_new
                height, width, byteValue = img_new.shape
                byteValue = byteValue * width

                qImage = QtGui.QImage(cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB), width, height, byteValue,
                                      QtGui.QImage.Format_RGB888)
                pix = QtGui.QPixmap.fromImage(qImage)
                self.l_webcam.setPixmap(pix)
            else:
                self.__timer_webcam.stop()
                self._release_webcam()
                return 0
        except Exception as ex:
            print(ex)
            self.__timer_webcam.stop()
            self._release_webcam()

    def _on_recognize(self):
        t_detector = LabelDetector(self.__current_image, self.__controller)
        t_detector.sinOut.connect(self._add_textline_to_textedit_webcam)
        t_detector.start()

    def _add_textline_to_textedit_webcam(self, textline):
        try:
            self.te_webcam_result.setText(textline)
        except Exception as ex:
            print(ex)


class DocumentReader(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, filename, controller, parent=None):
        super(DocumentReader, self).__init__(parent)
        self.__controller = controller
        self.__filename = filename
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        self.__controller.read_text_to_xls(self.__filename, self.sinOut)


class LabelDetector(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, image, controller, parent=None):
        super(LabelDetector, self).__init__(parent)
        self.__controller = controller
        self.__image = image
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        #image = self.__controller.get_detected_image(self.__image)
        #cv2.imwrite(r'C:\my_repo\BizDoc-Ocr\pixlink_resut.jpg', image)
        result = self.__controller.read_sparse_text(self.__image)
        self.sinOut.emit(result)
        #cv2.imwrite(r'C:\my_repo\BizDoc-Ocr\pixlink_resut.jpg', self.__image)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui_Main = MainUI()
    # ui_Main.resize(600, 480)
    ui_Main.show()
    sys.exit(app.exec_())
