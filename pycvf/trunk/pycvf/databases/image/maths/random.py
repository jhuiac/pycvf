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
from pycvf.datatypes import image
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

class DB(database.ContentsDatabase,image.Datatype):
  """
    * Create noise images
  """
  #TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})}
  def __init__(self,resolution=(256,256), maximage=None ):
     self.resolution=resolution
     self.maximage=maximage
  def __iter__(self):
      cont=True
      while cont:
          st=numpy.random.get_state()
          yield ((numpy.random.random(self.resolution)*255).astype(numpy.uint8),st)
          if self.maximage!=None:
              self.maximage-=1
              if self.maximage<=0:
                  break
  def __getitem__(self,a):
          numpy.random.set_state(st)
          return (numpy.random.random(self.resolution)*255).astype(numpy.uint8)

ContentsDatabase=DB
__call__=DB