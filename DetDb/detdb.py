#!/usr/bin/env python
# coding=utf-8

import re
from PyQt4.QtCore import *
from PyQt4.QtSql import *

class detdb():

    def __init__(self):
        pass
        #self.db = QSqlDatabase.addDatabase("QMYSQL")
        
    def open(self, dbserver, username, password, dbname=''):
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName(dbserver)
        db.setUserName(username)
        db.setPassword(password)
        db.setDatabaseName(dbname)
        return db.open()
    
    def close(self):
        pass
        #return self.db.close()
    
    def createDb(self, dbname):
        query=QSqlQuery()
        query.exec_("CREATE DATABASE IF NOT EXISTS "+dbname)        
        
    def dropTables(self):
        print "Dropping tables..."
        query = QSqlQuery()
        #must drop table bind first because of foreign key.
        query.exec_("DROP TABLE bind")
        query.exec_("DROP TABLE crystal")
        query.exec_("DROP TABLE board")
    
    
    def createTables(self):
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
    
    
    def createFakeData(self):
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
    
    def setBindingTime(self, crystalid, boardid, time):
        query = QSqlQuery()
        print "set binding time for crystal id "+str(crystalid)+" and board id "+str(boardid)+" as "+time
        
        query.prepare("UPDATE bind set time='"+time+"' "
                         "where crystalid="+str(crystalid)+" and boardid="+str(boardid)+" and status='binding'")
        query.exec_()
        
    def importData(self, crystal, board, time):
        
        if not self.matchCrystalSn(crystal):
            print 'invalid crystal sn#'+crystal+', ignore'
            return
        elif not self.matchBoardSn(board):
            print 'invalid board sn#'+board+', ignore'
            return
        else:
            print "import csv data: crystal sn#"+crystal+' to board sn#'+board+' at '+time

        result=self.bind(crystal, board)
        
        if not result[3]:
            print "Crystal record is NOT exist and CANNOT be added"
            return
            
        if not result[4]:
            print "Board record is NOT exist and CANNOT be added"
            return
        
        if result[0] and result[1] and result[2]:
            print "done: binding crystal sn#"+crystal+" to board sn#"+board
            self.setBindingTime(result[3], result[4], time)

        elif not result[0] and result[1] and result[2]:
            print "failed: already binding crystal sn#"+crystal+" to board sn#"+board

        elif result[0] and not result[1] and result[2]:
            print "falied: already binding crystal sn#"+crystal+" to board sn#"+self.getBoardSn(result[4])

        elif result[0] and result[1] and not result[2]:
            print "falied: already binding crystal sn#"+self.getCrystalSn(result[3])+" to board sn#"+board

        else:
            print "failed: insert record error"
            
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
        result=[False, False, False, crystalid, boardid, '']
        
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
            print "insert new crystal sn#"+sn
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
            print "insert new board sn#"+sn
            query.prepare("INSERT INTO board (sn) "
                    "VALUES (:sn)")
            query.bindValue(":sn", sn)
            query.exec_()
            
            query.exec_("SELECT id FROM board WHERE sn='"+sn+"'" )
            if not query.next():
                return 0    
            
        boardid = query.value(0).toInt()[0]
        return boardid

    def matchCrystalSn(self, sn):
        return re.match("^[0-9][A-Za-z][0-9]{4}$", sn)
    
    def matchBoardSn(self, sn):
        return re.match("^[A-Za-z]{2}[0-9]{7}$", sn)
