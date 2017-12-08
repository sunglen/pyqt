#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time

import threading

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_threadtest

class Power():
    def turnOn(self):
        logger.logToWidget('Machine Power On')

    def turnOff(self):
        logger.logToWidget('Machine Power Off')
        

class myThread(threading.Thread):
    def __init__(self, threadID, name, testList):
        super(myThread, self).__init__()
        self.threadID = threadID
        self.name = name
        self.testList = testList
        
        #manage the exit of my thread
        self.runFlag =True
        
    def run(self):
        for i in self.testList:
            if not self.runFlag:
                return
            if i.text() == u'自检':
                logger.logToWidget('Process Self-Test')
                time.sleep(2)
            elif i.text() == u'预热':
                logger.logToWidget('Process Pre-Heating')
                time.sleep(2)
            elif i.text() == u'扫描1':
                logger.logToWidget('Process Scan-1')
                time.sleep(3)
            elif i.text() == u'扫描2':
                logger.logToWidget('Process Scan-2')
                time.sleep(3)
            else:
                logger.logToWidget('Process Unknown')

    def stop(self):
        self.runFlag = False

class MsgLogger(QObject):
    sigMsg = pyqtSignal(str)
    
    def __init__(self):
        super(MsgLogger, self).__init__()
        
    def logToWidget(self, msg):
        self.sigMsg.emit(msg)

class ThreadTest(QWidget, ui_threadtest.Ui_ThreadTest):
    
    sigStart = pyqtSignal(list)
    
    def __init__(self):
        super(ThreadTest, self).__init__()
        self.setupUi(self)
        
        self.sigStart.connect(self.startTest)
        
        self.checkBox.stateChanged.connect(self.onCheck)
        
        self.startButton.clicked.connect(self.onStart)

        self.stopButton.clicked.connect(self.onStop)
        
        self.logger = logger
        self.logger.sigMsg.connect(self.appendMsg)
        
    def updateMsg(self, msg):
        self.textEdit.setText(msg)
        
    def appendMsg(self, msg):
        self.textEdit.append(msg)
        
    def onCheck(self):
        if self.checkBox.isChecked():
            self.listWidget.selectAll()
        
    def onStart(self):
        self.updateMsg(u'开始测试……')
        power.turnOn()
        self.sigStart.emit(self.listWidget.selectedItems())
    
    def onStop(self):
        self.thread1.stop()
        power.turnOff()
    
    def startTest(self, testList):
        self.thread1 = myThread(1, "normal", testList)
        self.thread1.start()

if __name__ == '__main__':
    logger = MsgLogger()
    power = Power()
    app = QApplication(sys.argv)
    t = ThreadTest()
    t.show()
    sys.exit(app.exec_())
