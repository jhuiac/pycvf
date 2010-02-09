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

class StatModel:
   """
    A Statistical Model used for Probability Density Estimation
   """
   def __init__(self,  *args, **kwargs):
      """
      initialization of your model
      """ 
    
   def get_as_vector(self):
      """
       return a vector describing the parameters of the models that has been trained.
      """
   def dump(self,file_):
       """
       Allow to save the model by serializing into some file.
       """
   @staticmethod
   def load(file_, *args, **kwargs):
       """
       Allow to read the model by deserializing it
       """
   def train(self,obs,obsN=False,online=False):
       """
       Train by taking in accountt some positive and optionally some negative observations
       If online is equal to True previous observations must remain in memory. 
       """
   def test(self,obs,log=False):
       """
       return probability density estimate for on the query observation.
         if log enabled returns log probability density estimate.
       """
   def sample(self,numsamples=10):
       """
         Allows to sample data according to the probability distribution
       """
   def memory_cost(self, *args, **kwargs):
       """
         Specifies the memory amount used by the model
       """
       assert(False)
   def cpu_cost(self, *args, **kwargs):
       """
        (optional)
        return a dictionary of integer specifying how costful it is train/query/sample
        the model, according to its current state.
       """
       assert(False)       
   def random_improve(self,value,amount=0.5, prec=1):
        ## look at for in with higher probability in surrounding area
        """
        (OPTIONAL)
        Use the statistical estimate to modify value of amount in
        a direction that would increase its probability estiate
        """

__call__=StatModel
