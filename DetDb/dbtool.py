#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
import re
from detdb import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui_mainform
import ui_mainform2
import ui_loginform
import qrc_resources
from functools import partial

DB_SERVER="localhost"
ROOT_PASS="glop3c"

DB_NAME="det"

LOGIN=False
SELECT=False
INSERT=False
UPDATE=False

QUERY=False

MESSAGE_TITLE=u"组装记录数据库"

class LoginForm(QDialog, ui_loginform.Ui_LoginForm):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setupUi(self)
        self.updateUi()
        self.updateUser()
        
        self.mainform = MainForm()
        self.mainform2 = MainForm2()
        
        self.connect(self.toBindButton, SIGNAL("clicked()"), partial(self.on_loginButton_clicked, "toBind"))
        self.connect(self.toUnbindButton, SIGNAL("clicked()"), partial(self.on_loginButton_clicked, "toUnbind"))
        self.connect(self.toQueryButton, SIGNAL("clicked()"), partial(self.on_loginButton_clicked, "toQuery"))
    
        self.connect(self.loginCloseButton, SIGNAL("clicked()"), self.on_loginCloseButton_clicked)
        
    def updateUser(self):
        query = QSqlQuery()
        query.exec_("SELECT User FROM mysql.user WHERE User <> 'root' and User <> 'mysql.session' and User <> 'mysql.sys'")
        while query.next():
            user=query.value(0).toString()
            self.userComboBox.addItem(user)

    def updateUi(self):
        global LOGIN
        if LOGIN:
            pass
            #self.loginButton.setEnabled(False)
            #self.passLine.setReadOnly(True)

    def on_loginCloseButton_clicked(self):
        sys.exit(0)
        
    def on_loginButton_clicked(self, which):
        print which+"Button has been pressed"
        global LOGIN, SELECT, INSERT, UPDATE, QUERY
        
        username=self.userComboBox.currentText()
        password=self.passLine.text()
        
        #check priv for username by root
        SELECT=True
        INSERT=True
        UPDATE=True
        
        QUERY=False
        
        db=detdb()
        if not db.haveSelectPriv(username):
            privMsg1=u"<font color=red>用户"+username+u"没有查询记录权限，因此无法使用查询、高级查询、绑定、解绑功能。</font>"
            SELECT=False

        if not db.haveInsertPriv(username):
            privMsg2=u"<font color=red>用户"+username+u"没有插入记录权限，因此无法使用绑定及解绑功能。</font>"
            INSERT=False                
        
        if not db.haveUpdatePriv(username):
            privMsg3=u"<font color=red>用户"+username+u"没有更新记录权限，因此无法使用绑定及解绑功能。</font>"
            UPDATE=False
        
        self.loginTextEdit.setText(u"用户"+username+u"正在登录服务器"+DB_SERVER+u"上的数据库"+DB_NAME)
        
        #test connection
        if db.open(DB_SERVER, username, password, DB_NAME):
            LOGIN=True
            self.loginTextEdit.append(u"<font color=green>用户"+username+u"登录OK。</font>")
            if not SELECT:
                self.loginTextEdit.append(privMsg1)
                
            if not INSERT:
                self.loginTextEdit.append(privMsg2)
                
            if not UPDATE:
                self.loginTextEdit.append(privMsg3)   
            
            if which == "toBind":    
                self.mainform.show()
                self.mainform.updateUi()
            elif which == "toQuery":
                QUERY=True
                self.mainform2.show()
                self.mainform2.updateUi()
            else:
                self.mainform2.show()
                self.mainform2.updateUi()
                
        else:
            QMessageBox.warning(None, MESSAGE_TITLE, u'密码错误')
            #re-connect by root
            db.close()

            db.open(DB_SERVER, 'root', ROOT_PASS, DB_NAME)
        
        self.updateUi()


class MainForm(QDialog,
               ui_mainform.Ui_MainForm):

    #login=False
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.updateUi()

    def updateUi(self):
        global LOGIN, SELECT, INSERT, UPDATE
        
        self.queryButton.hide()
        self.unbindButton.hide()
        self.listButton.hide()
        self.snLine.hide()
            
        #print LOGIN
        #print SELECT
        if not LOGIN or not SELECT:
            self.bindButton.setEnabled(False)
            self.queryButton.setEnabled(False)
            self.unbindButton.setEnabled(False)
            self.listButton.setEnabled(False)
            
            #self.bindButton.hide()
            return
        
        #validate user input, min character numbers is useless.
        #self.crystalLine.setValidator(QRegExpValidator(QRegExp("[0-9A-Za-z\-]{6,20}"), self))
        self.crystalLine.setValidator(QRegExpValidator(QRegExp("[0-9][A-Za-z][0-9]{4}"), self))
        #self.boardLine.setValidator(QRegExpValidator(QRegExp("[0-9A-Za-z\-]{9,20}"), self))
        self.boardLine.setValidator(QRegExpValidator(QRegExp("[A-Za-z]{2}[0-9]{7}"), self))
        
        #validate min character numbers
        #if self.crystalLine.text().isEmpty() and self.boardLine.text().isEmpty():
        if self.crystalLine.text().length()<6 and self.boardLine.text().length()<9:
            self.queryButton.setEnabled(False)
            self.unbindButton.setEnabled(False)
            self.listButton.setEnabled(False)
        else:
            self.queryButton.setEnabled(True)
            self.unbindButton.setEnabled(True)
            self.listButton.setEnabled(True)
            
        #if self.crystalLine.text().isEmpty() or self.boardLine.text().isEmpty():
        if self.crystalLine.text().length()<6 or self.boardLine.text().length()<9:
            self.bindButton.setEnabled(False)
        else:
            self.bindButton.setEnabled(True)
            
        if not INSERT or not UPDATE:
            self.unbindButton.setEnabled(False)
            self.bindButton.setEnabled(False)

    #@pyqtSignature("QString")
    #def on_snLine_textEdited(self, text):
    #   self.updateUi()

    @pyqtSignature("QString")
    def on_crystalLine_textEdited(self, text):
        self.updateUi()

    @pyqtSignature("QString")
    def on_boardLine_textEdited(self, text):
        self.updateUi()
            
    @pyqtSignature("")
    def on_bindButton_clicked(self):
        print "bind crystal "+self.crystalLine.text()+" to board "+self.boardLine.text()
        crystal=self.crystalLine.text()
        board=self.boardLine.text()
        
        db=detdb()
        result=db.bind(crystal, board)
        
        #crystalid or boardid is invalid, fatal error
        if not result[3]:
            print "Crystal record is NOT exist and CANNOT be added"
            QMessageBox.warning(None, MESSAGE_TITLE, u'无法添加晶体记录。请检查数据库连接与用户权限。')
            sys.exit(1)
            
        if not result[4]:
            print "Board record is NOT exist and CANNOT be added"
            QMessageBox.warning(None, MESSAGE_TITLE, u'无法添加AD板记录。请检查数据库连接与用户权限。')
            sys.exit(1)
        
        if result[0] and result[1] and result[2]:
            print "done: binding crystal sn#"+crystal+" to board sn#"+board
            self.resultBrowser.append(u"绑定成功：晶体序列号#"+crystal+u"绑定AD板序列号#"+board)
        elif not result[0] and result[1] and result[2]:
            print "failed: already binding crystal sn#"+crystal+" to board sn#"+board
            self.resultBrowser.append(u"<font color=red>绑定失败</font>：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"已经绑定")
        elif result[0] and not result[1] and result[2]:
            print "falied: already binding crystal sn#"+crystal+" to board sn#"+db.getBoardSn(result[4])
            self.resultBrowser.append(u"<font color=red>绑定失败</font>：晶体序列号#"+crystal+u"与AD板序列号#"+db.getBoardSn(result[4])+u"已经绑定")
        elif result[0] and result[1] and not result[2]:
            print "falied: already binding crystal sn#"+db.getCrystalSn(result[3])+" to board sn#"+board
            self.resultBrowser.append(u"<font color=red>绑定失败</font>：晶体序列号#"+db.getCrystalSn(result[3])+u"与AD板序列号#"+board+u"已经绑定")
        else:
            print "failed: insert record error"
            
    @pyqtSignature("")
    def on_unbindButton_clicked(self):
        print "to unbind crystal sn#"+self.crystalLine.text()+" or/and board sn#"+self.boardLine.text()
        crystal=self.crystalLine.text()
        board=self.boardLine.text()
        
        crystalid=0
        boardid=0
        
        db=detdb()
        if not crystal.isEmpty():
            crystalid=db.getCrystalId(crystal)
            if crystalid:
                print "unbind crystal id "+str(crystalid)
            else:
                print "failed: no record for crystal sn#"+crystal
                self.resultBrowser.append(u"<font color=red>失败</font>：晶体序列号#"+crystal+u"无记录")
                
        if not board.isEmpty():
            boardid=db.getBoardId(board)
            if boardid:
                print "unbind board id "+str(boardid)
            else:
                print "failed: no record for board sn#"+board
                self.resultBrowser.append(u"<font color=red>失败</font>：AD板序列号#"+board+u"无记录")
        
        if crystalid or boardid:
            result=db.unbind(crystalid, boardid)
        else:
            return
        
        if result[0]:
            print "done: unbind crystal sn#"+crystal+" from board sn#"+board
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+crystal+u"脱离AD板序列号#"+board)
        elif result[1]:
            print "done: unbind crystal sn#"+crystal+" from board sn#"+db.getBoardSn(result[4])
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+crystal+u"脱离AD板序列号#"+db.getBoardSn(result[4]))
        elif result[2]:
            print "done: unbind  crystal sn#"+db.getCrystalSn(result[3])+" from board sn#"+board
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+db.getCrystalSn(result[3])+u"脱离AD板序列号#"+board)
        elif crystalid and boardid:
            print "failed: no binding record for crystal sn#"+crystal+" to board sn#"+board
            self.resultBrowser.append(u"<font color=red>解绑失败</font>：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"未绑定")
        elif crystalid:
            print "failed: no binding record for crystal sn#"+crystal     
            self.resultBrowser.append(u"<font color=red>解绑失败</font>：晶体序列号#"+crystal+u"未绑定")
        elif boardid:
            print "failed: no binding record for board sn#"+board
            self.resultBrowser.append(u"<font color=red>解绑失败</font>：AD板序列号#"+board+u"未绑定")
        else:
            return

    
    @pyqtSignature("")
    def on_queryButton_clicked(self):
        #self.resultBrowser.setText(u"<font color=red>查询</font>晶体序列号#"+self.crystalLine.text()+u"或/与AD板序列号#"+self.boardLine.text())
        crystal=self.crystalLine.text()
        board=self.boardLine.text()
        
        crystalid=0
        boardid=0
        
        db=detdb()
        if not crystal.isEmpty():
            crystalid=db.getCrystalId(crystal)
            if crystalid:
                print "query crystal id "+str(crystalid)
            else:
                print "no record: for crystal sn#"+crystal
                self.resultBrowser.append(u"无记录：晶体序列号#"+crystal)
                
        if not board.isEmpty():
            boardid=db.getBoardId(board)
            if boardid:
                print "query board id "+str(boardid)
            else:
                print "no record: for board sn#"+board
                self.resultBrowser.append(u"无记录：AD板序列号#"+board)
        
        if crystalid or boardid:
            result=db.query(crystalid, boardid)
        else:
            return
        
        if result[0]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"于"+db.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif result[1]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+db.getBoardSn(result[4])+" at "+db.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+db.getBoardSn(result[4])+u"于"+db.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif result[2]:
            print "is binding: crystal sn#"+db.getCrystalSn(result[3])+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+db.getCrystalSn(result[3])+u"与AD板序列号#"+board+u"于"+db.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif crystalid and boardid:
            print "no binding: crystal sn#"+crystal+" to board sn#"+board
            self.resultBrowser.append(u"未绑定：晶体序列号#"+crystal+u"到AD板序列号#"+board)
        elif crystalid:
            print "no binding: for crystal sn#"+crystal
            self.resultBrowser.append(u"未绑定：晶体序列号#"+crystal)
        elif boardid:
            print "no binding: for board sn#"+board
            self.resultBrowser.append(u"未绑定：AD板序列号#"+board)
        else:
            return


    @pyqtSignature("")
    def on_listButton_clicked(self):
        print "to list crystal sn#"+self.crystalLine.text()+" or/and board sn#"+self.boardLine.text()
        crystal=self.crystalLine.text()
        board=self.boardLine.text()
        
        crystalid=0
        boardid=0
        
        db=detdb()
        if not crystal.isEmpty():
            crystalid=db.getCrystalId(crystal)
            if crystalid:
                print "list crystal id "+str(crystalid)
            else:
                print "no record: for crystal sn#"+crystal
                self.resultBrowser.append(u"无记录：晶体序列号#"+crystal)
                
        if not board.isEmpty():
            boardid=db.getBoardId(board)
            if boardid:
                print "list board id "+str(boardid)
            else:
                print "no record: for board sn#"+board
                self.resultBrowser.append(u"无记录：AD板序列号#"+board)
        
        if crystalid or boardid:
            result=db.query(crystalid, boardid)
        else:
            return
        
        query = QSqlQuery()
        
        if result[0]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            #self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"于"+db.getBindingTime(result[3], result[4]))
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" and boardid="+str(boardid)+" ORDER BY time")
        elif result[1]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+db.getBoardSn(result[4])+" at "+db.getBindingTime(result[3], result[4])
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" ORDER BY time")
        elif result[2]:
            print "is binding: crystal sn#"+db.getCrystalSn(result[3])+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE boardid="+str(boardid)+" ORDER BY time")
        elif crystalid and boardid:
            print "no binding: crystal sn#"+crystal+" to board sn#"+board
            #query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" ORDER BY time")
            #query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE boardid="+str(boardid)+" ORDER BY time")
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" or boardid="+str(boardid)+" ORDER BY time")
        elif crystalid:
            print "no binding: for crystal sn#"+crystal
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" ORDER BY time")
        elif boardid:
            print "no binding: for board sn#"+board
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE boardid="+str(boardid)+" ORDER BY time")
        else:
            return
        
        bgColor="LightGreen"
        table='<TABLE BORDER="1" ALIGN="LEFT">'
        table+=u"<TR BGCOLOR="+bgColor+u"><TD>晶体序列号#</TD><TD>AD板序列号#</TD><TD>绑定状态</TD><TD>操作时间</TD><TD>操作者</TD></TR>"
        
        while query.next():
            crystalid=query.value(0).toInt()[0]
            boardid=query.value(1).toInt()[0]
            
            status=query.value(2).toString()
            if status == "binding":
                #statusHan=u"<font color=red>绑定</font>"
                statusHan=u"绑定"
                bgColor="LightCoral"
            elif status == "bound":
                statusHan=u"曾绑"
                bgColor="LightGoldenRodYellow"
            elif status == "unbind":
                statusHan=u"解绑"
                bgColor="LightCyan"
                
            time=query.value(3).toString()
            time.replace('T', ' ')
            
            operator=query.value(4).toString()
            exp=re.compile("@.*")
            #str() CANNOT convert utf-8 chinese charactor
            operator=exp.sub('', str(operator))
            
            #print db.getCrystalSn(crystalid)+" , "+db.getBoardSn(boardid)+" , "+status+" , "+time+" , "+operator
            table+="<TR BGCOLOR="+bgColor+"><TD>"+db.getCrystalSn(crystalid)+"</TD><TD>"+db.getBoardSn(boardid)+"</TD><TD>"+statusHan+"</TD><TD>"+time+"</TD><TD>"+operator+"</TD></TR>"
        
        table+="</TABLE>"
        #self.resultBrowser.append(table)
        self.resultBrowser.setText(table)


class MainForm2(QDialog, ui_mainform2.Ui_MainForm2):
    def __init__(self):
        super(MainForm2, self).__init__()
        self.setupUi(self)
        self.updateUi()
        
    def updateUi(self):
        global LOGIN, SELECT, INSERT, UPDATE, QUERY
        if not LOGIN or not SELECT:
            self.queryButton.setEnabled(False)
            self.unbindButton.setEnabled(False)
            self.listButton.setEnabled(False)
            return
        
        #validate user input, min character numbers is useless.
        self.snLine.setValidator(QRegExpValidator(QRegExp("[0-9][A-Za-z][0-9]{4}|[A-Za-z]{2}[0-9]{7}"), self))
        
        #validate min character numbers

        if self.snLine.text().length()<6:
            self.queryButton.setEnabled(False)
            self.unbindButton.setEnabled(False)
            self.listButton.setEnabled(False)
        else:
            self.queryButton.setEnabled(True)
            self.unbindButton.setEnabled(True)
            self.listButton.setEnabled(True)

        if not INSERT or not UPDATE:
            self.unbindButton.setEnabled(False)
        
        if QUERY:
            self.unbindButton.hide()
            self.queryButton.show()
            self.listButton.show() 
        else:
            self.unbindButton.show()
            self.queryButton.hide()
            self.listButton.hide() 

    @pyqtSignature("QString")
    def on_snLine_textEdited(self, text):
        self.updateUi()        
            
    @pyqtSignature("")
    def on_unbindButton_clicked(self):
        sn=self.snLine.text()
        
        crystal=QString('')
        board=QString('')
        
        db=detdb()
        if db.matchCrystalSn(sn):
            crystal=sn
        elif db.matchBoardSn(sn):
            board=sn

        crystalid=0
        boardid=0
        
        if not crystal.isEmpty():
            crystalid=db.getCrystalId(crystal)
            if crystalid:
                print "unbind crystal id "+str(crystalid)
            else:
                print "failed: no record for crystal sn#"+crystal
                self.resultBrowser.append(u"<font color=red>失败</font>：晶体序列号#"+crystal+u"无记录")
                
        if not board.isEmpty():
            boardid=db.getBoardId(board)
            if boardid:
                print "unbind board id "+str(boardid)
            else:
                print "failed: no record for board sn#"+board
                self.resultBrowser.append(u"<font color=red>失败</font>：AD板序列号#"+board+u"无记录")
        
        if crystalid or boardid:
            result=db.unbind(crystalid, boardid)
        else:
            return
        
        if result[0]:
            print "done: unbind crystal sn#"+crystal+" from board sn#"+board
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+crystal+u"脱离AD板序列号#"+board)
        elif result[1]:
            print "done: unbind crystal sn#"+crystal+" from board sn#"+db.getBoardSn(result[4])
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+crystal+u"脱离AD板序列号#"+db.getBoardSn(result[4]))
        elif result[2]:
            print "done: unbind  crystal sn#"+db.getCrystalSn(result[3])+" from board sn#"+board
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+db.getCrystalSn(result[3])+u"脱离AD板序列号#"+board)
        elif crystalid and boardid:
            print "failed: no binding record for crystal sn#"+crystal+" to board sn#"+board
            self.resultBrowser.append(u"<font color=red>解绑失败</font>：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"未绑定")
        elif crystalid:
            print "failed: no binding record for crystal sn#"+crystal     
            self.resultBrowser.append(u"<font color=red>解绑失败</font>：晶体序列号#"+crystal+u"未绑定")
        elif boardid:
            print "failed: no binding record for board sn#"+board
            self.resultBrowser.append(u"<font color=red>解绑失败</font>：AD板序列号#"+board+u"未绑定")
        else:
            return

    
    @pyqtSignature("")
    def on_queryButton_clicked(self):
        sn=self.snLine.text()
        
        crystal=QString('')
        board=QString('')
        
        db=detdb()
        
        if db.matchCrystalSn(sn):
            crystal=sn
        elif db.matchBoardSn(sn):
            board=sn
        
        crystalid=0
        boardid=0
        
        if not crystal.isEmpty():
            crystalid=db.getCrystalId(crystal)
            if crystalid:
                print "query crystal id "+str(crystalid)
            else:
                print "no record: for crystal sn#"+crystal
                self.resultBrowser.append(u"无记录：晶体序列号#"+crystal)
                
        if not board.isEmpty():
            boardid=db.getBoardId(board)
            if boardid:
                print "query board id "+str(boardid)
            else:
                print "no record: for board sn#"+board
                self.resultBrowser.append(u"无记录：AD板序列号#"+board)
        
        if crystalid or boardid:
            result=db.query(crystalid, boardid)
        else:
            return
        
        if result[0]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"于"+db.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif result[1]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+db.getBoardSn(result[4])+" at "+db.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+db.getBoardSn(result[4])+u"于"+db.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif result[2]:
            print "is binding: crystal sn#"+db.getCrystalSn(result[3])+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+db.getCrystalSn(result[3])+u"与AD板序列号#"+board+u"于"+db.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif crystalid and boardid:
            print "no binding: crystal sn#"+crystal+" to board sn#"+board
            self.resultBrowser.append(u"未绑定：晶体序列号#"+crystal+u"到AD板序列号#"+board)
        elif crystalid:
            print "no binding: for crystal sn#"+crystal
            self.resultBrowser.append(u"未绑定：晶体序列号#"+crystal)
        elif boardid:
            print "no binding: for board sn#"+board
            self.resultBrowser.append(u"未绑定：AD板序列号#"+board)
        else:
            return


    @pyqtSignature("")
    def on_listButton_clicked(self):
        sn=self.snLine.text()
        
        crystal=QString('')
        board=QString('')
        
        db=detdb()
        if db.matchCrystalSn(sn):
            crystal=sn
        elif db.matchBoardSn(sn):
            board=sn
        
        crystalid=0
        boardid=0
        
        if not crystal.isEmpty():
            crystalid=db.getCrystalId(crystal)
            if crystalid:
                print "list crystal id "+str(crystalid)
            else:
                print "no record: for crystal sn#"+crystal
                self.resultBrowser.append(u"无记录：晶体序列号#"+crystal)
                
        if not board.isEmpty():
            boardid=db.getBoardId(board)
            if boardid:
                print "list board id "+str(boardid)
            else:
                print "no record: for board sn#"+board
                self.resultBrowser.append(u"无记录：AD板序列号#"+board)
        
        if crystalid or boardid:
            result=db.query(crystalid, boardid)
        else:
            return
        
        query = QSqlQuery()
        
        if result[0]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            #self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"于"+db.getBindingTime(result[3], result[4]))
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" and boardid="+str(boardid)+" ORDER BY time")
        elif result[1]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+db.getBoardSn(result[4])+" at "+db.getBindingTime(result[3], result[4])
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" ORDER BY time")
        elif result[2]:
            print "is binding: crystal sn#"+db.getCrystalSn(result[3])+" to board sn#"+board+" at "+db.getBindingTime(result[3], result[4])
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE boardid="+str(boardid)+" ORDER BY time")
        elif crystalid and boardid:
            print "no binding: crystal sn#"+crystal+" to board sn#"+board
            #query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" ORDER BY time")
            #query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE boardid="+str(boardid)+" ORDER BY time")
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" or boardid="+str(boardid)+" ORDER BY time")
        elif crystalid:
            print "no binding: for crystal sn#"+crystal
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" ORDER BY time")
        elif boardid:
            print "no binding: for board sn#"+board
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE boardid="+str(boardid)+" ORDER BY time")
        else:
            return
        
        bgColor="LightGreen"
        table='<TABLE BORDER="1" ALIGN="LEFT">'
        table+=u"<TR BGCOLOR="+bgColor+u"><TD>晶体序列号#</TD><TD>AD板序列号#</TD><TD>操作</TD><TD>操作时间</TD><TD>操作者</TD></TR>"
        
        while query.next():
            crystalid=query.value(0).toInt()[0]
            boardid=query.value(1).toInt()[0]
            
            status=query.value(2).toString()
            if status == "binding":
                #statusHan=u"<font color=red>绑定</font>"
                statusHan=u"绑定中"
                bgColor="LightCoral"
            elif status == "bound":
                statusHan=u"绑定"
                bgColor="LightGoldenRodYellow"
            elif status == "unbind":
                statusHan=u"解绑"
                bgColor="LightCyan"
                
            time=query.value(3).toString()
            time.replace('T', ' ')
            
            operator=query.value(4).toString()
            exp=re.compile("@.*")
            #str() CANNOT convert utf-8 chinese charactor
            operator=exp.sub('', str(operator))
            
            #print db.getCrystalSn(crystalid)+" , "+db.getBoardSn(boardid)+" , "+status+" , "+time+" , "+operator
            table+="<TR BGCOLOR="+bgColor+"><TD>"+db.getCrystalSn(crystalid)+"</TD><TD>"+db.getBoardSn(boardid)+"</TD><TD>"+statusHan+"</TD><TD>"+time+"</TD><TD>"+operator+"</TD></TR>"
        
        table+="</TABLE>"
        #self.resultBrowser.append(table)
        self.resultBrowser.setText(table)
    
def main():
    app = QApplication(sys.argv)
    
    db=detdb()
    
    #test database server connection
    if not db.open(DB_SERVER, "root", ROOT_PASS):
        QMessageBox.warning(None, MESSAGE_TITLE,
            QString(u"数据库错误: %1").arg(u"连接服务器失败"))
        sys.exit(1)

    #connect to a database
    if db.open(DB_SERVER, "root", ROOT_PASS, DB_NAME):
        create=False
    else:
        create=True
        print "create database..."
        #re-connect
        db.open(DB_SERVER, "root", ROOT_PASS)
        
        db.createDb(DB_NAME)
        
        if not db.open(DB_SERVER, "root", ROOT_PASS, DB_NAME):
            QMessageBox.warning(None, MESSAGE_TITLE,
                QString(u"数据库错误: %1").arg(u"连接数据库失败"))
            sys.exit(1)
        
    splash = None
    if create:
        app.setOverrideCursor(QCursor(Qt.WaitCursor))
        splash = QLabel()
        pixmap = QPixmap(":/logo.png")
        splash.setPixmap(pixmap)
        splash.setMask(pixmap.createHeuristicMask())
        splash.setWindowFlags(Qt.SplashScreen)
        rect = app.desktop().availableGeometry()
        splash.move((rect.width() - pixmap.width()) / 2,
                    (rect.height() - pixmap.height()) / 2)
        splash.show()
        app.processEvents()
        
        #db.dropTables()
        #app.processEvents()
        db.createTables()
        app.processEvents()
        #db.createFakeData()
        #app.processEvents()

    #form = MainForm()
    #form.show()
    
    form_login=LoginForm()
    form_login.show()
    
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    app.exec_()
    #del form
    del form_login
    del db


main()

