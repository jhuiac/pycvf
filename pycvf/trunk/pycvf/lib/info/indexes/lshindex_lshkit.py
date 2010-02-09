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
from pylsh import *
from pycvf.core.errors import pycvf_debug, pycvf_warning, pycvf_error
from pycvf.lib.info.indexes.filearray import *

import os, marshal,cPickle
import scipy.io 
import itertools

def to2d(i):
  s=i.shape
  return i.reshape(s[0],reduce(lambda x,y:x*y,s[1:],1))

class LshKitIndex():
    def __init__(self,distance=None):
            self._values=None
            self._keys=None
            self.distance=distance
            self.lshindex=None
    def add_many(self,keys,values):
        if (not self.distance):
          try:
            self._keys=to2d(keys).astype(numpy.float32).copy('C')
          except ValueError:
            pycvf_warning("Errors LSH keys must be dense float vector in this implementation of LshIndex")
            pycvf_warning(u"here an example of your keys "  +unicode(keys[0]))
            raise
          self._values=to2d(values)
        else:
          self._keys=to2d(keys)
          self._values=to2d(values)          
        self.lshindex=MPLSHIndex(self._keys)
    @staticmethod
    def load(filename):
        pycvf_debug(10,"load "+filename)
        r=LshKitIndex()
        f=file(filename+"-values.dat","rb")
        r._values=pickle.load(f)
        r._keys=scipy.io.loadmat(filename+"-keys.mat")["keys"].copy('C')
        r.lshindex=MPLSHIndex(r._keys)
        #print r._keys
        r.lshindex.load(filename+"-lsh.lsh")
        pycvf_debug(10,"/load "+filename)
        return r
    def save(self,filename):
        pycvf_debug(10, "saving lsh")
        pycvf_debug(10, "keys : " + str(self._keys))
        if (self._keys not in [None,[]]): 
          pickle.dump(self._values,file(filename+"-values.dat","wb"))
          scipy.io.savemat(filename+"-keys.mat",{"keys":self._keys})
          self.lshindex.save(filename+"-lsh.lsh")#,self._keys)
    def __getitem__(self,query):
        numelem=1
        if (not self.distance):        
          if (type(query) in [ int, float, long ] ) : 
             query=[query]
          nquery=numpy.asarray(query).astype(numpy.float32).copy('C')
        else:
          nquery=[query]
        qrk,qrd,qrc=self.lshindex.query(nquery,numelem,*args,**kwargs)
        ci=qrc[0]
        if ci<numelem:
          qrk[0]=numpy.array([numpy.randint(0,self._keys.shape[0]-1) for x in numelem])
          #qrd[0]=scipy.spatial.distance.cdist( nquery, self._values[qrk[0][0]] )
          #raise Exception
        return self._values[qrk[0][0]]
    def getitem(self,query,numelem=1, exact=False,*args,**kwargs):
        if (not self.distance):
          if (type(query) in [ int, float, long ] ) : 
             query=[query]
          nquery=to2d(numpy.asarray([query])).astype(numpy.float32).copy('C')
        else:
          nquery=to2d(numpy.asarray([query]))
        qrk,qrd,qrc=self.lshindex.query(nquery,numelem,*args,**kwargs)
        for c in range(qrc.shape[0]):
           ci=qrc[c]
           if ci<numelem:
              # if LSH did not return the good number of elements we add some random points
              qrk[c][ci:]=numpy.array([numpy.randint(0,self._keys.shape[0]-1) for x in numelem])
              qrd[c][ci:]=scipy.spatial.distance.cdist( nquery, self._values.take(qrk[c][ci:]) ] ) **2
              perm=qrd[c].argsort()
              qrd[c]=qrd[c].take(*perm)
              qrk[c]=qrk[c].take(*perm)
             #raise Exception               
           res+=[zip(map(lambda i:self._values[i], qrk[c]),qrd[c])]
        return res#numpy.vstack(res)        

    def getitems(self,queries,numelem=1, exact=False, *args, **kwargs):
        #pycvf_debug(10, "query getitems:"+str( queries))
        if (not self.distance):        
          if (type(queries[0]) in [ int, float, long ] ) : 
            queries=map(lambda x:[x],queries)
          nqueries=to2d(numpy.asarray(queries)).astype(numpy.float32).copy('C')
        else:          
          nqueries=to2d(numpy.asarray(queries))
        res=[]
        qrk,qrd,qrc=self.lshindex.query(nqueries,numelem,*args,**kwargs)
        for c in range(qrc.shape[0]):
           ci=qrc[c]
           if ci<numelem:
              # if LSH did not return the good number of elements we add some random points
              qrk[c][ci:]=numpy.array([numpy.randint(0,self._keys.shape[0]-1) for x in numelem])
              qrd[c][ci:]=scipy.spatial.distance.cdist( nquery, self._values.take(qrk[c][ci:]) ] ) **2
              perm=qrd[c].argsort()
              qrd[c]=qrd[c].take(*perm)
              qrk[c]=qrk[c].take(*perm)
             #raise Exception               
           res+=[zip(map(lambda i:self._values[i], qrk[c]),qrd[c])]
        return res#numpy.vstack(res)
    def keys(self):
        return iter(self._keys) if self._keys!= None else []
    def values(self):
        return iter(self._values) if self._values!= None else []
    def __len__(self):
        return self._keys.shape[0]
    def reset(self):
         try:
             os.mkdir(filename)
         except:
             pass
         self._values=None
         self._keys=None
         self.lshindex=MPLshIndex()
