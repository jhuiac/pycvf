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
    from em import *
except:
    from sckits.learn.machine.em import *
    import sckits.learn.machine.em.online_em as online_em

    
class EmModel:
   class TexDoc:
       """
       Gaussian Mixture Models form an elegant and general framework for data modelization.
       
       
       The framework of Gaussian Mixtures have the good property of forming an algebra.
       
       A distribution $\\mathcal D$ is well modelized by a Gaussian model, if 
       its distribution is well approximated by a superposition of Gaussians :
       
       $$ \\mathcal D(x) = \\sum_{i=0}^{N} \\mathcal{N}_{\\theta_i}(X)  $$
       
       The parameters of the gaussian models are forms by the parameter of its Gaussian. 
       
       Gaussian Mixtures Models are trained based on the Expectation Maximization MetaAlgorithm.
       
       
       Expectation Maximization is the standard method used to learn Gaussian Mixtures Models.
       
        We recall that the Expectation Maximization work in two steps, that can be unformally summed up in these terms :
        \\begin{itemize}
        \\item compute the likelihood of an improved candidate according according to current knowledge and to training data
        \\item update current knowledge/parameters to the one that gives the best results 
        \\end{itemize}
        
        
       """
       def __init__(self,article):
           pass
       def History(self):
           """
           The Expectation Maximization method has precursor in the Baum-Welch algorithm
           """
       def InOtherWords(self):
           """
           We iteratively evaluate the likelihood of the model with respect to the data.
           """
           
   def __init__(self,ndim,k=9,mode=None):
      #if (ndim>6):
      #    print "hmm... does not seem to work with dim>6"
      self.lgm = GM(ndim, k, mode or ( ( ndim!=1) and "full" or "diag")) ## ndim , k: mixture, "full" covariance as opposed to diag...
      self.trained=False
      self.gmm=None
      self.online=False
   def init_gmm(self,online=False):
      if (self.gmm==None) or (self.online!=online):
        if (online):
           self.gmm = online_em.OnGMM(self.lgm,"kmean") 
        else:
           self.gmm = GMM(self.lgm, "kmean")
        assert(self.gmm!=None)
   def train(self,positive_training_set,negative_training_set=None, maxiter = 30, thresh = 1e-8,online=False):
      em=EM()
      _trained=False
      #if (online):
          #print "warning : online training is not yet efficient work to be done here !!!!"
          #if (self.trained):
          #  postive_training_set=numpy.vstack([numpy.array(positive_training_set), self.sample()])
      self.init_gmm(online)
      if (negative_training_set):
          print "warning : negative training set has not been taken in account"
      positive_training_set=numpy.array(positive_training_set)
      #print positive_training_set 
      while not _trained: 
        try:
          print self.gmm
          em.train(positive_training_set, self.gmm, maxiter=maxiter, thresh =thresh)
          _trained=True
          self.trained=True
        except numpy.linalg.linalg.LinAlgError:
          ## avoid bugging when not enough value
          print "warning not enough data provided ... increasing training set size (",positive_training_set.shape[0]," )"
          positive_training_set=positive_training_set.repeat(2,axis=0)+numpy.random.random((positive_training_set.shape[0]*2,positive_training_set.shape[1]))*positive_training_set.std()*0.001
   def test(self,data,log=True):
      return self.lgm.pdf(data,log)
   def sample(self,n=100):
      return self.lgm.sample(n)
   def dump(self,file_):
       pickle.dump(self.lgm,file_)
   @staticmethod
   def load(file_, *args, **kwargs):
      lgm=pickle.load(file_)
      x=EmModel(lgm.mu.shape[1],lgm.k)
      x.lgm=lgm
      x.gmm = GMM(x.lgm, "kmean")
      return x
   def memory_cost(self, *args, **kwargs):
      assert(False)
   def cpu_cost(self, *args, **kwargs):
       assert(False)
   def random_improve(self,value,amount=0.5, prec=1):
        ## look at for bin with higher probability in surrounding area
        assert(False)   


__call__=EmModel
StatModel=EmModel
