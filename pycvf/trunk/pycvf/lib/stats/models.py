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

# import elefant.crf
# import mvpa
# import mdp
##
## random random_improve(amount,prec)
##


class LineSearch:
    def __init__(self,va,k=2):
        self.va=numpy.array(va)
        self.va=self.va.reshape(scipy.prod(self.va.shape))
        self.va=self.va.copy()
        scipy.sort(self.va)
        self.k=k
    def _query(self,lv,k=None):
        if (k==None):
          k=self.k
        if (type(lv)!=numpy.ndarray):
            lv=numpy.array(lv)
        if (lv.ndim==1):
            lv=lv.reshape(1,lv.shape[0])
        if (lv.shape[0]==1):
          dt=abs(self.va.reshape(self.va.shape[0],1)-lv).T
          dr=scipy.argsort(dt)[0,:k]
          return numpy.vectorize(lambda x:self.va[x])(dr).reshape(1,k)
        else:
          dt=scipy.spatial.distance.cdist(lv,self.va.reshape(self.va.shape[0],1))
          dr=scipy.argsort(dt)[:,:k]
          return numpy.vectorize(lambda x:self.va[x])(dr)
    def xquery(self,lv,k=None):
        """ returns distance and element """
        if (k==None):
          k=self.k
        if (type(lv)!=numpy.ndarray):
            lv=numpy.array(lv)
        if (lv.ndim==1):
            lv=lv.reshape(1,lv.shape[0])
        if (lv.shape[0]==1):
          dt=abs(self.va.reshape(self.va.shape[0],1)-lv).T
          dr=scipy.argsort(dt)[0,:k]
          return dt.take(dr),numpy.vectorize(lambda x:self.va[x])(dr).reshape(k)
        else:
          dt=scipy.spatial.distance.cdist(lv,self.va.reshape(self.va.shape[0],1))
          dr=scipy.argsort(dt)[:,:k]
          return dt.take(dr),numpy.vectorize(lambda x:self.va[x])(dr)
    def query(self,lv,k=None):
        """ returns distance and element index"""
        if (k==None):
          k=self.k
        if (type(lv)!=numpy.ndarray):
            lv=numpy.array(lv)
        if (lv.ndim==1):
            lv=lv.reshape(1,lv.shape[0])
        if (lv.shape[0]==1):
          dt=abs(self.va.reshape(self.va.shape[0],1)-lv).T
          dr=scipy.argsort(dt)[0,:k]
          return dt.take(dr),dr.reshape(k)
        else:
          dt=scipy.spatial.distance.cdist(lv,self.va.reshape(self.va.shape[0],1))
          dr=scipy.argsort(dt)[:,:k]
          return dt.take(dr),dr

from pycvf.lib.stats.orangemodel import *
from pycvf.lib.stats.meanvariancemodel import *
from pycvf.lib.stats.histogrammodel import *
from pycvf.lib.stats.parzenmodel import *
from pycvf.lib.stats.pyemgmmmodel import *
from pycvf.lib.stats.pyem2gmmmodel import *
from pycvf.lib.stats.bayesianmodel import *
from pycvf.lib.stats.conditionalmodel import *
from pycvf.lib.stats.complexmodel import *
from pycvf.lib.stats.cachedmodel import *
from pycvf.lib.stats.dimreducedmodel import *
from pycvf.lib.stats.miscmodels import *            
         
        
        
#    basetree = orngTree.TreeLearner(mForPruning=2, name="tree") 
#    bstree = orngEnsemble.BoostedLearner(basetree, name="boosted tree") 
#    bgtree = orngEnsemble.BaggedLearner(basetree, name="bagged tree",t=5) 
#    baseknn = orange.kNNLearner(name="5-nn",k=2) 
#    bsknn = orngEnsemble.BoostedLearner(baseknn, name="boosted 5nn") 
#    bgknn = orngEnsemble.BaggedLearner(baseknn, name="bagged 5nn",t=5) 



