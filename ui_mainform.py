# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Fri Nov 10 17:40:27 2017
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
        MainForm.resize(573, 407)
        self.userLine = QtGui.QLineEdit(MainForm)
        self.userLine.setGeometry(QtCore.QRect(90, 20, 113, 27))
        self.userLine.setObjectName(_fromUtf8("userLine"))
        self.label_2 = QtGui.QLabel(MainForm)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 66, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.passLine = QtGui.QLineEdit(MainForm)
        self.passLine.setGeometry(QtCore.QRect(90, 50, 113, 27))
        self.passLine.setEchoMode(QtGui.QLineEdit.Password)
        self.passLine.setObjectName(_fromUtf8("passLine"))
        self.loginButton = QtGui.QPushButton(MainForm)
        self.loginButton.setGeometry(QtCore.QRect(250, 20, 98, 27))
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.logoutButton = QtGui.QPushButton(MainForm)
        self.logoutButton.setGeometry(QtCore.QRect(250, 50, 98, 27))
        self.logoutButton.setObjectName(_fromUtf8("logoutButton"))
        self.crystalLine = QtGui.QLineEdit(MainForm)
        self.crystalLine.setGeometry(QtCore.QRect(90, 120, 113, 27))
        self.crystalLine.setObjectName(_fromUtf8("crystalLine"))
        self.label_4 = QtGui.QLabel(MainForm)
        self.label_4.setGeometry(QtCore.QRect(20, 160, 66, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.boardLine = QtGui.QLineEdit(MainForm)
        self.boardLine.setGeometry(QtCore.QRect(90, 160, 113, 27))
        self.boardLine.setObjectName(_fromUtf8("boardLine"))
        self.label_1 = QtGui.QLabel(MainForm)
        self.label_1.setGeometry(QtCore.QRect(20, 20, 66, 17))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.label_3 = QtGui.QLabel(MainForm)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 66, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.bindButton = QtGui.QPushButton(MainForm)
        self.bindButton.setGeometry(QtCore.QRect(250, 120, 98, 27))
        self.bindButton.setObjectName(_fromUtf8("bindButton"))
        self.unbindButton = QtGui.QPushButton(MainForm)
        self.unbindButton.setGeometry(QtCore.QRect(250, 160, 98, 27))
        self.unbindButton.setObjectName(_fromUtf8("unbindButton"))
        self.queryButton = QtGui.QPushButton(MainForm)
        self.queryButton.setGeometry(QtCore.QRect(250, 200, 98, 27))
        self.queryButton.setObjectName(_fromUtf8("queryButton"))
        self.closeButton = QtGui.QPushButton(MainForm)
        self.closeButton.setGeometry(QtCore.QRect(440, 20, 98, 27))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.listButton = QtGui.QPushButton(MainForm)
        self.listButton.setGeometry(QtCore.QRect(440, 140, 98, 27))
        self.listButton.setObjectName(_fromUtf8("listButton"))

        self.retranslateUi(MainForm)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainForm.reject)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(_translate("MainForm", "探测器模块组装记录", None))
        self.label_2.setText(_translate("MainForm", "Password", None))
        self.loginButton.setText(_translate("MainForm", "Login", None))
        self.logoutButton.setText(_translate("MainForm", "Logout", None))
        self.label_4.setText(_translate("MainForm", "Board", None))
        self.label_1.setText(_translate("MainForm", "Username", None))
        self.label_3.setText(_translate("MainForm", "Crystal", None))
        self.bindButton.setText(_translate("MainForm", "Bind", None))
        self.unbindButton.setText(_translate("MainForm", "Unbind", None))
        self.queryButton.setText(_translate("MainForm", "Query", None))
        self.closeButton.setText(_translate("MainForm", "Close", None))
        self.listButton.setText(_translate("MainForm", "List", None))

