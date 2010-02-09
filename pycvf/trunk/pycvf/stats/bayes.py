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
  

#   bm1=model.BayesianModel(lambda x:x[:,-1:], lambda x:x[:,:-1], model.EmModel(4), model.EmModel(1), model.EmModel(3))
#   sine=[ numpy.cos(x*0.1) for x in range(100) ]
#   sinetset=numpy.array([ (lambda y:(sine[y:y+4]))(random.randint(0,len(sine)-4))  for x in range(100) ])
#   bm1.train(sinetset)
#   bm1.train()     
class StatModel:
    class TexDoc:
         """
         To learn the probabilty distribution of $\P(A|B)$ when the domain of possible contexts ($B$) is large compared to the set of possible edges ($A$)
         within this context it is somehow meaningful when extensions are not that required discontinuous with respect to context to use 
         Bayesian inversion formula.
         P of A and B is unlikely to be learned.
     
         """
         def __init__(self,article):
             pass        
    def __init__(self,project_prior, project_evidence, likeliness_model, prior_model,evidence_model,full_train=False, *args, **kwargs):
        self.project_prior=project_prior
        self.project_evidence=project_evidence
        self.likeliness_model=likeliness_model
        self.prior_model=prior_model
        self.evidence_model=evidence_model
        self.full_train=full_train
    def test_separated_no_log(self,A,B):
        return (self.likeliness_model.test_separated(A,B,log=False) * self.evidence_model.test(A,log=False))/self.prior_model.test(B,log=False)         
    def test_no_log(self,AandB):
        A=self.project_prior(AandB)
        B=self.project_evidence(AandB)
        return (self.likeliness_model.test(AandB,log=False) * self.evidence_model(A,log=False))/self.prior_model(B,log=False)
    def test_separated_log(self,A,B):
        return (self.likeliness_model.test_separated(A,B,log=True) + self.evidence_model.test(A,log=True))-self.prior_model.test(B,log=True)         
    def test_log(self,AandB):
        A=self.project_prior(AandB)
        B=self.project_evidence(AandB)
        return (self.likeliness_model.test(AandB,log=True) + self.evidence_model.test(A,log=True))-self.prior_model.test(B,log=True)
    def test(self,AndB,log=True):
        if (log):
            return self.test_log(AandB)
        else:
            return self.test_no_log(AandB)
    def test_separated(self,A,B,log=True):
        if (log):
            return self.test_separated_log(A,B)
        else:
            return self.test_separated__no_log(A,B)
    def train_separated(self,pA,pB,nA=None,nB=None,full_train=None, *args, **kwargs):
        if full_train==None:
          full_train=self.full_train
        if (full_train):
          self.prior_model.train(pA,nA)
          self.evidence_model.train(pB,nB)
        self.likeliness_model.train_separated(pA,pB,nA,nB, *args, **kwargs)
    def train(self,positive_training_set,negative_training_set=None,full_train=True, *args, **kwargs):
        if full_train==None:
          full_train=self.full_train
        pA=self.project_prior(positive_training_set)
        pB=self.project_evidence(positive_training_set)
        if (negative_training_set):
          nA=self.project_prior(negative_training_set)
          nB=self.project_evidence(negative_training_set)
        else:
          nA=None
          nB=None 
        #self.likeliness_model.train(positive_training_set,negative_training_set, *args, **kwargs)
        if (full_train):
          print args
          print kwargs
          self.prior_model.train(pA,nA, *args, **kwargs)
          self.evidence_model.train(pB,nB, *args, **kwargs)
        self.likeliness_model.train_separated(pA,pB,nA,nB, *args, **kwargs)
    def sample(self,n=100, withstate=None,prec=25, *args, ** kwargs):
        print "TODO  sampling through bayesian inversion formula : to be corrected /remove bs**=5!!!!"
        # TODO a regression should be integrated
        #bs=[ self.test(numpy.array([withstate]),withstate=state) for state in self.prior_model.sample(prec) ]
        ## we do montecarlo like stuffs ...
        prio=self.prior_model.sample(prec*withstate.shape[0])
        bs=self.likeliness_model.test_with_state(prio, numpy.array([withstate]).repeat(prec,axis=0).reshape(withstate.shape[0]*prec,withstate.shape[1]))          
        bs=bs.reshape(withstate.shape[0],prec)
        bsm=bs.min()
        bsM=bs.max()
        bs-=bsm
        bs/=(bsM-bsm+1e-24)
        bs**=5 ## strongly make appear the best...
        ## random sampling among best ?
        bsi=scipy.cumsum(bs,axis=1)
        sra=numpy.asarray(numpy.random.random((withstate.shape[0],1)))
        srb=numpy.asarray(bsi[:,-1:])
        sr=(sra*srb)
        sr=sr.repeat(prec,axis=1)
        ridx=((bsi<sr).sum(axis=1))
	ridx+=numpy.arange(0,prec*withstate.shape[0],prec)
        return prio[ridx.astype(int)]
        #return [ self.likeliness_model.sample(AandB, 1, withstate=self.likeliness_model.prior_model.sample(1)) for x in range(n) ]
    def dump(self,file_):
        #pickle.dump( self, file_)
        pass
    #@staticmethod
    #def load(file_, *args, **kwargs):
    #return pickle.load(file_)
    @staticmethod
    def load(file_, *args, **kwargs):
        return BayesianModel(*args,**kwargs)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
    
__call__=StatModel
