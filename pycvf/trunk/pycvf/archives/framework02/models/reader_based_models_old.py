# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Abstract Model
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved Bertrand Nouvel
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback,logging
from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *

ltick=0


from genericmodel import GenericModel


# all object can be read trhough time and indexed through time axis..
# somehow these object tend to be like discrete time dynamical systems
#

class TemporalModel(object):
  def __init__(self):
         pass
  def do_process(self,observer):
         pass
  def train(self,vdb,basepath,saveaftereachsequence=False,**kwargs):
      try:
          os.stat(basepath)
      except:
          os.mkdir(basepath)
      if (self.mode!="W"):
        self.observed_features=[]          
        self.init_features()
        self.init_models(basepath=basepath)
        self.connect_models(basepath=basepath)
        self.mode="W"
      track=NullTrack(self.observed_features)
      for vr in vdb.all():
        try:
          self.xreader=vr
          observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
          self.do_process(observer)
          self.xreader=None
          if (saveaftereachsequence):
             self.savemodels()
             self.observed_features=None
             self.observed_features=[]          
             self.init_features()
             self.init_models(basepath=basepath)
             self.connect_models(basepath=basepath)
             self.mode="W"
        except Exception,e:
          print "Exception during training"
          print str(e)
          if (hasattr(sys,"last_traceback")):
           traceback.print_tb(sys.last_traceback)
          else:
           traceback.print_tb(sys.exc_traceback)          

  def test(self,basepath,trkfilename,vr, **kwargs):
     if (self.mode!="R"):
       self.observed_features=[]
       self.init_features()
       self.init_models(basepath=basepath,mlop="test",mlargs="")
       self.connect_models(basepath=basepath,mlop="test",mlargs="")
       self.mode="R"
     track=OnDiskMultiTrackLargeZ(filename=trkfilename,meta=map(lambda x: x[2],self.observed_features))
     self.xreader=vr
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     self.do_process(observer)
     self.xreader=None

  def sample(self,basepath,trkfilename, nsamples=1, **kwargs):
     """
         Generate samples according to the model and save them in appropriate files
         If the model is conditional, then the sample a hypothes provider has to be   
         provided.
     """
     if (self.mode!="RS"):
       self.observed_features=[]
       self.init_features()
       self.init_models(basepath=basepath,mlop="sample",mlargs=str(nsamples))
       self.mode="RS"
     track=OnDiskMultiTrackLargeZ(filename=trkfilename,meta=map(lambda x: x[2],self.observed_features))
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     #self.do_process(observer)
     print "sampling over ", self.models
     for m in self.models:
        rs=m.sample(nsamples)
        print rs
        import pylab
        for i in range(len(rs)):
            pylab.clf()
            pylab.gray()
            pylab.imshow(rs[i])
            pylab.savefig("/tmp/outgen"+str(i)+".png")

  def process(self,basepath,vr,external_processor_f):
     """
       Apply external processing function with the help of the model and save the
       result.
     """
     if (self.mode!="R"):
       self.observed_features=[]
       self.init_features()
       self.init_observed_features_statistics(basepath=basepath,mlop="external_process",mlargs="external_processor_f")
       self.mode="R"
     self.xreader=vr
     self.add_ctx['external_processor_f']=external_processor_f
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     self.do_process(observer)
     self.xreader=None

  def prepare_build_index(self,basepath):
      try:
          os.stat(basepath)
      except:
          os.mkdir(basepath)
      if (self.mode!="I"):
        self.observed_features=[]          
        self.init_features()
        self.init_indexes(basepath=basepath,idxop="add")
        self.mode="I"

  def init_indexes(*xars,**xxargs):
     pass

  def build_index(self,vdb,basepath,idx,saveaftereachsequence=False):
      assert(self.mode=="I")
      for vr in vdb.all():
        try:
          self.xreader=vr
          track=NullTrack(self.observed_features)
          observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
          self.do_process(observer)
          observer=None
          self.xreader=None
          if (saveaftereachsequence):
             self.saveindexes()
             self.observed_features=None
             self.observed_features=[]          
             self.init_features()
             self.init_observed_features_statistics(basepath=basepath)
             self.mode="I"
        except Exception,e:
          print "Exception during indexing"
          print str(e)
          if (hasattr(sys,"last_traceback")):
           traceback.print_tb(sys.last_traceback)
          else:
           traceback.print_tb(sys.exc_traceback)          
      self.saveindexes()

  def cbir_query(self,vdb,basepath,idx):
      """
       Here ones do query an index for a specific model...
      """
      assert(self.mode=="I")
      for vr in vdb.all():
        try:
          self.xreader=vr
          track=NullTrack(self.observed_features)
          observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
          self.do_process(observer)
          self.xreader=None
          if (saveaftereachsequence):
             self.saveindexes()
             self.observed_features=None
             self.observed_features=[]          
             self.init_features()
             self.init_models(basepath=basepath)
             self.connect_models(basepath=basepath)
             self.mode="I"
        except Exception,e:
          print "Exception during content based query"
          print str(e)
          if (hasattr(sys,"last_traceback")):
           traceback.print_tb(sys.last_traceback)
          else:
           traceback.print_tb(sys.exc_traceback)          


  ##############
  # To be cleaned a littled bit ...
  ##############
#
#  def do_record2(self,x):
#    import time
#    import cPickle as pickle
#    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
#    from pycvf.lib.graphics.colortransforms import hsv2rgb
#    NumPy2PIL(x.astype(numpy.uint8)).save("/tmp2/sampler-o-%s.png"%(str(time.time())))

#  def do_record(self,x):
#    import time
#    import cPickle as pickle
#    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
#    from pycvf.lib.graphics.colortransforms import hsv2rgb
#    pickle.dump(x,file("/tmp2/sampler-%s.pcl"%(str(time.time()),),"wb"),protocol=2)
#    print "dr"
#    xo=x[0].reshape(91,123,3).astype(numpy.uint8)
#    #hr=hsv2rgb(xo).copy()
#    NumPy2PIL(xo).save("/tmp2/sampler-%s.png"%(str(time.time())))
#    xo[0]=0
#    print "/dr"
#    #print x.shape

  def msample(self,basepath,trkfilename,vr):
     """
       This function returns conditional samples according to T-1 in 
       a temporal model.
     """
     if (self.mode!="R"):
       self.observed_features=[]
       self.init_features()
       self.init_models(basepath=basepath,mlop="samplev",mlargs="")
       self.connect_models(basepath=basepath,mlop="samplev",mlargs="")
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
     self.xreader=vr
     observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
     contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],self.observed_features),{})
     contextadd=dict(contextadd.keys()+self.add_ctx.keys(),contextadd.values()+self.add_ctx.values())
     observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))
     self.xreader.set_observer(observer.iterproceed)
     self.xreader.run()
     observer.context=None
     observer=None
     self.xreader=None
  