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

class DB(database.ContentsDatabase):
  """
    * Create noise images
  """
  #TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})}
  def datatype(self):
    return basics.NumericArray.Datatype
  def __init__(self,ndim=4,nvectors=256, amplitude=1,offset=-0.5,maxelems=None ):
     self.resolution=(nvectors,ndim)
     self.maxelems=maxelems
     self.amplitude=amplitude
     self.offset=offset
  def __iter__(self):
      cont=True
      while cont:
          st=numpy.random.get_state()
          yield (((numpy.random.random(self.resolution)+self.offset)*self.amplitude),st)
          if self.maxelems!=None:
              self.maxelems-=1
              if self.maxelems<=0:
                  break
  def __getitem__(self,a):
          numpy.random.set_state(st)
          return ((numpy.random.random(self.resolution)+self.offset)*self.amplitude)

ContentsDatabase=DB
__call__=DB