#!/usr/bin/env python
# coding=utf-8

import sys
import re
from detdb import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui_adminform
from functools import partial

DB_SERVER="localhost"
ROOT_PASS="glop3c"

DB_NAME="det"

MESSAGE_TITLE=u"组装记录数据库用户管理工具"

class AdminForm(QDialog, ui_adminform.Ui_AdminForm):
    def __init__(self):
        super(AdminForm, self).__init__()
        self.setupUi(self)
        self.updateUi()
    
        #self.connect(self.adminCloseButton, SIGNAL("clicked()"), self.on_adminCloseButton_clicked)
        #self.connect(self.updateButton, SIGNAL("clicked()"), self.on_updateButton_clicked)

    def updateUi(self):
        isValidPass=False
        if self.passLine.text().length() == self.passAgainLine.text().length() and self.passLine.text().length() > 4:
            isValidPass=True
            
        if self.userLine.text().length()>4 and isValidPass:
            self.updateButton.setEnabled(True)
        else:
            self.updateButton.setEnabled(False)

    @pyqtSignature("QString")
    def on_userLine_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_passLine_textEdited(self, text):
        self.updateUi()
        
    @pyqtSignature("QString")
    def on_passAgainLine_textEdited(self, text):
        self.updateUi()
    
    @pyqtSignature("")    
    def on_adminCloseButton_clicked(self):
        sys.exit(0)
        
    @pyqtSignature("")    
    def on_updateButton_clicked(self):
        if self.passLine.text() <> self.passAgainLine.text():
            QMessageBox.warning(None, MESSAGE_TITLE, u'两次输入的密码不一致')
            return
        
        if self.queryOnlycheckBox.isChecked():
            type='query'
        else:
            type='bind'
            
        username=self.userLine.text()
        password=self.passLine.text()
            
        db=detdb()
        
        if db.haveDbUser(username):
            #print "user "+username+" exist, update its password."
            self.adminTextEdit.setText(u"因用户"+username+u"存在，故此次操作为更新密码。")
            db.updatePass(username, password)
            self.adminTextEdit.append(u"用户的新密码是：<font color=green>"+password+u"</font>")
  
        else:
            self.adminTextEdit.setText(u"因用户"+username+u"不存在，故此次操作为新建帐号。")
            if db.createDbUser(type, username, password):
                #print "create user "+username+" OK"
                self.adminTextEdit.append(u"新建"+username+u"账户成功。")
                self.adminTextEdit.append(u"用户名称：<font color=green>"+username+u"</font>")
                self.adminTextEdit.append(u"密码：<font color=green>"+password+u"</font>")
            else:
                self.loginTextEdit.append(u"<font color=red>新建"+username+u"账户失败。</font>")
                
        self.updateUi()

    
def main():
    app = QApplication(sys.argv)
    
    db=detdb()
    
    #test database server connection
    if not db.open(DB_SERVER, "root", ROOT_PASS):
        QMessageBox.warning(None, MESSAGE_TITLE,
            QString(u"数据库错误: %1").arg(u"连接服务器失败"))
        sys.exit(1)
        
    form_admin=AdminForm()
    form_admin.show()

    app.exec_()

    del form_admin
    del db

main()

