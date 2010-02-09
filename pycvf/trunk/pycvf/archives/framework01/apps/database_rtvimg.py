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

from pycvf.lib.video.simplevideoreader7 import *
from pycvf.lib.graphics.zopencv import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.graphics import features
from pycvf.lib.graphics.randomtvimages import *

import Image
from pycvf.lib.graphics.imgfmtutils import *

from jfli.project_specific.mvp.mvpaccess import *


#########################################################################################################################################
# Create the VideoDatabase Object
#########################################################################################################################################

class VideoDatabase(object):
  #TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})} 
  def __init__(self,channels=None,maxframes=10):
     self.channels=channels or MvpAccess.stationnames[1:]
     self.maxframes=maxframes
  def all(self):
      yield RandomTVImageReader(channels=self.channels, max_frames=self.maxframes)


          
              


