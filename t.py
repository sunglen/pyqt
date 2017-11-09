#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time

def t():
  return [0, "abc", False]

print t()[1]

r=t()

if r[2]:
  print "OK"

[one, two, three]=t()

print one
