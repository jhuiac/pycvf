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
import Image

try:
  from pycvf.lib.graphics.zopencv import *
except:
  pass


from pycvf.lib.video.simplevideoreader7 import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.graphics import features
from pycvf.lib.graphics.imgfmtutils import *
#from pycvf.lib.video.lazydisplay import LazyDisplay
from pycvfext.niiindex.mvp.mvpaccess import *

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import video 


class DB(database.ContentsDatabase,video.Datatype):
  CONTENT_TYPE="VIDEO"
  TRACK_SELECTOR={ 'video1':(0, -1,{})}
  ld=None
  def __init__(self,with_mvp=True,channels=None,startfrom=None,keyframes_only=True, smallpics=True,track_selector=None):
     if (with_mvp):
       self.mvp=MvpAccess(with_ontology=False);
     self.td=datetime.datetime.today()
     self.tdb=datetime.datetime(self.td.year,self.td.month, self.td.day,6,0,0,0)
     self.tdb=self.td-datetime.timedelta(3,0,0)
     self.channels=channels or MvpAccess.stationnames[1:]
     print self.channels
     self.startfrom=(startfrom==None) and  -20*29.97 or startfrom
     self.track_selector=track_selector or ContentsDatabase.TRACK_SELECTOR
     if (smallpics):
        self.track_selector['video1'][2]['dest_width']=128
        self.track_selector['video1'][2]['dest_height']=96
     if (keyframes_only):
        self.track_selector['video1'][2]['skip_frame']=32
  def __iter__(self):
      for channel in self.channels:
        print channel
        for hour in range(10):
            d=self.tdb+datetime.timedelta(0,hour*3600)
            try:
              print "query = ",dict(channel=channel,year=d.year,month=d.month,day=d.day,hour=d.hour)
              filename=self.mvp.find_video(channel=channel,year=d.year,month=d.month,day=d.day,hour=d.hour)
            except Exception,e:
              print "Error while looking for video in mvptrainingdatabase", e
            try:
              #print "Found Video  :", filename, d
              videoreader=SimpleVideoReader7(filename,track_selector=self.track_selector)
            except Exception,e:
              print "Error while looking for file :", filename, d,  e
            startfrom=self.startfrom
            if (startfrom):
              if (startfrom<0):
                #print videoreader.vr.duration_time()
                videoreader.seek_to(startfrom+videoreader.vr.duration_time()*29.7)
              else:
                videoreader.seek_to(startfrom)
            yield (videoreader, (channel,d))


ContentsDatabase=DB
__call__=DB