# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database for Training
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
################################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback, datetime
from pycvf.lib.graphics.imgfmtutils import *


from pycvf.core import database
from pycvf.datatypes import basics
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

class DB(database.ContentsDatabase,basics.NumericArray.Datatype):
  """
    * Create noise images
  """
  #TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})}
  def __init__(self,vdbconstructor, maxelems=None ):
     self.vdb=vdbconstructor
     self.maxelems=maxelems
  def __iter__(self):
      cont=True
      while cont:
          st=numpy.random.get_state()
          yield (numpy.vstack([x[0] for x in self.vdb()]),st)
          if self.maxelems!=None:
              self.maxelems-=1
              if self.maxelems<=0:
                  break
  def __getitem__(self,a):
          numpy.random.set_state(st)
          return numpy.vstack([x[0] for x in self.vdb()])

ContentsDatabase=DB
__call__=DB