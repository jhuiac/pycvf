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

from pycvfext.niiindex.mvp.randomtvimages import *

import Image
from pycvf.lib.graphics.imgfmtutils import *




#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

from pycvf.datatypes import image
from pycvf.core import database

class DB(database.ContentsDatabase,image.Datatype):
  #TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})} 
  def __init__(self,channels=None,maxframes=100):
     self.channels=channels or MvpAccess.stationnames[1:]
     self.maxframes=maxframes
  def __iter__(self):
      rtvimg=RandomTVImageReader(channels=self.channels, max_frames=self.maxframes)
      while True:
         i,a=rtvimg.step()
         #a=rtvimg.get_current_address()
         yield (i,a)
  
__call__=DB          
ContentsDatabase=DB

