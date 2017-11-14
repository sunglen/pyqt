# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginform.ui'
#
# Created: Tue Nov 14 16:10:12 2017
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

class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName(_fromUtf8("LoginForm"))
        LoginForm.setEnabled(True)
        LoginForm.resize(429, 272)
        self.horizontalLayoutWidget = QtGui.QWidget(LoginForm)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 391, 131))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.userComboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.userComboBox.setFont(font)
        self.userComboBox.setObjectName(_fromUtf8("userComboBox"))
        self.gridLayout_4.addWidget(self.userComboBox, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_1 = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_1.setFont(font)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout_4.addWidget(self.label_1, 0, 0, 1, 2)
        self.passLine = QtGui.QLineEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.passLine.setFont(font)
        self.passLine.setEchoMode(QtGui.QLineEdit.Password)
        self.passLine.setObjectName(_fromUtf8("passLine"))
        self.gridLayout_4.addWidget(self.passLine, 1, 2, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_4)
        self.loginButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(15)
        self.loginButton.setFont(font)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.horizontalLayout_3.addWidget(self.loginButton)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(LoginForm)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 160, 391, 80))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.loginTextEdit = QtGui.QTextEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.loginTextEdit.setFont(font)
        self.loginTextEdit.setReadOnly(True)
        self.loginTextEdit.setObjectName(_fromUtf8("loginTextEdit"))
        self.horizontalLayout_4.addWidget(self.loginTextEdit)
        self.loginCloseButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.loginCloseButton.setFont(font)
        self.loginCloseButton.setObjectName(_fromUtf8("loginCloseButton"))
        self.horizontalLayout_4.addWidget(self.loginCloseButton)

        self.retranslateUi(LoginForm)
        QtCore.QObject.connect(self.loginCloseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), LoginForm.reject)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

    def retranslateUi(self, LoginForm):
        LoginForm.setWindowTitle(_translate("LoginForm", "用户登录", None))
        self.label_2.setText(_translate("LoginForm", "密码", None))
        self.label_1.setText(_translate("LoginForm", "用户名", None))
        self.loginButton.setText(_translate("LoginForm", "登录", None))
        self.loginCloseButton.setText(_translate("LoginForm", "关闭", None))

