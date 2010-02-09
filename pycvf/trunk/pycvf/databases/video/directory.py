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

import re, os, math, random, time,sys, traceback, datetime,itertools

from pycvf.lib.video.simplevideoreader7 import *
from pycvf.lib.readers.directoryreader import *
from pyffmpeg import FFMpegReader

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import video

class DB(database.ContentsDatabase, video.Datatype):
  al=None
  def __init__(self,path=None,filefilter=None,extensions="mpg|avi|mp4|flv"):
     if (filefilter==None):
       filefilter="(.*).("+extensions+")"
     self.ir=DirectoryReader(path,filefilter)
     self.itx=iter(self.ir)
  def __iter__(self):
      self.itx,it2=itertools.tee(self.itx)
      try:
        while True:
          #rdr=FFMpegReader()
          fn=it2.next()
          #rdr.open(fn)
          rdr=SimpleVideoReader7(fn)
          yield (rdr, fn)
      except StopIteration:
        pass

ContentsDatabase=DB       
__call__=DB

