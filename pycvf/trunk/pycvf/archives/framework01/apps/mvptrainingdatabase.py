# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database for Training
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
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

import Image
from pycvf.lib.graphics.imgfmtutils import *

from jfli.project_specific.mvp.mvpaccess import *


#########################################################################################################################################
# Create the VideoDatabase Object
#########################################################################################################################################

class VideoDatabase(object):
  TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})} 
  def __init__(self,with_mvp=True,channels=None,startfrom=None):
     if (with_mvp):
       self.mvp=MvpAccess(with_ontology=False);
     self.td=datetime.datetime.today()
     self.tdb=datetime.datetime(self.td.year,self.td.month, self.td.day,6,0,0,0)
     self.tdb=self.td-datetime.timedelta(2,0,0)
     self.channels=channels or MvpAccess.stationnames[1:]
     self.startfrom=startfrom or 3580*29.97
  def all(self):
      for channel in self.channels:
        for hour in range(10):
            d=self.tdb+datetime.timedelta(hour)
            try:
              filename=self.mvp.find_video(channel=channel,year=d.year,month=d.month,day=d.day,hour=d.hour)
              videoreader=SimpleVideoReader7(filename,track_selector=VideoDatabase.TS_SMALLVIDEO)
              startfrom=self.startfrom 
              videoreader.seek_to(startfrom)
              yield videoreader
            except:
              print "Error while looking for video in mvptrainingdatabase"
              pass
          
              


