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



class BaggedModel():
  def __init__(self,transform_model_list):
     """
       (Project, Releve, Model)
        Project x -> p
        Releve : x0,p -> x1    | project(x1 )=p and "kernel"(Project) from x0
     """
     self.tml=transform_model_list
  def train(self,pos,neg=None, *args , **kwargs ):
    print "posshp", pos.shape
    for mdl in self.tml:
       mdl[2].train(mdl[0](pos),(neg and mdl[0](neg) or None ),*args,**kwargs)
  def train_separated(self,posA,posB,negA=None,negB=None, *args , **kwargs ):
    for mdl in self.tml:
       mdl.train_separated(mdl[0](posA),
                           mdl[0](posB),
                           (negA and mdl[0](negA) or None ),
                           (negB and mdl[0](negB) or None ),
                           *args,
                           **kwargs
                           )
  def test(self,A,log=False,*args, **kwargs):
    if (log):
      r=0
      op=lambda x,y:numpy.asarray(x)+numpy.asarray(y)
    else:
      r=1
      op=lambda x,y:numpy.asarray(x)*numpy.asarray(y)
    print A.shape
    for mdl in self.tml:
       r=op(r,mdl[2].test(mdl[0](A),
                  *args,
                  **kwargs
                  )
            )
    return r
  def test_separated(self,A,B, log=False,*args , **kwargs ):
    if (log):
      r=0
      op=lambda x,y:x+y
    else:
      r=1
      op=lambda x,y:x*y
    for mdl in self.tml:
       r=op(r,mdl.test_separated( mdl[0](A),
                           mdl[0](A),
                           log=log
                           *args,
                           **kwargs
                           )
            )
  def sample(self,n, *args, ** kwargs):
     """ I have not yet implemented sample for bagged model
         To compute the product distribution seems complicated 
         I put this for the moment that may generate relatively good candidates for the moment
     """
     print "warning : approximative sample function"
     tml=self.tml[:]
     random.shuffle(tml)
     value=numpy.array(tml[0][1](tml[0][2].sample(n, *args, ** kwargs)))
     print type(value)
     print value.shape
     for mdli in range(1,len(tml)):
         value=tml[mdli][1](tml[mdli][2].random_improve(tml[mdli][0](value),1./len(tml),1),value) 
         print type(value)
     return value
  def random_improve(self,value,amount=0.5,prec=1):
        """
          randomly improve along the different models respecting the queried amount
        """
        tml=self.tml[:]
        random.shuffle(tml)
        tp=[0] + [ random.random() for i in range(len(tml)-1) ] + [ amount ]
        tp.sort()
        for mdli in range(len(tml)):
          print "prec",prec
          value=tml[mdli][1](tml[mdli][2].random_improve(tml[mdli][0](value),tp[i+1]-tp[i],prec),value) 
        return value


class ShapePreservingModel:
    def __init__(self,instance):
          self.instance=instance
          self.shape=None
          self.shapeA=None
          self.shapeB=None
    def flatten(self,data,shape):
        if (isintance(data,numpy.ndarray)):
            return data.reshape(data.shape[0],scipy.prod(data.shape[1:]))
        else:
            ns=scipy.prod(shape)
            return numpy.array([ x.reshape((ns,)) for x in data  ])
    def unflatten(self,data,shape):
        if (isintance(data,numpy.ndarray)):
            return data.reshape((data.shape[0],)+shape)
        else:
            return numpy.array([ x.reshape(shape) for x in data ])
    def train(self,pos,neg=None,*args, **xargs):
        if (not self.shape):
            self.shape=pos[0].shape
        pos=self.flatten(pos, self.shape)
        if (neg):
            neg=self.flatten(neg, self.shape)
        return self.instance.train(pos,neg,*args, **xargs)
    def train_separated(self,pA,pB,nA=None,nB=None,*args, **xargs):
        if (not self.shapeA):
            self.shapeA=pA[0].shapeA[1:]
        if (not self.shapeB):
            self.shapeB=pB[1].shapeB[1:]
        pA=self.flatten(pA,self.shapeA)
        pB=self.flatten(pB,self.shapeB)
        if (nA):
            nA=self.flatten(nA,self.shapeA)
        if (nB):
            nB=self.flatten(nB,self.shapeB)            
        return self.instance.train_separated(pA,pB,nA,nB,*args, **xargs)
    def test(self,td,*args, **xargs):
        if (not self.shape):
            self.shape=td[0].shape
        td=self.flatten(td, self.shape)        
        return self.instance.test(td,*args, **xargs)
    def test_separated(self,tA,tB,*args, **xargs):
        if (not self.shapeA):
            self.shapeA=tA[0].shape
        if (not self.shapeB):
            self.shapeB=tB[0].shape
        tA=self.flatten(tA, self.shapeA)        
        tB=self.flatten(tB, self.shapeA)
        return self.instance.test_separated(tA,tB,*args, **xargs)
    def sample(self,*args, **xargs):
        return self.unflatten(self.instance.test(*args, **xargs), self.shape)

class TransformedModel():
    def __init__(self,f,finv,pmodel,burnin=None):
        self.f=f
        self.finv=finv
        self.pmodel=pmodel
        self.burnin=burnin
    def train(self,positive_training_set,negative_training_set=None, *args, **kwargs):
        if (self.burnin):
            self.f(positive_training_set)
            self.burnin-=positive_training_set.shape[0]
            if (self.burnin<=0):
                self.burnin=None
            if (self.burnin):
               return
        positive_training_set_r=self.f(positive_training_set)
        negative_training_set_r=None
        if (negative_training_set):
           negative_training_set_r=self.f(negative_training_set)
        self.pmodel.train(numpy.asarray(positive_training_set_r),negative_training_set_r and numpy.asarray(negative_training_set_r) or None, *args, **kwargs)
    def test(self,data,log=True):
        rdata=self.f(data)
        return self.pmodel.test(numpy.asarray(rdata),log)
    def sample(self,n=100):
        rdata=self.pmodel.sample(n)
        return self.finv(rdata)
    def dump(self,file_):
        self.pmodel.dump(file_)
    @staticmethod
    def load(file_,*args, **kwargs):
        assert(False)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
    def random_improve(self,value,amount=0.5, prec=1):
	return self.finv(self.pmodel.random_improve(self.f(value,amount,prec)))    


class WhitenedModel:
    def __init__(self,pmodel,whitener=None,burnin=20):
        self.pmodel=pmodel
        self.whitener=whitener or SimpleMeanVarianceModel()
        self.burnin=burnin
    def whiten(self,data):
        eps=1e-24
        data=data-self.whitener.mean()
        data/=(self.whitener.std()+eps)
        return data
    def unwhiten(self,data):
        data=data*self.whitener.std()
        data+=self.whitener.mean()
        return data
    def train(self,positive_training_set,negative_training_set=None, *args, **kwargs):
        if (self.burnin):
            self.whitener.train(positive_training_set)
            self.burnin-=positive_training_set.shape[0]
            if (self.burnin<=0):
                self.burnin=None
            if (self.burnin):
               return
        positive_training_set_r=self.whiten(positive_training_set)
        negative_training_set_r=None
        if (negative_training_set):
           negative_training_set_r=self.whiten(negative_training_set)
        self.pmodel.train(numpy.asarray(positive_training_set_r),negative_training_set_r and numpy.asarray(negative_training_set_r) or None, *args, **kwargs)
    def test(self,data,log=True):
        rdata=self.whiten(data)
        return self.pmodel.test(numpy.asarray(rdata),log)
    def sample(self,n=100):
        rdata=self.pmodel.sample(n)
        return self.unwhiten(rdata)
    def dump(self,file_):
        self.pickle(type(self.whitener),file_)
        self.whitener.dump(file_)
        self.pickle(type(pmodel),file_)
        self.pmodel.dump(file_)
        pickle.dump(self.burnin,file_)
    @staticmethod
    def load(file_,*args, **kwargs):
         wm=WhitenedModel(*args,**kwargs)
         wm.whitener=(pickle.load(file_)).load()
         wm.pmodel=(pickle.load(file_)).load()
         wm.burnin=pickle.load(file_)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
    def random_improve(self,value,amount=0.5, prec=1):
        return self.unwhiten(self.pmodel.random_improve(self.whiten(value),amount, prec))


