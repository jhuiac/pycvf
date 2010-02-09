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

from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *

from pycvf.lib.video.lazydisplayqt import *
from pycvf.lib.video.simplevideoreader7 import *

from pycvf.lib.graphics.zopencv import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.graphics import features
from pycvf.lib.graphics.rescale import *


from jfli.signal.blockops_opt import *
from pycvf.lib.stats.models import *

################################################################################################################################################################################
# Library
################################################################################################################################################################################

def recomposef(base, cliquelist,log):
  s=base.shape
  cl=cliquelist.reshape(s[0],s[1])
  if log:
    base+=cl
  else:
    base*=cl

 
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
                    ('src'  ,{},  {}), # 0
                  ]
  def init_observed_features_statistics(self, basepath,   mlop="train", mlargs="online=True"):   
     mdl1=CachedModel(HistogramModel,
                      lambda:HistogramModel((64,)*(3),(0,)*(3),(256,)*(3) ),
                      basepath+ "/colormodel.mdl"
                      )
     mmkov=MarkovModel(
         [
                MarkovModel.CliquesSet(
                    lambda x:x.reshape(x.shape[0]*x.shape[1],3),
                    mdl1,
                    recomposef0=recomposef,
                    recomposef1=recomposef
                 )
         ]
         ) 
     ######################################################################################################################################
     # operator
     ######################################################################################################################################     
     self.observed_features+=[
                    #
                    (self.observed_features[0][0]+"|mmkov."+mlop+"("+mlargs+")",{'mmkov':mmkov  }, 
                                                                                {'title':'graylevel likelihood'})
                    #
                   ]      
                  
#####################################################################################################################################