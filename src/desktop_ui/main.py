# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow_OCR(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {\n"
"    background-color: none;\n"
"    border: 1px solid;\n"
"}\n"
"\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setStyleSheet("QTabWidget{\n"
"    border: 1px solid rgb(0, 0, 0);\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_doc = QtWidgets.QWidget()
        self.tab_doc.setObjectName("tab_doc")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_doc)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 791, 381))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(4, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.l_image = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.l_image.setText("")
        self.l_image.setObjectName("l_image")
        self.verticalLayout.addWidget(self.l_image)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab_doc)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, 379, 791, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(4, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.le_file = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.le_file.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\\nborder: 1px solid darkgrey;")
        self.le_file.setObjectName("le_file")
        self.le_file.setEnabled(False)
        self.horizontalLayout_2.addWidget(self.le_file)
        self.pbtn_open = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pbtn_open.setMinimumSize(QtCore.QSize(60, 20))
        self.pbtn_open.setStyleSheet("QPushButton {\n"
"    font-size: 14px;\n"
"    color: #fff;\n"
"    background-color: rgb(133, 129, 255);\n"
"    font: 75 12pt \"Calibri\";\n"
"    border: 1px solid transparent;\n"
"    border-color: #357ebd;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(224, 232, 246);\n"
"}")
        self.pbtn_open.setObjectName("pbtn_open")
        self.horizontalLayout_2.addWidget(self.pbtn_open)
        self.pbtn_read = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pbtn_read.setMinimumSize(QtCore.QSize(80, 20))
        self.pbtn_read.setStyleSheet("QPushButton {\n"
"    font-size: 14px;\n"
"    color: #fff;\n"
"    background-color: rgb(133, 129, 255);\n"
"    font: 75 12pt \"Calibri\";\n"
"    border: 1px solid transparent;\n"
"    border-color: #357ebd;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(224, 232, 246);\n"
"}")
        self.pbtn_read.setObjectName("pbtn_read")
        self.horizontalLayout_2.addWidget(self.pbtn_read)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_doc)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(-1, 409, 791, 121))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setContentsMargins(4, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.te_result = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.te_result.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\\nborder: 1px solid darkgrey;")
        self.te_result.setObjectName("te_result")
        self.verticalLayout_2.addWidget(self.te_result)
        self.tabWidget.addTab(self.tab_doc, "")
        self.tab_cam = QtWidgets.QWidget()
        self.tab_cam.setObjectName("tab_cam")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tab_cam)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 791, 381))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_3.setContentsMargins(4, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.l_webcam = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.l_webcam.setText("")
        self.l_webcam.setObjectName("l_webcam")
        self.verticalLayout_3.addWidget(self.l_webcam)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab_cam)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 380, 791, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(4, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pbtn_recognize = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pbtn_recognize.setMinimumSize(QtCore.QSize(0, 20))
        self.pbtn_recognize.setStyleSheet("QPushButton {\n"
"    font-size: 14px;\n"
"    color: #fff;\n"
"    background-color: rgb(133, 129, 255);\n"
"    font: 75 12pt \"Calibri\";\n"
"    border: 1px solid transparent;\n"
"    border-color: #357ebd;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(224, 232, 246);\n"
"}")
        self.pbtn_recognize.setObjectName("pbtn_recognize")
        self.horizontalLayout_3.addWidget(self.pbtn_recognize)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.tab_cam)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 410, 791, 121))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_6.setContentsMargins(4, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.te_webcam_result = QtWidgets.QTextEdit(self.verticalLayoutWidget_5)
        self.te_webcam_result.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\\nborder: 1px solid darkgrey;")
        self.te_webcam_result.setObjectName("te_webcam_result")
        self.verticalLayout_6.addWidget(self.te_webcam_result)
        self.tabWidget.addTab(self.tab_cam, "")
        self.verticalLayout_1.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        self.menuExit = QtWidgets.QMenu(self.menubar)
        self.menuExit.setObjectName("menuExit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_train = QtWidgets.QAction(MainWindow)
        self.action_train.setObjectName("action_train")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.action_camera = QtWidgets.QAction(MainWindow)
        self.action_camera.setCheckable(True)
        self.action_camera.setObjectName("action_camera")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menuExit.addSeparator()
        self.menuExit.addAction(self.action_quit)
        self.menuHelp.addAction(self.action_about)
        self.menubar.addAction(self.menuExit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pbtn_open.setText(_translate("MainWindow", "Open"))
        self.pbtn_read.setText(_translate("MainWindow", "Read"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_doc), _translate("MainWindow", "Document"))
        self.pbtn_recognize.setText(_translate("MainWindow", "Recognize"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_cam), _translate("MainWindow", "WebCam"))
        self.menuExit.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.action_train.setText(_translate("MainWindow", "Train"))
        self.action_quit.setText(_translate("MainWindow", "Quit"))
        self.action_camera.setText(_translate("MainWindow", "Camera"))
        self.action_about.setText(_translate("MainWindow", "About"))

