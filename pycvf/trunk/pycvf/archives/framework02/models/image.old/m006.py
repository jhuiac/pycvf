# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
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

#ef test1_anal_scale(scl):
  
#########################################################################################################################################
# Define our model
#########################################################################################################################################


from pycvf.nodes import visionmodel_with_segmentation as mymodel

class MyModel(visionmodel.MyModel):
  def init_features(self):
     otime=time.time()
     #########################################################################################################################################
     # The model of the graph for the experiment
     #########################################################################################################################################
     self.observed_features=[
                    ('src|rgb2hsv|lum'  ,{'lum':lambda x:x[:,:,2] },  {}), # 0
                    #('wtp2()',{'wtp2':(lambda :sys.stderr.write("\r"+self.videoreader.get_current_address()[0]+((lambda t:"%d - %f - %f - %f"%( t,(1+t)/29.97,time.time()-otime, ((1+t)/29.97)/(time.time()-otime) ))(self.videoreader.get_current_address()[1]))))},{})
                  ]
  def init_models(self, basepath,   mlop="train", mlargs="online=True"):   
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
     
     mdl1=CachedModel(HistogramModel,
                      lambda:HistogramModel((3,)*(4**2),(0,)*(4**2),(256,)*(4**2) ),
                      basepath+ "/mdl1_0001.mdl"
                      )
     mmkov=MarkovModel(
         [
                MarkovModel.CliquesSet(
                    (mlop=="train" ) and (lambda b:to2d(sample_blocks2d1d_u8(b,4,4,2,2))) or (lambda b:to2d(all_blocks2d1d_i(b.astype(int),4,4,2,2))),
                    mdl1,
                    recomposef=recomposef
                 )
         ]
         ) 
     ######################################################################################################################################
     # operator
     ######################################################################################################################################     
  def connect_models(self, basepath,   mlop="train", mlargs="online=True"):   
     self.observed_features+=[
                    #
                    (self.observed_features[0][0]+"|mmkov."+mlop+"("+mlargs+")",{'mmkov':self.mmkov  }, 
                                                                                {'title':'graylevel likelihood'})
                    #
                   ]      
    

                  
#####################################################################################################################################