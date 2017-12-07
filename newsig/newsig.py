#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_newsig

class NewSigTest(QWidget, ui_newsig.Ui_NewSig):
    
    sigStart = pyqtSignal(list)
    
    def __init__(self):
        super(NewSigTest, self).__init__()
        self.setupUi(self)
        
        self.sigStart.connect(self.startTest)
        
        self.checkBox.stateChanged.connect(self.onCheck)
        
        self.pushButton.clicked.connect(self.onStart)
        
    def updateMsg(self, msg):
        self.textEdit.setText(msg)
        
    def appendMsg(self, msg):
        self.textEdit.append(msg)
        
    def onCheck(self):
        if self.checkBox.isChecked():
            self.listWidget.selectAll()
        
    def onStart(self):
        self.updateMsg(u'开始测试……')
        self.sigStart.emit(self.listWidget.selectedItems())
    
    def startTest(self, testList):
        #run testList in order
        for i in testList:
            self.appendMsg(i.text())
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    newsig = NewSigTest()
    newsig.show()
    sys.exit(app.exec_())
