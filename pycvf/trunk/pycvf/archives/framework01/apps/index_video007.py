# -*- coding: utf-8 -*-

#########################################################################################################################################
#
# Video Database builder By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback
import scipy,pylab,scipy.ndimage
from scipy.spatial.kdtree import KDTree

from jfli.project_specific.mvp.mvpaccess import *

from pycvf.lib.video.lazydisplayqt import *
from pycvf.lib.video.simplevideoreader7 import *

from pycvf.lib.graphics.zopencv import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.graphics import features

from pycvf.indexes.bssdbindex import *
from pycvf.indexes.indexbuilders import *
from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *
from jfli.signal.blockops_opt import *

from pycvf.lib.stats.models import *

import os
import sys
import time
import logging

import scipy.spatial

#########################################################################################################################################


class VideoIndexer(VisionModel7):
  TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})} 
  def __init__(self,with_mvp=True):
     if (with_mvp):
       self.mvp=MvpAccess(with_ontology=False);
     #self.
  def train(self,**kwargs):
     if "channel" in kwargs.keys():
       channel=kwargs["channel"]
       d=kwargs["d"]
       filename=self.mvp.find_video(channel=channel,year=d.year,month=d.month,day=d.day,hour=d.hour)
       self.channel=channel
       self.d=d
       self.videoreader=SimpleVideoReader7(filename,track_selector=VideoIndexer.TS_SMALLVIDEO)       
     else:
       channel=kwargs["filename"]
       d=datetime.datetime(2009,1,1,0,0,0)
       filename=kwargs["filename"]
       self.channel=channel
       self.d=d
       self.videoreader=SimpleVideoReader7(filename,track_selector=VideoIndexer.TS_SMALLVIDEO)       
     self.init_observed_features_video()
     self.init_observed_features_statistics()
     track=NullTrack(self.observed_features)     
     #########################################################################################################################################
     # Link with all the required, Run  and Destroy
     #########################################################################################################################################
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],self.observed_features),{})
     observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))
     self.videoreader.set_observer(observer.iterproceed)
     self.videoreader.seek_to(3580*29.97)
     self.videoreader.run()
     self.observed_features=None
     observer.context=None
     observer=None
     self.videoreader=None
     
  def test(self,**kwargs):
     if "d" in kwargs.keys():
       channel=kwargs["channel"]
       d=kwargs["d"]
       filename=self.mvp.find_video(channel=channel,year=d.year,month=d.month,day=d.day,hour=d.hour)
       self.channel=channel
       self.d=d
       self.videoreader=SimpleVideoReader7(filename,track_selector=VideoIndexer.TS_SMALLVIDEO)
       startfrom=3580*29.97
       trkfilename="/tmp2/video_test-idx7-%04d-%02d-%02d-%02d-%s.trk"%(d.year,d.month,d.day,d.hour,channel)
     else:
       channel=kwargs["channel"]
       d=datetime.datetime(2009,1,1,0,0,0)
       filename=kwargs["filename"]
       self.channel=channel
       self.d=d
       self.videoreader=SimpleVideoReader7(filename,track_selector=VideoIndexer.TS_SMALLVIDEO)
       startfrom=None
       trkfilename="/tmp2/video_test-idx7-%s-%s.trk"%(filename.split("/")[-1],channel)
     self.init_observed_features_video()
     self.init_observed_features_statistics(mlop="test",mlargs="")
     track=OnDiskMultiTrackLargeZ(filename=trkfilename,meta=map(lambda x: x[2],self.observed_features))
     #########################################################################################################################################
     # Link with all the required, Run  and Destroy
     #########################################################################################################################################
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],self.observed_features),{})
     observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))
     self.videoreader.set_observer(observer.iterproceed)
     if (startfrom):
       self.videoreader.seek_to(startfrom)
     self.videoreader.run()
     self.observed_features=None
     observer.context=None
     observer=None
     self.videoreader=None

     
#####################################################################################################################################
## run the model/ train / test
#####################################################################################################################################


if __name__=="__main__":
  import datetime
  vi=VideoIndexer()
  td=datetime.datetime.today()
  tdb=datetime.datetime(td.year,td.month, td.day,6,0,0,0)
  tdb=td-datetime.timedelta(2,0,0)
  for channel in MvpAccess.stationnames[1:]:
    print channel
    for hour in range(10):
       try:
         vi.train(channel=channel,d=tdb+datetime.timedelta(0,hour*3600))
       except Exception,e:
         sys.stderr.write("error during index process of channel : %s at %d:00 : %s\n"%(channel,hour,str(e)))
         if (hasattr(sys,"last_traceback")):
           traceback.print_tb(sys.last_traceback)
         else:
           traceback.print_tb(sys.exc_traceback)
         logging.log(logging.ERROR,"error during index process of channel : %s at %d:00 : %s"%(channel,hour,str(e)))
  for channel in MvpAccess.stationnames[1:]:
    print channel
    for hour in range(10):
       try:
         vi.test(channel=channel,d=tdb+datetime.timedelta(0,hour*3600))
       except Exception,e:
         sys.stderr.write("error during index process of channel : %s at %d:00 : %s\n"%(channel,hour,str(e)))
         if (hasattr(sys,"last_traceback")):
           traceback.print_tb(sys.last_traceback)
         else:
           traceback.print_tb(sys.exc_traceback)
         logging.log(logging.ERROR,"error during index process of channel : %s at %d:00 : %s"%(channel,hour,str(e)))


#####################################################################################################################################
#####################################################################################################################################