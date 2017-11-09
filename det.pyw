#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui_mainform
import qrc_resources


def createFakeData():
    import random

    print "Dropping tables..."
    query = QSqlQuery()
    #must drop table bind first because of foreign key.
    query.exec_("DROP TABLE bind")
    query.exec_("DROP TABLE crystal")
    query.exec_("DROP TABLE board")

    QApplication.processEvents()

    print "Creating tables..."
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

    print "Populating tables..."
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
        
    time.sleep(5)

    query.prepare("INSERT INTO bind (crystalid, boardid, status, time, operator) "
                     "VALUES (:crystalid, :boardid, :status, now(), user())") 
    query.bindValue(":crystalid", crystalid)
    query.bindValue(":boardid", boardid)
    query.bindValue(":status", "unbind")
    query.exec_()
    
    query.prepare("UPDATE bind set status='bound' "
                     "where crystalid="+str(crystalid)+" and boardid="+str(boardid)+" and status='binding'")
    query.exec_()

class MainForm(QDialog,
               ui_mainform.Ui_MainForm):

    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.updateUi()

    def updateUi(self):
        #validate user input, min character numbers is useless.
        self.crystalLine.setValidator(QRegExpValidator(QRegExp("[0-9A-Za-z\-]{6,20}"), self))
        self.boardLine.setValidator(QRegExpValidator(QRegExp("[0-9A-Za-z\-]{7,20}"), self))
        
        #validate min character numbers
        #if self.crystalLine.text().isEmpty() and self.boardLine.text().isEmpty():
        if self.crystalLine.text().length()<6 and self.boardLine.text().length()<7:
            self.queryButton.setEnabled(False)
            self.unbindButton.setEnabled(False)
        else:
            self.queryButton.setEnabled(True)
            self.unbindButton.setEnabled(True)
            
        #if self.crystalLine.text().isEmpty() or self.boardLine.text().isEmpty():
        if self.crystalLine.text().length()<6 or self.boardLine.text().length()<7:
            self.bindButton.setEnabled(False)
        else:
            self.bindButton.setEnabled(True)

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
        self.bind(crystal, board)
    
    @pyqtSignature("")
    def on_unbindButton_clicked(self):
        print "unbind crystal "+self.crystalLine.text()+" from board "+self.boardLine.text()
        crystal=self.crystalLine.text()
        board=self.boardLine.text()
        result=self.unbind(crystal, board)
        if result[0]:
            print "done: unbind crystal sn#"+crystal+" from board sn#"+board
        
        if result[1]:
            print "done: unbind crystal sn#"+crystal
            
        if result[2]:
            print "done: unbind  board sn#"+board

        #[detached, crystalid, boardid]=self.unbind(crystal, board)
        #if detached:
        #    print "done: unbind crystal sn#"+self.getCrystalSn(crystalid)+" from board sn#"+self.getBoardSn(boardid)
        #else:
        #    print "do again: unbind crystal sn#"+self.getCrystalSn(crystalid)+" from board sn#"+self.getBoardSn(boardid)
    
    @pyqtSignature("")
    def on_queryButton_clicked(self):
        print self.boardLine.text()

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
            query.next()
            
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
            query.next()    
            
        boardid = query.value(0).toInt()[0]
        return boardid

    def bind(self, crystal, board):
        crystalid=self.addCrystal(crystal)
        boardid=self.addBoard(board)
        print "bind crystal id "+str(crystalid)+" to board id "+str(boardid)
        if self.isBinding(crystalid, boardid):
            print "impossible, binding already"
            return True
        if self.isBinding(crystalid):
            print "failed, crystal is binding already, unbind first"
            #self.getCrystalBinding(crystalid)
            return False
        if self.isBinding(0, boardid):
            print "failed, board is binding already, unbind first"
            #self.getBoardBinding(boardid)
            return False
        query = QSqlQuery()
        query.prepare("INSERT INTO bind (crystalid, boardid, status, time, operator) "
                     "VALUES (:crystalid, :boardid, :status, now(), user())") 
        query.bindValue(":crystalid", crystalid)
        query.bindValue(":boardid", boardid)
        query.bindValue(":status", "binding")
        query.exec_()
        return True

    def unbind(self, crystal, board):
        crystalid=self.getCrystalId(crystal)
        boardid=self.getBoardId(board)
        
        result=[False, False, False]
        
        if crystalid and boardid:
            if self.isBinding(crystalid, boardid):
                return [self.detach(crystalid, boardid), False, False]
        
        if crystalid:
            if self.isBinding(crystalid):
                boardid=self.getCrystalBinding(crystalid)
                #print "impossible, crystal is binding to boardid %d"%boardid
                #return [self.detach(crystalid, boardid), crystalid, boardid]
                result[1]=self.detach(crystalid, boardid)
        
        if boardid:    
            if self.isBinding(0, boardid):
                crystalid=self.getBoardBinding(boardid)
                #print "impossible, board is binding to crystalid %d"%crystalid
                #return [False, crystalid, boardid]
                result[2]=self.detach(crystalid, boardid)
                
        #return [result, crystalid, boardid]
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
            #cannot be all zero
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
            print "return boardid "+str(boardid)
            return boardid
        else:
            return 0

    def getBoardBinding(self, boardid):
        query = QSqlQuery()
        query.exec_("SELECT crystalid FROM bind WHERE boardid="+str(boardid)+" and status='binding'")
        if query.next():
            crystalid = query.value(0).toInt()[0]
            print "return crystalid "+str(crystalid)
            return crystalid
        else:
            return 0
        
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

    def addAsset(self):
        row = self.assetView.currentIndex().row() \
            if self.assetView.currentIndex().isValid() else 0

        QSqlDatabase.database().transaction()
        self.assetModel.insertRow(row)
        index = self.assetModel.index(row, NAME)
        self.assetView.setCurrentIndex(index)

        assetid = 1
        query = QSqlQuery()
        query.exec_("SELECT MAX(id) FROM assets")
        if query.next():
            assetid = query.value(0).toInt()[0]
        query.prepare("INSERT INTO logs (assetid, date, actionid) "
                      "VALUES (:assetid, :date, :actionid)")
        query.bindValue(":assetid", QVariant(assetid + 1))
        query.bindValue(":date", QVariant(QDate.currentDate()))
        query.bindValue(":actionid", QVariant(ACQUIRED))
        query.exec_()
        QSqlDatabase.database().commit()
        self.assetView.edit(index)


    def deleteAsset(self):
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
        QSqlDatabase.database().transaction()
        record = self.assetModel.record(index.row())
        assetid = record.value(ID).toInt()[0]
        logrecords = 1
        query = QSqlQuery(QString("SELECT COUNT(*) FROM logs "
                                  "WHERE assetid = %1").arg(assetid))
        if query.next():
            logrecords = query.value(0).toInt()[0]
        msg = QString("<font color=red>Delete</font><br><b>%1</b>"
                      "<br>from room %2") \
                      .arg(record.value(NAME).toString()) \
                      .arg(record.value(ROOM).toString())
        if logrecords > 1:
            msg += QString(", along with %1 log records") \
                   .arg(logrecords)
        msg += "?"
        if QMessageBox.question(self, "Delete Asset", msg,
                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            QSqlDatabase.database().rollback()
            return
        query.exec_(QString("DELETE FROM logs WHERE assetid = %1") \
                    .arg(assetid))
        self.assetModel.removeRow(index.row())
        self.assetModel.submitAll()
        QSqlDatabase.database().commit()
        self.assetChanged(self.assetView.currentIndex())

    def deleteAction(self):
        index = self.logView.currentIndex()
        if not index.isValid():
            return
        record = self.logModel.record(index.row())
        action = record.value(ACTIONID).toString()
        if action == "Acquired":
            QMessageBox.information(self, "Delete Log",
                    "The 'Acquired' log record cannot be deleted.<br>"
                    "You could delete the entire asset instead.")
            return
        when = unicode(record.value(DATE).toString())
        if QMessageBox.question(self, "Delete Log",
                "Delete log<br>%s %s?" % (when, action),
                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        self.logModel.removeRow(index.row())
        self.logModel.submitAll()


def main():
    app = QApplication(sys.argv)

    dbname="det"

    db = QSqlDatabase.addDatabase("QMYSQL")
    #todo: get host, user and password from diaglog
    db.setHostName("localhost")
    db.setUserName("root")
    db.setPassword("glop3c")
    
    #test connection
    if not db.open():
        QMessageBox.warning(None, u"探测器模块组装记录",
            QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)
        
    db.setDatabaseName(dbname)

    if db.open():
        create=False
    else:
        create=True
        print "create database..."
        #re-connect
        db.setDatabaseName('')
        db.open()
        query=QSqlQuery()
        query.exec_("CREATE DATABASE IF NOT EXISTS "+dbname)        
        db.setDatabaseName(dbname)
        if not db.open():
            QMessageBox.warning(None, u"探测器模块组装记录",
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
        createFakeData()

    form = MainForm()
    form.show()
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    app.exec_()
    del form
    del db


main()

