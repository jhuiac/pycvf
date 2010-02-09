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


import numpy
import scipy
import random

#####################################################################################################################
class IncrementalModel():
    ##
    ## Here the problem is to learn a PDF according to a continuous flow of observation were we always want to have  
    ## an opinion on the question
    ##
    """ 
        we wonder about building a good example set, 
        that include a little bit of all the diversity, by taking also in account exceptional points
        but not taking in accout noise..

        to do so we create two list 
            (one prior, and one observed, and we also memorize the number of observations) 
    """
    def __init__(self,model,refresh_rate=10,max_examples=20,rel_like_thres=0.9):
           self.new_examples=[]
           self.examples=[]
           self.model=model
           self.refresh_rate=refresh_rate
           self.gen_samples=5
           self.notify_threshold=10
           self.max_examples=max_examples
           self.rel_like_thres=rel_like_thres
           self.like_threshold=scipy.Infinity ## at the beginning we learn everything
    def likelihood_of_examples(self):
        return map(self.likelihood,self.examples)
    def reinforce_confidence(self):
        self.gen_samples=min(self.gen_samples+1,200)
    def update_if_necessary(self):        
        if (len(self.new_examples)>self.refresh_rate):
            self.update()
    def update(self):
           print "<update>",
           training_set= numpy.vsplit(self.model.sample(self.gen_samples), self.gen_samples )
           training_set+=self.new_examples
           self.model.train(numpy.vstack(training_set))
           self.examples=self.examples+self.new_examples
           exl=self.likelihood_of_examples()
           self.like_threshold=scipy.mean(exl)
           exc=(scipy.cumsum(exl)/(scipy.sum(exl)+1e-43))[:-1]
           self.examples=[ self.examples[(exc<random.random()).astype(int).sum()]  for i in range(self.max_examples) ]
           self.new_examples=[]
           print "</update>"
    def test(self,x):
        return self.model.test(x)
    def likelihood(self,x):
        return self.model.test(x,log=False)
    def learn(self,x):
        if (self.likelihood(x)<self.like_threshold):
            self.new_examples.append(x)
            self.update_if_necessary()
        else:
            self.reinforce_confidence()
