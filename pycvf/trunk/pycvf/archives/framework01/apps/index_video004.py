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

import re, os, math, random, time,sys
import scipy,pylab

from jfli.project_specific.mvp import mvpaccess

from pycvf.lib.video.lazydisplayqt import *
from pycvf.lib.video.simplevideoreader7 import *

from pycvf.lib.graphics.zopencv import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *

from pycvf.indexes.bssdbindex import *
from pycvf.indexes.indexbuilders import *
from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *

from pycvf.lib.stats.models import *

import os


class VideoIndexer:
  TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})} 
  def __init__(self):
     self.mvp=mvpaccess.MvpAccess(with_ontology=False);
     #self.
  def process(self,channel,d):
     filename=self.mvp.find_video(channel=channel,year=d.year,month=d.month,day=d.day,hour=d.hour)
     videoreader=SimpleVideoReader7(filename,track_selector=VideoIndexer.TS_SMALLVIDEO)
     shareddbbasepath="/home/tranx/videodatabase/db1"
     specdbbasepath="/home/tranx/videodatabase/db1/x-%02d-%02d-%02d"%(d.year,d.month,d.day)
     try:
       os.mkdir(specdbbasepath)
     except :
       pass
     db1idx=MultidimensionalDb(specdbbasepath+"/db1","db1",17)
     #########################################################################################################################################
     # The model of the graph for the experiment
     #########################################################################################################################################
     observed_features=[
                    ('src.mean()|numpy.matrix'  ,{ },  {'title':'meangray','color':(1,0,0)}),
                    ('src|rgb2hsv|h_topleft()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_topleft':lambda x:x[:(x.shape[0]//2),:(x.shape[1]//2),0]},{}),
                    ('src|rgb2hsv|h_topright()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_topright':lambda x:x[:(x.shape[0]//2),(x.shape[1]//2):,0]},{}),
                    ('src|rgb2hsv|h_bottomleft()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_bottomleft':lambda x:x[:(x.shape[0]//2):,:(x.shape[1]//2),0]},{}),
                    ('src|rgb2hsv|h_bottomright()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_bottomright':lambda x:x[(x.shape[0]//2):,(x.shape[1]//2):,0]},{}),
                  ]
     observed_features+=[
                    #
                    (observed_features[0][0]+"|HistoModel0.online_train",{'HistoModel0':CachedModel(HistogramModel,lambda:HistogramModel( bins=(256,),base=(0,),delta=(256)), shareddbbasepath+ "model0.mdl" )   }, {}),
                    (observed_features[1][0]+"|HistoModel1.online_train",{'HistoModel1':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), shareddbbasepath+ "model1.mdl" )  }, {}),
                    (observed_features[2][0]+"|HistoModel2.online_train",{'HistoModel2':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), shareddbbasepath+ "model2.mdl" )  }, {}),
                    (observed_features[3][0]+"|HistoModel3.online_train",{'HistoModel3':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), shareddbbasepath+ "model3.mdl" )   }, {}),
                    (observed_features[4][0]+"|HistoModel4.online_train",{'HistoModel4':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), shareddbbasepath+ "model4.mdl" )   }, {}),
                    #
                    ('indexerdb1.f([ x for x in thesrc[feature0].flat]+ [x for x in thesrc[feature1].flat] + [x for x in thesrc[feature2].flat]+[x for x in thesrc[feature3].flat]+[x for x in thesrc[feature4].flat])', {
                                                         'feature0':observed_features[0][0],
                                                         'feature1':observed_features[1][0],
                                                         'feature2':observed_features[2][0],
                                                         'feature3':observed_features[3][0],
                                                         'feature4':observed_features[4][0],
                                                         'indexerdb1':IndexBuilder(db1idx, videoreader.get_current_address ,False)
                                                        }, {}),
                    #
                   ]
     track=NullTrack(observed_features)
     #########################################################################################################################################
     # Link with all the required
     #########################################################################################################################################
     observer=MultipleObserver(map(lambda x:x[0],observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],observed_features),{})
     observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))
     videoreader.set_observer(observer.proceed)
     #########################################################################################################################################
     # Run
     #########################################################################################################################################
     videoreader.run()


if __name__=="__main__":
  import datetime
  vi=VideoIndexer()
  vi.process("tbs",datetime.datetime.today()-datetime.timedelta(2,0,0))