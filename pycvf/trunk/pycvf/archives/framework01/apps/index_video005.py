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
                    ('src.mean()|numpy.matrix'  ,{ },  {'title':'meangray','color':(1,0,0)}),  #0 
                    ('src|rgb2hsv|h_topleft()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_topleft':lambda x:x[:(x.shape[0]//2),:(x.shape[1]//2),0]},{}), # 1
                    ('src|rgb2hsv|h_topright()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_topright':lambda x:x[:(x.shape[0]//2),(x.shape[1]//2):,0]},{}), # 2
                    ('src|rgb2hsv|h_bottomleft()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_bottomleft':lambda x:x[:(x.shape[0]//2):,:(x.shape[1]//2),0]},{}), # 3
                    ('src|rgb2hsv|h_bottomright()|numpy.histogram(bins=4, range=(0,256),normed=True)[0].reshape(1,4)',{'h_bottomright':lambda x:x[(x.shape[0]//2):,(x.shape[1]//2):,0]},{}), # 4
                    ('src|rgb2hsv|lum|xmean|numpy.matrix'  ,{'lum':lambda x:x[:,:,2] },  {}), # 5
                    ('src|rgb2hsv|lum|entropy'  ,{'entropy':lambda x:scipy.stats.entropy(x.reshape(scipy.prod(x.shape))) },  {}), # 6
                    ('src|rgb2hsv|lum|centerofmass'  ,{ 'centerofmass':scipy.ndimage.center_of_mass },  {}), # 7
                    ('src|rgb2hsv|lum|invert|centerofmass'  ,{ 'invert': lambda x: 255-x },  {}), # 8 
                    ('src|rgb2hsv|lum|gl_edges|energy'  ,{ 'gl_edges':(lambda img: scipy.ndimage.gaussian_laplace(img,2)), 'energy': numpy.linalg.norm},  {}), # 9 
                    ('src|rgb2hsv|lum|gl_edges|fft|numpy.abs|energy'  ,{'fft':scipy.fft },  {}), # 10
                    ('src|rgb2hsv|lum|gl_edges|distancetransform|numpy.abs().mean()',{'distancetransform':scipy.ndimage.distance_transform_edt},  {}), # 11
                    ('src|rgb2hsv|lum|gl_edges|distancetransform|gradient|aangle|numpy.histogram(bins=4, range=(0,256),normed=True)',
                                                                                          {'gradient': lambda x:scipy.gradient(x), 
                                                                                           'aangle':lambda x: scipy.angle(x[0]+1J*x[1])},  {}),#12
                    ('src|rgb2hsv|lum|gl_edges|lbp'  ,{ 'lbp': features.lbp },  {}),#13
                    ('src|rgb2hsv|lum|gl_edges|per_block|numpy.array()|numpy.linalg.norm'  ,{ 'per_block':(lambda x: all_sqblocks2d1d_f(x.astype(numpy.float64),3)) },  {}),#14
                    ('src|rgb2hsv|lum|fft'  ,{'fft':scipy.fft },  {}), # 15
                    ('src|rgb2hsv|lum|fft|numpy.abs|onedim'  ,{ 'onedim': (lambda x: x.reshape((1,scipy.prod(x.shape))) )},  {}), # 16
                    ('src|rgb2hsv|lum|fft|numpy.abs|xmean|numpy.matrix'  ,{'xmean':(lambda x:x.mean()) },  {}), # 17
                    ('wtp17()',{'wtp17':(lambda :sys.stderr.write("\r"+self.videoreader.get_current_address()[0]+((lambda t:"%d - %f - %f - %f"%( t,(1+t)/29.97,time.time()-otime, ((1+t)/29.97)/(time.time()-otime) ))(self.videoreader.get_current_address()[1]))))},{})
                  ]
  def init_observed_features_statistics(self,   mlop="train", mlargs="online=True"):
     shareddbbasepath="/home/tranx/videodatabase/db2-%s"%(self.channel,)
     specdbbasepath="/home/tranx/videodatabase/db2-%s/x-%02d-%02d-%02d"%(self.channel,self.d.year,self.d.month,self.d.day)
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
     bip1=CachedModel(
                        HistogramModel,
                        lambda:HistogramModel( bins=(256,), base=(0,), delta=(256,)),
                        shareddbbasepath+ "/isb_prior_0001.mdl"
                     )
     bie1=CachedModel(
                      SimpleMeanVarianceModel,
                      lambda:SimpleMeanVarianceModel(), 
                      shareddbbasepath+ "/isb_evidence_0001.mdl"
                     )
                     
     ######################################################################################################################################
     # operator
     ######################################################################################################################################     
     self.observed_features+=[
                    #
                    (self.observed_features[0][0]+"|HistoModel0."+mlop+"("+mlargs+")",{'HistoModel0':CachedModel(HistogramModel,lambda:HistogramModel( bins=(256,),base=(0,),delta=(256)), 
                                                                                                          shareddbbasepath+ "/graylevels.mdl" )   }, 
                                                                                                          {'title':'graylevel likelihood'}),
                    (self.observed_features[1][0]+"|HistoModel1."+mlop+"("+mlargs+")",{'HistoModel1':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), 
                                                                                                          shareddbbasepath+ "/hue_tl_histogram4.mdl" )  }, 
                                                                                                          {'title':'color distributioln topleft'}),
                    (self.observed_features[2][0]+"|HistoModel2."+mlop+"("+mlargs+")",{'HistoModel2':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), 
                                                                                                          shareddbbasepath+ "/hue_tr_histogram4.mdl" )  }, 
                                                                                                          {'title':'color distributioln topright'}),
                    (self.observed_features[3][0]+"|HistoModel3."+mlop+"("+mlargs+")",{'HistoModel3':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), 
                                                                                                          shareddbbasepath+ "/hue_bl_histogram4.mdl" )   }, 
                                                                                                          {'title':'color distributioln bottom-left'}),                                                                                                          
                    (self.observed_features[4][0]+"|HistoModel4."+mlop+"("+mlargs+")",{'HistoModel4':CachedModel(HistogramModel,lambda:HistogramModel( bins=(4,4,4,4),base=(0,0,0,0),delta=(256,256,256,256)), 
                                                                                                          shareddbbasepath+ "/hue_br_histogram4.mdl" )   }, {}),
                    (self.observed_features[17][0]+"|BayesianModel5."+mlop+"_separated(thesrc[edge_source]"+(mlargs and (','+mlargs) or "")+")",{
                                                                           'BayesianModel5':
                                                                             BayesianModel(
                                                                                 project_prior=None,
                                                                                 project_evidence=None,
                                                                                 likeliness_model=bil1,
                                                                                 prior_model=bip1,
                                                                                 evidence_model=bie1
                                                                               ),
                                                                            'edge_source':self.observed_features[16][0]
                                                                              }, 
                                                                              {}
                                                                              )
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
       trkfilename="/tmp2/video_test--%04d-%02d-%02d-%02d-%s.trk"%(d.year,d.month,d.day,d.hour,channel)
     else:
       channel=kwargs["channel"]
       d=datetime.datetime(2009,1,1,0,0,0)
       filename=kwargs["filename"]
       self.channel=channel
       self.d=d
       self.videoreader=SimpleVideoReader7(filename,track_selector=VideoIndexer.TS_SMALLVIDEO)
       startfrom=None
       trkfilename="/tmp2/video_test--%s-%s.trk"%(filename.split("/")[-1],channel)
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