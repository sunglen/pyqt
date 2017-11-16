#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui_mainform
import ui_loginform
import qrc_resources

LOGIN=False
SELECT=False
INSERT=False
UPDATE=False

DB_SERVER="localhost"
DB_NAME="det"
ROOT_PASS="glop3c"
MESSAGE_TITLE=u"组装记录数据库"

def dropTables():
    print "Dropping tables..."
    query = QSqlQuery()
    #must drop table bind first because of foreign key.
    query.exec_("DROP TABLE bind")
    query.exec_("DROP TABLE crystal")
    query.exec_("DROP TABLE board")

    QApplication.processEvents()

def createTables():
    print "Creating tables..."
    query = QSqlQuery()
    query.exec_("""CREATE TABLE crystal (
                id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL,
                sn VARCHAR(20) UNIQUE NOT NULL,
                descrip VARCHAR(40))""")
    query.exec_("""CREATE TABLE board (
                id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL,
                sn VARCHAR(20) UNIQUE NOT NULL,
                descrip VARCHAR(40))""")
    query.exec_("""CREATE TABLE bind (
                id INTEGER PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL,
                crystalid INTEGER NOT NULL,
                boardid INTEGER NOT NULL,
                status ENUM('binding', 'bound', 'unbind') NOT NULL,
                time DATETIME NOT NULL,
                operator VARCHAR(20) NOT NULL,
                descrip VARCHAR(40),
                FOREIGN KEY (crystalid) REFERENCES crystal(id),
                FOREIGN KEY (boardid) REFERENCES board(id))""")

    QApplication.processEvents()

def createFakeData():
    print "Populating tables..."
    query = QSqlQuery()
    query.exec_("INSERT INTO crystal (sn) "
                "VALUES ('6G0124')")
    query.exec_("INSERT INTO crystal (sn) "
                "VALUES ('6G0125')")
    query.exec_("INSERT INTO crystal (sn) "
                "VALUES ('6G0126')")
    
    query.exec_("INSERT INTO board (sn) VALUES "
                "('HJ1438041')")
    query.exec_("INSERT INTO board (sn) VALUES "
                "('HJ1438042')")
    query.exec_("INSERT INTO board (sn) VALUES "
                "('HJ1438043')")
    
    sn="6G0127"
    query.exec_("SELECT id FROM crystal WHERE sn='"+sn+"'" )
    
    if not query.next():
        print "insert new crystal"
        query.prepare("INSERT INTO crystal (sn) "
                "VALUES (:sn)")
        query.bindValue(":sn", sn)
        query.exec_()
        query.exec_("SELECT id FROM crystal WHERE sn='"+sn+"'" )
        query.next()
        
    crystalid = query.value(0).toInt()[0]
    print crystalid
        
    sn="HJ1438044"
    query.exec_("SELECT id FROM board WHERE sn='"+sn+"'" )
    
    if not query.next():
        print "insert new board"
        query.prepare("INSERT INTO board (sn) "
                "VALUES (:sn)")
        query.bindValue(":sn", sn)
        query.exec_()
        query.exec_("SELECT id FROM board WHERE sn='"+sn+"'" )
        query.next()    
        
    boardid = query.value(0).toInt()[0]
    print boardid
 
    query.prepare("INSERT INTO bind (crystalid, boardid, status, time, operator) "
                     "VALUES (:crystalid, :boardid, :status, now(), user())") 
    query.bindValue(":crystalid", crystalid)
    query.bindValue(":boardid", boardid)
    query.bindValue(":status", "binding")
    #query.bindValue(":time", "now()")
    #query.bindValue(":operator", "user()")
    query.exec_()
        
    time.sleep(3)

    query.prepare("INSERT INTO bind (crystalid, boardid, status, time, operator) "
                     "VALUES (:crystalid, :boardid, :status, now(), user())") 
    query.bindValue(":crystalid", crystalid)
    query.bindValue(":boardid", boardid)
    query.bindValue(":status", "unbind")
    query.exec_()
    
    query.prepare("UPDATE bind set status='bound' "
                     "where crystalid="+str(crystalid)+" and boardid="+str(boardid)+" and status='binding'")
    query.exec_()

    QApplication.processEvents()

class LoginForm(QDialog, ui_loginform.Ui_LoginForm):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setupUi(self)
        self.updateUi()
        self.updateUser()
    
    def updateUser(self):
        query = QSqlQuery()
        query.exec_("SELECT User FROM mysql.user WHERE User <> 'root'")
        while query.next():
            user=query.value(0).toString()
            self.userComboBox.addItem(user)

    def updateUi(self):
        global LOGIN
        if LOGIN:
            self.loginButton.setEnabled(False)
            self.passLine.setReadOnly(True)
            
    def haveSelectPriv(self, username):
        query = QSqlQuery()
        query.exec_("SELECT Select_priv FROM mysql.user WHERE User = '"+username+"'")
        if query.next():
            priv=query.value(0).toString()
            if priv == "Y":
                return True
        return False

    def haveInsertPriv(self, username):
        query = QSqlQuery()
        query.exec_("SELECT Insert_priv FROM mysql.user WHERE User = '"+username+"'")
        if query.next():
            priv=query.value(0).toString()
            if priv == "Y":
                return True
        return False

    def haveUpdatePriv(self, username):
        query = QSqlQuery()
        query.exec_("SELECT Update_priv FROM mysql.user WHERE User = '"+username+"'")
        if query.next():
            priv=query.value(0).toString()
            if priv == "Y":
                return True
        return False

    @pyqtSignature("")
    def on_loginButton_clicked(self):
        global LOGIN, SELECT, INSERT, UPDATE
        
        username=self.userComboBox.currentText()
        password=self.passLine.text()
        
        #check priv for username by root
        SELECT=True
        INSERT=True
        UPDATE=True
        
        if not self.haveSelectPriv(username):
            privMsg1=u"<font color=red>用户"+username+u"没有查询记录权限，因此无法使用查询、高级查询、绑定、解绑功能。</font>"
            SELECT=False

        if not self.haveInsertPriv(username):
            privMsg2=u"<font color=red>用户"+username+u"没有插入记录权限，因此无法使用绑定及解绑功能。</font>"
            INSERT=False                
        
        if not self.haveUpdatePriv(username):
            privMsg3=u"<font color=red>用户"+username+u"没有更新记录权限，因此无法使用绑定及解绑功能。</font>"
            UPDATE=False
        
        self.loginTextEdit.setText(u"用户"+username+u"正在登录服务器"+DB_SERVER+u"上的数据库"+DB_NAME)
        
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName(DB_SERVER)
        db.setUserName(username)
        db.setPassword(password)
        db.setDatabaseName(DB_NAME)
        
        #test connection
        if db.open():
            LOGIN=True
            self.loginTextEdit.append(u"<font color=green>用户"+username+u"登录OK。</font>")
            if not SELECT:
                self.loginTextEdit.append(privMsg1)
                
            if not INSERT:
                self.loginTextEdit.append(privMsg2)
                
            if not UPDATE:
                self.loginTextEdit.append(privMsg3)   
        else:
            QMessageBox.warning(None, MESSAGE_TITLE, u'密码错误')
            #re-connect by root
            db.close()
            db.setUserName('root')
            db.setPassword(ROOT_PASS)
            db.open()
        
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
        if not LOGIN or not SELECT:
            self.bindButton.setEnabled(False)
            self.queryButton.setEnabled(False)
            self.unbindButton.setEnabled(False)
            self.listButton.setEnabled(False)
            return
        
        #validate user input, min character numbers is useless.
        self.crystalLine.setValidator(QRegExpValidator(QRegExp("[0-9A-Za-z\-]{6,20}"), self))
        self.boardLine.setValidator(QRegExpValidator(QRegExp("[0-9A-Za-z\-]{9,20}"), self))
        
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
        
        result=self.bind(crystal, board)
        
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
            print "falied: already binding crystal sn#"+crystal+" to board sn#"+self.getBoardSn(result[4])
            self.resultBrowser.append(u"<font color=red>绑定失败</font>：晶体序列号#"+crystal+u"与AD板序列号#"+self.getBoardSn(result[4])+u"已经绑定")
        elif result[0] and result[1] and not result[2]:
            print "falied: already binding crystal sn#"+self.getCrystalSn(result[3])+" to board sn#"+board
            self.resultBrowser.append(u"<font color=red>绑定失败</font>：晶体序列号#"+self.getCrystalSn(result[3])+u"与AD板序列号#"+board+u"已经绑定")
        else:
            print "failed: insert record error"
            
    @pyqtSignature("")
    def on_unbindButton_clicked(self):
        print "to unbind crystal sn#"+self.crystalLine.text()+" or/and board sn#"+self.boardLine.text()
        crystal=self.crystalLine.text()
        board=self.boardLine.text()
        
        crystalid=0
        boardid=0
        
        if not crystal.isEmpty():
            crystalid=self.getCrystalId(crystal)
            if crystalid:
                print "unbind crystal id "+str(crystalid)
            else:
                print "failed: no record for crystal sn#"+crystal
                self.resultBrowser.append(u"<font color=red>失败</font>：晶体序列号#"+crystal+u"无记录")
                
        if not board.isEmpty():
            boardid=self.getBoardId(board)
            if boardid:
                print "unbind board id "+str(boardid)
            else:
                print "failed: no record for board sn#"+board
                self.resultBrowser.append(u"<font color=red>失败</font>：AD板序列号#"+board+u"无记录")
        
        if crystalid or boardid:
            result=self.unbind(crystalid, boardid)
        else:
            return
        
        if result[0]:
            print "done: unbind crystal sn#"+crystal+" from board sn#"+board
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+crystal+u"脱离AD板序列号#"+board)
        elif result[1]:
            print "done: unbind crystal sn#"+crystal+" from board sn#"+self.getBoardSn(result[4])
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+crystal+u"脱离AD板序列号#"+self.getBoardSn(result[4]))
        elif result[2]:
            print "done: unbind  crystal sn#"+self.getCrystalSn(result[3])+" from board sn#"+board
            self.resultBrowser.append(u"解绑成功：晶体序列号#"+self.getCrystalSn(result[3])+u"脱离AD板序列号#"+board)
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
        
        if not crystal.isEmpty():
            crystalid=self.getCrystalId(crystal)
            if crystalid:
                print "query crystal id "+str(crystalid)
            else:
                print "no record: for crystal sn#"+crystal
                self.resultBrowser.append(u"无记录：晶体序列号#"+crystal)
                
        if not board.isEmpty():
            boardid=self.getBoardId(board)
            if boardid:
                print "query board id "+str(boardid)
            else:
                print "no record: for board sn#"+board
                self.resultBrowser.append(u"无记录：AD板序列号#"+board)
        
        if crystalid or boardid:
            result=self.query(crystalid, boardid)
        else:
            return
        
        if result[0]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+board+" at "+self.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"于"+self.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif result[1]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+self.getBoardSn(result[4])+" at "+self.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+self.getBoardSn(result[4])+u"于"+self.getBindingTime(result[3], result[4]).replace('T', ' '))
        elif result[2]:
            print "is binding: crystal sn#"+self.getCrystalSn(result[3])+" to board sn#"+board+" at "+self.getBindingTime(result[3], result[4])
            self.resultBrowser.append(u"已绑定：晶体序列号#"+self.getCrystalSn(result[3])+u"与AD板序列号#"+board+u"于"+self.getBindingTime(result[3], result[4]).replace('T', ' '))
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
        
        if not crystal.isEmpty():
            crystalid=self.getCrystalId(crystal)
            if crystalid:
                print "list crystal id "+str(crystalid)
            else:
                print "no record: for crystal sn#"+crystal
                self.resultBrowser.append(u"无记录：晶体序列号#"+crystal)
                
        if not board.isEmpty():
            boardid=self.getBoardId(board)
            if boardid:
                print "list board id "+str(boardid)
            else:
                print "no record: for board sn#"+board
                self.resultBrowser.append(u"无记录：AD板序列号#"+board)
        
        if crystalid or boardid:
            result=self.query(crystalid, boardid)
        else:
            return
        
        query = QSqlQuery()
        
        if result[0]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+board+" at "+self.getBindingTime(result[3], result[4])
            #self.resultBrowser.append(u"已绑定：晶体序列号#"+crystal+u"与AD板序列号#"+board+u"于"+self.getBindingTime(result[3], result[4]))
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" and boardid="+str(boardid)+" ORDER BY time")
        elif result[1]:
            print "is binding: crystal sn#"+crystal+" to board sn#"+self.getBoardSn(result[4])+" at "+self.getBindingTime(result[3], result[4])
            query.exec_("SELECT crystalid,boardid,status,time,operator FROM bind WHERE crystalid="+str(crystalid)+" ORDER BY time")
        elif result[2]:
            print "is binding: crystal sn#"+self.getCrystalSn(result[3])+" to board sn#"+board+" at "+self.getBindingTime(result[3], result[4])
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
            
            #print self.getCrystalSn(crystalid)+" , "+self.getBoardSn(boardid)+" , "+status+" , "+time+" , "+operator
            table+="<TR BGCOLOR="+bgColor+"><TD>"+self.getCrystalSn(crystalid)+"</TD><TD>"+self.getBoardSn(boardid)+"</TD><TD>"+statusHan+"</TD><TD>"+time+"</TD><TD>"+operator+"</TD></TR>"
        
        table+="</TABLE>"
        #self.resultBrowser.append(table)
        self.resultBrowser.setText(table)
        
    def bind(self, crystal, board):
        crystalid=self.addCrystal(crystal)
        boardid=self.addBoard(board)
        
        #result[0] is False: All binding already
        #result[1] is False: crystal binding already
        #result[2] is False: board binding already
        #result[0,1,2] are all True, and crystalid & boardid are valid : binding OK
        #result[0,1,2] are all False, and crystalid & boardid are valid: binding failed
        result=[True, True, True, crystalid, boardid]
        
        if not crystalid or not boardid:
            return result
        
        if self.isBinding(crystalid, boardid):
            #print "impossible, binding already"
            result[0]=False
            return result
        
        if self.isBinding(crystalid):
            #print "failed: crystal is binding already, unbind first"
            boardid=self.getCrystalBinding(crystalid)
            result[1]=False
            result[4]=boardid
            return result
        
        if self.isBinding(0, boardid):
            #print "failed: board is binding already, unbind first"
            crystalid=self.getBoardBinding(boardid)
            result[2]=False
            result[3]=crystalid
            return result
        
        query = QSqlQuery()
        query.prepare("INSERT INTO bind (crystalid, boardid, status, time, operator) "
                     "VALUES (:crystalid, :boardid, :status, now(), user())") 
        query.bindValue(":crystalid", crystalid)
        query.bindValue(":boardid", boardid)
        query.bindValue(":status", "binding")
        query.exec_()
        
        if not self.isBinding(crystalid, boardid):
            result[0]=False
            result[1]=False
            result[2]=False
        
        return result

    def query(self, crystalid, boardid):
        
        #result[0] is True: crystal is binding to board.
        #result[1] is True: crystal is binding to other board, result[4] is the boardid.
        #result[2] is True: other crystal is binding to board, result[3] is the crystalid.
        #result[5] is the binding time.
        result=[False, False, False, crystalid, boardid, time]
        
        if crystalid and boardid:
            if self.isBinding(crystalid, boardid):
                result[0]=True
                result[5]=self.getBindingTime(result[3], result[4])
        
        elif crystalid:
            if self.isBinding(crystalid):
                boardid=self.getCrystalBinding(crystalid)
                result[1]=True
                result[4]=boardid
                result[5]=self.getBindingTime(result[3], result[4])
                
        elif boardid:
            if self.isBinding(0, boardid):
                crystalid=self.getBoardBinding(boardid)
                result[2]=True
                result[3]=crystalid
                result[5]=self.getBindingTime(result[3], result[4])
                
        #result[5]=self.getBindingTime(result[3], result[4])
        
        return result

    def unbind(self, crystalid, boardid):
        #result[0] is True: detach OK
        #result[1] is True: detach crystal from other board OK,result[4] is the boardid.
        #result[2] is True: detach other crystal from board OK, result[3] is the crystalid.
        result=[False, False, False, crystalid, boardid]
        
        if crystalid and boardid:
            if self.isBinding(crystalid, boardid):
                result[0]=self.detach(crystalid, boardid)
        
        elif crystalid:
            if self.isBinding(crystalid):
                boardid=self.getCrystalBinding(crystalid)
                #print "impossible, crystal is binding to boardid %d"%boardid
                result[1]=self.detach(crystalid, boardid)
                result[4]=boardid
                
        elif boardid:
            if self.isBinding(0, boardid):
                crystalid=self.getBoardBinding(boardid)
                #print "impossible, board is binding to crystalid %d"%crystalid
                result[2]=self.detach(crystalid, boardid)
                result[3]=crystalid
                
        return result
        
    #There are two steps of detach: first insert then update
    def detach(self, crystalid, boardid):
        query = QSqlQuery()
        print "detach crystal id "+str(crystalid)+" from board id "+str(boardid)
        #insert unbind record
        query.prepare("INSERT INTO bind (crystalid, boardid, status, time, operator) "
                     "VALUES (:crystalid, :boardid, :status, now(), user())") 
        query.bindValue(":crystalid", crystalid)
        query.bindValue(":boardid", boardid)
        query.bindValue(":status", "unbind")
        query.exec_()
        
        #update status from binding to bound
        query.prepare("UPDATE bind set status='bound' "
                         "where crystalid="+str(crystalid)+" and boardid="+str(boardid)+" and status='binding'")
        query.exec_()
        
        #check
        if self.isBinding(crystalid, boardid):
            return False
        else:
            return True
    
    def isBinding(self, crystalid, boardid=0):
        query = QSqlQuery()
        if crystalid and boardid:
            query.exec_("SELECT status FROM bind WHERE crystalid="+str(crystalid)+" and boardid="+str(boardid))
        elif crystalid:
            query.exec_("SELECT status FROM bind WHERE crystalid="+str(crystalid))
        elif boardid:
            query.exec_("SELECT status FROM bind WHERE boardid="+str(boardid))
        else:
            #cannot be all zero, fatal error
            sys.exit(1)
        
        while query.next():
            if query.value(0).toString() == "binding":
                #print query.value(0).toString()
                return True
            
        return False
    

    def getCrystalBinding(self, crystalid):
        query = QSqlQuery()
        query.exec_("SELECT boardid FROM bind WHERE crystalid="+str(crystalid)+" and status='binding'")
        if query.next():
            boardid = query.value(0).toInt()[0]
            #print "return boardid "+str(boardid)
            return boardid
        else:
            return 0

    def getBoardBinding(self, boardid):
        query = QSqlQuery()
        query.exec_("SELECT crystalid FROM bind WHERE boardid="+str(boardid)+" and status='binding'")
        if query.next():
            crystalid = query.value(0).toInt()[0]
            #print "return crystalid "+str(crystalid)
            return crystalid
        else:
            return 0
        
    def getBindingTime(self, crystalid, boardid):
        query = QSqlQuery()
        query.exec_("SELECT time FROM bind WHERE crystalid="+str(crystalid)+" and boardid="+str(boardid)+" and status='binding'")
        if query.next():
            bindingTime = query.value(0).toString()
            return bindingTime
        else:
            return ''
  
        
    def getCrystalSn(self, id):
        query = QSqlQuery()
        query.exec_("SELECT sn FROM crystal WHERE id="+str(id))
        if query.next():
            return query.value(0).toString()
        else:
            return ''

    def getBoardSn(self, id):
        query = QSqlQuery()
        query.exec_("SELECT sn FROM board WHERE id="+str(id))
        if query.next():
            return query.value(0).toString()
        else:
            return ''

    def getCrystalId(self, sn):
        query = QSqlQuery()
        query.exec_("SELECT id FROM crystal WHERE sn='"+sn+"'" )
    
        if not query.next():
            return 0
            
        return query.value(0).toInt()[0]

    def getBoardId(self, sn):
        query = QSqlQuery()
        query.exec_("SELECT id FROM board WHERE sn='"+sn+"'" )
    
        if not query.next():
            return 0
            
        return query.value(0).toInt()[0]

    def addCrystal(self, sn):
        query = QSqlQuery()
        query.exec_("SELECT id FROM crystal WHERE sn='"+sn+"'" )
    
        if not query.next():
            print "insert new crystal"
            query.prepare("INSERT INTO crystal (sn) "
                    "VALUES (:sn)")
            query.bindValue(":sn", sn)
            query.exec_()
            
            query.exec_("SELECT id FROM crystal WHERE sn='"+sn+"'" )
            if not query.next():
                return 0
            
        crystalid = query.value(0).toInt()[0]
        return crystalid

    def addBoard(self, sn):
        query = QSqlQuery()
        query.exec_("SELECT id FROM board WHERE sn='"+sn+"'" )
    
        if not query.next():
            print "insert new board"
            query.prepare("INSERT INTO board (sn) "
                    "VALUES (:sn)")
            query.bindValue(":sn", sn)
            query.exec_()
            
            query.exec_("SELECT id FROM board WHERE sn='"+sn+"'" )
            if not query.next():
                return 0    
            
        boardid = query.value(0).toInt()[0]
        return boardid


def main():
    app = QApplication(sys.argv)

    db = QSqlDatabase.addDatabase("QMYSQL")
    #todo: get host, user and password from diaglog
    db.setHostName(DB_SERVER)
    db.setUserName("root")
    db.setPassword(ROOT_PASS)
    
    #test connection
    if not db.open():
        QMessageBox.warning(None, MESSAGE_TITLE,
            QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)
        
    db.setDatabaseName(DB_NAME)

    if db.open():
        create=False
    else:
        create=True
        print "create database..."
        #re-connect
        db.setDatabaseName('')
        db.open()
        query=QSqlQuery()
        query.exec_("CREATE DATABASE IF NOT EXISTS "+DB_NAME)        
        db.setDatabaseName(DB_NAME)
        if not db.open():
            QMessageBox.warning(None, MESSAGE_TITLE,
                QString("Database Error: %1").arg(db.lastError().text()))
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
        
        #dropTables()
        createTables()
        #createFakeData()

    form = MainForm()
    form.show()
    
    form_login=LoginForm()
    form_login.show()
    
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    app.exec_()
    del form
    del db


main()

