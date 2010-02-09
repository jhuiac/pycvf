#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


################################################################################################################################################################################
# Includes
################################################################################################################################################################################

import re, os, math, random, time,sys, traceback, time, logging
import scipy,pylab,scipy.ndimage
from scipy.spatial.kdtree import KDTree

from jfli.project_specific.mvp.mvpaccess import *

from pycvf.lib.info.observations import *
from pycvf.lib.info.gaussian import *
from pycvf.lib.info.track import *

from pycvf.lib.video.lazydisplayqt import *
from pycvf.lib.video.simplevideoreader7 import *

from pycvf.lib.graphics.zopencv import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.graphics import features
from pycvf.lib.graphics.rescale import *
from pycvf.lib.graphics.genkanjis import *


from jfli.signal.blockops_opt import *
from pycvf.lib.stats.models import *

################################################################################################################################################################################
# Library
################################################################################################################################################################################


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


class VideoMemory:
    def __init__(self,img0,n=2):
        self.bufs=[img0]*n
    def process(self,img):
        self.bufs.pop(0)
        self.bufs.append(img0)
        return self.bufs

class MarkovObservationMaker:
   def __init__(self):
        self.w=self.h=16
        self.xs=self.w//2
        self.ys=self.h//2
   def blkred1(self,blk):
       h=blk[:,:,0]
       s=blk[:,:,1]
       v=blk[:,:,2]
       dv=pywt.wavedec2(v,"db2")
       return [x for x in dv[0].flat] + [ s.mean(),s.std(), h.mean, h.std() ]
   def obs_at(imgm,px,py):
       o0=self.blkred1(o[0][py:py+self.h,px:px+self.w])
       o1=o[1][py+self.ys,px+self.xs]
       return (o0,o1)
   def sample_observations(imgm,numsamples):
    shape=imgm[0]
    ishape=(shape[0]-self.h+1,shape[1]-self.h+1)
    r=[]
    for i in numsamples():
        py=random.randint(ishape[0])
        px=random.randint(ishape[1])
        r.append(self.obs_at(imgm,self.px,self.py))
    return r


################################################################################################################################################################################
# Model
################################################################################################################################################################################


import visionmodel

class VisionModel(visionmodel.VisionModel):
  def init_observed_features_video(self):
     self.observed_features=[
                    ('src|rgb2hsv|vm'  ,{'lum':lambda x:x[:,:,2], 'vm': VideoMemory },  {}), # 0
                    ('wtp2()',{'wtp2':(lambda :sys.stderr.write("\r"+self.videoreader.get_current_address()[0]+((lambda t:"%d - %f - %f - %f"%( t,(1+t)/29.97,time.time()-otime, ((1+t)/29.97)/(time.time()-otime) ))(self.videoreader.get_current_address()[1]))))},{})
                  ]
  def init_observed_features_statistics(self, basepath,   mlop="train", mlargs="online=True"):
     states=numpy.arange(0,256,16).reshape(16,1)
     mom=MarkovObservationMaker()
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
                      basepath+ "/isb_like_0001.mdl",
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
     
     #mdl1=CachedModel(HistogramModel,
     #                 lambda:HistogramModel((3,)*(4**2),(0,)*(4**2),(256,)*(4**2) ),
     #                 shareddbbasepath+ "/mdl1_0001.mdl"
     #                
     # )
     mdl1=CachedModel(
               InterpolatedStateConditionalModelSv,
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
                      basepath+ "/condtnal_output_0001.mdl",
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
     
     
     mdl_pixels=UniformModel((256,256,256))
     
     
     
     mdl_patterns=UniformModel((256)**16)
     
     
     
     mdlb=BayesianModel(
                                                                                                    project_prior=lambda o:o[1],
                                                                                                    project_evidence=lambda o:o[0],
                                                                                                    likeliness_model=mdl1,
                                                                                                    prior_model=mdl_pixels,
                                                                                                    evidence_model=mdl_patterns 
                                                                                                    )
     mmkov=MarkovModel(
         [
                MarkovModel.CliquesSet(
                    #lambda b:to2d(all_blocks2d1d_i(b.astype(int),4,4,2,2)),
                    mom.process,
                    mdlb,
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
