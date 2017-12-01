#!/usr/bin/env python
# coding=utf-8

import csv
import sys
from detdb import *

DB_SERVER="localhost"
ROOT_PASS="glop3c"

DB_NAME="det"

with open('ModuleId.csv', 'rb') as f:
    lines=csv.reader(f)
    
    db=detdb()
    
    #test database server connection
    if not db.open(DB_SERVER, "root", ROOT_PASS):
        print 'connect server failed'
        sys.exit(1)

    #connect to a database
    if db.open(DB_SERVER, "root", ROOT_PASS, DB_NAME):
        print 'connect database ok'
    else:
        print "create database..."
        #re-connect
        db.open(DB_SERVER, "root", ROOT_PASS)
        
        db.createDb(DB_NAME)
        
        if db.open(DB_SERVER, "root", ROOT_PASS, DB_NAME):
            print "ok"
        else:
            print "failed"
            sys.exit(1)
    
    #dangerous!
    #db.dropTables()

    db.createTables()
    
    lasttime=''
    
    for line in lines:        
        crystal=line[2]
        board=line[3]
        
        if line[4] == '':
            time=lasttime
        else:
            time=line[4]
            lasttime=time
            
        db.importData(crystal, board, time)
