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
from pycvf.lib.video.videosequencereader import *

from jfli.project_specific.mvp.mvpaccess import *

from pycvf.lib.video.lazydisplay import LazyDisplay
from pycvf.datatypes import video

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database

class DB(database.ContentsDatabase,video.Datatypes):
  #TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})} 
  ld=None
  def __init__(self,channels=None,max_videos=10):
     self.channels=channels or MvpAccess.stationnames[1:]
     self.max_videos=max_videos
  def __iter__(self):
     rtv=RandomTVSequenceReader(channels=self.channels, max_videos=self.max_videos,minlen=90,maxlen=500,)
     try:
       while True:
         vr=(VideoSequenceReader(rtv.step()), rtv.get_current_address())
         yield vr
     except StopIteration:
        pass
          
ContentsDatabase=DB
__call__=DB      
