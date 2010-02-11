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
     Pazen Window is a very simple density estimator, that estimates the probability of an event by taking in account the 
     all the previous observations, and by considering that new observations are likely to occur at similar places plus some noise.

     It has of course the inconvenient of requiring as much data as input trained data, and normally evalutating the density function require to sum over
      the contributions of all the points. 
  
     This implementation suggest two kind of speed up : use knn to find nearest neighbor points or 
     use random points, in large space knn search is of course supposed to provide the best results.
   """
   def __init__(self,sigma=1,test_approx=20,ndim=-1, ann=None):
      #self.ndim=ndim
      self.sigma=sigma
      self.test_approx=test_approx
      self.data=None
      self.ann=ann
   def train(self,positive_training_set, online=False):
      if (online) and (self.data!=None ):
        pl=len(self.data)
        self.data=numpy.vstack([self.data,positive_training_set])
        if (self.ann):
           ann.add_many(positive_training_set,range(pl,len(self.data)))
      else:
        self.data=positive_training_set
        if (self.ann):
           self.ann.reset()
           ann.add_many(positive_training_set,range(pl,len(self.data)))
   def kernelf(self,p0,p1):
      return numpy.exp(-numpy.linalg.norm((p0-p1)/self.sigma))
   def test(self,data,log=False):
      if log:
        f=numpy.log
      else:
        f=lambda x:x
      if (self.test_approx!=None):
        if (self.ann):
           rq=self.ann.query(data,self.test_approx)
           print rq
           rq=None#...
           return f(numpy.vstack([numpy.mean([ self.kernelf(data[dt0,:],self.data[dt1,:]) for dt1 in rq ]) for dt0 in range(data.shape[0]) ]))
        else:
           return f(numpy.vstack([numpy.mean([ self.kernelf(data[dt0,:],self.data[dt1,:]) for dt1 in  random.sample(range(self.data.shape[0]),self.test_approx) ]) for dt0 in range(data.shape[0]) ]))
      else:
        return f(numpy.vstack([numpy.mean([ self.kernelf(data[dt0,:],self.data[dt1,:]) for dt1 in range(self.data.shape[0]) ]) for dt0 in range(data.shape[0]) ]))
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
