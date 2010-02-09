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


import Image
import random
import os
import re
import scipy
import scipy.ndimage
#import cPickle as pickle

from pycvf.lib.info.gaussian import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.stats.models import *
from jfli.signal.blockops_opt import *

import scipy.ndimage
from pycvf.lib.graphics.rescale import *
from  pycvf.lib.graphics.genkanjis import *
pylab.ion()
pylab.gray()

def patch(ary,pos,sz):
    off=sum(map(lambda x,y,z:x*(y%z),ary.strides,pos,ary.shape))
    return numpy.ndarray(buffer=buffer(ary.data,off,len(ary.data)-off) ,shape=sz, strides=ary.strides, dtype=ary.dtype )

 
def to2d(x):
  x=numpy.array(x)
  xs1=scipy.prod(x.shape[1:])
  return x.reshape(x.shape[0],xs1)

def recomposef(base, cliquelist,log):
  s=base.shape
  cl=cliquelist.reshape(s[0]//2-1,s[1]//2-1)
  cl=Rescaler2d((s[0],s[1])).process(cl)
  if log:
    base+=cl
  else:
    base*=cl

#ef test1_anal_scale(scl):
  
#########################################################################################################################################
# Define our model
#########################################################################################################################################

class VideoIndexer(object):
  TS_SMALLVIDEO={ 'video1':(0, -1, {'videoframebanksz':1, 'dest_width':128, 'dest_height':96})} 
  def __init__(self,with_mvp=True):
     if (with_mvp):
       self.mvp=MvpAccess(with_ontology=False);
     #self.
  def init_observed_features_video(self):
     otime=time.time()
     #########################################################################################################################################
     # The model of the graph for the experiment
     #########################################################################################################################################
     self.observed_features=[
                    ('src|rgb2hsv|lum'  ,{'lum':lambda x:x[:,:,2] },  {}), # 0
                    ('wtp2()',{'wtp2':(lambda :sys.stderr.write("\r"+self.videoreader.get_current_address()[0]+((lambda t:"%d - %f - %f - %f"%( t,(1+t)/29.97,time.time()-otime, ((1+t)/29.97)/(time.time()-otime) ))(self.videoreader.get_current_address()[1]))))},{})
                  ]
  def init_observed_features_statistics(self,   mlop="train", mlargs="online=True"):
     shareddbbasepath="/home/tranx/videodatabase/db6-%s"%(self.channel,)
     specdbbasepath="/home/tranx/videodatabase/db6-%s/x-%02d-%02d-%02d"%(self.channel,self.d.year,self.d.month,self.d.day)
     try:
       os.mkdir(shareddbbasepath)
     except :
       pass
     try:
       os.mkdir(specdbbasepath)
     except :
       pass                  
     states=numpy.arange(0,256,16).reshape(16,1)
     bil1=CachedModel( InterpolatedStateConditionalModelSv,                                                                                           
                      lambda project_prior, project_evidence, individual_model_factory, individual_model_class, SearchStructure,k:
                              InterpolatedStateConditionalModelSv(
                                                            states,
                                                            k=k,
                                                            SearchStructure=SearchStructure,
                                                            project_prior=project_prior,
                                                            project_evidence=project_evidence,
                                                            individual_model_factory=individual_model_factory,
                                                            individual_model_class=individual_model_class
                                                        ),
                      shareddbbasepath+ "/isb_like_0001.mdl",
                      suppkwargs=dict(      k=3,
                                            SearchStructure=KDTree,
                                            project_prior=None ,
                                            project_evidence=None,
                                            individual_model_factory=( 
                                                                        lambda x: SimpleMeanVarianceModel()
                                                                     ),
                                            individual_model_class=(
                                                                        lambda x: SimpleMeanVarianceModel
                                                                    )
                      )
                    )
     
     mdl1=CachedModel(HistogramModel,
                      lambda:HistogramModel((3,)*(4**2),(0,)*(4**2),(256,)*(4**2) ),
                      shareddbbasepath+ "/mdl1_0001.mdl"
                      )
     mmkov=MarkovModel(
         [
                MarkovModel.CliquesSet(
                    #lambda b:to2d(all_blocks2d1d_i(b.astype(int),4,4,2,2)),
                    lambda b:to2d(sample_blocks2d1d_u8(b,4,4,2,2)),
                    mdl1,
                    recomposef=recomposef
                 )
         ]
         ) 
  
    #m.train(k,online=True)
    #mdl1.dump(file("static_anal5_44_%s.pcl"%(str(scl)),"wb"))

    # bm1=MarkovModel(
    #                 cliques_sets=
    #                   [
    #                     (  horizontal_edge_extractor, 
    #                        BayesianModel(
    #                                project_prior=lambda x:x[:,-1],
    #                                project_evidence=lambda x:x[:,:-1],
    #                                likeliness_model=bil1,
    #                                prior_model=bip1,
    #                                evidence_model=bie1
    #                        )  
    #                     )
    #                   ]
    #                )
     ######################################################################################################################################
     # operator
     ######################################################################################################################################     
     self.observed_features+=[
                    #
                    (self.observed_features[0][0]+"|mmkov."+mlop+"("+mlargs+")",{'mmkov':mmkov  }, 
                                                                                {'title':'graylevel likelihood'})
                    #
                   ]      


                  
                   
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
       trkfilename="/tmp2/video_test-idx6-%04d-%02d-%02d-%02d-%s.trk"%(d.year,d.month,d.day,d.hour,channel)
     else:
       channel=kwargs["channel"]
       d=datetime.datetime(2009,1,1,0,0,0)
       filename=kwargs["filename"]
       self.channel=channel
       self.d=d
       self.videoreader=SimpleVideoReader7(filename,track_selector=VideoIndexer.TS_SMALLVIDEO)
       startfrom=None
       trkfilename="/tmp2/video_test-idx6-%s-%s.trk"%(filename.split("/")[-1],channel)
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