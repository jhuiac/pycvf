# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database for Training
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
################################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import basics
import numpy

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
def udist(npoints, center, radius):
   """ generate npoints from uniform distribution within a cube centered on center with radius radius """
   return ((numpy.random.random((npoints,len(center)))-0.5)*radius+numpy.array(center))

def gdist(npoints, center, radius):
   """ generate npoints from gaussian distribution centered on center with radius radius """
   return numpy.random.normal(center,radius,(npoints,len(center)))

class DB(database.ContentsDatabase,basics.NumericVector.Datatype):
   def __init__(self, npoints_per_clusters=100, clusters=10, ndim=4, sigma=0.12, space_size=20, seed=None, shuffled=True):
     self.NE=npoints_per_clusters
     self.nclusters=clusters
     self.ndim=ndim
     self.sigma=sigma
     self.space_size=space_size
     self.shuffled=shuffled
     if (seed!=None):
       numpy.random.seed(seed)
     self.data=numpy.vstack([gdist(self.NE,tuple([numpy.random.randint(0,self.space_size) for x in range(ndim)]),self.sigma) for i in range(self.nclusters)])
     self.gtdata=reduce(lambda x,y:x+[y]*self.NE ,range(self.nclusters),[])
   def __iter__(self):
       r=range(len(self))
       if (self.shuffled):
          numpy.random.shuffle(r)
       for x in r:
           #print self.data.shape
           yield (self.data[x,:],x)
   def __getitem__(self,key):
      return self.data[key]
   def __len__(self):
      return self.data.shape[0]
   def labeling_clusterid(selfdb):
        import unicodedata
        class Labels:
            @staticmethod
            def datatype():
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
             r=range(len(selfdb))
             if (self.shuffled):
               numpy.random.shuffle(r)
             for x in r:
               yield (selfdb.gtdata[x],x)
            @staticmethod
            def __getitem__(x):        
                assert(x!=None)        
                return selfdb.gtdata[x]
        return Labels()      
# Framework 2 compatibility
ContentsDatabase=DB
__call__=DB