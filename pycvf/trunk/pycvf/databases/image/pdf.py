
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

class DB(database.ContentsDatabase,image.Datatype):
  """
   Provide a way to use strucutred directory as database of images.
   File may be filtered by name, randomized in order , and rescale.
   
   TODO:
      * provide more complex file selection schemes (recursion ..)
  """
  #TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})}
  def __init__(self,filename,resolution=150):
      self.filename=filename
      self.resolution=resolution
  def __iter__(self):
      p=1
      tfb="/tmp/page"
      while True:
          #yield PseudoReader(self.ir.step())
          r=os.system("pdftoppm -png -r %d -f %d  -l %d %s %s"%(self.resolution,p,p,self.filename,tfb))
          if (r!=0):
              break
          else:
            try: 
              i=PIL2NumPy(Image.open("%s-%02d.png"%(tfb,p)))
              yield (i,p)
              p+=1
            except:
              break
  def __getitem__(self,a):
     #if (self.rescale!=None):
     #   r=Rescaler2d(self.rescale).process
     #else:
     #   r=lambda x:x
     #return r(self.ir[a])
     assert False

ContentsDatabase=DB
__call__=DB