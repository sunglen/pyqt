# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Wed Nov 15 17:16:51 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName(_fromUtf8("MainForm"))
        MainForm.resize(633, 645)
        self.resultBrowser = QtGui.QTextBrowser(MainForm)
        self.resultBrowser.setGeometry(QtCore.QRect(20, 240, 581, 341))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.resultBrowser.setFont(font)
        self.resultBrowser.setObjectName(_fromUtf8("resultBrowser"))
        self.verticalLayoutWidget_7 = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(480, 40, 101, 171))
        self.verticalLayoutWidget_7.setObjectName(_fromUtf8("verticalLayoutWidget_7"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_10.setMargin(0)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.queryButton = QtGui.QPushButton(self.verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.queryButton.setFont(font)
        self.queryButton.setObjectName(_fromUtf8("queryButton"))
        self.verticalLayout_10.addWidget(self.queryButton)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem)
        self.listButton = QtGui.QPushButton(self.verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.listButton.setFont(font)
        self.listButton.setObjectName(_fromUtf8("listButton"))
        self.verticalLayout_10.addWidget(self.listButton)
        self.gridLayoutWidget = QtGui.QWidget(MainForm)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 10, 421, 231))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.boardLine = QtGui.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.boardLine.setFont(font)
        self.boardLine.setObjectName(_fromUtf8("boardLine"))
        self.gridLayout.addWidget(self.boardLine, 6, 1, 1, 1)
        self.crystalLine = QtGui.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.crystalLine.setFont(font)
        self.crystalLine.setObjectName(_fromUtf8("crystalLine"))
        self.gridLayout.addWidget(self.crystalLine, 1, 1, 1, 1)
        self.bindButton = QtGui.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.bindButton.setFont(font)
        self.bindButton.setObjectName(_fromUtf8("bindButton"))
        self.gridLayout.addWidget(self.bindButton, 2, 1, 1, 1)
        self.unbindButton = QtGui.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.unbindButton.setFont(font)
        self.unbindButton.setObjectName(_fromUtf8("unbindButton"))
        self.gridLayout.addWidget(self.unbindButton, 2, 0, 1, 1)
        self.closeButton = QtGui.QPushButton(MainForm)
        self.closeButton.setGeometry(QtCore.QRect(260, 590, 99, 37))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))

        self.retranslateUi(MainForm)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainForm.reject)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(_translate("MainForm", "探测器模块组装记录", None))
        self.queryButton.setText(_translate("MainForm", "查询", None))
        self.listButton.setText(_translate("MainForm", "高级查询", None))
        self.label_4.setText(_translate("MainForm", "AD板序列号", None))
        self.label_3.setText(_translate("MainForm", "晶体序列号", None))
        self.bindButton.setText(_translate("MainForm", "绑    定", None))
        self.unbindButton.setText(_translate("MainForm", "解绑", None))
        self.closeButton.setText(_translate("MainForm", "退出", None))

