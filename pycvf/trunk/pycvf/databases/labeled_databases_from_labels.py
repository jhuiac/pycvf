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
from pycvf.datatypes import couple
from pycvf.datatypes import basics

class DB(database.ContentsDatabase):
  def __init__(self,db="subsampled_database",
                    dbargs=""" 'db':"image_directory",'nsamples':4,'dbargs':{'path':'/databases/101ObjectCategories/PNGImages/$label$' , 'rescale':(128,128,'T')} """,labels="os.listdir(eval(self.dbargs.replace('$label$','.'))['dbargs']['path'])"):
      try:
        exec("from "+ db +" import ContentsDatabase as cdb")
      except:
        exec("from pycvf.databases."+ db +" import ContentsDatabase as cdb")  
      self.cdb=cdb
      self.dbargs='{'+dbargs+'}'     
      if (type(labels) in [str,unicode]):
        self.labels=eval(labels)
      else:
        self.labels=labels
      l=self.labels[0]
      self.vdb=self.cdb( **eval((self.dbargs).replace('$label$',l))) 
      self.dtp=couple.Datatype(self.vdb,basics.Label.Datatype)
      #for f in dir(dtp):
      #    if (not hasattr(self,f)):
      #        exec("self."+f+"=dtp."+f)
  def datatype(self):
      return self.dtp
  def __iter__(self):
      for l in self.labels:
         self.vdb=self.cdb( **eval((self.dbargs).replace('$label$',l))) 
         for e in self.vdb:
             yield ((e[0],l),(l,e[1]))
  def __getitem__(self, addr):
      self.vdb=self.cdb( **eval((self.dbargs).replace('$label$',l)))
      return self.vdb[addr]
  def keys(self):
      return reduce(lambda x,y:x+y,
         self.cdb( **eval((self.dbargs).replace('$label$',l))),
         []
         ) 


ContentsDatabase=DB
__call__=DB