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
from pycvf.core.errors import *
from pycvf.core import database
import itertools
import pickle
from pycvf.lib.ui.qt import qapp

class DB(database.ContentsDatabase):
  def __init__(self,db,session="std",threshold=0.8,annfile=os.environ["HOME"]+"/"+"weights/$database-$session.pcl",reevaluate=False):
      self.vdb=database_builder(db)
      self.threshold=threshold
      for f in dir(dtp):
          if (not hasattr(self,f)):
              exec("self."+f+"=dtp."+f)
      self.annfile=annfile
      self.annfile=self.annfile.replace("$database",db)
      self.annfile=self.annfile.replace("$session",session)
      print self.annfile
      try:
           if (reevaluate):
               raise Exception    
           self.vdbval=pickle.load(file(self.annfile,"rb"))
           self.vdbaddr=pickle.load(file(self.annfile+".keys","rb"))
      except: 
            pycvf_debug(10, "Evaluating db")
            self.vdbval=None
            self.vdbaddr=None
            try:           
               self.vdbval=pickle.load(file(self.annfile,"rb"))
               self.vdbaddr=pickle.load(file(self.annfile+".keys","rb"))
            except:
               pycvf_debug(10,"no load")
               pass
            print "Go QT.."
            from pycvf.lib.ui import qtdbevaluator
            d=qtdbevaluator.QtDBEvaluatorDialog(self.vdb,self.vdbval,self.vdbaddr)
            qapp.processEvents()
            pycvf_debug(10,"Run dialog")
            if d.exec_():
                pickle.dump(d.pwl.vdbval,file(self.annfile,"wb"),protocol=2)
                pickle.dump(d.pwl.addr,file(self.annfile+".keys","wb"),protocol=2)
                self.vdbval=d.pwl.vdbval
                self.vdbaddr=d.pwl.addr
            else:
                if (self.vdbval==None):
                  raise Exception, "No user evaluation for database"
  def __iter__(self):
      for e in itertools.ifilter(lambda x:self.vdbval[self.vdbaddr.index(x[1])]>self.threshold ,self.vdb):
         yield e
  def __getitem__(self, addr):
      return self.vdb[addr]
  def keys(self):
      return self.vdbaddr
       


ContentsDatabase=DB
__call__=DB

  