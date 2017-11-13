# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Mon Nov 13 18:36:56 2017
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
        MainForm.resize(594, 462)
        self.resultBrowser = QtGui.QTextBrowser(MainForm)
        self.resultBrowser.setGeometry(QtCore.QRect(20, 320, 551, 111))
        self.resultBrowser.setObjectName(_fromUtf8("resultBrowser"))
        self.verticalLayoutWidget = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 91, 80))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_1 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.verticalLayout_2.addWidget(self.label_1)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayoutWidget_2 = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(120, 20, 121, 80))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.userComboBox = QtGui.QComboBox(self.verticalLayoutWidget_2)
        self.userComboBox.setObjectName(_fromUtf8("userComboBox"))
        self.verticalLayout_3.addWidget(self.userComboBox)
        self.passLine = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.passLine.setEchoMode(QtGui.QLineEdit.Password)
        self.passLine.setObjectName(_fromUtf8("passLine"))
        self.verticalLayout_3.addWidget(self.passLine)
        self.horizontalLayoutWidget = QtGui.QWidget(MainForm)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(250, 20, 87, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.loginButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.horizontalLayout_6.addWidget(self.loginButton)
        self.verticalLayoutWidget_3 = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(440, 20, 91, 80))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.closeButton = QtGui.QPushButton(self.verticalLayoutWidget_3)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.verticalLayout_4.addWidget(self.closeButton)
        self.verticalLayoutWidget_4 = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 150, 81, 121))
        self.verticalLayoutWidget_4.setObjectName(_fromUtf8("verticalLayoutWidget_4"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_6.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget_4)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_6.addWidget(self.label_4)
        self.verticalLayoutWidget_5 = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(120, 139, 191, 161))
        self.verticalLayoutWidget_5.setObjectName(_fromUtf8("verticalLayoutWidget_5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.crystalLine = QtGui.QLineEdit(self.verticalLayoutWidget_5)
        self.crystalLine.setObjectName(_fromUtf8("crystalLine"))
        self.verticalLayout_7.addWidget(self.crystalLine)
        self.boardLine = QtGui.QLineEdit(self.verticalLayoutWidget_5)
        self.boardLine.setObjectName(_fromUtf8("boardLine"))
        self.verticalLayout_7.addWidget(self.boardLine)
        self.verticalLayoutWidget_6 = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(330, 150, 131, 131))
        self.verticalLayoutWidget_6.setObjectName(_fromUtf8("verticalLayoutWidget_6"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_8.setMargin(0)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.bindButton = QtGui.QPushButton(self.verticalLayoutWidget_6)
        self.bindButton.setObjectName(_fromUtf8("bindButton"))
        self.verticalLayout_8.addWidget(self.bindButton)
        self.verticalLayoutWidget_7 = QtGui.QWidget(MainForm)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(490, 150, 91, 121))
        self.verticalLayoutWidget_7.setObjectName(_fromUtf8("verticalLayoutWidget_7"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_10.setMargin(0)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.unbindButton = QtGui.QPushButton(self.verticalLayoutWidget_7)
        self.unbindButton.setObjectName(_fromUtf8("unbindButton"))
        self.verticalLayout_10.addWidget(self.unbindButton)
        self.queryButton = QtGui.QPushButton(self.verticalLayoutWidget_7)
        self.queryButton.setObjectName(_fromUtf8("queryButton"))
        self.verticalLayout_10.addWidget(self.queryButton)
        self.listButton = QtGui.QPushButton(self.verticalLayoutWidget_7)
        self.listButton.setObjectName(_fromUtf8("listButton"))
        self.verticalLayout_10.addWidget(self.listButton)

        self.retranslateUi(MainForm)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainForm.reject)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(_translate("MainForm", "探测器模块组装记录", None))
        self.label_1.setText(_translate("MainForm", "Username", None))
        self.label_2.setText(_translate("MainForm", "Password", None))
        self.loginButton.setText(_translate("MainForm", "Login", None))
        self.closeButton.setText(_translate("MainForm", "Close", None))
        self.label_3.setText(_translate("MainForm", "Crystal", None))
        self.label_4.setText(_translate("MainForm", "Board", None))
        self.bindButton.setText(_translate("MainForm", "Bind", None))
        self.unbindButton.setText(_translate("MainForm", "Unbind", None))
        self.queryButton.setText(_translate("MainForm", "Query", None))
        self.listButton.setText(_translate("MainForm", "List", None))

