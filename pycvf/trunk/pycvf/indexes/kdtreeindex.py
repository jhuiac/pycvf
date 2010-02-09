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

import numpy
import scipy.io
from scipy.spatial import KDTree
import cPickle as pickle

def to2d(i):
  s=i.shape
  return i.reshape(s[0],reduce(lambda x,y:x*y,s[1:],1))

class KDTreeIndex():
    def __init__(self):
            #from opencv import cv
            #self.cv=cv
            self.values=None
            self.keys=None
            #self.lshindex=cv.cvCreateMemoryLSH(d, n)
            self.tree=None
    def add_many(self,keys,values):
        assert(self.tree==None)
        self.keys=to2d(keys).astype(numpy.float32)
        self.values=to2d(values)
        self.tree=KDTree(self.keys)
    @staticmethod
    def load(filename):
        r=KDTreeIndex()
        f=file(filename+"-values.dat","rb")
        r.values=pickle.load(f)
        r.keys=scipy.io.loadmat(filename+"-keys.mat")["keys"].astype(numpy.float64).copy('C')
        r.tree=KDTree(r.keys)
        return r
    def save(self,filename):
        print "saving kdt"
        pickle.dump(self.values,file(filename+"-values.dat","wb"))
        scipy.io.savemat(filename+"-keys.mat",{"keys":self.keys})
        #self.sashindex.save(filename+"-sash.sash")#,self.keys)
    def __getitem__(self,query):
        if (type(query) in [ int, float, long ] ) : 
           query=[query]
           return self.getitem(query)[0]
        else:
           if ((type(query)==numpy.ndarray) and ((query.ndim==1) or  (query.shape[0]==1))):
               return self.getitem(query)[0]
           else:
               return self.getitem(query)
    def getitem(self,query,numelem=1, *args, **kwargs):
        if (type(query) in [ int, float, long ] ) : 
           query=[query]
        nquery=numpy.asmatrix(query).astype(numpy.float64, *args, **kwargs)
        distv,indicesv=self.tree.query(nquery,numelem)
        r=[]
        for y in range(indicesv.shape[0]):
          tr=[]
          for x in range(indicesv.shape[1]):
	    tr.append((self.values[indicesv[y,x]],distv[y,x]))
          r.append(tr)
        return r
    @staticmethod
    def __tex__(o):
        return "KDTREEs"    
