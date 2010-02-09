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
  
  
class MarkovModel():
    """ 
     When we face a complex model/markov model/field.
     It means that we do observations according to different sets of cliques.
     To each clique_set is associated a different model
    """
    class CliquesSet:
        def __init__(self,enumeratef,model,recomposef0=None,recomposef1=None):
            self.enumeratef=enumeratef
            self.recomposef0=recomposef0
            self.recomposef1=recomposef1
            self.model=model
        def enumerate(self,obj):
            return self.enumeratef(obj)
        def train(self,obj,*args,**kwargs):
            self.model.train(self.enumeratef(obj),*args,**kwargs)
        def test(self,obj,*args,**kwargs):
            return self.model.test(self.enumeratef(obj), *args,**kwargs)  
        def testv(self,obj,log=False,*args,**kwargs):
            #print "obj",obj.shape
            tm=self.model.test(self.enumeratef(obj),log=log, *args,**kwargs)
            #print tm
            r=self.recomposef0(tm,obj.shape,log)
            return r
        def testmap(self,obj,xmap,*args,**kwargs):
            self.recomposef1(xmap,
                            self.model.test(self.enumeratef(obj), *args,**kwargs),
                            log=(("log" in kwargs.keys()) and kwargs["log"] or True)
                            )
        def samplev(self,n,withstate,*args,**kwargs):
            print "n unused so far / with state0 comes from projection !!"
            tm=self.model.sample(1,withstate=numpy.vstack(self.enumeratef(withstate)[:,0].tolist()), *args,**kwargs)
            r=self.recomposef0(numpy.array([tm]),withstate.shape,log=False)
            return r
    def __init__(self,clique_sets,topology_check_f=None):
      self.topology_check_f=topology_check_f
      self.cliques_sets=clique_sets
    @staticmethod
    def load(f,clique_sets,topology_check_f=None, *args, **kwargs):
 #     for e in cliques_sets:
       raise Exception, "Markov models are not to be saved..."
#          .load(f, *args, **kwargs)
    def dump(self,f):
        pass
    def train(self,o,*args, ** kwargs):
      for c in self.cliques_sets:
         c.train(o,*args, ** kwargs) 
    def test(self,o,log=True,*args, ** kwargs):
       rv=[c.test(o,log=log,*args, ** kwargs)  for c in self.cliques_sets]
       return sum(rv)
    def testmap(self,o,dmap,log=True,*args, ** kwargs):
       for c in self.cliques_sets:
         c.testmap(o,dmap,log=log,*args, ** kwargs) 
    def testv(self,o,log=True,*args, ** kwargs):
       return [ c.testv(o,log=log,*args, ** kwargs)  for c in self.cliques_sets ]
    def onesample(self,shp,minv=0,maxv=1,iter_limit=1000,verbose=False,temperature_map_generator=None,observer=None):
        """ Gibbs sampler is a way to optimize not too sample....
            We assume some kind of clean framework for the states so var all vraible are continuous in between 0 and 1
                (we may change this later)
        """
        TDECAY=0.05**(1./iter_limit)
        #raise Exception, "Gibbs sampler not yet implemented"
        base=(numpy.random.random(shp)*(maxv-minv)-minv).clip(minv,maxv)
        baseproba=numpy.zeros(base.shape)
        self.testmap(base,baseproba)
        temp=1
        i=0
        while (i<iter_limit):
          baseproba=baseproba.clip(-1000,1000)
          if (verbose):
            print i, temp, bpm
          cand=base+(numpy.random.random(base.shape)-0.5)*temp  ### les etats sont senses etre continus
          cand=cand.clip(0,1)
          candproba=numpy.zeros(base.shape)
          self.testmap(cand,candproba)
          for y in numpy.ndindex(shp):
                if (candproba[y]>baseproba[y]): 
                    base[y]=cand[y] # set the variable to be X...
          #
          self.testmap(base,baseproba)
          if (observer):
             self.observer(base,baseproba)
          temp=temp*TDECAY
          i+=1
        return base
    ###
    def onesample2(self,shp,minv=0,maxv=1,iter_limit=10000,verbose=False,temperature_map_generator=None,observer=None):
        """ -- resample one by one --
        
            Gibbs sampler is a way to optimize not too sample....
            We assume some kind of clean framework for the states so var all vraible are continuous in between 0 and 1
                (we may change this later)
        """
        TDECAY=0.05**(1./iter_limit)
        #raise Exception, "Gibbs sampler not yet implemented"
        base=(numpy.random.random(shp)*(maxv-minv)-minv).clip(minv,maxv)
        baseproba=numpy.zeros(base.shape)
        self.testmap(base,baseproba)
        temp=1
        i=0
        while (i<iter_limit):
          baseproba=baseproba.clip(-1000,1000)
          if (verbose):
            print i, temp, bpm
          p=random.choice(numpy.ndindex(shp))
          cand[p]=base[p]+(numpy.random.random()-0.5)*temp  ### les etats sont senses etre continus
          cand[p]=cand.clip(0,1)
          candproba=numpy.zeros(base.shape)
          self.testmap(cand,candproba)
          if (candproba[y]>baseproba[y]): 
                    base[y]=cand[y] # set the variable to be X...
          #
          self.testmap(base,baseproba)
          if (observer):
             self.observer(base,baseproba)
          temp=temp*TDECAY
          i+=1
        return base
    def parallel_adaptive_search(self,shp,improvq=0.0001,minv=0,maxv=1,iter_limit=10000,verbose=False,temperature_map_generator=None,observer=None):
        """ resample more the bad part than the good part
                (we may change this later)
        """
        for nr in range(MAXR):
          A=(numpy.random.random(shp)*(maxv-minv)-minv).clip(minv,maxv)
          baseproba=numpy.zeros(base.shape)
          self.testmap(base,optimalcost)
          temp=1
          i=0
          #A=CSP.random_configuration()
          #T=numpy.zeros((len(CSP.variables)),dtype=numpy.uint8)
          T=[]
          nbtabu=0
          optimum=A
          #optimalcost=A.cost()
          for ni in range(MAXI):
            ve=[ (v.cost(CSP,optimum),v) for v in CSP.variables ]
            ve.sort(cmp=lambda x,y:sgn(x[0]-y[0]))
            #print ve
            r=filter( lambda x:not T[x[1].id],ve)
            #print r
            X=r[-1][1] # on prend la variable qui viole le plus de contrainte et qui n'est pas tabu
            xo=X.cost(CSP,optimum)
            #improvingmoves=filter(lambda m:m[0]<=0,map (lambda m: (X.cost(CSP,m(optimum))-xo,m),optimum.localmoves(X))) ## should be a local test here !!!
            improvingmoves=[]
            for x in c: 
              improvingmoves.append( self.submodel_random_improve(optimum)  )
            if (len(improvingmoves)<=improvq):
                T.append(X)
                nbtabu+=1
                if (nbtabu>=RL):
                    s=random.sample( range(len(T)) ,RP)
                    for i in s:
                        T[i]=0
                    nbtabu-=RP
            else:
                improvingmoves.sort(cmp=lambda x,y:sgn(x[0]-y[0]))
                m=improvingmoves[-1]
                A2=m[1](optimum)
                c2=A2.cost()
                if c2<=optimalcost:
                    optimum=A2
                    optimalcost=c2
            if (optimalcost==0): break
          if (optimalcost==0): break
        return optimum,optimalcost




        TDECAY=0.05**(1./iter_limit)
        #raise Exception, "Gibbs sampler not yet implemented"
        while (i<iter_limit):
          baseproba=baseproba.clip(-1000,1000)
          if (verbose):
            print i, temp, bpm
          p=random.choice(numpy.ndindex(shp))
          cand[p]=base[p]+(numpy.random.random()-0.5)*temp  ### les etats sont senses etre continus
          cand[p]=cand.clip(0,1)
          candproba=numpy.zeros(base.shape)
          self.testmap(cand,candproba)
          if (candproba[y]>baseproba[y]): 
                    base[y]=cand[y] # set the variable to be X...
          #
          self.testmap(base,baseproba)
          if (observer):
             self.observer(base,baseproba)
          temp=temp*TDECAY
          i+=1
        return base
    def onesample3(self,shp,minv=0,maxv=1,iter_limit=10000,verbose=False,temperature_map_generator=None,observer=None):
        """ resample more the bad part than the good part
                (we may change this later)
        """
        TDECAY=0.05**(1./iter_limit)
        #raise Exception, "Gibbs sampler not yet implemented"
        base=(numpy.random.random(shp)*(maxv-minv)-minv).clip(minv,maxv)
        baseproba=numpy.zeros(base.shape)
        self.testmap(base,baseproba)
        temp=1
        i=0
        while (i<iter_limit):
          baseproba=baseproba.clip(-1000,1000)
          if (verbose):
            print i, temp, bpm
          p=random.choice(numpy.ndindex(shp))
          cand[p]=base[p]+(numpy.random.random()-0.5)*temp  ### les etats sont senses etre continus
          cand[p]=cand.clip(0,1)
          candproba=numpy.zeros(base.shape)
          self.testmap(cand,candproba)
          if (candproba[y]>baseproba[y]): 
                    base[y]=cand[y] # set the variable to be X...
          #
          self.testmap(base,baseproba)
          if (observer):
             self.observer(base,baseproba)
          temp=temp*TDECAY
          i+=1
        return base
    def sample(self, nsample):
        return [ self.onesample((20,20)) for x  in range(nsample) ] 
    def samplev(self,withstate,n=100,*args, **kwargs):
        ## we try to get sample according to cliques, the samples are done with respect of with state ws
        ## the results is returned as an array for each clique set (we don't try to merge the constraints on sampling)
        return [ c.samplev(n,withstate=withstate,*args, ** kwargs)  for c in self.cliques_sets ] 

    
    ###
    # we may also try wavelet like decomposition of the space 



    # we may also try wavelet like decomposition of the space 
#class MarkovDynamicalModel(MarkovModel):
#    def reaggragate_test()
#       self.test()
    #class CliqueSet(MarkovModel.Cliquset)
    #  def __init__(self, source_p, target_p):
    #     self.source_p=source_p
    #     self.target_p=target_p
    #class PseudoNode_For_Pattern():
    #  def __init__("pattern")
    #  def attributes(self):
    #
    #  def outproba(self,edge_pattern):
    #
    #  def 


    
def von_neuman_h(i):
  ## we enumerate all doublon
  pass

#class InterpolatedStateConditionalModel1d(FiniteStateConditionalModel):
#    def __init__(self, svl,*args, ** xargs):
#      self.svl=svl
#      super(self,InterpolatedStateConditionalModel).__init__(*args, **xargs)
#    def test(self,data):    
#      pass


#from jfli.dimred.PCA import *
class RemotelyTrainedModel():
   def __init__(self):
    #   self .t=...
      pass