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
import hashlib
import pickle
#from pycvf.lib.ui.qt import qapp
from pycvf.datatypes import couple
from pycvf.datatypes import basics
from pycvf.core.builders import *
from pycvf.core.errors import *

class DB(database.ContentsDatabase):
  """
  This create a dabase from another database by exploding all the elements of the initial database
  according to specified structure.
  """
  def __init__(self,db,structure=None,quick_len=False,cache_id=None):
      self.vdb=(model_builder(db) if type(db) in [str, unicode] else db)
      if (structure==None):
          #structure=self.vdb.datatype.default_structure()
          structure=self.vdb.default_structure()
      self.structure=(pycvf_builder(structure) if type(structure) in [str, unicode] else structure)
      self.quick_len=quick_len
      self.cache_id=cache_id
      self.dtp=self.structure.output_datatype(self.vdb.datatype())
      #for f in dir(dtp):
      #    if (not hasattr(self,f)):
      #        exec("self."+f+"=dtp."+f)
  def datatype(self):
      return self.dtp
  def __iter__(self):
         try:
           for e in self.vdb:
             #print "E=",e
             decomposed=self.structure.items(e[0])
             #print "TYPEE0=",type(e[0]),
             #print "E0",e[0]             
             #print "DETYPE=",type(decomposed)
             #print "ED=",len(list(decomposed))
             for s in decomposed:
                #print "s[0]",s[0]
                print type(s[1])
                yield (s[1],(e[1],s[0]))
         except Exception,e:
            pycvf_warning("Exception "+str(e)+" converted to stopiteration")
            pycvf_backtrace()
            raise StopIteration 
  def __getitem__(self, addr):
      e=self.vdb[addr[0]]
      #print addr[0],":",e
      l=list(self.structure.items(e))
      #print e,l
      decomposed=dict(l)
      return decomposed[addr[1]] 
  def keys(self):
        if (self.cache_id):
              try:
                   os.stat(self.cache_id)
                   pycvf_warning("Exploded datatabase : Key cache has been found : using it\n")
                   return pickle.load(file(self.cache_id,"rb"))
              except OSError:
                  pycvf_warning("Exploded database : Recomputing Key Cache\n")
                  r=[]
                  for e in self.vdb:
                     decomposed=self.structure.items(e[0])
                     for s in decomposed:
                        r.append((e[1],s[0]))
                     del e
                  pickle.dump(r,file(self.cache_id,"wb"),2)
                  return r
        else:
            return self.gkeys()
  def gkeys(self):
           for e in self.vdb:
             decomposed=self.structure.items(e[0])
             for s in decomposed:
                print  (e[1],s[0])
                yield  (e[1],s[0])
             del e
  def __len__(self):
      r=0
      if self.quick_len:
          e=iter(self.vdb).next()
          decomposed=self.structure.keys(e[0])
          return len(self.vdb)*len(decomposed)
      else:
        for e in self.vdb:
             decomposed=self.structure.keys(e[0])
             r+=len(decomposed)
      return r


ContentsDatabase=DB
__call__=DB