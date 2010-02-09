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
from pycvf.datatypes import couple
from pycvf.datatypes import basics

class DB(database.ContentsDatabase):
  """
   This database either  DEPRECATED either to be up UPDATED.
  """
  def __init__(self,db="image_directory",dbargs="",samplefrom=0,nsamples=20):
      try:
        exec("from "+ db +" import ContentsDatabase as cdb")
      except:
        exec("from pycvf.databases."+ db +" import ContentsDatabase as cdb")
      self.samplefrom=samplefrom
      self.nsamples=nsamples
      self.cdb=cdb
      if (type(dbargs) in [ str, unicode]):
        self.vdb=self.cdb( **eval('{'+dbargs+'}') )
      else:
        self.vdb=self.cdb( **dbargs )
      try:
         self.keys=self.vdb.keys()[samplefrom:(samplefrom+nsamples)]
      except:
         ki=self.vdb.keys()
         for i in range(samplefrom):
            ki.next()
         self.keys=[ki.next() for i in range(nsamples)]
      dtp=self.vdb
      for f in dir(dtp):
          if (not hasattr(self,f)):
              exec("self."+f+"=dtp."+f)
  def __iter__(self):
      for k in self.keys:
          yield (self.vdb[k],k)
  def __getitem__(self, addr):
      return self.vdb[addr]
  def keys(self):
      return self.keys
  def values():
      return map(self.vdb.__getitem__, self.keys)


ContentsDatabase=DB