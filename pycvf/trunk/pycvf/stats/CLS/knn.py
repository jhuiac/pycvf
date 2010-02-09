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
###
###
###
from pycvf.indexes.pseudoincremental import PseudoIncrementalIndex
from pycvf.indexes.sashindex import SashIndex

class StatModel:
   def __init__(self, k):
      """
       We approximate by the mean of our nearest neighbors
      """ 
      self.k=k
      self.idx=PseudoIncrementalIndex(SashIndex)
   def dump(self,file_):
       assert(False)
   @staticmethod
   def load(file_, *args, **kwargs):
       assert(False)   
   def train(self,A,B,online=False):
       ## basically train consists in creating 1 or 2 sahs
       assert(A!=None)
       assert(B!=None)
       self.idx.add_many(A,B)
       self.idx.recompute()
   def predict(self,A,AN=None,B=None,BN=None,log=False):
       """
        Predict what will be the label according to $k$-closest neighbors
       """
       ### basically train consists in checking out the average distance of neighbors
       ### basically train consists in checking out the average distance of neighbors compared to oponents features...
       #
       # basically we consider density estimation as a 
       # 
       res=self.idx.getitems(A,self.k)
       return map(lambda x:x[0][0][0],res)

       #parzenestimator()
       #return scipy.mean(map(self.idx.getitem(obs,self.k),lambda x:x[1]))
   def memory_cost(self, *args, **kwargs):
        assert(False)
   def cpu_cost(self, *args, **kwargs):
        assert(False)
   def random_improve(self,value,amount=0.5, prec=1):
        ## TRY TO RANDOMLY CHANGE WITH A NEAREST NEIGHBOR
        #print "random_improve not yet implemented doing sample instead !!! hist"
        #return self.sample(value.shape[0])
        assert(False)   

__call__=StatModel
