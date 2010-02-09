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
from pycvf.core.builders import *
from pycvf.core.errors import *

class DB(database.ContentsDatabase):
  def __init__(self,db="imgkanji()",model="histogram()",modelpath="/",datatype=None):
      self.vdb=(pycvf_builder(db) if type(db) in [str,unicode] else db)
      self.model=(pycvf_builder(model) if type(model) in [str,unicode] else model)
      self.model.init("/",self.vdb,self)
      self.modelpath=modelpath
      metak= self.model.get_features_meta().keys()
      pycvf_warning("TRANSFORMED DB BE SURE TO HAVE CHOSEN THE GOOD MODEL OUTPUT !")      
      pycvf_warning("metak = %r"%(metak,))
      self.modelpathno=metak.index(modelpath)
      pycvf_warning("modelpathno %s -> %d\n"%(modelpath,self.modelpathno,))
      dtp=(self.model.output_datatype(self.vdb) if datatype==None else datatype)
      for f in dir(dtp):
          if (not hasattr(self,f)):
              exec("self."+f+"=dtp."+f)
      self.model.metainfo_curdb=self.vdb              
  def __iter__(self):
         for e in self.vdb:
             #print "ET=",e
             #self.model.metainfo_curaddr=e[1]
             r=self.model.process(e[0],addr=e[1]) # e[0][0] ?
             yield (r[self.modelpathno],e[1])
             del e
  def __getitem__(self, addr):
      #self.model.metainfo_curaddr=addr
      #pycvf_warning( addr)
      e=self.vdb[addr]
      r=self.model.process(e[0],addr=addr) # e[0][0]           
      del e
      return r[self.modelpathno]
  def keys(self):
    return self.vdb.keys()
  def __len__(self):
      return len(self.vdb)


ContentsDatabase=DB
__call__=DB