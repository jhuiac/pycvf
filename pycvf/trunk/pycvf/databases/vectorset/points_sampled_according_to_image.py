# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
################################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import datapoints2d
from pycvf.stats.DE.histogram import StatModel as HistogramModel
import numpy, random

class DB(database.ContentsDatabase):
   """
   This database returns a set of 2d points that are distributed according to an input
   image coming from an inputdatabase when this input database is considered as 
   a Probability Density Function.
   
   
   """
   def datatype(self):
       return datapoints2d.Datatype
   def __init__(self, parent_database, npoints_per_clusters=1000):
     self.NE=npoints_per_clusters
     self.parent_database=parent_database
   def __iter__(self):
       for x in self.parent_database:
           img=x[0]
           if img.ndim==3:
             img=img.mean(axis=2)
           assert(img.ndim==2)
           img=numpy.flipud(img).T
           h=HistogramModel( (img.ravel().shape[0],), (0,), (img.ravel().shape[0],) )
           h.push_histogram(img.ravel())
           rp=h.sample(self.NE).astype(int)
           w=img.shape[1]
           rp=numpy.array(map(lambda x:(x//w,x%w),rp)).squeeze()
           yield (rp,x[1])
   def __getitem__(self,key):
        v=self.parent_database.key()
   def __len__(self):
      return len(self.parent_database)

# Framework 2 compatibility
ContentsDatabase=DB
__call__=DB