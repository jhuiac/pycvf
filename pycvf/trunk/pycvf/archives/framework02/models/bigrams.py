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
   This is a very slow but very general implementaion of bigram models
"""


class Memory:
  def __init__(self,n):
     self.mem=[None] * (n-1)
  def push(self,data):
     self.mem.append(data)
     if (self.mem[0]!=None):
        r=self.mem[:]
        self.mem.pop(0)
        return [r]
     else:
        self.mem.pop(0)
        return None

class DicoHistogramModel:
  def dump(self,file_):
       pickle.dump(self,file_)
  @staticmethod
  def load(file_,*args,**kwargs):
      return pickle.load(file_)
  def __init__(self):
     self.h={}
     self.no=0
  def train(self, data, online=True):
      if (not online):
         self.h={}
      for d in data:
         #print "d",d
         if self.h.has_key(d[0]):
            self.h[d[0]]+=1
         else:
            self.h[d[0]]=1
      self.no+=len(data)
  def test(self, data):
      return numpy.ndarray([ [ self.h[d] ] for d in data ]).astype(float)/self.no
         

from pycvf.core import genericmodel
from pycvf.lib.stats.cachedmodel import *
from pycvf.lib.stats.conditionalmodel import *

class Model(genericmodel.GenericModel):
  def init_features(self):
     self.observed_features=[ ('src|memory.push'  ,{'memory':Memory(2)},  {'title':'bigrams'})  ]
  def init_models(self,basepath, *args, ** kwargs):
     def new_model_factory(x):
         print "new model for" , x
         m=CachedModel(
                          DicoHistogramModel,
                          lambda :DicoHistogramModel(),
                          basepath+u"/bigrams-"+unicode(x)+u".mdl"
                       )
         self.models.append(m)
         return m
     mdl1=CachedModel(
           FiniteStateConditionalModel,
           lambda:FiniteStateConditionalModel(
             lambda x:x[1],
             lambda x:x[0],
             individual_model_factory=new_model_factory,
             individual_model_class=DicoHistogramModel,
             states=[],
             check_new=True
           ),
           basepath+"/bigrams.mdl"
         )
     self.models.append(mdl1)
     #self.cached_models.append(mdl1)
  def connect_models(self,basepath,   mlop="train", mlargs="online=True"):
     self.observed_features+=[
                    (self.observed_features[0][0]+"|model_bigram."+mlop+"("+mlargs+")",{'model_bigram':self.models[0]  }, 
                                                                                {'title':'bigrams'})
                             ]      

__call__=MyModel
