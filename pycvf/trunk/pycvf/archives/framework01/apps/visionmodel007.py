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
#########################################################################################################################################3
# Includes
#########################################################################################################################################3

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

import scipy.spatial

#########################################################################################################################################3
# Library
#########################################################################################################################################3


def recomposef(base,x,xx):
    pass

def to2d(x):
  x=numpy.array(x,dtype=object)
  xs1=scipy.prod(x.shape[1:])
  return x.reshape(x.shape[0],xs1)


#########################################################################################################################################3
# Model
#########################################################################################################################################3


import visionmodel
class VisionModel(visionmodel.VisionModel):
  def init_observed_features_video(self):
     otime=time.time()
     #########################################################################################################################################
     # The model of the graph for the experiment
     #########################################################################################################################################
     self.observed_features=[
                    ('src|rgb2hsv|lum'  ,{'lum':lambda x:x[:,:,2] },  {'title':'lumimg','color':(1,0,0)}),  #0 
                    ('wtp2()',{'wtp2':(lambda :sys.stderr.write("\r"+self.videoreader.get_current_address()[0]+((lambda t:"%d - %f - %f - %f"%( t,(1+t)/29.97,time.time()-otime, ((1+t)/29.97)/(time.time()-otime) ))(self.videoreader.get_current_address()[1]))))},{})
                  ]
  def init_observed_features_statistics(self,   mlop="train", mlargs="online=True",basepath="/home/tranx/videodatabase/db7x"):
      lummodel=CachedModel(
                           HistogramModel((256,),(0,),(256,)),
                           lambda :HistogramModel((2,)*(4**2),(0,)*(4**2),(2,)*(4**2) ),
                           basepath+ "/luminance_001.mdl"
                         )
      pat_mdl={}
      lumstates=numpy.arange(0,256.,32.).tolist()
      def mdl_patterns_for_lum(x):
          if (pat_mdl.has_key(x)):
              return pat_mdl
          mdl_patterns=CachedModel(HistogramModel,
                           lambda :HistogramModel((3,)*(3*3),(0,)*(3*3),(255,)*(3*3) ),
                           basepath+ "/pattern_"+str(x)+".mdl"
                           )
          pat_mdl[x]=mdl_patterns
          return mdl_patterns
      def mdl_edges_h_for_lum(x):  
          mdl_edges_h=CachedModel(HistogramModel,
                           lambda :HistogramModel((3,)*(3*1),(0,)*(3*1),(255,)*(3*1) ),
                           basepath+ "/edge_h_"+str(x)+".mdl"
                           )
          return mdl_edges_h
      def mdl_pattern_knowing_edge_h_for_lum(xl):
          states=(numpy.array([ x for x in numpy.ndindex((2,2,2))])*255).tolist()
          mdl_pattern_knowing_edge_h=CachedModel(
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
                                  basepath+ "/isb_edge_h_"+str(xl)+".mdl",
                                  suppkwargs=dict(      k=3,
                                                    SearchStructure=KDTree,
                                                    project_prior=None ,
                                                    project_evidence=None,
                                                    individual_model_factory=( 
                                                                                lambda x: EmModel(9,20 )
                                                                             ),
                                                    individual_model_class=(
                                                                                lambda x:  EmModel
                                                                            )
                                  ) 
                            )
          return mdl_pattern_knowing_edge_h
      def mdl_edges_v_for_lum(x):
          mdl_edges_v=CachedModel(HistogramModel,
                           lambda :HistogramModel((3,)*(3*1),(0,)*(3*1),(255,)*(3*1) ),
                           basepath+ "/edge_v_"+str(x)+".mdl"
                           )
          return mdl_edges_v
      def mdl_pattern_knowing_edge_v_for_lum(xl):
          states=(numpy.array([ x for x in numpy.ndindex((2,2,2))])*255).tolist()
          mdl_pattern_knowing_edge_v=CachedModel(
                            InterpolatedStateConditionalModelSv,                                                                                           
                              lambda project_prior, project_evidence, individual_model_factory, individual_model_class, SearchStructure,k,nosubload:
                                  InterpolatedStateConditionalModelSv(
                                                                states,
                                                                k=k,
                                                                SearchStructure=SearchStructure,
                                                                project_prior=project_prior,
                                                                project_evidence=project_evidence,
                                                                individual_model_factory=individual_model_factory,
                                                                individual_model_class=individual_model_class
                                                            ),
                              basepath+ "/isb_edge_v_"+str(xl)+".mdl",
                              suppkwargs=dict(      k=3,
                                                SearchStructure=KDTree,
                                                project_prior=None ,
                                                project_evidence=None,
                                                individual_model_factory=( 
                                                                            lambda x: EmModel(9,20)
                                                                         ),
                                                individual_model_class=(
                                                                            lambda x:  EmModel
                                                                        ),
                                                nosubload=True
                              ) 
                       )
          return mdl_pattern_knowing_edge_v 
      ## suggest dynamically instantiated GMM
      ## on dynamic framework with detailed context
      
      def edgeh_extract_f(pats):
          #print "pats",pats, pats.shape
          return pats[:,:,-1].reshape(pats.shape[0],3)
      def edgev_extract_f(pats):
          #print "pats",pats, pats.shape
          return pats[:,-1,:].reshape(pats.shape[0],3)
      def pat_extract_f(pats):
          #print "pats",pats, pats.shape
          return pats[:,:3,:3].reshape(pats.shape[0],9)
      
      
      mdl_edges_h=CachedModel( InterpolatedStateConditionalModelSv,                                                                                           
                              lambda project_prior, project_evidence, individual_model_factory, individual_model_class, SearchStructure,k:
                                  InterpolatedStateConditionalModelSv(
                                                                lumstates,
                                                                k=k,
                                                                SearchStructure=SearchStructure,
                                                                project_prior=project_prior,
                                                                project_evidence=project_evidence,
                                                                individual_model_factory=individual_model_factory,
                                                                individual_model_class=individual_model_class
                                                            ),
                              basepath+ "/isb_lume_edge_h_bayesian_001.mdl",
                              suppkwargs=dict(      k=3,
                                                SearchStructure=LineSearch,
                                                project_prior=lambda x:x[0],
                                                project_evidence=lambda x:x[1],
                                                individual_model_factory=( 
                                                                            lambda x: BayesianModel(
                                                                                                    project_prior=edgeh_extract_f,
                                                                                                    project_evidence=pat_extract_f,
                                                                                                    likeliness_model=mdl_pattern_knowing_edge_h_for_lum(x),
                                                                                                    prior_model=mdl_edges_h_for_lum(x),
                                                                                                    evidence_model=mdl_patterns_for_lum(x) 
                                                                                                    )
                                                                         ),
                                                individual_model_class=(
                                                                            lambda x: BayesianModel
                                                                        )
                          )
                        )
      
      mdl_edges_v=CachedModel( InterpolatedStateConditionalModelSv,                                                                                           
                              lambda project_prior, project_evidence, individual_model_factory, individual_model_class, SearchStructure,k,nosubload:
                                  InterpolatedStateConditionalModelSv(
                                                                lumstates,
                                                                k=k,
                                                                SearchStructure=SearchStructure,
                                                                project_prior=project_prior,
                                                                project_evidence=project_evidence,
                                                                individual_model_factory=individual_model_factory,
                                                                individual_model_class=individual_model_class
                                                            ),
                              basepath+ "/isb_lum_edge_v_bayesian_001.mdl",
                              suppkwargs=dict(      k=3,
                                                SearchStructure=LineSearch,
                                                project_prior=lambda x:x[0],
                                                project_evidence=lambda x:x[1],
                                                individual_model_factory=( 
                                                                            lambda x: BayesianModel(
                                                                                                    project_prior=edgev_extract_f,
                                                                                                    project_evidence=pat_extract_f,
                                                                                                    likeliness_model=mdl_pattern_knowing_edge_v_for_lum(x),
                                                                                                    prior_model=mdl_edges_v_for_lum(x),
                                                                                                    evidence_model=mdl_patterns_for_lum(x) 
                                                                                                    )
                                                                         ),
                                                individual_model_class=(
                                                                            lambda x: BayesianModel
                                                                        ),
                                                nosubload=True
                          )
                        )
      
      
      
      def obs_edge_h(img):
            m=img.mean()
            ab=all_blocks2d1d_u8(img,3,4,2,2)
            ra=numpy.array(reduce(lambda b,l:b+[(l,m)],ab,[]),dtype=object)
            #print ab
            #print ra
            return ra
      def obs_edge_v(img):
            m=img.mean()
            ab=all_blocks2d1d_u8(img,4,3,2,2)
            ra=numpy.array(reduce(lambda b,l:b+[(l,m)],ab,[]),dtype=object)
            #print ab
            #print ra
            return ra       
      self.mm=MarkovModel(
          [
         #  MarkovModel.CliquesSet(
         #               lambda b:to2d(all_blocks2d1d_i(b.astype(int),3,3,2,2)),
         #               mdl1,
         #               recomposef=recomposef
         #            ),
           MarkovModel.CliquesSet(
                        obs_edge_h,
                        mdl_edges_h,
                        recomposef=recomposef
                     ),
           MarkovModel.CliquesSet(
                        lambda b:to2d(all_blocks2d1d_i(downscale(b,2).astype(int),3,4,2,2)),
                        mdl_edges_v,
                        recomposef=recomposef
                     )
    
          ]
      ) 
      self.observed_features+=[
                    (self.observed_features[0][0]+"|MarkovModel."+mlop+"("+mlargs+")",{'MarkovModel':self.mm}, {"title":"Naturalness 1"}),
                   ]      
