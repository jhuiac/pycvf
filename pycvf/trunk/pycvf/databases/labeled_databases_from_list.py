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

from pycvf.core.autoimp import * 
from pycvf.core.builders import * 

from pycvf.datatypes import couple
from pycvf.datatypes import basics


class ContentsDatabase(database.ContentsDatabase):
  def __init__(self,databases={}
#                       { "factory": (pycvf.databases.imagenet.DB, dict(query="factory")),
#                         "plate": (pycvf.databases.imagenet.DB, dict(query="plate"))
#                       }
               ):
      self.databases=dict(map(lambda x:(x[0],x[1][0](**x[1][1])),databases.items()))
      self.labels=self.keys()
      self.vdb=self.databases.values()[0]
      self.dtp=couple.Datatype(self.vdb,basics.Label.Datatype)
      #for f in dir(dtp):
      #    if (not hasattr(self,f)):
      #        exec("self."+f+"=dtp."+f)
  def datatype(self):
      return self.dtp
  def __iter__(self):
      for l in self.databases.items():
         for e in l[1]:
             yield ((e[0],l[0]),(l[0],e[1]))
  def __getitem__(self, addr):
      rdb=self.databases[addr[0]][addr[1]]
      return rdb[addr[1]]
  def __len__(self):
      r=0
      for i in self.databases.values():
          r+=len(i)
      return r
  def labeling_label(selfdb):
        class Labels:
            @staticmethod
            def datatype(self):
                return Label.Datatype
            @staticmethod
            def __iter__():
                return iter(self.databases.keys())
            @staticmethod
            def __getitem__(x):
                return x[0]
        return Labels()      
    


DB=ContentsDatabase
__call__=ContentsDatabase
