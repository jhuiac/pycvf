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


# -*- coding: utf-8 -*-
"""
A simplification of model 9

"""


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

from jfli.dimred import PCA

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
    def __init__(self,img0,lb=2):
        self.bufs=[img0,]*lb
    def process(self,img):
        #print "bufs",self.bufs
        self.bufs.pop(0)
        self.bufs.append(img)
        return self.bufs


class MarkovObservationMaker:
   def __init__(self):
        self.w=self.h=5
        self.xs=self.w//2
        self.ys=self.h//2
   def blkred1(self,blk):
       h=blk[:,:,0]
       s=blk[:,:,1]
       v=blk[:,:,2]
       dv=pywt.wavedec2(v,"db2")
       return [x for x in dv[0].flat] + [ s.mean(),s.std(), h.mean, h.std() ]
   def obs_at(self,imgm,px,py):
       #o0=self.blkred1(o[0][py:py+self.h,px:px+self.w])
       #print py,px
       #print imgm[0].shape, imgm[1].shape
       o0=imgm[0][py:(py+self.h),px:(px+self.w)].reshape(self.h*self.w*3)
       o1=imgm[1][py+self.ys,px+self.xs].reshape(3)
       return (o0,o1)
   def sample_observations(self,imgm,numsamples=1000):
     shape=imgm[0].shape
     ishape=(shape[0]-self.h,shape[1]-self.w)
     r=[]
     for i in range(numsamples):
        py=random.randint(0,ishape[0])
        px=random.randint(0,ishape[1])
        r.append(self.obs_at(imgm,px,py))
     r=numpy.array(r,dtype=object)
     #print r.shape
     #print "r",r,"/r",r.shape
     return r
   def all_observations(self,imgm):
     shape=imgm[0].shape
     ishape=(shape[0]-self.h,shape[1]-self.w)
     r=[]
     for py in range(0,ishape[0]):
       for px in range(0,ishape[1]):
         r.append(self.obs_at(imgm,px,py))
     r=numpy.array(r,dtype=object)
     return r
   def process(self,imgm,exhaustive=False,*args,**kwargs):
       if exhaustive:
          return self.all_observations(imgm)
       else:
          return self.sample_observations(imgm,*args,**kwargs)



################################################################################################################################################################################
# Model
################################################################################################################################################################################


"""

The block-model is has 3 important parts according to bayesian formalism...
     from a block model on one side
################################################################################################################################################################################
   A) The model for the blocks is a bagged model

   B) The model for the individual observations of the pixels on the other side
            
   C) The linking model which is just a 
        BaggedModel of 
           Interpolated Conditional Model Based
             Avoiding thus to have a too large oversampling of the space
             Each submodels is simply seen as a SimpleMeanVarianceNode
         Thanks to bayesian inversion the sampling is on the output color space (and is thus a not too large space)

   Finally, everything is linked by a markovian model...
"""


#################################################################################################################################################################################

from pycvf.nodes import visionmodel


     #def md1_project(block):
     #   return angle(sum(numpy.exp(block[:,:,0].astype(float)*1J*numpy.pi/128.)))
     #def md1_releve,(color,block):
     #   cangle=angle(sum(numpy.exp(block[:,:,0].astype(float)*1J*numpy.pi/128.)))
     #   return block[:,:,0].mean(axis=0).mean(axis=1)


def pattern_model(vm,basepath,name, blksz, precision):
     ##
     ## Create a pattern model with the given '''precision''' (expected to be 2,3 or maybe 4)
     ## 
     blkszp=scipy.prod(blksz)
     #############################################################################################################
     # color 
     #############################################################################################################
     def md1_project(block):
        return block.reshape(block.shape[0],blkszp,3).mean(axis=1)
     def md1_releve(color,block=None):
        print "md1r"
        if (block==None):
           block=numpy.zeros((color.shape[0],blkszp*3))
        cmean=block.reshape(block.shape[0],blkszp,3).mean(axis=1)   
        dcolor=color-cmean
        print block.shape, dcolor.shape
        a=block.reshape(block.shape[0],blkszp,3)
        b=(dcolor.reshape(dcolor.shape+(1,)).repeat(blkszp,axis=2).swapaxes(1,2)).reshape(block.shape[0],blkszp,3)
        print a.shape, b.shape
        c=a+b
        print "/md1r"
        return c.reshape(block.shape[0],blkszp*3)
     mdx1=( md1_project,
            md1_releve,
            CachedModel( 
                  HistogramModel,
                  lambda:HistogramModel((2**precision,)*3,(0,)*(3),(256,)*(3)),
                  basepath+ "/"+name+"-outcolor_model_rel_0001.mdl",
            )
           )
     vm.cachedmodels.append(mdx1[2])

     def md2a_project(block):
        return block.reshape(block.shape[0],blksz[0],blksz[1],3)[:,:,:,0].sum(axis=2)
     def md2a_releve(color,block=None):
        assert(False)
     mdx2a=( md2a_project,
            md2a_releve,
            CachedModel( 
                  HistogramModel,
                  lambda:HistogramModel((4,)*(blksz[0]),(0,)*(blksz[0]),(256*blksz[1],)*(blksz[0])),
                  basepath+ "/"+name+"-md2a.mdl",
            )
           )
     vm.cachedmodels.append(mdx2a[2])
     def md2b_project(block):
        return block.reshape(block.shape[0],blksz[0],blksz[1],3)[:,:,:,0].sum(axis=1)
     def md2b_releve(color,block=None):
        assert(False)
     mdx2b=( md2b_project,
            md2b_releve,
            CachedModel( 
                  HistogramModel,
                  lambda:HistogramModel((4,)*(blksz[1]),(0,)*(blksz[1]),(256*blksz[0],)*(blksz[1])),
                  basepath+ "/"+name+"-md2b.mdl",
            )
           )
     vm.cachedmodels.append(mdx2b[2])


     def md3a_project(block):
        return block.reshape(block.shape[0],blksz[0],blksz[1],3)[:,:,:,1].sum(axis=2)
     def md3a_releve(color,block=None):
        assert(False)
     mdx3a=( md3a_project,
            md3a_releve,
            CachedModel( 
                  HistogramModel,
                  lambda:HistogramModel((4,)*(blksz[0]),(0,)*(blksz[0]),(256*blksz[1],)*(blksz[0])),
                  basepath+ "/"+name+"-md3a.mdl",
            )
           )
     vm.cachedmodels.append(mdx3a[2])
     def md3b_project(block):
        return block.reshape(block.shape[0],blksz[0],blksz[1],3)[:,:,:,1].sum(axis=1)
     def md3b_releve(color,block=None):
        assert(False)
     mdx3b=( md3b_project,
            md3b_releve,
            CachedModel( 
                  HistogramModel,
                  lambda:HistogramModel((4,)*(blksz[1]),(0,)*(blksz[1]),(256*blksz[0],)*(blksz[1])),
                  basepath+ "/"+name+"-md3b.mdl",
            )
           )
     vm.cachedmodels.append(mdx3b[2])


     def md4a_project(block):
        return block.reshape(block.shape[0],blksz[0],blksz[1],3)[:,:,:,2].sum(axis=2)
     def md4a_releve(color,block=None):
        assert(False)
     mdx4a=( md4a_project,
            md4a_releve,
            CachedModel( 
                  HistogramModel,
                  lambda:HistogramModel((4,)*(blksz[0]),(0,)*(blksz[0]),(256*blksz[1],)*(blksz[0])),
                  basepath+ "/"+name+"-md4a.mdl",
            )
           )
     vm.cachedmodels.append(mdx4a[2])
     def md4b_project(block):
        return block.reshape(block.shape[0],blksz[0],blksz[1],3)[:,:,:,2].sum(axis=1)
     def md4b_releve(color,block=None):
        assert(False)
     mdx4b=( md4b_project,
            md4b_releve,
            CachedModel( 
                  HistogramModel,
                  lambda:HistogramModel((4,)*(blksz[1]),(0,)*(blksz[1]),(256*blksz[0],)*(blksz[1])),
                  basepath+ "/"+name+"-md4b.mdl",
            )
           )
     vm.cachedmodels.append(mdx4b[2])


     return BaggedModel([mdx1,mdx2a,mdx2b,mdx3a,mdx3b,mdx4a,mdx4b])





class MyModel(visionmodel.MyModel):
  def init_features(self):
     self.observed_features=[
                    ('src|rgb2hsv|vm.process'  ,
                     {'vm': VideoMemory(numpy.zeros((96,128,3))) },  #(240,352,3)
                     {}
                    ), # 0
                  ]
     
  def init_models(self, basepath,   mlop="train", mlargs="online=True"):
     self.cachedmodels=[]
     states=numpy.array(map( lambda x:[8+x[0]*80,8+x[1]*80,8+x[2]*80] , numpy.ndindex(3,3,3) ))
     #print states.shape
     mom=MarkovObservationMaker()
     mdl1=InterpolatedStateConditionalModelSv(
                                                            states,
                                                            k=3,
                                                            SearchStructure=KDTree,
                                                            project_prior=None,
                                                            project_evidence=None,
                                                            individual_model_factory=(lambda x:pattern_model(self,basepath,"sub-"+str(x),(5,5),3)),
                                                            individual_model_class=None,
                                                            
                                              )
     
     mdl_pixels=CachedModel(
             HistogramModel,
             lambda:HistogramModel(
                               (16,16,16),
                               (0,0,0),
                               (256,256,256)
                              ),
             basepath+"/pixelmodel.mdl")
       
     self.cachedmodels.append(mdl_pixels)

     mdl_patterns=pattern_model(self,basepath,"base",(5,5),3)
 
     mdlb=BayesianModel(
                         project_prior=lambda o:numpy.vstack(o[:,1].tolist()),
                         project_evidence=lambda o:numpy.vstack(o[:,0].tolist()),
                         likeliness_model=mdl1,
                         prior_model=mdl_pixels,
                         evidence_model=mdl_patterns ,
                         full_train=True
                         )



    ########################################################################################################################################################################
    ## Now we make it markovian or something like this ;)
    ########################################################################################################################################################################
     def recomposef0(x,log):
         print x.shape
         return x.reshape(x.shape[0],123,91,scipy.prod(x.shape[1:])/(123*91))
     mmkov=MarkovModel(
         [
                MarkovModel.CliquesSet(
                    #lambda b:to2d(all_blocks2d1d_i(b.astype(int),5,5,2,2)),
                    lambda x:mom.process(x,exhaustive=(mlop!="test")),
                    mdlb,
                    recomposef0=recomposef0
                 )
         ]
      ) 
  
     ######################################################################################################################################
     # operator
     ######################################################################################################################################     
  def connect_models(self,   mlop="train", mlargs="online=True",basepath="/home/tranx/videodatabase/db10"):
     self.observed_features+=[
                    #
                    (self.observed_features[0][0]+"|mmkov."+mlop+"("+mlargs+")",{'mmkov':mmkov  }, 
                                                                                {'title':'likelihood'})
                    #
                   ]      
  def savemodels(self):
     for m in self.cachedmodels:
        m.save()
     
