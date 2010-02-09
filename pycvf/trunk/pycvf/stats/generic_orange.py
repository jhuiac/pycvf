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
        
try:
  from orange import *
  
  class OrangeModel():
    def __init__(self,ndim,numclass=2,Model=None):
      classvar=orange.EnumVariable("y",values=map(str,range(numclass))) 
      self.mydomain=orange.Domain( [ orange.FloatVariable("x"+str(d),startValue=-10,endValue=10) for d in range(ndim) ]
                      + [  classvar  ] )
      if (not Model):
          Model=orange.BayesLearner(name="bayes")
      self.Model=Model
    def train_model(self,positive_training_set, negative_training_set):
      # negative
      training_set=positive_training_set+negative_training_set
      training_data=orange.ExampleTable(self.mydomain , training_set )
      self.model=self.Model(training_tada)
    def test(self,data,log=True): ## return likelihood of samples
      orange.ExampleTable(self.mydomain , training_set )
      return numpy.log(self.model(data))
    def sample(self,data): ## random sample from learner (if possible)
      return self.model.random()
    def dump(self,file_):
      self.a.dump(file_, self)
    @staticmethod
    def load(file_, *args, ** kwargs):
      return pickle.load(file_)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
  
except:
  print "please install orange" 