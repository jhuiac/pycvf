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

from pycvf.lib.video.simplevideoreader7 import *
#from zopencv import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.graphics import features

import Image
from pycvf.lib.graphics.imgfmtutils import *





#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

#from pycvf.lib.video.lazydisplay import LazyDisplay
from pycvf.lib.video.capture.camerareader2 import CameraReader2
from pycvf.datatypes import image
from pycvf.core import database

class DB(database.ContentsDatabase,image.Datatype):
  ld=None
  def __init__(self,maximg=None,camno=0,bgr=True):
      self.maximg=maximg
      self.cr=CameraReader2(camno,bgr=bgr)
  def __iter__(self):
     class O:
         def __init__(self):
            self.o=None
         def f(self,x):
             self.o=x
     o=O()
     self.cr.set_observer(o.f)
     while True:
        if (self.maximg!=None):
            if self.maximg==0:
                break
            self.maximg-=1
        self.cr.step()
        yield (o.o,None)

ContentsDatabase=DB
__call__=DB
          
              
