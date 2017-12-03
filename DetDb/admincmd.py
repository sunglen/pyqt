#!/usr/bin/env python
# coding=utf-8

import sys
from detdb import *

DB_SERVER="localhost"
ROOT_PASS="glop3c"

DB_NAME="det"

username=sys.argv[1]
password=sys.argv[2]

db=detdb()

#test database server connection
if not db.open(DB_SERVER, "root", ROOT_PASS):
    print 'connect server failed'
    sys.exit(1)


if db.haveDbUser(sys.argv[1]):
    print "user "+username+" exist, update its password."
    db.updatePass(username, password)
  
else:  
    if db.createDbUser("query", username, password):
        print "create user "+username+" OK"
