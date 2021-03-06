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
from pycvf.core.builders import *

class DB(database.ContentsDatabase):
  """
   This is a filter database that allows you to limit the number of elements extracted in a database.
   This avoid developpers to include this useful feature in all the database.
  """
  def datatype(self):
      return self.vdb.datatype()
  def __init__(self,db="image.kanji()",limit=50):
      self.vdb=(pycvf_builder(db) if type(db) in [str,unicode] else db)
      self.limit=limit
      for x in dir(self.vdb):
          if (not hasattr(self,x)):
              setattr(self,x,getattr(self.vdb,x))
  def __iter__(self):
         it=iter(self.vdb)
         for e in range(self.limit):
             yield it.next()
  def __getitem__(self, addr):
      return self.vdb[addr]
  def keys(self):
    it=iter(self.vdb.keys())
    try:
      return [it.next() for x in range(self.limit) ]
    except:
      return list(self.vdb.keys())[:self.limit]
  def __len__(self):
      return min(self.limit,len(self.vdb))


ContentsDatabase=DB
__call__=DB
