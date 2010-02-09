#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-
import re, os, math, random, time,sys, traceback, datetime
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
import os
from pycvf.core import database
import itertools
import pickle
from pycvf.lib.ui.qt import qapp

class DB(database.ContentsDatabase):
  def __init__(self,dbs):
      self.dbs=dbs
      for db in range(len(self.dbs)):
        try:
          exec("from "+ db +" import ContentsDatabase")
        except:
          exec("from pycvf.databases."+ db +" import ContentsDatabase")  
        ##      
        ##
        ##
        print dbargs
        if (type(dbargs)==dict):
          self.vdb=ContentsDatabase( **dbargs)
        else:
           self.vdb=ContentsDatabase( **eval('{'+dbargs+'}'))
  def datatype(self):
       retun self.dbs.datatype()           
  def __iter__(self):
      for db in self.dbs:
        for e in itertools.ifilter(lambda x:self.vdbval[self.vdbaddr.index(x[1])]>self.threshold ,self.vdb):
           yield e
  def __getitem__(self, addr):
      return self.dbs[addr[0]][addr[1]]
  def keys(self):
      return reduce(lambda b,y: b+map(lambda l:(y[1],l),y[0].keys()) ,zip(self.dbs,range(len(self.dbs))),[])
  

# Framework 2 compatibility       
ContentsDatabase=DB
__call__=DB



  