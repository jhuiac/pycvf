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

from pycvf.core.errors import *
import numpy
import scipy.io
import cPickle as pickle

def to2d(i):
  s=i.shape
  return i.reshape(s[0],reduce(lambda x,y:x*y,s[1:],1))

class LshIndex():
    def __init__(self,n=10000):
            try:
              import zopencv
              cv=None
            except:
              zopencv=None
              try:
                from opencv_orig import cv
              except:
                try:
                  from opencv import cv
                except:
                  cv=None
            self.cv=cv
            self.zcv=zopencv
            self._values=None
            self._keys=None
            self.lshindex=None
            self.n=n
    def add_many(self,keys,values):
        self._keys=to2d(keys).astype(numpy.float64)
        self._values=to2d(values)
        d=self._keys.shape[1]
        print d,self.n,self._keys.shape
        if (self.cv):
          self.lshindex=self.cv.cvCreateMemoryLSH(d, self.n)
        else:
          self.lshindex=self.zcv.cvCreateMemoryLSH(d, self.n,10, 10,self.zcv.CV_64FC1, 4.,-1 )
	if (self.cv):
          self.cv.cvLSHAdd(self.lshindex,self._keys)
        else:
          self.zcv.cvLSHAdd(self.lshindex,self._keys)
    def keys(self):
        return iter(self._keys) if self._keys!= None else []
    def values(self):
        return iter(self._values) if self._values!= None else []
    def reset(self):
         self._values=None
         self._keys=None
         self.lshindex=None 
    @staticmethod
    def load(filename):
        r=LshIndex()
        pycvf_debug(10,"about to load values (1)")
        f=file(filename+"-_values.dat","rb")
        pycvf_debug(10,"about to load values")
        r._values=pickle.load(f)
        pycvf_debug(10,"about to load keys")
        r._keys=scipy.io.loadmat(filename+"-_keys.mat")["keys"].astype(numpy.float64).copy('C')
        pycvf_debug(10,"creating memory LSH")
	r.lshindex=r.cv.cvCreateMemoryLSH(r._keys.shape[1], r._keys.shape[0])
	print r._keys.shape, r._keys.dtype
        pycvf_debug(10,"adding the values")
        r.cv.cvLSHAdd(r.lshindex,r._keys)
        #r.lshindex.r._keys,filename=filename+"-lsh.lsh")
        return r
    def save(self,filename):
        print "saving lsh"
        pickle.dump(self._values,file(filename+"-_values.dat","wb"))
        scipy.io.savemat(filename+"-_keys.mat",{"keys":self._keys})
        #self.sashindex.save(filename+"-sash.sash")#,self._keys)
    def __getitem__(self,query):
        pycvf_debug(10, "__getitem__:"+str( query))
        if (type(query) in [ int, float, long ] ) : 
           query=[query]
           return self.getitem(query)[0]
        else:
           if ((type(query)==numpy.ndarray) and ((query.ndim==1) or  (query.shape[0]==1))):
               return self.getitem(query)[0]
           else:
               return self.getitem(query)
    def getitem(self,query,numelem=1,k0=1):
        #pycvf_debug(10, "query getitem:"+str( query))
        if (type(query) in [ int, float, long ] ) : 
           #query=[query]
           nquery=to2d(numpy.asarray([query])).astype(numpy.float64).copy('C')
        else:
           nquery=to2d(numpy.asarray(query)).astype(numpy.float64).copy('C')
        print nquery 
        #nquery=numpy.asmatrix(query).astype(numpy.float64)
        #indices=numpy.zeros((nquery.shape[0],) ,dtype=numpy.int64)
        #dist=numpy.zeros((nquery.shape[0],) ,dtype=numpy.float64)
        indicesv,distv=self.cv.cvLSHQuery(self.lshindex, nquery, k0,numelem)
        #print nquery, nquery.shape
        #self.sashindex.findNear(nquery,numelem)
        from opencv.adaptors import Ipl2NumPy
	indicesv=Ipl2NumPy(indicesv)
        distv=Ipl2NumPy(distv)
        return zip(map(lambda i :self._values[i], indicesv),distv)
    def getitems(self,query,numelem=1,*args):
        pycvf_debug(10, "query getitems:"+str( query))
        #nquery=numpy.asmatrix(query).astype(numpy.float64)
        nquery=to2d(numpy.asarray(query)).astype(numpy.float64).copy('C')
        indicesv,distv=self.cv.cvLSHQuery(self.lshindex, nquery, k0,numelem)
        from opencv.adaptors import Ipl2NumPy
        indicesv=Ipl2NumPy(indicesv)
        distv=Ipl2NumPy(distv)
        return zip(map(lambda i :self._values[i], indicesv),distv)
     
    def __len__(self):
         return (self._keys.shape[0] if self._keys!=None else 0)
    @staticmethod
    def __tex__(o):
        o.put_bib(os.environ["JFLIPATH"]+"/pycvf.lib.info/indexes/lshindex.bib")
        return "\\cite{DatarLSH}"    
