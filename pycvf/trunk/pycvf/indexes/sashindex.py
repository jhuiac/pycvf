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

from pycvf.core.errors import pycvf_debug, pycvf_warning, pycvf_error
from pycvf.core.distribution import *
pycvf_dist(PYCVFD_REQUIRE_PACKAGE,'pysash')
pycvf_dist(PYCVFD_SPECIFIC_LICENSE,"Sash is patented and is not under LGPL-3. Please refer at the Sash documentation. Do not use in any commercial application.")

from pysash import *

from pycvf.indexes.filearray import *

import os, marshal,cPickle
import scipy.io 
import itertools, time

class CachedSashIndex():
    def __init__(self,filename,keysz,valuesz,distance=None):
        self.filename=filename
        self.distance=distance
        try: 
            os.stat(filename)
            self._values=FileArray(filename+"/values.tbl",valuesz)
            self._keys=FileArray(filename+"/keys.tbl",keysz)
            self.sashindex=Sash(filename+"/index",self._keys)
            print filename+" sash successfully loaded"
        except:
            try:
               os.mkdir(filename)
            except:
               pass
            self._values=FileArray(filename+"/values.tbl",valuesz)
            self._keys=FileArray(filename+"/keys.tbl",keysz)
            if (self.distance):
               self.sashindex=GenericSash(self.distance)                
            else:
               self.sashindex=Sash()            
    def reset(self):
         try:
             os.mkdir(filename)
         except:
             pass
         self._values=FileArray(filename+"/values.tbl",valuesz)
         self._keys=FileArray(filename+"/keys.tbl",keysz)
         self.sashindex=Sash()
    def __del__(self):
        self.save()
    def add_many(self,keys,values):
        #assert(self._values==None) # SASH INDEX IS NOT INCREMENTAL
        #assert(self._keys==None) # SASH INDEX IS NOT INCREMENTAL
        self._values.appenditems(values)
        self._keys.appenditems(keys)
        self.sashindex.build(keys.astype(numpy.float32))
    def __getitem__(self,query):
        return self.sashindex.getitem(query)[0]
    def getitem(self,query,numelem=1):
        nquery=numpy.asarray(query).squeeze().astype(numpy.float32)
        #print nquery, nquery.shape
        self.sashindex.findNear(nquery,numelem)
        return zip(map(lambda i :self._values[i], self.sashindex.getResultIndices(numelem).tolist()),self.sashindex.getResultDists(numelem).tolist())
    def save(self):
        self.sashindex.save(filename+"/sash",self._keys)
    def keys(self):
        return iter(self._keys)
    def __len__(self):
        return self.sashindex.getNumItems()
    def values(self):
        return iter(self._values)
    @staticmethod
    def __tex__(o):
        o.put_bib(os.environ["JFLIPATH"]+"/pycvf.indexes/sashindex.bib")
        return "\\cite{Houle}"

def to2d(i):
  s=i.shape
  return i.reshape(s[0],reduce(lambda x,y:x*y,s[1:],1))

class SashIndex(object):
    def __init__(self,distance=None):
            self._values=None
            self._keys=None
            self.distance=distance
            if (distance):
               self.sashindex=GenericSash(distance)                
            else:
               self.sashindex=Sash()
    def add_many(self,keys,values):
        print "checking empty sash"
        assert(self._values==None) # SASH INDEX IS NOT INCREMENTAL
        assert(self._keys==None) # SASH INDEX IS NOT INCREMENTAL
        if (not self.distance):
          try:
            self._keys=to2d(keys).astype(numpy.float32).copy('C')
          except ValueError:
            pycvf_warning("Errors SASH keys must be dense float vector in this implementation of SashIndex")
            pycvf_warning(u"here an example of your keys "  +unicode(keys[0]))
            raise
          #print type(values), values#,values[0]
          self._values=to2d(values)
          #print "shapes : ", self._keys.shape, self._values.shape
        else:
          self._keys=to2d(keys)
          self._values=to2d(values)          
        self.sashindex.build(self._keys)
        #print "/built"
    @staticmethod
    def load(filename):
        pycvf_debug(10,"load "+filename)
        r=SashIndex()
        f=file(filename+"values.dat","rb")
        r._values=pickle.load(f)
        r._keys=scipy.io.loadmat(filename+"keys.mat")["keys"].copy('C')
        r.sashindex=Sash()
        #print r._keys
        r.sashindex.build(r._keys,filename=filename+"index")
        pycvf_debug(10,"/load "+filename)
        return r
    def save(self,filename):
        pycvf_debug(10, "saving sash")
        pycvf_debug(10, "keys : " + str(self._keys.shape) +":"  + str(self._keys))
        if (self._keys not in [None,[]]): 
          pickle.dump(self._values,file(filename+"values.dat","wb"))
          scipy.io.savemat(filename+"keys.mat",{"keys":self._keys})
          self.sashindex.save(filename+"index")#,self._keys)
    def __getitem__(self,query):
        if (not self.distance):        
          if (type(query) in [ int, float, long ] ) : 
             query=[query]
          nquery=numpy.asarray(query).astype(numpy.float32).copy('C')
        else:
          nquery=[query]
        self.sashindex.findNearest(nquery,1)
        rl=map(lambda i :self._values[i], self.sashindex.getResultIndices(1).tolist())
        return rl[0]
    def getitem(self,query,numelem=1, exact=False,*args,**kwargs):
        if (not self.distance):
          if (type(query) in [ int, float, long ] ) : 
             query=[query]
          nquery=to2d(numpy.asarray([query])).astype(numpy.float32).copy('C')
        else:
          nquery=to2d(numpy.asarray([query]))
        if (exact): 
           self.sashindex.findNearest(nquery[0],numelem,*args,**kwargs)
        else:
           self.sashindex.findNear(nquery[0],numelem,*args,**kwargs)
        return zip(map(lambda i :self._values[i], self.sashindex.getResultIndices(numelem).tolist()),self.sashindex.getResultDists(numelem).tolist())
    def getitems(self,queries,numelem=1, exact=False, *args, **kwargs):
        #pycvf_debug(10, "query getitems:"+str( queries))
        #time.sleep(10)
        if (not self.distance):        
          if (type(queries[0]) in [ int, float, long ] ) : 
            queries=map(lambda x:[x],queries)
          nqueries=to2d(numpy.asarray(queries)).astype(numpy.float32).copy('C')
        else:          
          nqueries=to2d(numpy.asarray(queries))
        res=[]
        for r in range(nqueries.shape[0]):
          if (exact): 
            self.sashindex.findNearest(nqueries[r],numelem,*args,**kwargs)
          else:
            self.sashindex.findNear(nqueries[r],numelem,*args,**kwargs)
          #print self._values.shape, self.sashindex.getResultIndices(numelem).tolist(), self.sashindex.getResultDists(numelem).tolist()
          res+=[zip(map(lambda i :self._values[i], self.sashindex.getResultIndices(numelem).tolist()),self.sashindex.getResultDists(numelem).tolist())]
        return res#numpy.vstack(res)
    def keys(self):
        return iter(self._keys) if self._keys!= None else []
    def values(self):
        return iter(self._values) if self._values!= None else []
    def __len__(self):
        return self.sashindex.getNumItems()
    def reset(self):
         try:
             os.mkdir(filename)
         except:
             pass
         self._values=None
         self._keys=None
         self.sashindex=Sash()
    @staticmethod
    def __tex__(o):
        o.put_bib(os.environ["JFLIPATH"]+"/pycvf.indexes/sashindex.bib")
        return "\\cite{Houle}"    

__call__=SashIndex
load=SashIndex.load
