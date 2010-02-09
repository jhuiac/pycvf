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
from pycvf.lib.graphics import features
from pycvf.lib.readers.directoryreader import *

import Image
from pycvf.lib.graphics.imgfmtutils import *


#from pycvf.nodes.pseudoreader import PseudoReader
from pycvf.lib.graphics.rescale import Rescaler2d

#from jfli.project_specific.mvp.mvpaccess import *

from pycvf.core import database
from pycvf.datatypes import image
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

class DB(database.ContentsDatabase):
  """
   Provide a way to use strucutred directory as database of images.
   File may be filtered by name, randomized in order , and rescale.
   
   TODO:
      * provide more complex file selection schemes (recursion ..)
  """

  def datatype(self):
      return image.Datatype
  def __init__(self,path=None,rescale=None,filefilter=None,extensions="jpg|png|gif|tif|tga|pgm|ppm",randomized=True):
     if (filefilter==None):
       filefilter="(.*).("+extensions+")"
     self.ir=ImageDirectoryReader(path,filtere=filefilter,randomized=randomized)
     self.rescale=rescale
  def __iter__(self):
      if (self.rescale!=None):
        r=Rescaler2d(self.rescale).process
      else:
        r=lambda x:x
      try:
        while True:
          #yield PseudoReader(self.ir.step())
          i,a=self.ir.next()
          i=r(i)
          yield (i,a)
      except StopIteration:
        pass
  def __getitem__(self,a):
     if (self.rescale!=None):
        r=Rescaler2d(self.rescale).process
     else:
        r=lambda x:x
     return r(self.ir[a])

ContentsDatabase=DB
__call__=DB