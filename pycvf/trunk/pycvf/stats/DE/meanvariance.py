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

from pycvf.core.errors import pycvf_warning        

class StatModel():
    ## well this is a simple mean variance model
   def __init__(self):
       self.no=0
       self.so=0
       self.svc=0
   def get_as_vector(self):
      return numpy.hstack([self.mean(), self.std()])
   def mean(self):
       return self.so/float(self.no)
   def std(self):
       return ((self.svc/float(self.no))-self.mean()**2)**.5
   def var(self):
       return ((self.svc/float(self.no))-self.mean()**2)
   def train(self,tp,tn=None,online=False, *args, **kwargs):
       if (online):
           self.train_online(tp,tn,*args,**kwargs)
       else:
           self.train_offline(tp,tn,*args,**kwargs)
   def train_offline(self,tset,tnset=None):
       if (hasattr(tset,"dtype") and tset.dtype in [numpy.uint8, numpy.int8,numpy.uint16, numpy.int16 ,numpy.uint32, numpy.int32  ] ):
          tset=tset.astype(numpy.int64)
       else:
          tset=numpy.array(tset)
       self.no=len(tset)
       self.so=reduce(lambda x,y: x+y,tset, 0 )
       self.svc=reduce(lambda x,y: x+y**2,tset, 0 )
   def train_online(self,tset,tnset=None):
       if (hasattr(tset,"dtype") and tset.dtype==object):
           pycvf_warning("pushing object array of online train !!!")
           tset=map(lambda x:x,tset.flat)
       if (hasattr(tset,"dtype") and tset.dtype in [numpy.uint8, numpy.int8,numpy.uint16, numpy.int16 ,numpy.uint32, numpy.int32 ,object ] ):
          if tset.dtype in [numpy.uint8, numpy.int8,numpy.uint16, numpy.int16 ,numpy.uint32, numpy.int32 ]: 
            tset=tset.astype(numpy.int64)
          else:
            print tset[0]
            if (type(tset)==list):
               tset=map(lambda x:x.astype(numpy.float64),tset)
            else:
               print type(tset)
               print tset.dtype
               assert(False) 
       else:
         try:
           tset=map(lambda x:x.astype(numpy.float64),tset)
         except:
           pass
       tset=numpy.array(tset)#
       self.no+=len(tset)
       self.so+=reduce(lambda x,y: x+y,tset, 0 )
       self.svc+=reduce(lambda x,y: x+y**2,tset, 0 )
   def testmap(self,tset,log=False):
       if (not self.no):
           print "SimpleMeanVariance model should be trained before any use"
           return 0
       if (log):
         return -(tset-self.mean())**2/(2*self.var()+1e-24)
       else:
         v=self.var()
         v1=-(tset-self.mean())**2/(2*v+1e-24)
         #print dir(numpy)
         #print v1.shape
         v1=numpy.exp(tset)
         return 1./(numpy.pi*(2*v)**.5) * v1
   def test(self,tset,log=False):
       print "###TEST NO=",self.no
       if (not self.no):
           print "SimpleMeanVariance model should be trained before any use"
           return 0
       if (log):
         return -((tset-self.mean())**2/(2*self.var()+1e-24)).mean(axis=1)
       else:
         v=self.var()
         v1=-(tset-self.mean())**2/(2*v+1e-24)
         print v1.shape
         print v1
         v1=v1.astype(float)
         v1=numpy.exp(v1).mean(axis=1)
         return (1./(numpy.pi*(2*v.mean())**.5) * v1)
   def sample(self,nsamples=100):
       a=(self.so/self.no) # moyenne
       b= numpy.random.random(((nsamples,)+self.so.shape)) * (((self.svc/self.no)).astype(float)**(1./2.)-(self.so/self.no)) # ecart type
       #print a.shape
       #print b.shape
       return b+a
   def memory_cost(self, *args, **kwargs):
       return len(self.so)
   def cpu_cost(self, *args, **kwargs):
       return 1
   def dump(self,file_):
      marshal.dump(self.no,file_)  
      #marshal.dump(self.so,file_)
      #marshal.dump(self.svc,file_)
      pickle.dump(self.so,file_,protocol=2)
      pickle.dump(self.svc,file_,protocol=2)
      #pickle.dump( self,file_)
      #pickle.dump(self.no,file_)
      #if (isinstance(self.so,numpy.ndarray)):
      #   pickle.dump(self.no)
   @staticmethod
   def load(file_, *args , ** kwargs):
      m=SimpleMeanVarianceModel()
      m.no=marshal.load(file_)
      m.so=pickle.load(file_)
      m.svc=pickle.load(file_)
      return m
      #return pickle.load(file_)
   def random_improve(self,value,amount=0.5, prec=1):
      ## prec is not used here
      assert(amount>=0.)
      assert(amount<=1.)
      return (amount*value) + ((1.-amount)*self.mean())

__call__=StatModel
