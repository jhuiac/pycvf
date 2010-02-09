# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database Model
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback,logging
from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *


class VisionModel(object):
  def __init__(self,vdb=None):
      self.vdb=vdb
      self.mode=" "
                   
      
  def train(self,basepath,saveaftereachvideo=False,**kwargs):
      try:
          os.stat(basepath)
      except:
          os.mkdir(basepath)
      if (self.mode!="W"):
        self.observed_features=[]          
        self.init_observed_features_video()
        self.init_observed_features_statistics(basepath=basepath)
        self.mode="W"
      track=NullTrack(self.observed_features)
      for vr in self.vdb.all():
        try:
          self.videoreader=vr
          observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
          contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],self.observed_features),{})
          observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))       
          self.videoreader.set_observer(observer.iterproceed)
          self.videoreader.run()
          #self.observed_features=None
          observer.context=None
          observer=None
          self.videoreader=None
          if (saveaftereachvideo):
             self.savemodels()
             self.observed_features=None
             self.observed_features=[]          
             self.init_observed_features_video()
             self.init_observed_features_statistics(basepath=basepath)
             self.mode="W"
        except Exception,e:
          print "Exception during training"
          print str(e)
          if (hasattr(sys,"last_traceback")):
           traceback.print_tb(sys.last_traceback)
          else:
           traceback.print_tb(sys.exc_traceback)          
  def savemodels(self):
     pass       

  def test(self,basepath,trkfilename,vr, **kwargs):
     if (self.mode!="R"):
       self.observed_features=[]
       self.init_observed_features_video()
       self.init_observed_features_statistics(basepath=basepath,mlop="test",mlargs="")
       self.mode="R"
     track=OnDiskMultiTrackLargeZ(filename=trkfilename,meta=map(lambda x: x[2],self.observed_features))
     self.videoreader=vr
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],self.observed_features),{})
     observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))
     self.videoreader.set_observer(observer.iterproceed)
     self.videoreader.run()
     #self.observed_features=None
     observer.context=None
     observer=None
     self.videoreader=None


  def do_record2(self,x):
    import time
    import cPickle as pickle
    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
    from pycvf.lib.graphics.colortransforms import hsv2rgb
    NumPy2PIL(x.astype(numpy.uint8)).save("/tmp2/sampler-o-%s.png"%(str(time.time())))

  def do_record(self,x):
    import time
    import cPickle as pickle
    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
    from pycvf.lib.graphics.colortransforms import hsv2rgb
    pickle.dump(x,file("/tmp2/sampler-%s.pcl"%(str(time.time()),),"wb"),protocol=2)
    print "dr"
    xo=x[0].reshape(91,123,3).astype(numpy.uint8)
    #hr=hsv2rgb(xo).copy()
    NumPy2PIL(xo).save("/tmp2/sampler-%s.png"%(str(time.time())))
    xo[0]=0
    print "/dr"
    #print x.shape

  def msample(self,basepath,trkfilename,vr):
     if (self.mode!="R"):
       self.observed_features=[]
       self.init_observed_features_video()
       self.init_observed_features_statistics(basepath=basepath,mlop="samplev",mlargs="")
       self.mode="R"
       #track=OnDiskMultiTrackLargeZ(filename=trkfilename,meta=map(lambda x: x[2],self.observed_features))
       vs_patatrack=self.observed_features[-1][0]        
       #
       self.observed_features.append(
         ('thesrc[vs_patatrack][0]',{'vs_patatrack':vs_patatrack},{})
       )
       print "vs_patatrack",vs_patatrack
       self.observed_features.append(
           ('vs_record(thesrc[vs_patatrack])',  
              {
             'vs_record':self.do_record,
             'vs_patatrack':vs_patatrack,
             },
             {'title' : "segmentation"}  )
            )
       self.observed_features.append(
           ('src|vs_record2',  
              {
             'vs_record2':self.do_record2,
             },
             {'title' : "orig record"}  )
            )

     track=NullTrack(meta=map(lambda x: x[2],self.observed_features))
     #self.observed_features[-1]
     self.videoreader=vr
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],self.observed_features),{})
     observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))
     self.videoreader.set_observer(observer.iterproceed)
     self.videoreader.run()
     #self.observed_features=None
     observer.context=None
     observer=None
     self.videoreader=None
  

