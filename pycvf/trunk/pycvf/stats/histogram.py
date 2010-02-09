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
        
class StatModel:
   def __init__(self,  bins, base, delta):
      """
       Bins define the number of bins in each direction.
       Base define the position of the 0 element in the space
       Delta defines the length of the area that is under observation along each component
      """ 
      self.no=0
      self.a=numpy.zeros(bins,dtype=long)
      self.nbins=numpy.prod(bins)
      self.lnbins=int(numpy.ceil(numpy.log2(numpy.prod(bins))))
      self.pa=numpy.zeros(1<<self.lnbins,dtype=long)
      self.bins=bins
      if (type(bins) in [tuple, list, numpy.matrix] ):
          self.bins=numpy.array(bins,dtype=int)
      self.base=base
      if (type(base) in [tuple, list, numpy.matrix] ):
          self.base=numpy.array(base,dtype=float)
      self.delta=delta
      if (type(delta) in [tuple, list, numpy.matrix] ):
          self.delta=numpy.array(delta,dtype=float)
      self.ov=numpy.fliplr(numpy.fliplr(numpy.matrix(tuple(self.bins[1:].tolist())+(1,))).cumprod())
   def dump(self,file_):
      marshal.dump( self.bins.shape, file_)
      marshal.dump( self.bins, file_)
      marshal.dump( self.base.shape, file_)
      marshal.dump( self.base, file_)
      marshal.dump( self.delta.shape, file_)
      marshal.dump( self.delta, file_)
      #numpy.save(file_,a)
      #numpy.save(file_,pa)
      marshal.dump( self.a.shape, file_)
      marshal.dump( self.a, file_)
      marshal.dump( self.pa.shape, file_)
      marshal.dump( self.pa, file_) ## TODO : we may recompute this actually
   @staticmethod
   def load(file_, *args, **kwargs):
      bins_shp=marshal.load(file_)
      bins_buf=marshal.load(file_)
      bins=numpy.ndarray(buffer=bins_buf,shape=bins_shp,dtype=int)
      base_shp=marshal.load(file_)
      base_buf=marshal.load(file_)
      base=numpy.ndarray(buffer=base_buf,shape=base_shp,dtype=float)
      delta_shp=marshal.load(file_)
      delta_buf=marshal.load(file_)
      delta=numpy.ndarray(buffer=delta_buf,shape=delta_shp,dtype=float)
      m=HistogramModel(bins,base,delta)
      a_shp=marshal.load(file_)
      m.a=numpy.ndarray(buffer=marshal.load(file_), shape=a_shp ,dtype=long).copy()
      pa_shp=marshal.load(file_)
      m.pa=numpy.ndarray(buffer=marshal.load(file_), shape=pa_shp ,dtype=long).copy()
      #m.a=numpy.load(file_)
      #m.pa=numpy.load(file_)
      return m
   def _subscale(self,p,scale):
      # on insere des 1 à chaque au debut du chiffre binaire a chaque fois que l'on monte d'une coodonnées
      rp=0
      for i in range(scale-1):
        rp|=1
        rp<<=1
      ## puis on s'assure que l'on passe notr position au bon endroit...
      rp<<=(self.lnbins-scale)
      p>>=scale # on abaisse la precision nu,erique en fonction de l'échelle
      rp|=p
      return rp
   def subscale(self,p,scale):
      # on linearise les coordonnes
      p=numpy.dot(self.ov,numpy.matrix(p).T)[0,0]
      # on insere des 1 à chaque au debut du chiffre binaire a chaque fois que l'on monte d'une coodonnées
      rp=0
      for i in range(scale-1):
        rp|=1
        rp<<=1
      ## puis on s'assure que l'on passe notr position au bon endroit...
      rp<<=(self.lnbins-scale)
      p>>=scale # on abaisse la precision nu,erique en fonction de l'échelle
      rp|=p
      return rp
   def subscale_histo(self,scale):
       if (scale==0):
           return self.a
       else: 
           idxs=self._subscale(0,scale)
           idxd=self._subscale(self.nbins-1,scale)+1
           #print idxs, idxd
           return self.pa[idxs:idxd]
   def _online_train(self,obs):
      if (type(obs) in [ tuple, list, numpy.array, numpy.matrix] ):
        robs=obs-self.base
        dv=(robs*self.bins/self.delta).astype(int)
      #dv=self.ov.T*dv
      for x in dv:
         x=tuple(x.tolist())
         self.a[x]+=1
         for scale in range(1,self.lnbins):
           nx=self.subscale(x,scale)
           self.pa[nx]+=1
      self.no+=self.dv.shape[0]
   def train(self,obs,obsN=False,online=False):
      if ((obs==None) or len(obs)==0):
          sys.stderr.write("Learning : nothing to be learned...")
          return
      assert(not(obsN))
      if (not online):
        self.a.fill(0)
        self.pa.fill(0)
        self.no=0
      obs=numpy.array(obs)
      #print "obs train", obs.shape, self.base.shape, "obs=",obs
      assert(obs.ndim==2)
      #print obs.shape, self.base.shape
      robs=obs-self.base#.repeat(obs.shape[0],axis=1)
      dv=(robs*self.bins/self.delta).astype(int)
      #dv=numpy.dot(self.ov,dv.T)
      for x in dv:
         try:
           x=tuple(x.tolist())
           self.a[x]+=1
           for scale in range(1,self.lnbins):
             nx=self.subscale(x,scale)
             self.pa[nx]+=1
         except IndexError: 
           pass
      self.no+=dv.shape[0]
   def push_histogram(self,histo):
      for x in numpy.ndindex(histo.shape):
         self.a[x]+=histo[x]
         for scale in range(1,self.lnbins):
             nx=self.subscale(x,scale)
             self.pa[nx]+=histo[x]
   def online_train(self,*args,**kwargs):
       kwargs["online"]=True
       #print args[0](1), kwargs
       return self.train(*args,**kwargs)
   def test(self,obs,log=False):
      if obs==None:
        return 0
      try:
        self.ov+=0
        #print numpy.array(obs), "babar"
        if ((obs==None) or len(obs)==0):
            sys.stderr.write("I need observation to perform tests...")
            return 0
        #print "obs test", obs.shape
        dv=((numpy.array(obs)-self.base)*self.bins/self.delta).astype(int)
        #dv=numpy.dot(ov,dv.T)
        r=[]
        for x in dv:
          try:
            x=tuple(x.tolist())
            r.append(float(self.a[x]+1)/float(self.no+len(self.bins)))
          except IndexError:
            r.append(0)
        #print self.a.shape,dv,r, type(r)
        if (not log):
          r=numpy.matrix( [r]).T
          sys.stderr.write("res hist "+str(r)+"\n")
          return r
        else:
          r=numpy.log(numpy.matrix( [r]).T)
          sys.stderr.write("log res hist "+str(r)+"\n")
          return r
      except:
          sys.stderr.write("Exception during histogram test, returning 0\n")
          return 0
   def onesample(self):
      b=0
      for v in range(self.lnbins-2): # used to be -2
         scale=self.lnbins-2-v
         idxs=self._subscale(0,scale)
         b<<=1                     
         zp=self.pa[idxs+b]
         op=self.pa[idxs+b+1]
         #print self.subscale_histo(scale)
         #print "zp:",zp,"op:",op,"zp+op",zp+op, "b",b, idxs,  idxs+b, idxd, self.subscale_histo(scale).sum()
         if ((random.random()*(zp+op))>zp):
            b+=1
      b<<=1
      vb0=reduce(lambda x,y:  (x[0]//y,(x[1] + [x[0]%y]))  , self.bins, (b, []) )[1]
      vb1=reduce(lambda x,y:  (x[0]//y,(x[1] + [x[0]%y]))  , self.bins, (b+1, []) )[1]
      p0=self.a.__getitem__(tuple(vb0))
      p1=self.a.__getitem__(tuple(vb1))
      r=p0/(p0+p1)
      if ( random.random() > r):
     	return ((vb1)*self.delta/self.bins)+self.base
      else:
        return ((vb0)*self.delta/self.bins)+self.base
   def manysamples(self,numsamples):
       eps=1e-24
       def prepos(a,b): # we compute how far we are compared with the CDF
         return [ ((b<x).astype(int).sum()) for x in a ]
       #
       # to <- total number of elements
       to=self.subscale_histo(self.lnbins-1).sum()
       #
       # ok decide position
       rs=numpy.random.random((numsamples,))*to
       #rp=numpy.zeros((numsamples,))
       #
       # we compute the position up to last level -1
       rp=prepos(rs,self.subscale_histo(1).cumsum()) # we use cumsum to get the CDF
       ##
       ## we are now about to do latest steps to add some noise within the resuls...
       res=[]
       for b in rp:
         b<<=1
         vb0=reduce(lambda base,y:  (base[0]//y,(base[1] + [base[0]%y]))  , self.bins, (b, []) )[1]
         vb1=reduce(lambda base,y:  (base[0]//y,(base[1] + [base[0]%y]))  , self.bins, (b+1, []) )[1] 
         # print vb0
         p0=self.a.__getitem__(tuple(vb0))
         p1=self.a.__getitem__(tuple(vb1))
         r=float(p0+eps)/float(p0+p1+eps)
         if ( random.random() > r):
     	   res.append(vb1)
         else:
           res.append(vb0)
       res=numpy.array(res)
       return (res+numpy.random.random(res.shape))*self.delta/self.bins + self.base
              
#      b=0
#      tb=(1<<(self.lnbins))-3
#      for v in range(self.lnbins-2):
#         zp=self.pa[tb+b],
#         op=self.pa[tb+b+1]
#         b<<=1
#         if ((random.random()*(zp+op))>zp):
#            b+=1
#         tb-=(1<<(2+v))
#      b<<=1
# 
#      p0=self.a.__getitem__(tuple(vb0))
#      p1=self.a.__getitem__(tuple(vb1))
#      r=p0/(p0+p1)
#      if ( random.random() > r):
#     	return vb1
#      else:
#        return vb0
   def sample(self,numsamples=10):
       if (numsamples < self.nbins) :
         return numpy.array([self.onesample() for x in range(numsamples) ])
       else:
         return self.manysamples(numsamples)
   def memory_cost(self, *args, **kwargs):
        assert(False)
   def cpu_cost(self, *args, **kwargs):
        assert(False)
   def random_improve(self,value,amount=0.5, prec=1):
        ## look at for in with higher probability in surrounding area
        print "random_improve not yet implemented doing sample instead !!! hist"
        return self.sample(value.shape[0])
        assert(False)   

__call__=StatModel