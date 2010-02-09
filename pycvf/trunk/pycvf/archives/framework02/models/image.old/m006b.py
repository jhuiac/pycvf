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


def to2d(x):
  #ea=[e.copy('C') for e in x]
  print "2d"
  x=numpy.array(x)
  xs1=scipy.prod(x.shape[1:])
  r=x.reshape(x.shape[0],xs1)
  print "rshape",r.shape
  return r

#class Recomposer(object):
#  def __init__(self,shape):
#     self.shape=shape
#  def recomposef0(self,cliquelist,log):
#    s=self.shape
#    print cliquelist.shape , s
#    assert(cliquelist.shape[0]==(s[0]*s[1]))
#    return cliquelist.reshape(s[0],s[1])

def recomposef0(ps):
  def _recomposef0(cliquelistres,s,log):
     # to geometric cliquesets
     return cliquelistres.reshape(s[0]-ps[0],s[1]-ps[1])
  return _recomposef0
def recomposef1(ps):
  def _recomposef1(base, cliquelist,log):
    # to variables
    s=base.shape
    print s
    print cliquelist.shape
    cl=cliquelist.reshape(s[0]-ps[0],s[1]-ps[1])
    cl=Rescaler2d((s[0],s[1])).process(cl)
    if log:
      base+=cl
    else:
      base*=cl
  return _recomposef1
#########################################################################################################################################
# Define our model
#########################################################################################################################################


from pycvf.nodes import visionmodel_with_segmentation as mymodel

class MyModel(visionmodel.MyModel):
  def init_features(self):
     otime=time.time()
     self.observed_features=[
                    ('src|rgb2hsv|lum'  ,{'lum':lambda x:x[:,:,2] },  {}), # 0
                    #('wtp2()',{'wtp2':(lambda :sys.stderr.write("\r"+self.videoreader.get_current_address()[0]+((lambda t:"%d - %f - %f - %f"%( t,(1+t)/29.97,time.time()-otime, ((1+t)/29.97)/(time.time()-otime) ))(self.videoreader.get_current_address()[1]))))},{})
                  ]

  

  def init_models(self, basepath,   mlop="train", mlargs="online=True"):       
     self.mdl1_pat=CachedModel(HistogramModel,
                      lambda:HistogramModel((3,)*(3*3),(0,)*(3*3),(256,)*(3*3) ),
                      basepath+ "/mdl1_pat.mdl"
                      )
     self.mdl1_eh=CachedModel(HistogramModel,
                      lambda:HistogramModel((3,)*(4*3),(0,)*(4*3),(256,)*(4*3) ),
                      basepath+ "/mdl1_eh_0001.mdl"
                      )
     self.mdl1_ev=CachedModel(HistogramModel,
                      lambda:HistogramModel((3,)*(4*3),(0,)*(4*3),(256,)*(4*3) ),
                      basepath+ "/mdl1_ev_0001.mdl"
                      )
     #self.rc0=Recomposer((47,63))
     #self.rc1=Recomposer((47,63))
     #self.rc2=Recomposer((47,63))
     #self.rc0=Recomposer((94,126))
     #self.rc1=Recomposer((94,125))
     #self.rc2=Recomposer((93,126))

     mmkov=MarkovModel(
         [
                MarkovModel.CliquesSet(
                    (mlop=='train')
                      and (lambda b:to2d(sample_blocks2d1d_u8(b,3,3,1,1,1000)))
                      or (lambda b:to2d(all_blocks2d1d_i(b.astype(int),3,3,1,1))),
                    self.mdl1_pat,
                    #recomposef0=lambda x,l:self.rc0.recomposef0(x,l),
                    recomposef0=recomposef0((2,2)),
                    recomposef1=recomposef1((2,2))
                 ),         
                MarkovModel.CliquesSet(
                    (mlop=='train')
                      and (lambda b:to2d(sample_blocks2d1d_u8(b,3,4,1,1,1000)))
                      or (lambda b:to2d(all_blocks2d1d_i(b.astype(int),3,4,1,1))),
                    self.mdl1_eh,
#                    recomposef0=lambda x,l:self.rc1.recomposef0(x,l),
                    recomposef0=recomposef0((2,3)),
                    recomposef1=recomposef1((2,3)),
                 ),
                MarkovModel.CliquesSet(
                    (mlop=='train')
                        and (lambda b:to2d(sample_blocks2d1d_u8(b,4,3,1,1,1000)))
                        or (lambda b:to2d(all_blocks2d1d_i(b.astype(int),4,3,1,1))),
                    self.mdl1_ev,
#                    recomposef0=lambda x,l:self.rc2.recomposef0(x,l),
                    recomposef0=recomposef0((3,2)),
                    recomposef1=recomposef1((3,2))
                 )

         ]
         ) 
     self.models=[mmkov]
 


  def connect_models(self,basepath,   mlop="train", mlargs="online=True"):
     self.observed_features+=[
                    #
                    (self.observed_features[0][0]+"|mmkov."+mlop+"("+mlargs+")",{'mmkov':self.mmkov  }, 
                                                                                {'title':'pattern based likeliness'})
                    #
                   ]      
  def savemodels(self):
     self.mdl1_pat.save()
     self.mdl1_eh.save()
     self.mdl1_ev.save()
     
                  
#####################################################################################################################################
