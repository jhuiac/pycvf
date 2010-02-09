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
import sys
import traceback
import numpy
import scipy
import random
import cPickle as pickle
import marshal
        

class ParzenModel:
   """
     Pazen Window is a very simple Positive examples definite model.
     In this example it has of course the inconvenient of requiring as much data as input trained data.

     It seem that PyEm has problem with 1d model it may be used there for the moment,
   """
   def __init__(self,ndim,sigma,test_approx=20):
      self.ndim=ndim
      self.sigma=sigma
      self.test_approx=test_approx
      self.data=None
      self.ndata=None
   def train(self,positive_training_set, negative_training_set=None,online=False):
      if (online) and (self.data!=None or self.ndata!=None):
        self.data=positive_training_set
        self.ndata=negative_training_set
      else:
        self.data=positive_training_set
        self.ndata=negative_training_set        
   def kernelf(self,p0,p1):
      return numpy.exp(-numpy.linalg.norm((p0-p1)/self.sigma))
   def test(self,data):
      if (self.test_approx!=None):
        return numpy.vstack([numpy.mean([ self.kernelf(data[dt0,:],self.data[dt1,:]) for dt1 in  random.sample(range(self.data.shape[0]),self.test_approx) ]) for dt0 in range(data.shape[0]) ])
      else:
        return numpy.vstack([numpy.mean([ self.kernelf(data[dt0,:],self.data[dt1,:]) for dt1 in range(self.data.shape[0]) ]) for dt0 in range(data.shape[0]) ])
   def sample(self,n=100):
      """ we assume gaussian kernel """
      res=[]
      for i in range(n):
        res.append(map(lambda x:x+random.gauss(0,self.sigma),random.choice(self.data)))
      return numpy.array(res)
   def dump(self,file_):
       pickle.dump(self,file_)
   @staticmethod
   def load(file_,*args,**kwargs):
      return pickle.load(file_)
   def random_improve(self,value,amount=0.5, prec=1):
        ## look at for bin with higher probability in surrounding area
        assert(False)   

__call__=ParzenModel
StatModel=ParzenModel
