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

import sys,numpy,time
from pycvf.lib.info import persistent
from pycvf.core.errors import *

from scipy import cluster
from scipy import spatial
from scipy import stats

class BagOfWords(persistent.PersistentObject):
  ### aka histograms upon vectorial quantization
  """
  """
  def __init__(self,categories,burnin=2000, 
               vocabulary=None, 
               clustering="kmean", 
               clusteringargs=(),
               describer="histogram",
               describerargs=(),
               algo=0, 
               *args,
               **kwargs):
     self.burnin=burnin
     self.categories=(vocabulary) and len(vocabulary) or categories
     self.vocabulary=vocabulary
     self.labels=[]
     self.te=[]
     self.args=args
     self.kwargs=kwargs
     #print "BAGOFWORDS CREATED!", len(self.te),"/",self.burnin
     self.algo=algo
     self.algos=[self.algo0,self.algo1,self.algo2]
  def algo0(self,r):
     """ simply return histogram of distance to the closest element in vocabulary
         r is the distance matrix on the queries
     """
     return numpy.histogram(r.argmin(axis=1),self.categories,range=(0,self.categories),normed=True)[0]
  def algo1(self,r):
     """ simply return an histogram of distance to the 3 closest elements in vocabulary ,and arbitrary weighting"""
     rag=r.argsort(axis=1)
     return (1*numpy.histogram(rag[:,0],self.categories,range=(0,self.categories),normed=True)[0]
            +0.5*numpy.histogram(rag[:,1],self.categories,range=(0,self.categories),normed=True)[0]
            +0.25*numpy.histogram(rag[:,2],self.categories,range=(0,self.categories),normed=True)[0]    
            )
  def algo2(self,r):
     """ simply return an histogram of distance to the 3 closest elements in vocabulary ,and weighting done accordingly to the elements"""
     rag=r.argsort(axis=1)
     d1=r[rag[:,0]]
     d2=r[rag[:,1]]
     d3=r[rag[:,2]]
     e1=1/(1+d1)
     e2=1/(1+d2)
     e3=1/(1+d3)
     es=e1+e2+e3
     c1=e1/es
     c2=e2/es
     c3=e3/es
     return (c1*numpy.histogram(rag[:,0],self.categories,range=(0,self.categories),normed=True)[0]
            +c2*numpy.histogram(rag[:,1],self.categories,range=(0,self.categories),normed=True)[0]
            +c3*numpy.histogram(rag[:,2],self.categories,range=(0,self.categories),normed=True)[0]    
            )
  def get_status():
      return (STATUS_READY if self.vocabulary!=None else STATUS_NOT_READY)
  def push(self,entries):
    if (entries)==None:
      return None
    if (self.vocabulary==None):
     #print "BAGOFWORDS PUSH NV!", len(self.te),"/",self.burnin, type(entries), entries.shape, self
     try:
       maxe=self.burnin-len(self.te)
       if (type(entries)==numpy.ndarray):
          entries=entries.tolist()
       self.te.extend(filter (lambda x:x!=None,entries))
       if (len(self.te)>=self.burnin):
          x=cluster.vq.kmeans2(numpy.array(self.te).squeeze(), self.categories)
          self.vocabulary=x[0]
       self.dirty=True 
     except Exception,ex:
        print ex,numpy.array(self.te).ndim, numpy.array(self.te).shape
    else:
       #print "BAGOFWORDS PUSH GV!", len(self.te),"/",self.burnin, type(entries), entries.shape
       if (type(entries)==numpy.ndarray):
         if (entries.shape[0]==0):
           sys.stderr.write("bagofwords: maybe strange... no entry in bag of words...")
           return numpy.zeros((self.categories,))
         assert(entries[0]!=None)
       else:
         if (len(entries))==0:
           sys.stderr.write("bagofwords: maybe strange... no entry in bag of words...")
           return numpy.zeros((self.categories,))
       if entries[0]==None:
           pycvf_warning("bagofwords: maybe strange... none in bag of words...")
           return numpy.zeros((self.categories,))
       try:
         r=spatial.distance.cdist(entries,self.vocabulary)
         #r=stats.histogram(r.argmin(axis=1),self.categories,defaultlimits=(0,self.categories),normed=True)[0]         
         r=self.algos[self.algo](r)
         return r
       except:
         print "entries,shape/voc.shape=", entries.shape, self.vocabulary.shape
         #print "entries=", repr(entries)
         #print "vocabulary=", repr(self.vocabulary)
         raise 
  def cluster_kmeans(self,tes,categ):
     return cluster.vq.kmeans2(tes, self.categories)[0]
     
     
class WeightedBagOfWords(BagOfWords):
  def __init__(self,categories, walgo=0, *args,**kwargs):
     super(WeightedBagOfWords,self).__init__(categories,*args,**kwargs)
     self.walgo=walgo
     self.walgos=[self.walgo0,self.walgo1]
  def walgo0(self,weights,r):
     """ simply return histogram of distance to the closest element in vocabulary"""
     return numpy.histogram(r.argmin(axis=1),self.categories,range=(0,self.categories),weights=weights,normed=True)[0]
  def walgo1(self,r):
     """ simply return an histogram of distance to the 3 closest elements in vocabulary ,and arbitrary weighting"""
     rag=r.argsort(axis=1)
     return (1*numpy.histogram(rag[:,0],self.categories,range=(0,self.categories),weights=weights,normed=True)[0]
            +0.5*numpy.histogram(rag[:,1],self.categories,range=(0,self.categories),weights=weights,normed=True)[0]
            +0.25*numpy.histogram(rag[:,2],self.categories,range=(0,self.categories),weights=weights,normed=True)[0]    
            )
  def push(self,weights,entries):
    if (entries)==None:
      return None
    if (self.vocabulary==None):
     try:
       maxe=self.burnin-len(self.te)
       if (type(entries)==numpy.ndarray):
          entries=entries.tolist()
       self.te.extend(filter (lambda x:x!=None,entries))
       if (len(self.te)>=self.burnin):
          tes=numpy.array(self.te).squeeze()
          x=cluster.vq.kmeans2(tes, self.categories)
          self.vocabulary=x[0]
       self.dirty=True 
     except Exception,ex:
        print ex,numpy.array(self.te).ndim, numpy.array(self.te).shape
    else:
       if (type(entries)==numpy.ndarray):
         if (entries.shape[0]==0):
           sys.stderr.write("maybe strange... no entry in bag of words...")
           return numpy.zeros((self.categories,))
         assert(entries[0]!=None)
       else:
         if (len(entries))==0:
           sys.stderr.write("maybe strange... no entry in bag of words...")
           return numpy.zeros((self.categories,))
       if entries[0]==None:
           sys.stderr.write("maybe strange... none in bag of words...")
           return numpy.zeros((self.categories,))
       try:
         r=spatial.distance.cdist(entries,self.vocabulary)
         r=self.walgos[self.walgo](weights,r)
         return r
       except:
         print "entries,shape/voc.shape=", entries.shape, self.vocabulary.shape
         raise 


